import os
from config import RESULT_FILE

def show_player_scores():
    """Show only player scores from the game result file."""
    if not os.path.exists(RESULT_FILE):
        print(f"No result file found at {RESULT_FILE}")
        return
    with open(RESULT_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Expecting format: Game_1: Player score: 110, All scores: {...}
            if 'Player score:' in line:
                # Extract the score after 'Player score:' and before ','
                try:
                    score_part = line.split('Player score:')[1]
                    score_str = score_part.split(',')[0].strip()
                    print(score_str)
                except Exception:
                    continue

if __name__ == "__main__":
    show_player_scores()