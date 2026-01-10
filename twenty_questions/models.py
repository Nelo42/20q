"""
Data models for the 20 Questions game.

Defines the core data structures: Entity, Attribute, and BeliefState.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
import copy


@dataclass
class Entity:
    """
    An entity (animal) that can be guessed.

    Attributes:
        id: Unique identifier
        name: Display name (e.g., "a dog", "an elephant")
        attributes: Dict mapping attribute_id -> P(yes|entity)
                   Values are probabilities between 0.0 and 1.0
        times_played: Number of times this entity was the target
        times_guessed_correctly: Number of successful guesses
    """
    id: str
    name: str
    attributes: Dict[str, float] = field(default_factory=dict)
    times_played: int = 0
    times_guessed_correctly: int = 0

    def get_attribute_probability(self, attr_id: str) -> float:
        """Get P(yes|entity) for an attribute, default 0.5 if unknown."""
        return self.attributes.get(attr_id, 0.5)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "attributes": self.attributes,
            "times_played": self.times_played,
            "times_guessed_correctly": self.times_guessed_correctly,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Entity":
        """Create Entity from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            attributes=data.get("attributes", {}),
            times_played=data.get("times_played", 0),
            times_guessed_correctly=data.get("times_guessed_correctly", 0),
        )


@dataclass
class Attribute:
    """
    A question/attribute used to distinguish entities.

    Attributes:
        id: Unique identifier
        question: The question text (e.g., "Is it a mammal?")
        category: Category for organization (e.g., "biology", "habitat")
        alpha: Beta distribution parameter (prior successes + 1)
        beta: Beta distribution parameter (prior failures + 1)
    """
    id: str
    question: str
    category: str = "general"
    alpha: float = 1.0  # Beta distribution param
    beta: float = 1.0   # Beta distribution param

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "question": self.question,
            "category": self.category,
            "alpha": self.alpha,
            "beta": self.beta,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Attribute":
        """Create Attribute from dictionary."""
        return cls(
            id=data["id"],
            question=data["question"],
            category=data.get("category", "general"),
            alpha=data.get("alpha", 1.0),
            beta=data.get("beta", 1.0),
        )


@dataclass
class BeliefState:
    """
    Probability distribution over entities.

    Represents the current belief about which entity the user is thinking of.
    """
    probabilities: Dict[str, float] = field(default_factory=dict)

    def normalize(self) -> None:
        """Normalize probabilities to sum to 1.0."""
        total = sum(self.probabilities.values())
        if total > 0:
            for k in self.probabilities:
                self.probabilities[k] /= total

    def get_top_entities(self, n: int = 5) -> list:
        """Get top n entities by probability."""
        sorted_entities = sorted(
            self.probabilities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_entities[:n]

    def get_probability(self, entity_id: str) -> float:
        """Get probability for a specific entity."""
        return self.probabilities.get(entity_id, 0.0)

    def get_max_probability(self) -> tuple:
        """Get the entity with highest probability and its value."""
        if not self.probabilities:
            return None, 0.0
        max_entity = max(self.probabilities.items(), key=lambda x: x[1])
        return max_entity

    def copy(self) -> "BeliefState":
        """Create a deep copy of the belief state."""
        return BeliefState(probabilities=copy.deepcopy(self.probabilities))

    @classmethod
    def uniform(cls, entity_ids: list) -> "BeliefState":
        """Create uniform distribution over entities."""
        n = len(entity_ids)
        if n == 0:
            return cls()
        prob = 1.0 / n
        return cls(probabilities={eid: prob for eid in entity_ids})


@dataclass
class GameSession:
    """
    Tracks the state of a single game session.
    """
    questions_asked: list = field(default_factory=list)  # List of (attr_id, answer)
    current_question: int = 0
    belief_history: list = field(default_factory=list)  # Entropy values
    guessed_entity: Optional[str] = None
    actual_entity: Optional[str] = None
    was_correct: Optional[bool] = None
