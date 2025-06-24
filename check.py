import os
from config import RESULT_FILE

def extract_score():
    """Extract and print the average score from the game result file."""
    if not os.path.exists(RESULT_FILE):
        print("0")
        return
    
    try:
        with open(RESULT_FILE, 'r') as f:
            content = f.read()
        
        # Look for "Average: X" pattern
        if "Average:" in content:
            # Extract the number after "Average:"
            lines = content.split('\n')
            for line in lines:
                if "Average:" in line:
                    try:
                        # Extract the number after "Average:"
                        score_str = line.split("Average:")[1].strip()
                        print(score_str)
                        return
                    except Exception:
                        continue
        
        # Look for "Total: X" pattern as fallback
        elif "Total:" in content:
            lines = content.split('\n')
            for line in lines:
                if "Total:" in line:
                    try:
                        # Extract the number after "Total:" and before ","
                        score_part = line.split("Total:")[1]
                        score_str = score_part.split(",")[0].strip()
                        print(score_str)
                        return
                    except Exception:
                        continue
        
        # Look for individual game scores as fallback
        elif "Player score:" in content:
            lines = content.split('\n')
            for line in lines:
                if "Player score:" in line:
                    try:
                        # Extract the score after 'Player score:' and before ','
                        score_part = line.split('Player score:')[1]
                        score_str = score_part.split(',')[0].strip()
                        print(score_str)
                        return
                    except Exception:
                        continue
        
        # If no score found, print 0
        print("0")
        
    except Exception as e:
        print("0")

if __name__ == "__main__":
    extract_score()