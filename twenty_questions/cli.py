#!/usr/bin/env python3
"""
Command-line interface for the 20 Questions game.

Provides an interactive terminal experience with rich feedback.
"""

import os
import sys
from typing import Optional
from .game_engine import GameEngine, GameConfig, GameState


def clear_screen():
    """Clear the terminal screen (cross-platform)."""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')


def print_header():
    """Print the game header."""
    print("=" * 60)
    print("         TWENTY QUESTIONS - Animal Guessing Game")
    print("           Powered by Bayesian Inference")
    print("=" * 60)


def print_stats_bar(entropy: float, confidence: float, question_num: int, max_questions: int):
    """Print a status bar with current game stats."""
    # Confidence bar
    conf_width = 20
    conf_filled = int(confidence * conf_width)
    conf_bar = "█" * conf_filled + "░" * (conf_width - conf_filled)

    print(f"\n┌{'─' * 58}┐")
    print(f"│ Q: {question_num:2d}/{max_questions}  │  Entropy: {entropy:5.2f}  │  Confidence: [{conf_bar}] {confidence*100:5.1f}% │")
    print(f"└{'─' * 58}┘")


def print_top_guesses(top_entities: list, kb):
    """Print the current top guesses."""
    if not top_entities:
        return

    print("\n  Current top guesses:")
    for i, (eid, prob) in enumerate(top_entities[:3], 1):
        entity = kb.get_entity(eid)
        name = entity.name if entity else eid
        bar_width = int(prob * 30)
        bar = "▓" * bar_width + "░" * (30 - bar_width)
        print(f"    {i}. {name:20s} [{bar}] {prob*100:5.1f}%")


def get_yes_no_maybe(prompt: str) -> float:
    """
    Get a yes/no/maybe answer from the user.

    Returns:
        1.0 for yes, 0.0 for no, 0.5 for maybe/unknown
    """
    while True:
        print(f"\n  {prompt}")
        answer = input("  Your answer (yes/no/maybe/y/n/m): ").strip().lower()

        if answer in ('yes', 'y'):
            return 1.0
        elif answer in ('no', 'n'):
            return 0.0
        elif answer in ('maybe', 'm', 'unknown', 'u', "don't know", 'dk', '?'):
            return 0.5
        else:
            print("  Please answer 'yes', 'no', or 'maybe'.")


def play_game(engine: GameEngine, show_debug: bool = False) -> bool:
    """Play a single game.

    Returns:
        True if the system guessed correctly, False otherwise.
    """
    engine.start_game()

    print("\n  Think of an animal and I'll try to guess it!")
    print("  Answer my questions with 'yes', 'no', or 'maybe'.")
    input("\n  Press Enter when you're ready...")

    while engine.state == GameState.ASKING_QUESTIONS:
        # Get current state
        state = engine.get_current_state()

        if show_debug:
            print_stats_bar(
                state['entropy'],
                state['confidence'],
                state['question_number'],
                engine.config.max_questions
            )
            print_top_guesses(
                [(e['id'], e['probability']) for e in state['top_entities']],
                engine.kb
            )

        # Get next question
        question_info = engine.get_next_question()

        if question_info is None:
            # Time to guess
            break

        attr_id, question_text = question_info

        # Ask the question
        print(f"\n  Question {state['question_number'] + 1}:")
        answer = get_yes_no_maybe(question_text)

        # Process answer
        result = engine.process_answer(attr_id, answer)

        if show_debug:
            entropy_reduction = result.entropy_before - result.entropy_after
            print(f"\n  [Entropy reduced by {entropy_reduction:.3f}]")

    # Make a guess
    guess = engine.get_guess()
    if guess:
        entity_id, entity_name, confidence = guess

        print("\n" + "=" * 60)
        print(f"\n  After {engine.current_question} questions, I think you're thinking of...")
        print(f"\n  >>> {entity_name.upper()} <<<")
        print(f"\n  (Confidence: {confidence*100:.1f}%)")
        print("\n" + "=" * 60)

        correct = get_yes_no_maybe("Am I correct?")

        if correct > 0.7:  # Yes
            print("\n  🎉 Excellent! I guessed it!")
            engine.process_guess_result(was_correct=True)
            return True
        else:
            print("\n  Oh no! I couldn't guess it.")
            handle_wrong_guess(engine)
            return False
    else:
        print("\n  I'm stumped! I couldn't narrow it down.")
        handle_wrong_guess(engine)
        return False


def handle_wrong_guess(engine: GameEngine):
    """Handle a wrong guess by learning from the user."""
    print("\n  What animal were you thinking of?")
    actual_name = input("  Animal name: ").strip()

    if not actual_name:
        print("  No name provided. Skipping learning.")
        engine.state = GameState.GAME_OVER
        return

    # Format the name
    if not actual_name.lower().startswith(('a ', 'an ')):
        if actual_name[0].lower() in 'aeiou':
            actual_name = f"an {actual_name}"
        else:
            actual_name = f"a {actual_name}"

    # Check if entity exists
    engine.process_guess_result(was_correct=False, actual_entity_name=actual_name)

    if engine.state == GameState.LEARNING_NEW:
        print(f"\n  I don't know '{actual_name}' yet. Let me learn it!")

        # Ask for a distinguishing question
        print("\n  Can you give me a yes/no question that would help")
        print("  distinguish this animal from others?")
        print("  (Press Enter to skip)")

        dist_question = input("  Question: ").strip()

        if dist_question:
            if not dist_question.endswith('?'):
                dist_question += '?'

            dist_answer = get_yes_no_maybe(f"And what's the answer for {actual_name}?")

            engine.learn_new_entity(
                actual_name,
                distinguishing_question=dist_question,
                distinguishing_answer=dist_answer
            )
            print(f"\n  Thanks! I've learned about {actual_name}.")
        else:
            engine.learn_new_entity(actual_name)
            print(f"\n  Got it! I've added {actual_name} to my knowledge base.")
    else:
        print(f"\n  Thanks! I've adjusted my knowledge about {actual_name}.")


def show_stats(engine: GameEngine):
    """Show global game statistics."""
    stats = engine.get_stats()

    print("\n" + "=" * 60)
    print("                    GAME STATISTICS")
    print("=" * 60)
    print(f"\n  Total entities in database:    {stats['total_entities']}")
    print(f"  Total questions available:     {stats['total_attributes']}")
    print(f"  Entities with play history:    {stats['entities_with_play_data']}")
    print(f"\n  Total games played:            {stats['total_games_played']}")
    print(f"  Correct guesses:               {stats['total_correct_guesses']}")
    print(f"  Overall accuracy:              {stats['overall_accuracy']*100:.1f}%")
    print("\n" + "=" * 60)


def main():
    """Main entry point for the CLI."""
    # Parse simple command line args
    show_debug = '--debug' in sys.argv or '-d' in sys.argv

    # Create game engine
    config = GameConfig(show_debug=show_debug)
    engine = GameEngine(config=config)

    clear_screen()
    print_header()

    wins = 0
    games = 0

    while True:
        was_correct = play_game(engine, show_debug=show_debug)

        # Track score
        games += 1
        if was_correct:
            wins += 1

        print(f"\n  Games played this session: {games} (Wins: {wins})")

        # Show stats option
        print("\n  Options:")
        print("    [P]lay again")
        print("    [S]how statistics")
        print("    [Q]uit")

        choice = input("\n  Your choice: ").strip().lower()

        if choice in ('q', 'quit', 'exit'):
            break
        elif choice in ('s', 'stats', 'statistics'):
            show_stats(engine)
            input("\n  Press Enter to continue...")
        elif choice in ('p', 'play', 'again', ''):
            clear_screen()
            print_header()
            continue
        else:
            clear_screen()
            print_header()

    print("\n  Thanks for playing Twenty Questions!")
    print("  Your knowledge helps me learn and improve.")
    print("\n  Goodbye!\n")


if __name__ == "__main__":
    main()
