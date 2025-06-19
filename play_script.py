# python play_script.py
# This script to test functionality of player class for our docker service

from player import SimplePlayer

p = SimplePlayer()

p.on_start(1000, ["As", "Kd"], 10, 2, 1)

# Test on_round_start
from type.round_state import RoundStateClient

# Create a sample round state
round_state = RoundStateClient(
    round="PREFLOP",
    round_num=1,
    community_cards=[],
    pot=30,
    current_player=1,
    current_bet=10,
    player_bets={1: 5, 2: 10},
    player_actions={1: "CALL", 2: "RAISE"},
    min_raise=20,
    max_raise=990
)

# Test on_round_start
p.on_round_start(round_state, 990)

# Test get_action
action = p.get_action(round_state, 990)
print(f"Player action: {action}")

# Test on_round_end
p.on_end_round(round_state, 200)

# Test on_game_end
p.on_end_game(round_state, 50)  # Test with a score of 50
