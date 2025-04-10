import argparse
from runner import Runner
import logging

from player import SimplePlayer


def main(host: str = 'localhost', port: int = 5000, log_file: bool= False, result_path='/app/output/game_result.log') -> None:
    """Main entry point for the poker bot runner."""
    
    # Configure logger to write to a file
    if log_file:
        logging.basicConfig(
            filename='poker_runner.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    runner = Runner(host, port, result_path)
    simple_bot = SimplePlayer()
    runner.set_bot(simple_bot)
    runner.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Poker Bot Runner")
    parser.add_argument('-H', '--host', type=str, default='localhost', help='Server hostname or IP address')
    parser.add_argument('-p', '--port', type=int, default=5000, help='Server port')
    parser.add_argument('-lf', '--log_file', type=bool, default=False, help='Log to file or console')
    parser.add_argument('-r', '--result', type=str, default='/app/output/game_result.log', help='File to save the result')
    args = parser.parse_args()

    # Run the main function with command line arguments
    main(args.host, args.port, args.log_file, args.result)