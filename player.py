import ast
import random
import eval7
from typing import List, Tuple
from bot import Bot
from type.poker_action import PokerAction
from type.round_state import RoundStateClient

class SimplePlayer(Bot):
    def __init__(self):
        super().__init__()
        self.my_hand = None  # List[eval7.Card]
        self.all_players = []
        self.preflop_aggressor = False

    def on_start(self, starting_chips: int, player_hands: List[str], blind_amount: int, big_blind_player_id: int, small_blind_player_id: int, all_players: List[int]):
        print("Player called on game start")
        print("Player hands: ", player_hands)
        print("Blind: ", blind_amount)
        print("Big blind player id: ", big_blind_player_id)
        print("Small blind player id: ", small_blind_player_id)
        print("All players in game: ", all_players)
        print("My id: ", self.id)
        self.all_players = all_players
        # Parse hand from string using eval7
        if player_hands and isinstance(player_hands[0], str) and player_hands[0].startswith('Hands: '):
            hands_str = player_hands[0].replace('Hands: ', '')
            hands_dict = ast.literal_eval(hands_str)
            my_hand_strs = hands_dict.get(self.id)
            if my_hand_strs:
                self.my_hand = [self.card_from_string(card_str) for card_str in my_hand_strs]
            else:
                self.my_hand = None
        else:
            # fallback: assume player_hands is a list of card strings
            self.my_hand = [eval7.Card(card) for card in player_hands[self.id]] if self.id < len(player_hands) else None
        self.preflop_aggressor = False

    def card_from_string(self, card_str):
        # card_str is like 'Card("9s")' or 'Card("Kc")'
        if card_str.startswith('Card("') and card_str.endswith('")'):
            rank_suit = card_str[6:-2]
            return eval7.Card(rank_suit)
        else:
            return eval7.Card(card_str)

    def on_round_start(self, round_state: RoundStateClient, remaining_chips: int):
        print("Player called on round start")
        print("Round state: ", round_state)

    def evaluate_hand_strength(self, hand, community_cards) -> float:
        # Use eval7 to evaluate hand strength
        if not hand or len(hand) < 2:
            return 1.0
        evaluator = eval7.Evaluator()
        # Preflop: use a simple lookup or simulation (here, use high card value as proxy)
        if not community_cards:
            ranks = [c.rank for c in hand]
            values = [eval7.RANKS.index(r) for r in ranks]
            # Pair
            if ranks[0] == ranks[1]:
                return 9.5 if values[0] >= 10 else 8.5
            # Suited connectors
            if hand[0].suit == hand[1].suit and abs(values[0] - values[1]) == 1:
                return 8.0
            # Both high cards
            if values[0] >= 10 and values[1] >= 10:
                return 8.5
            # One high card
            if max(values) >= 11:
                return 7.5
            return 5.0
        # Postflop: use eval7 to get hand strength percentile
        board = [self.card_from_string(c) if isinstance(c, str) else c for c in community_cards]
        hand_value = evaluator.evaluate(board, hand)
        # Normalize: 1 (worst) to 10 (best)
        # eval7: lower value is better (0 is best hand)
        max_score = evaluator._rank_to_handtype[7462][0]  # 7462 is the worst hand rank
        norm = 1 + 9 * (max_score - hand_value) / max_score
        return max(1.0, min(10.0, norm))

    def is_pair(self, hand, rank):
        return hand[0].rank == hand[1].rank and hand[0].rank == rank

    def is_top_pair(self, hand, community_cards):
        if not community_cards:
            return False
        board = [self.card_from_string(c) if isinstance(c, str) else c for c in community_cards]
        board_ranks = [c.rank for c in board]
        hand_ranks = [c.rank for c in hand]
        top_board = max(board_ranks, key=lambda r: eval7.RANKS.index(r))
        return any(r == top_board for r in hand_ranks)

    def is_overcard(self, card, community_cards):
        if not community_cards:
            return False
        board = [self.card_from_string(c) if isinstance(c, str) else c for c in community_cards]
        card_val = eval7.RANKS.index(card.rank)
        return all(card_val > eval7.RANKS.index(c.rank) for c in board)

    def has_flush_draw(self, hand, community_cards):
        all_cards = hand + [self.card_from_string(c) if isinstance(c, str) else c for c in community_cards]
        suits = [c.suit for c in all_cards]
        return max([suits.count(s) for s in set(suits)]) == 4

    def get_position(self, round_state):
        idx = self.all_players.index(self.id) if self.id in self.all_players else 0
        if idx < len(self.all_players) // 2:
            return "early"
        else:
            return "late"

    def get_action(self, round_state: RoundStateClient, remaining_chips: int) -> Tuple[PokerAction, int]:
        print("Player called get action")
        round_type = round_state.round.upper() if hasattr(round_state, 'round') else "PREFLOP"
        strength = self.evaluate_hand_strength(self.my_hand, round_state.community_cards)
        pot = round_state.pot
        position = self.get_position(round_state)
        min_raise = round_state.min_raise
        max_raise = round_state.max_raise
        current_bet = round_state.current_bet
        player_bets = round_state.player_bets
        player_actions = round_state.player_actions
        my_bet = player_bets.get(str(self.id), 0)
        # Preflop logic
        if round_type == "PREFLOP":
            # Squeeze and all-in with AA/KK/QQ
            if self.is_pair(self.my_hand, 'A') or self.is_pair(self.my_hand, 'K') or self.is_pair(self.my_hand, 'Q'):
                self.preflop_aggressor = True
                return PokerAction.RAISE, remaining_chips  # All-in
            # Call other opens with hand score > 7
            if strength > 7.0 and current_bet > 0 and my_bet < current_bet:
                return PokerAction.CALL, current_bet - my_bet
            # Otherwise fold
            return PokerAction.FOLD, 0
        # Postflop logic: all-in with top pair or better
        if self.has_top_pair_or_better(self.my_hand, round_state.community_cards):
            return PokerAction.ALL_IN, remaining_chips
        return PokerAction.FOLD, 0

    def has_top_pair_or_better(self, hand, community_cards):
        if not community_cards:
            return False
        evaluator = eval7.Evaluator()
        board = [self.card_from_string(c) if isinstance(c, str) else c for c in community_cards]
        hand_value = evaluator.evaluate(board, hand)
        # Find the best possible top pair hand for this board
        board_ranks = [c.rank for c in board]
        top_board = max(board_ranks, key=lambda r: eval7.RANKS.index(r))
        # Try all possible top pair hands with this board
        top_pair_hands = []
        for c in hand:
            if c.rank == top_board:
                # The other card is kicker
                for kicker in eval7.RANKS:
                    if kicker != top_board:
                        top_pair_hands.append([eval7.Card(f"{top_board}{hand[0].suit}"), eval7.Card(f"{kicker}{hand[1].suit}")])
        # If our hand is at least as strong as any top pair hand, return True
        for tp_hand in top_pair_hands:
            tp_value = evaluator.evaluate(board, tp_hand)
            if hand_value <= tp_value:
                return True
        # If no top pair hand found, fallback to original top pair logic
        return self.is_top_pair(hand, community_cards)

    def has_medium_or_better_kicker(self, hand, community_cards):
        # Assume top pair is present, check if kicker is Q or better
        board = [self.card_from_string(c) if isinstance(c, str) else c for c in community_cards]
        board_ranks = [c.rank for c in board]
        hand_ranks = [c.rank for c in hand]
        top_board = max(board_ranks, key=lambda r: eval7.RANKS.index(r))
        # Find the kicker (the non-top-pair card)
        for c in hand:
            if c.rank != top_board:
                # Q or better kicker
                return eval7.RANKS.index(c.rank) >= eval7.RANKS.index('Q')
        return False

    def has_straight_draw(self, hand, community_cards):
        # Only open-ended straight draws (OESD): 4 consecutive ranks with two outs
        all_cards = hand + [self.card_from_string(c) if isinstance(c, str) else c for c in community_cards]
        values = sorted(set([eval7.RANKS.index(c.rank) for c in all_cards]))
        for i in range(len(values) - 3):
            # OESD: four consecutive cards, and both ends are open
            if values[i+3] - values[i] == 3 and values[i+1] - values[i] == 1 and values[i+2] - values[i+1] == 1 and values[i+3] - values[i+2] == 1:
                # Check that neither the lowest nor highest card is an Ace-low wrap (A234 is not open-ended)
                # OESD is e.g. 5-6-7-8 (outs: 4 or 9)
                return True
        return False

    def board_is_high(self, community_cards):
        if not community_cards:
            return False
        board = [self.card_from_string(c) if isinstance(c, str) else c for c in community_cards]
        values = [eval7.RANKS.index(c.rank) for c in board]
        return sum(v >= 8 for v in values) >= 2  # 8 = 'T', so T/J/Q/K/A

    def on_end_round(self, round_state: RoundStateClient, remaining_chips: int):
        """ Called at the end of the round. """
        print("Player called on end round")

    def on_end_game(self, round_state: RoundStateClient, player_score: float, all_scores: dict, active_players_hands: dict):
        print("Player called on end game, with player score: ", player_score)
        print("All final scores: ", all_scores)
        print("Active players hands: ", active_players_hands)