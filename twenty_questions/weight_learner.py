"""
Weight Learner for the 20 Questions game.

Implements dynamic weight adjustment based on game sessions.
"""

import numpy as np
from typing import List, Tuple, Optional
from .models import Entity, Attribute, GameSession
from .knowledge_base import KnowledgeBase


class WeightLearner:
    """
    Learns and adjusts entity-attribute weights based on gameplay.

    Uses exponential moving average to update weights based on:
    1. Correct guesses (reinforce the pattern)
    2. Wrong guesses (adjust toward actual answers)
    3. New entities (learn from user corrections)
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        learning_rate: float = 0.1,
        min_weight: float = 0.01,
        max_weight: float = 0.99
    ):
        """
        Initialize the weight learner.

        Args:
            knowledge_base: The knowledge base to update
            learning_rate: Rate of weight updates (0.0-1.0)
            min_weight: Minimum allowed weight value
            max_weight: Maximum allowed weight value
        """
        self.kb = knowledge_base
        self.learning_rate = learning_rate
        self.min_weight = min_weight
        self.max_weight = max_weight

    def update_from_session(
        self,
        entity_id: str,
        question_answers: List[Tuple[str, float]],
        was_correct_guess: bool
    ) -> None:
        """
        Update entity weights based on a completed game session.

        Args:
            entity_id: The ID of the actual entity
            question_answers: List of (attribute_id, answer) tuples
            was_correct_guess: Whether the system guessed correctly
        """
        entity = self.kb.get_entity(entity_id)
        if entity is None:
            return

        # Use a higher learning rate for correct guesses (stronger reinforcement)
        # and a lower rate for incorrect guesses (gentler correction)
        effective_rate = self.learning_rate if was_correct_guess else self.learning_rate * 0.5

        for attr_id, answer in question_answers:
            current_weight = entity.attributes.get(attr_id, 0.5)

            # Move weight toward the user's answer using exponential moving average
            new_weight = current_weight + effective_rate * (answer - current_weight)
            new_weight = np.clip(new_weight, self.min_weight, self.max_weight)

            entity.attributes[attr_id] = new_weight

        # Update play statistics
        entity.times_played += 1
        if was_correct_guess:
            entity.times_guessed_correctly += 1

        # Persist changes
        self.kb.save()

    def learn_new_entity(
        self,
        name: str,
        question_answers: List[Tuple[str, float]],
        distinguishing_question: Optional[str] = None,
        distinguishing_answer: Optional[float] = None
    ) -> Entity:
        """
        Add a new entity to the knowledge base.

        Args:
            name: Name of the new entity
            question_answers: List of (attribute_id, answer) tuples from the game
            distinguishing_question: Optional new question to distinguish this entity
            distinguishing_answer: Answer to the distinguishing question

        Returns:
            The newly created Entity
        """
        # Generate unique ID
        entity_id = self.kb.generate_entity_id(name)

        # Build attributes from Q&A session
        attributes = {}
        for attr_id, answer in question_answers:
            attributes[attr_id] = answer

        # Add distinguishing question if provided
        if distinguishing_question and distinguishing_answer is not None:
            # Create a new attribute ID from the question
            attr_id = self._generate_attribute_id(distinguishing_question)

            # Check if this is a new question
            if self.kb.get_attribute(attr_id) is None:
                new_attr = Attribute(
                    id=attr_id,
                    question=distinguishing_question,
                    category="learned"
                )
                self.kb.add_attribute(new_attr)

            attributes[attr_id] = distinguishing_answer

        # Create and add the new entity
        new_entity = Entity(
            id=entity_id,
            name=name,
            attributes=attributes,
            times_played=1,
            times_guessed_correctly=0
        )

        self.kb.add_entity(new_entity)

        return new_entity

    def _generate_attribute_id(self, question: str) -> str:
        """
        Generate an attribute ID from a question text.

        Args:
            question: The question text

        Returns:
            Generated attribute ID
        """
        # Clean and convert to snake_case
        clean = question.lower()
        for char in "?.,!':\"":
            clean = clean.replace(char, "")

        # Replace spaces and common words
        words = clean.split()
        filtered = [w for w in words if w not in ("is", "it", "a", "an", "the", "does", "can")]
        attr_id = "_".join(filtered[:5])  # Limit length

        # Ensure uniqueness
        base_id = attr_id
        counter = 1
        while self.kb.get_attribute(attr_id) is not None:
            attr_id = f"{base_id}_{counter}"
            counter += 1

        return attr_id

    def adjust_weights_for_confusion(
        self,
        guessed_entity_id: str,
        actual_entity_id: str,
        question_answers: List[Tuple[str, float]]
    ) -> None:
        """
        Adjust weights when the system confused two entities.

        This helps the system learn to distinguish between similar entities.

        Args:
            guessed_entity_id: The entity the system guessed
            actual_entity_id: The actual entity
            question_answers: The Q&A from the session
        """
        guessed = self.kb.get_entity(guessed_entity_id)
        actual = self.kb.get_entity(actual_entity_id)

        if guessed is None or actual is None:
            return

        # For each question answered, adjust weights to create more separation
        for attr_id, answer in question_answers:
            guessed_weight = guessed.attributes.get(attr_id, 0.5)
            actual_weight = actual.attributes.get(attr_id, 0.5)

            # Move guessed entity's weight away from the answer
            # (since it was wrong)
            guessed_target = 1.0 - answer
            new_guessed = guessed_weight + (self.learning_rate * 0.5) * (guessed_target - guessed_weight)
            guessed.attributes[attr_id] = np.clip(new_guessed, self.min_weight, self.max_weight)

            # Move actual entity's weight toward the answer
            new_actual = actual_weight + self.learning_rate * (answer - actual_weight)
            actual.attributes[attr_id] = np.clip(new_actual, self.min_weight, self.max_weight)

        # Update statistics
        guessed.times_played += 1
        actual.times_played += 1
        # Neither was guessed correctly

        self.kb.save()

    def get_learning_stats(self, entity_id: str) -> dict:
        """
        Get learning statistics for an entity.

        Args:
            entity_id: The entity ID

        Returns:
            Dictionary with learning stats
        """
        entity = self.kb.get_entity(entity_id)
        if entity is None:
            return {}

        accuracy = 0.0
        if entity.times_played > 0:
            accuracy = entity.times_guessed_correctly / entity.times_played

        return {
            "entity_id": entity_id,
            "name": entity.name,
            "times_played": entity.times_played,
            "times_guessed_correctly": entity.times_guessed_correctly,
            "accuracy": accuracy,
            "num_attributes": len(entity.attributes)
        }

    def get_global_stats(self) -> dict:
        """
        Get global learning statistics.

        Returns:
            Dictionary with global stats
        """
        total_played = 0
        total_correct = 0
        entities_with_data = 0

        for entity in self.kb.get_all_entities():
            if entity.times_played > 0:
                entities_with_data += 1
                total_played += entity.times_played
                total_correct += entity.times_guessed_correctly

        accuracy = total_correct / total_played if total_played > 0 else 0.0

        return {
            "total_entities": self.kb.get_entity_count(),
            "total_attributes": self.kb.get_attribute_count(),
            "entities_with_play_data": entities_with_data,
            "total_games_played": total_played,
            "total_correct_guesses": total_correct,
            "overall_accuracy": accuracy
        }
