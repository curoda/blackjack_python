import random
# global variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs') # Tuples
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {
'Two':2,
'Three':3,
'Four':4,
'Five':5,
'Six':6,
'Seven':7,
'Eight':8,
'Nine':9, 
'Ten':10,
'Jack':10,
'Queen':10,
'King':10,
'Ace':11
} # dictionary
playing = True # bool

# create a card class
class Card():
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
	def __str__(self):
		return self.rank + " of " + self.suit

# create deck class
class Deck():
	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit,rank)) # appending the Card object to self.deck list

	def __str__(self):
		deckComposition = '' # set the deck comp as an empty string
		for card in self.deck:
			deckComposition += '\n'+ card.__str__() # Card class string representation
		return "The deck has: " + deckComposition
	
	def shuffle(self):
		random.shuffle(self.deck)

# grab the deck attribute of Deck class then pop off card item from list and set it to single card
	def deal(self):
		singleCard = self.deck.pop()
		return singleCard

# testing everything so far
# testDeck = Deck()
# testDeck.shuffle()
# print(testDeck)

# create hand class: grabbing the single card and adding to someone's hand
class Hand():
	def __init__(self):
		self.cards = [] # start with 0 cards in hand
		self.value = 0 # starting with 0 value
		self.aces = 0 # keep track of aces

	# card object is Deck.deal() that has single card and sc has suit and rank
	def addCard(self, card):
		self.cards.append(card) # taking card object and appending it to self.cards list
		# take the cards rank and lookup in values dict and add to self.value
		# if value is > 21 this particular hand has lost the game
		self.value += values [card.rank]

		# track aces
		if card.rank == 'Ace':
			self.aces += 1
	
# test_deck = Deck()
# test_deck.shuffle()
# test_player = Hand()
# pulled_card = test_deck.deal()
# print(pulled_card)
# test_player.addCard(pulled_card)
# print(test_player.value)
	def checkAces(self):
		# if value > 21 and if ace is available
		while self.value > 21 and self.aces: # we can also set this to > 0
			self.value -= 10 # take my value and subtract 10 
			self.aces -= 1 # take my aces and subtract 1

# create chips class
class Chips():
	def __init__(self, total=1000):
		self.total = total # set a default value or allow user to input
		self.bet = 0

	def winBet(self):
		self.total += self.bet

	def loseBet(self):
		self.total -= self.bet

# create a function for taking bets
def takeBet(chips):
	while True:
		try:
			chips.bet = int(input("How many chips would you like to bet? "))
		except ValueError:
			print('Sorry, a bet must be a number!')
		else:
			if chips.bet > chips.total:
				print("Sorry, your bet can't exceed, you have only {} chips left." .format(chips.total))
			else:
				break

# function for taking hits
def hit(deck, hand):
	# handCard = deck.deal()
	# hand.addCard(singleCard)
	# hand.checkAces()
	hand.addCard(deck.deal())
	hand.checkAces()

# function for asking player hit/stand
def hitOrStand(deck, hand):
	global playing

	while True:
		x = input("Would you like to Hit or Stand? Enter 'h' or 's': ")

		if x[0].lower() == 'h':
			hit(deck, hand)
		elif x[0].lower() == 's':
			print("Player stands. Dealer is playing.")
			playing = False
		else:
			print("Sorry, try again!")
			continue

		break


# function for showing cards
def showCards(player, dealer):
	
	print("\nDealers's Turn: ")
	print("<card hidden>")
	# print(' ' + dealer.cards[1].__str__())
	print('',dealer.cards[1])
	print("\nPlayer's Turn:", *player.cards, sep='\n ')

def showAll(player,dealer):

	# asterisk * symbol is used to print every item in a collection
	print("\nDealer's Turn:", *dealer.cards, sep='\n ') # sep='\n ' argument prints each item on a separate line
	print("Dealer's Turn =", dealer.value)
	print("\nPlayer's Turn:", *player.cards, sep='\n ')
	print("Player's Turn =", player.value)

# functions for ending game scenarios
def playerBusted(player, dealer, chips):
	
	print("Player busted!")
	chips.loseBet()

def playerWins(player, dealer, chips):
	
	print("Player wins!")
	chips.winBet()

def dealerBusted(player, dealer, chips):
	
	print("Dealer busted!")
	chips.loseBet()

def dealerWins(player, dealer, chips):
	print("Dealer busted!")
	chips.winBet()

def greatTie(player, dealer):
	print("Wow! This is a tie")

# play logic for game

while True:
	print("Welcome to BlackJack")
	# shuffle and deal two cards to each player
	deck = Deck()
	deck.shuffle()

	playerHand = Hand()
	playerHand.addCard(deck.deal())
	playerHand.addCard(deck.deal())

	dealerHand = Hand()
	dealerHand.addCard(deck.deal())
	dealerHand.addCard(deck.deal())

	playerChips = Chips() # players chips
	takeBet(playerChips) # prompting player for their bet

	showCards(playerHand, dealerHand) # show cards for dealer and player

	while playing:
		hitOrStand(deck, playerHand) # prompt for hit or stand

		showCards(playerHand, dealerHand)

		# if player hand exceeds 21 run playerBusted() and break
		if playerHand.value > 21:
			playerBusted(playerHand, dealerHand, playerChips)

			break

	# soft 17 rule: keep playing until dealer reaches 17
	if playerHand.value <= 21:
		while dealerHand.value < playerHand.value:
			hit(deck, dealerHand)

		showAll(playerHand, dealerHand) # show all cards

		# run a different game win scenario
		if dealerHand.value > 21:
			dealerBusted(playerHand, dealerHand, playerChips)
		elif dealerHand.value > playerHand.value:
			dealerWins(playerHand, dealerHand, playerChips)
		elif dealerHand.value < playerHand.value:
			playerWins(playerHand, dealerHand, playerChips)
		else:
			greatTie(playerHand, dealerHand)

	# show player their total remaining chips
	print("\n Player total chips are at: {}" .format(playerChips.total))

	#ask to play again
	newGame = input("Want to play again? y/n: ")
	
	if newGame[0].lower() == 'y':
		playing = True
		continue
	else:
		print("Thank you for playing BlackJack! See you again.")
		break
