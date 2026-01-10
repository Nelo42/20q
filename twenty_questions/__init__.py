"""
Sophisticated 20 Questions Game

A probabilistic animal guessing game using Bayesian inference,
entropy-based question selection, and dynamic weight learning.
"""

from .models import Entity, Attribute, BeliefState
from .knowledge_base import KnowledgeBase
from .belief_tracker import BeliefTracker
from .question_selector import QuestionSelector
from .weight_learner import WeightLearner
from .game_engine import GameEngine

__version__ = "1.0.0"
__all__ = [
    "Entity",
    "Attribute",
    "BeliefState",
    "KnowledgeBase",
    "BeliefTracker",
    "QuestionSelector",
    "WeightLearner",
    "GameEngine",
]
