from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class RoundStateClient:
    round_num: int
    round: str
    community_cards: list
    pot: int
    current_player: int
    current_bet: int
    min_raise: int
    max_raise: int
    player_bets: dict[int, int]
    player_actions: dict[int, str]
    player_money: dict[int, int] = None  # New field for player money
    side_pots: list[dict[str, any]] = None  # List of dicts with 'amount' and 'eligible_players' keys
    
    @classmethod
    def from_message(cls, message: Dict[str, Any]) -> 'RoundStateClient':
        """Create RoundStateClient from a message dictionary"""
        return cls(
            round_num=message['round_num'],
            round=message['round'],
            community_cards=message['community_cards'],
            pot=message['pot'],
            current_player=message['current_player'],
            current_bet=message['current_bet'],
            min_raise=message['min_raise'],
            max_raise=message['max_raise'],
            player_bets=message['player_bets'],
            player_actions=message['player_actions'],
            player_money=message.get('player_money'),
            side_pots=message.get('side_pots', [])
        )