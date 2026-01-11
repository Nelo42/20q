"""
Simulation test for 20 Questions game.
Runs 400 games per category and analyzes identification accuracy.
"""

import random
import json
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from twenty_questions.game_engine import GameEngine, GameState


@dataclass
class GameResult:
    """Result of a single simulated game."""
    target_id: str
    target_name: str
    category: str
    guessed_id: Optional[str]
    guessed_name: Optional[str]
    correct: bool
    num_questions: int
    final_confidence: float
    was_in_top_5: bool
    rank_at_end: int


@dataclass
class CategoryStats:
    """Statistics for a category."""
    total_games: int = 0
    correct_guesses: int = 0
    avg_questions: float = 0.0
    avg_confidence: float = 0.0
    top_5_rate: float = 0.0
    failed_entities: List[Tuple[str, str, int]] = None  # (id, name, times_failed)

    def __post_init__(self):
        if self.failed_entities is None:
            self.failed_entities = []


def simulate_game(engine: GameEngine, target_id: str) -> GameResult:
    """
    Simulate a single game with a target entity.

    Args:
        engine: Game engine instance
        target_id: ID of the entity to guess

    Returns:
        GameResult with outcome details
    """
    target = engine.kb.get_entity(target_id)
    if target is None:
        raise ValueError(f"Entity not found: {target_id}")

    engine.start_game()
    question_num = 0

    while question_num < 20:
        result = engine.get_next_question()

        # Check if game should make a guess
        if result is None or engine.state == GameState.MAKING_GUESS:
            break

        question_num += 1
        attr_id, _ = result

        # Get answer from target entity
        target_prob = target.get_attribute_probability(attr_id)
        if target_prob > 0.7:
            answer = 1.0
        elif target_prob < 0.3:
            answer = 0.0
        else:
            answer = 0.5

        # Process the answer
        engine.process_answer(attr_id, answer)

    # Get the guess - returns (entity_id, entity_name, confidence)
    guess_result = engine.get_guess()
    if guess_result is None:
        return GameResult(
            target_id=target_id,
            target_name=target.name,
            category=getattr(target, 'category', 'unknown'),
            guessed_id=None,
            guessed_name=None,
            correct=False,
            num_questions=question_num,
            final_confidence=0.0,
            was_in_top_5=False,
            rank_at_end=-1
        )

    guessed_id, guessed_name, confidence = guess_result

    # Check if correct
    correct = guessed_id == target_id

    # Check rank of target in final beliefs
    top_entities = engine.beliefs.get_top_entities(100)
    rank = -1
    was_in_top_5 = False
    for i, (eid, _) in enumerate(top_entities):
        if eid == target_id:
            rank = i + 1
            was_in_top_5 = (i < 5)
            break

    return GameResult(
        target_id=target_id,
        target_name=target.name,
        category=getattr(target, 'category', 'unknown'),
        guessed_id=guessed_id,
        guessed_name=guessed_name,
        correct=correct,
        num_questions=question_num,
        final_confidence=confidence,
        was_in_top_5=was_in_top_5,
        rank_at_end=rank
    )


def run_simulation(games_per_category: int = 400, seed: int = 42) -> Dict:
    """
    Run simulation across all categories.

    Args:
        games_per_category: Number of games to simulate per category
        seed: Random seed for reproducibility

    Returns:
        Dictionary with results and statistics
    """
    random.seed(seed)

    engine = GameEngine()

    # Group entities by category
    entities_by_category = defaultdict(list)
    for entity in engine.kb.entities.values():
        cat = getattr(entity, 'category', 'unknown')
        entities_by_category[cat].append(entity.id)

    print(f"\nEntities by category:")
    for cat, ids in entities_by_category.items():
        print(f"  {cat}: {len(ids)} entities")

    results = []
    category_stats = {}

    for category, entity_ids in entities_by_category.items():
        print(f"\n{'='*60}")
        print(f"Simulating {category.upper()} category...")
        print(f"{'='*60}")

        # Select entities for this category (with replacement if needed)
        if len(entity_ids) >= games_per_category:
            selected = random.sample(entity_ids, games_per_category)
        else:
            # Sample with replacement
            selected = random.choices(entity_ids, k=games_per_category)

        category_results = []
        failed_counts = defaultdict(int)

        for i, target_id in enumerate(selected):
            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{games_per_category} games...")

            try:
                result = simulate_game(engine, target_id)
                category_results.append(result)
                results.append(result)

                if not result.correct:
                    failed_counts[target_id] += 1
            except Exception as e:
                print(f"  Error with {target_id}: {e}")

        # Calculate category statistics
        if category_results:
            correct = sum(1 for r in category_results if r.correct)
            avg_q = sum(r.num_questions for r in category_results) / len(category_results)
            avg_conf = sum(r.final_confidence for r in category_results) / len(category_results)
            top_5 = sum(1 for r in category_results if r.was_in_top_5) / len(category_results)

            # Get top failed entities
            failed_list = [(eid, engine.kb.get_entity(eid).name, count)
                          for eid, count in sorted(failed_counts.items(), key=lambda x: -x[1])[:10]]

            stats = CategoryStats(
                total_games=len(category_results),
                correct_guesses=correct,
                avg_questions=avg_q,
                avg_confidence=avg_conf,
                top_5_rate=top_5,
                failed_entities=failed_list
            )
            category_stats[category] = stats

            print(f"\n  Results for {category}:")
            print(f"    Accuracy: {correct}/{len(category_results)} ({100*correct/len(category_results):.1f}%)")
            print(f"    Avg questions: {avg_q:.1f}")
            print(f"    Avg confidence: {avg_conf:.1%}")
            print(f"    Top-5 rate: {top_5:.1%}")

    return {
        "results": results,
        "category_stats": category_stats,
        "total_games": len(results),
        "overall_accuracy": sum(1 for r in results if r.correct) / len(results) if results else 0
    }


def print_report(simulation_data: Dict):
    """Print a detailed report of simulation results."""

    print("\n" + "="*70)
    print("                    SIMULATION REPORT")
    print("="*70)

    total = simulation_data["total_games"]
    accuracy = simulation_data["overall_accuracy"]

    print(f"\nOVERALL STATISTICS:")
    print(f"  Total games simulated: {total}")
    print(f"  Overall accuracy: {accuracy:.1%}")

    print(f"\n{'='*70}")
    print("CATEGORY BREAKDOWN:")
    print(f"{'='*70}")

    for category, stats in simulation_data["category_stats"].items():
        acc = stats.correct_guesses / stats.total_games if stats.total_games > 0 else 0
        print(f"\n{category.upper()}:")
        print(f"  Games: {stats.total_games}")
        print(f"  Accuracy: {stats.correct_guesses}/{stats.total_games} ({acc:.1%})")
        print(f"  Avg Questions: {stats.avg_questions:.1f}")
        print(f"  Avg Confidence: {stats.avg_confidence:.1%}")
        print(f"  In Top-5: {stats.top_5_rate:.1%}")

        if stats.failed_entities:
            print(f"  Most Failed Entities:")
            for eid, name, count in stats.failed_entities[:5]:
                print(f"    - {name} ({eid}): failed {count} times")

    # Find confusions
    print(f"\n{'='*70}")
    print("COMMON CONFUSIONS (guessed wrong):")
    print(f"{'='*70}")

    confusion_pairs = defaultdict(int)
    for r in simulation_data["results"]:
        if not r.correct:
            pair = (r.target_name, r.guessed_name)
            confusion_pairs[pair] += 1

    top_confusions = sorted(confusion_pairs.items(), key=lambda x: -x[1])[:15]
    for (target, guessed), count in top_confusions:
        print(f"  {target} -> guessed as {guessed} ({count} times)")

    # Recommendations
    print(f"\n{'='*70}")
    print("RECOMMENDATIONS:")
    print(f"{'='*70}")

    for category, stats in simulation_data["category_stats"].items():
        acc = stats.correct_guesses / stats.total_games if stats.total_games > 0 else 0
        if acc < 0.7:
            print(f"\n{category.upper()} needs improvement (accuracy: {acc:.1%}):")
            if stats.failed_entities:
                print(f"  - Add distinguishing attributes for: {', '.join(e[1] for e in stats.failed_entities[:3])}")


def save_results(simulation_data: Dict, filename: str = "simulation_results.json"):
    """Save simulation results to JSON file."""

    # Convert to serializable format
    output = {
        "total_games": simulation_data["total_games"],
        "overall_accuracy": simulation_data["overall_accuracy"],
        "categories": {}
    }

    for category, stats in simulation_data["category_stats"].items():
        output["categories"][category] = {
            "total_games": stats.total_games,
            "correct_guesses": stats.correct_guesses,
            "accuracy": stats.correct_guesses / stats.total_games if stats.total_games > 0 else 0,
            "avg_questions": stats.avg_questions,
            "avg_confidence": stats.avg_confidence,
            "top_5_rate": stats.top_5_rate,
            "failed_entities": [{"id": e[0], "name": e[1], "failures": e[2]}
                               for e in stats.failed_entities]
        }

    # Add confusion matrix
    confusion_pairs = defaultdict(int)
    for r in simulation_data["results"]:
        if not r.correct:
            pair = f"{r.target_id} -> {r.guessed_id}"
            confusion_pairs[pair] += 1

    output["top_confusions"] = [
        {"target": k.split(" -> ")[0], "guessed": k.split(" -> ")[1], "count": v}
        for k, v in sorted(confusion_pairs.items(), key=lambda x: -x[1])[:20]
    ]

    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {filename}")


if __name__ == "__main__":
    import sys

    # Allow custom number of games
    games = 400
    if len(sys.argv) > 1:
        games = int(sys.argv[1])

    print(f"Running simulation with {games} games per category...")

    simulation_data = run_simulation(games_per_category=games)
    print_report(simulation_data)
    save_results(simulation_data, "twenty_questions/data/simulation_results.json")
