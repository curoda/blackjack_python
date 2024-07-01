import random
from collections import defaultdict
import numpy as np
import streamlit as st

# Basic strategy lookup table
basic_strategy = {
    'hard': {
        (5, 6, 7, 8): 'H',
        (9,): {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 'A': 'H'},
        (10,): {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'H', 'A': 'H'},
        (11,): {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'D', 'A': 'H'},
        (12,): {2: 'H', 3: 'H', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 'A': 'H'},
        (13, 14): {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 'A': 'H'},
        (15,): {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'R', 'A': 'H'},
        (16,): {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'R', 10: 'R', 'A': 'R'},
        (17, 18, 19, 20, 21): 'S'
    },
    'soft': {
        (13, 14): {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 'A': 'H'},
        (15, 16): {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 'A': 'H'},
        (17,): {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 'A': 'H'},
        (18,): {2: 'S', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'S', 8: 'S', 9: 'H', 10: 'H', 'A': 'H'},
        (19, 20, 21): 'S'
    },
    'pair': {
        ('A', 'A'): 'Y',
        ('T', 'T'): 'N',
        ('9', '9'): {2: 'Y', 3: 'Y', 4: 'Y', 5: 'Y', 6: 'Y', 7: 'N', 8: 'Y', 9: 'Y', 10: 'N', 'A': 'N'},
        ('8', '8'): 'Y',
        ('7', '7'): {2: 'Y', 3: 'Y', 4: 'Y', 5: 'Y', 6: 'Y', 7: 'Y', 8: 'N', 9: 'N', 10: 'N', 'A': 'N'},
        ('6', '6'): {2: 'Y', 3: 'Y', 4: 'Y', 5: 'Y', 6: 'Y', 7: 'N', 8: 'N', 9: 'N', 10: 'N', 'A': 'N'},
        ('5', '5'): 'N',
        ('4', '4'): {2: 'N', 3: 'N', 4: 'N', 5: 'Y', 6: 'Y', 7: 'N', 8: 'N', 9: 'N', 10: 'N', 'A': 'N'},
        ('3', '3'): {2: 'Y', 3: 'Y', 4: 'Y', 5: 'Y', 6: 'Y', 7: 'Y', 8: 'N', 9: 'N', 10: 'N', 'A': 'N'},
        ('2', '2'): {2: 'Y', 3: 'Y', 4: 'Y', 5: 'Y', 6: 'Y', 7: 'Y', 8: 'N', 9: 'N', 10: 'N', 'A': 'N'}
    }
}

def get_action(player_hand, dealer_upcard):
    """Returns the optimal action based on the player's hand and the dealer's upcard."""
    # Map dealer upcard values correctly
    dealer_value = dealer_upcard.value()
    if dealer_value == 11:
        dealer_value = 'A'
    
    if len(player_hand.cards) == 2 and player_hand.cards[0].rank == player_hand.cards[1].rank:
        pair = (player_hand.cards[0].rank, player_hand.cards[1].rank)
        if pair in basic_strategy['pair']:
            action = basic_strategy['pair'][pair]
            return action if isinstance(action, str) else action[dealer_value]

    hand_type = 'soft' if any(card.rank == 'A' and card.value() == 11 for card in player_hand.cards) else 'hard'
    player_total = player_hand.value()
    
    if hand_type == 'soft':
        if player_total in basic_strategy['soft']:
            action = basic_strategy['soft'][player_total]
            return action if isinstance(action, str) else action[dealer_value]
    else:
        if player_total in basic_strategy['hard']:
            action = basic_strategy['hard'][player_total]
            return action if isinstance(action, str) else action[dealer_value]

    return 'H'  # Default action if not specified

class Card:
    """Represents a single card in a deck."""
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value(self):
        """Returns the value of the card."""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

class Deck:
    """Represents a deck of cards, which can consist of multiple decks."""
    def __init__(self, num_decks=8):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = [Card(rank, suit) for _ in range(num_decks) for rank in ranks for suit in suits]
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def deal(self):
        """Deals a card from the deck, reinitializing if the deck is empty."""
        if not self.cards:
            self.__init__()
        return self.cards.pop()

class Hand:
    """Represents a player's or dealer's hand in blackjack."""
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """Adds a card to the hand."""
        self.cards.append(card)

    def value(self):
        """Calculates the total value of the hand, adjusting for Aces as needed."""
        total = sum(card.value() for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 'A')
        while total > 21 and num_aces > 0:
            total -= 10
            num_aces -= 1
        return total

class BlackjackGame:
    """Represents a game of blackjack."""
    def __init__(self, num_decks=8, blackjack_payout=1.5, dealer_hit_soft_17=True):
        self.deck = Deck(num_decks)
        self.blackjack_payout = blackjack_payout
        self.dealer_hit_soft_17 = dealer_hit_soft_17

    def play_hand(self, bet):
        """Simulates a single hand of blackjack."""
        player_hand = Hand()
        dealer_hand = Hand()

        # Initial deal
        player_hand.add_card(self.deck.deal())
        dealer_hand.add_card(self.deck.deal())
        player_hand.add_card(self.deck.deal())
        dealer_hand.add_card(self.deck.deal())

        # Check for blackjack
        if player_hand.value() == 21:
            if dealer_hand.value() == 21:
                return 0  # Push
            else:
                return bet * self.blackjack_payout

        # Player decisions based on basic strategy
        while True:
            action = get_action(player_hand, dealer_hand.cards[0])
            st.write(f"Player action: {action}, Player hand value: {player_hand.value()}")
            if action == 'H':
                player_hand.add_card(self.deck.deal())
                if player_hand.value() > 21:
                    return -bet  # Player busts
            elif action == 'S':
                break
            elif action == 'D':
                player_hand.add_card(self.deck.deal())
                bet *= 2
                break
            elif action == 'Y':
                return self.handle_split(player_hand, dealer_hand, bet)
            elif action == 'R':
                return -bet / 2  # Player surrenders

        # Dealer decisions
        while dealer_hand.value() < 17 or (dealer_hand.value() == 17 and self.dealer_hit_soft_17):
            dealer_hand.add_card(self.deck.deal())
            st.write(f"Dealer hand value: {dealer_hand.value()}")

        return self.resolve_hand(player_hand, dealer_hand) * bet

    def resolve_hand(self, player_hand, dealer_hand):
        """Resolves the outcome of a hand."""
        if player_hand.value() > 21:
            return -1  # Player busts
        elif dealer_hand.value() > 21 or player_hand.value() > dealer_hand.value():
            return 1  # Player wins
        elif player_hand.value() == dealer_hand.value():
            return 0  # Push
        else:
            return -1  # Dealer wins

    def can_split(self, hand):
        """Determines if the player can split their hand."""
        return len(hand.cards) == 2 and hand.cards[0].rank == hand.cards[1].rank

    def handle_split(self, player_hand, dealer_hand, bet):
        """Handles splitting a hand."""
        split_hand_1 = Hand()
        split_hand_2 = Hand()
        
        split_hand_1.add_card(player_hand.cards[0])
        split_hand_2.add_card(player_hand.cards[1])
        
        split_hand_1.add_card(self.deck.deal())
        split_hand_2.add_card(self.deck.deal())
        
        result_1 = self.play_split_hand(split_hand_1, dealer_hand, bet)
        result_2 = self.play_split_hand(split_hand_2, dealer_hand, bet)
        
        return result_1 + result_2

    def play_split_hand(self, player_hand, dealer_hand, bet):
        """Plays a hand that has been split."""
        while True:
            action = get_action(player_hand, dealer_hand.cards[0])
            st.write(f"Player action: {action}, Player hand value: {player_hand.value()}")
            if action == 'H':
                player_hand.add_card(self.deck.deal())
                if player_hand.value() > 21:
                    return -bet  # Player busts
            elif action == 'S':
                break
            elif action == 'D':
                player_hand.add_card(self.deck.deal())
                bet *= 2
                break
            elif action == 'R':
                return -bet / 2  # Player surrenders

        # Dealer decisions
        while dealer_hand.value() < 17 or (dealer_hand.value() == 17 and self.dealer_hit_soft_17):
            dealer_hand.add_card(self.deck.deal())
            st.write(f"Dealer hand value: {dealer_hand.value()}")

        return self.resolve_hand(player_hand, dealer_hand) * bet

def run_simulation(num_simulations, max_hands, win_goal, max_loss, min_bet):
    """Runs the blackjack simulation."""
    game = BlackjackGame()
    results = []
    progress_bar = st.progress(0)

    for i in range(num_simulations):
        bankroll = 0
        hands_played = 0

        while hands_played < max_hands and bankroll > -max_loss and bankroll < win_goal:
            result = game.play_hand(min_bet)
            bankroll += result
            hands_played += 1

            # Debug log for each hand
            st.write(f"Simulation {i + 1}, Hand {hands_played}: Bankroll = {bankroll}")

        results.append((bankroll, hands_played))
        if i % 10 == 0:  # Update progress every 10 simulations
            progress_bar.progress(i / num_simulations)
            st.write(f"Simulation {i + 1} of {num_simulations} completed")

    progress_bar.progress(1.0)  # Complete the progress bar
    return results

def analyze_results(results, min_bet):
    """Analyzes the results of the simulation."""
    bankrolls, hands_played = zip(*results)
    
    avg_bankroll = np.mean(bankrolls)
    std_bankroll = np.std(bankrolls)
    
    wins = sum(1 for b in bankrolls if b > 0)
    losses = sum(1 for b in bankrolls if b < 0)
    
    avg_hands = np.mean(hands_played)
    
    return {
        'avg_bankroll': avg_bankroll,
        'std_bankroll': std_bankroll,
        'win_probability': wins / len(results),
        'loss_probability': losses / len(results),
        'avg_hands_played': avg_hands,
        'earnings_potential': avg_bankroll / min_bet
    }

def main(num_simulations, min_bet, max_hands):
    """Main function to run the blackjack simulation."""
    results = defaultdict(dict)
    
    for max_loss in [5, 10, 20]:
        for win_goal in [1, 2, 5, 10]:
            st.write(f"Running simulation for max_loss={max_loss}x, win_goal={win_goal}x")
            sim_results = run_simulation(num_simulations, max_hands, win_goal * min_bet, max_loss * min_bet, min_bet)
            results[max_loss][win_goal] = analyze_results(sim_results, min_bet)

    # Print results
    st.write("\nEarnings Potential (e_f):")
    st.write("   ", end="")
    for win_goal in [1, 2, 5, 10]:
        st.write(f"{win_goal:>8}x", end="")
    st.write()
    
    for max_loss in [5, 10, 20]:
        st.write(f"{max_loss:2}x", end="")
        for win_goal in [1, 2, 5, 10]:
            st.write(f"{results[max_loss][win_goal]['earnings_potential']:8.2f}", end="")
        st.write()

    return results

# Streamlit interface
st.title("Blackjack Simulation")

num_simulations = st.number_input("Number of Simulations", min_value=1, max_value=10000, value=10, step=1)
min_bet = st.number_input("Minimum Bet", min_value=1, max_value=1000, value=50, step=10)
max_hands = st.number_input("Maximum Hands", min_value=1, max_value=1000, value=200, step=10)

if st.button("Run Simulation"):
    simulation_results_further_reduced = main(num_simulations, min_bet, max_hands)
    st.write(simulation_results_further_reduced)
