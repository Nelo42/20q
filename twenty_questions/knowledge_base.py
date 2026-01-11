"""
Knowledge Base for the 20 Questions game.

Manages entities and attributes with JSON persistence.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from .models import Entity, Attribute


class KnowledgeBase:
    """
    Manages the knowledge base of entities and attributes.

    Provides persistence to JSON files and methods for accessing
    and modifying the knowledge base.
    """

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the knowledge base.

        Args:
            data_dir: Directory for data files. Defaults to ./data relative to this file.
        """
        if data_dir is None:
            data_dir = Path(__file__).parent / "data"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.entities_file = self.data_dir / "entities.json"
        self.attributes_file = self.data_dir / "attributes.json"
        self.learned_file = self.data_dir / "learned.json"

        self.entities: Dict[str, Entity] = {}
        self.attributes: Dict[str, Attribute] = {}
        self._original_entities: Dict[str, dict] = {}  # Cache for original entity data

        self._load()

    def _load(self) -> None:
        """Load entities and attributes from JSON files."""
        # Load entities and cache original data
        if self.entities_file.exists():
            try:
                with open(self.entities_file, "r") as f:
                    data = json.load(f)
                    for e in data.get("entities", []):
                        self.entities[e["id"]] = Entity.from_dict(e)
                        # Cache original attributes for comparison during save
                        self._original_entities[e["id"]] = e.get("attributes", {})
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load entities file: {e}")

        # Load attributes
        if self.attributes_file.exists():
            try:
                with open(self.attributes_file, "r") as f:
                    data = json.load(f)
                    self.attributes = {
                        a["id"]: Attribute.from_dict(a) for a in data.get("attributes", [])
                    }
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load attributes file: {e}")

        # Load learned data (overrides for entities/attributes from play sessions)
        if self.learned_file.exists():
            try:
                with open(self.learned_file, "r") as f:
                    data = json.load(f)
                    # Merge learned entities
                    for e in data.get("entities", []):
                        entity = Entity.from_dict(e)
                        if entity.id in self.entities:
                            # Update existing entity's learned attributes
                            self.entities[entity.id].attributes.update(entity.attributes)
                            self.entities[entity.id].times_played = entity.times_played
                            self.entities[entity.id].times_guessed_correctly = entity.times_guessed_correctly
                        else:
                            self.entities[entity.id] = entity
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load learned file: {e}")

    def save(self) -> None:
        """Save learned data to JSON file."""
        learned_entities = [
            e.to_dict() for e in self.entities.values()
            if e.times_played > 0 or any(
                e.attributes.get(aid) != self._get_original_attribute(e.id, aid)
                for aid in e.attributes
            )
        ]

        learned_data = {"entities": learned_entities}

        # Write to temp file first, then rename for atomic operation
        temp_file = self.learned_file.with_suffix('.json.tmp')
        try:
            with open(temp_file, "w") as f:
                json.dump(learned_data, f, indent=2)
            # Atomic rename to prevent corruption on crash
            temp_file.replace(self.learned_file)
        except IOError as e:
            print(f"Warning: Failed to save learned file: {e}")
            if temp_file.exists():
                temp_file.unlink()

    def _get_original_attribute(self, entity_id: str, attr_id: str) -> Optional[float]:
        """Get original attribute value from cached base data (for comparison)."""
        original_attrs = self._original_entities.get(entity_id, {})
        return original_attrs.get(attr_id)

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get an entity by ID."""
        return self.entities.get(entity_id)

    def get_attribute(self, attr_id: str) -> Optional[Attribute]:
        """Get an attribute by ID."""
        return self.attributes.get(attr_id)

    def get_all_entities(self) -> List[Entity]:
        """Get all entities."""
        return list(self.entities.values())

    def get_all_entity_ids(self) -> List[str]:
        """Get all entity IDs."""
        return list(self.entities.keys())

    def get_all_attributes(self) -> List[Attribute]:
        """Get all attributes."""
        return list(self.attributes.values())

    def get_all_attribute_ids(self) -> List[str]:
        """Get all attribute IDs."""
        return list(self.attributes.keys())

    def add_entity(self, entity: Entity) -> None:
        """Add a new entity to the knowledge base."""
        self.entities[entity.id] = entity
        self.save()

    def add_attribute(self, attribute: Attribute) -> None:
        """Add a new attribute to the knowledge base."""
        self.attributes[attribute.id] = attribute
        # Save to learned file as well
        self.save()

    def update_entity(self, entity: Entity) -> None:
        """Update an existing entity."""
        self.entities[entity.id] = entity
        self.save()

    def get_entity_count(self) -> int:
        """Get total number of entities."""
        return len(self.entities)

    def get_attribute_count(self) -> int:
        """Get total number of attributes."""
        return len(self.attributes)

    def get_entities_by_attribute(
        self, attr_id: str, threshold: float = 0.5
    ) -> List[Entity]:
        """Get entities where P(yes|entity) > threshold for an attribute."""
        return [
            e for e in self.entities.values()
            if e.get_attribute_probability(attr_id) > threshold
        ]

    def generate_entity_id(self, name: str) -> str:
        """Generate a unique entity ID from a name."""
        base_id = name.lower().replace(" ", "_").replace("a ", "").replace("an ", "")
        # Remove common articles
        for article in ["the ", "a ", "an "]:
            if base_id.startswith(article):
                base_id = base_id[len(article):]

        entity_id = base_id
        counter = 1
        while entity_id in self.entities:
            entity_id = f"{base_id}_{counter}"
            counter += 1
        return entity_id
