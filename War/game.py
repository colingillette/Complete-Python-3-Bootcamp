import domain.classes as domain

player_one = domain.Player("One")
player_two = domain.Player("Two")

deck = domain.Deck()
deck.shuffle()

for x in range(26):
    player_one.add_cards(deck.deal_one())
    player_two.add_cards(deck.deal_one())

game_on = True
round_num = 0
war_count = 5

while game_on:
    round_num += 1
    print(f'Round {round_num}')

    if len(player_one.all_cards) == 0:
        print(f'Player {player_one.name}, out of cards! Loser!')
        game_on = False
        break
    if len(player_two.all_cards) == 0:
        print(f'Player {player_two.name}, out of cards! Loser!')
        game_on = False
        break

    player_one_cards = []
    player_one_cards.append(player_one.remove_one())
    player_two_cards = []
    player_two_cards.append(player_two.remove_one())

    at_war = True
    while at_war:
        print(f'{player_one_cards[-1].value} vs {player_two_cards[-1].value}')
        if player_one_cards[-1].value > player_two_cards[-1].value:
            player_one.add_cards(player_one_cards)
            player_two.add_cards(player_two_cards)
            at_war = False
            print(f'Player {player_one.name} Round Win')
        elif player_two_cards[-1].value > player_one_cards[-1].value:
            player_two.add_cards(player_one_cards)
            player_two.add_cards(player_two_cards)
            at_war = False
            print(f'Player {player_two.name} Round Win')
        else:
            print('WAR!')
            if len(player_one.all_cards) < war_count:
                print(f'Player {player_one.name} unable to declare war!')
                at_war = False
                game_on = False
                print('Loser!')
                break
            elif len(player_two.all_cards) < war_count:
                print(f'Player {player_two.name} unable to declare war!')
                at_war = False
                game_on = False
                print('Loser!')
                break
            else:
                for i in range(0, war_count):
                    player_one_cards.append(player_one.remove_one())
                    player_two_cards.append(player_two.remove_one())
            
