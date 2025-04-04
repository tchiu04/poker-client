import argparse
from runner import Runner
import logging

from player import SimplePlayer


def main(host: str = 'localhost', port: int = 5000, log_file: bool= False) -> None:
    """Main entry point for the poker bot runner."""
    host = 'localhost'
    port = 5000
    
    # Configure logger to write to a file
    if log_file:
        logging.basicConfig(
            filename='poker_runner.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    runner = Runner(host, port)
    simple_bot = SimplePlayer()
    runner.set_bot(simple_bot)
    runner.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Poker Bot Runner")
    parser.add_argument('--host', type=str, default='localhost', help='Server hostname or IP address')
    parser.add_argument('--port', type=int, default=5000, help='Server port')
    parser.add_argument('--log_file', type=bool, default=False, help='Log to file or console')
    args = parser.parse_args()

    # Run the main function with command line arguments
    main(args.host, args.port, args.log_file)