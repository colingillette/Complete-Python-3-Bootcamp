import random

### Domain
blackjack = 21
dealer_stand = 17
starting_chips = 100
values = { 'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11 }
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 
            'Jack', 'Queen', 'King', 'Ace')

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.visible = True
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:

    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        random.shuffle(self.cards)

    def update_deck(self, table_cards):
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                valid = True
                for tcard in table_cards:
                    if card.suit == tcard.suit and card.rank == tcard.rank:
                        valid = False
                        break
                if valid:
                    self.cards.append(card)
        
    def deal(self):
        return self.cards.pop()

class Player:

    def __init__(self, name, chips):
        self.name = name
        self.cards = []
        self.chips = chips
        self.bet = 0

    def hit(self, card):
        self.cards.append(card)

    def fold(self):
        self.cards = []

    def score(self):
        i = 0
        ace_count = 0
        for card in self.cards:
            if card.visible:
                i += card.value
                if card.value == 11:
                    ace_count += 1
        if ace_count > 0 and i > blackjack:
            temp = i
            for ace in range(0, ace_count):
                temp -= 10
                if temp <= blackjack:
                    return temp 
        return i

    def resolve_chips(self):
        self.chips += self.bet

    def hide_one(self):
        self.cards[-1].visible = False

    def __str__(self):
        return f'{self.name} showing {self.score()}'

### Functions

def get_players():
    players = []
    more = True
    while more:
        name = input('Please enter the name of the player. Type n to stop: ')
        if name.lower() == 'n':
            if len(players) == 0:
                print('Need at least one player.')
            else:
                more = False
        else:
            player = Player(name, starting_chips)
            players.append(player)
    return players

def get_player_cards(players):
    cards = []
    for player in players:
        cards.extend(player.cards)
    return cards

def get_bet(player):
    bet = 0
    go = True
    while go:
        command = input(f'{player.name} has {player.chips} chips. Enter bet, or enter 0 to stop: ')
        try:
            bet = int(command)
        except:
            print('Bet must be a whole number not exceeding your chips.')
        if bet > 0:
            if bet > player.chips:
                print('Bet must be a whole number not exceeding your chips.')
            else:
                go = False
        elif bet < 0:
            print('Bet must be a whole number not exceeding your chips.')
        else:
            go = False
    return bet

def player_quit(players):
    for i in range(0, len(players)):
        if i != (len(players) - 1):
            if players[i].bet == 0:
                return True
    return False

def play(player, deck, players):
    go = True
    while go:
        for card in player.cards:
            card.visible = True
        print(player)
        if player.score() >= blackjack:
            print('Hand done')
            break
        command = input('What would you like to do (hit or stand): ')
        if command.lower() == 'hit':
            if len(deck.cards) == 0:
                deck.update_deck(get_player_cards(players))
            player.hit(deck.deal())
        else:
            go = False

def automate_play(player, deck, players):
    for card in player.cards:
        card.visible = True
    while player.score() < dealer_stand:
        print(f'{player} Hits')
        if len(deck.cards) == 0:
            deck.update_deck(get_player_cards(players))
        player.hit(deck.deal())
    print(f'{player} Stands')

def resolve(player, dealer):
    result = player.bet
    if player.score() > blackjack:
        print(f'{player} Loses!')
        result *= -1
    elif dealer.score() > blackjack or player.score() > dealer.score():
        print(f'{player} Wins!')
        result *= 2
    elif player.score() == dealer.score():
        print(f'{player} Draw!')
    else:
        print(f'{player} Loses!')
        result *= -1
    player.bet = result

### Main

deck = Deck()
deck.shuffle()
players = []
players.extend(get_players())
players.append(Player('Dealer', 100000000))

go = True
while go:
    for i in range(0, len(players)):
        if i != (len(players) - 1):
            players[i].bet = get_bet(players[i])

    if player_quit(players):
        go = False
        print('Thanks for playing!')
        break
    
    for i in range(0,2):
        for player in players:
            if len(deck.cards) == 0:
                deck.update_deck(get_player_cards(players))
            player.hit(deck.deal())
    players[-1].hide_one()

    for i in range(0, len(players)):
        if i != (len(players) - 1):
            play(players[i], deck, players)
        else:
            automate_play(players[i], deck, players)

    dealer = players.pop()
    for player in players:
        resolve(player, dealer)
        player.fold()
        player.resolve_chips()
    players.append(dealer)