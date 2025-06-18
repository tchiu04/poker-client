import os
import argparse
from config import RESULT_FILE

def check_result(filename):
    """Check result from a given file."""
    if os.path.exists(filename) and os.path.isfile(filename):
        with open(filename, 'r') as file:
            content = file.readlines()
        
        if len(content) == 0:
            print("No result")
            return
        
        # Look for CONTINUOUS_MODE result
        for i, line in enumerate(content):
            line = line.strip()
            if line.startswith("CONTINUOUS_MODE"):
                # Found the continuous mode result, now look for the Average line
                for j in range(i, min(i + 5, len(content))):  # Look at most 5 lines after
                    avg_line = content[j].strip()
                    if avg_line.startswith("Average:"):
                        try:
                            # Extract everything after "Average:"
                            avg_part = avg_line.split("Average:")[1].strip()
                            # Remove any trailing commas or extra whitespace
                            avg_part = avg_part.rstrip(',').strip()
                            avg_score = float(avg_part)
                            print(avg_score)
                            return
                        except (ValueError, IndexError) as e:
                            print(f"Error parsing average: {e}")
                            return
                break
        
        # Look for the last result line (fallback)
        for line in reversed(content):
            line = line.strip()
            if line and not line.startswith("CONTINUOUS_MODE") and not line.startswith("Games:") and not line.startswith("Total:") and not line.startswith("Average:"):
                try:
                    # Try to parse as float (supports negative values)
                    result = float(line)
                    print(result)
                    return
                except ValueError:
                    # If we can't parse it, just print the line
                    print(line)
                    return
        
        print("No result")
    else:
        print("No result")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Check result from client output file.')
    parser.add_argument('--file', type=str, default=RESULT_FILE, help='Result file to check')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check the result from the specified file
    check_result(args.file)

if __name__ == "__main__":
    main()