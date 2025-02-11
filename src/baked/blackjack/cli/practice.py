import random
import time

from baked.blackjack.basicstrategy.practice.hands import FullPractice
from baked.blackjack.basicstrategy.service import Rule, Service as BasicStrategy
from baked.blackjack.model.model import Card, CardDeck, Play


def strategy_decks(double_down: bool, double_after_split: bool, surrender: bool, ignore: str, decks: int):
    if ignore:
        valid_ignore: set = set(["ACE", "SPLIT"])
        ignore: set = set(ignore.split(","))
        if ignore.difference(valid_ignore):
            raise Exception("Invalid ignore setting")
   
    bs = BasicStrategy()
    if double_down:
        bs.add_rule(Rule.ALLOW_DOUBLE)
    if double_after_split:
        bs.add_rule(Rule.ALLOW_DOUBLE_AFTER_SPLIT)
    if surrender:
        bs.add_rule(Rule.ALLOW_SURRENDER)

    card_deck = CardDeck() * decks
    
    random.shuffle(card_deck)
    player_hand = [None, None]
    dealer_hand = [None, None]
    render_card = lambda c: c.value if c != Card.ACE else c.name[0]

    correct = skip = total = 0
    total_time = 0
    while len(card_deck) >= 4:
        player_hand[0] = card_deck.pop(0)
        dealer_hand[0] = card_deck.pop(0)
        player_hand[1] = card_deck.pop(0)
        dealer_hand[1] = card_deck.pop(0)

        if ignore and "ACE" in ignore and (player_hand[0] == Card.ACE or player_hand[1] == Card.ACE):
            skip += 1
            continue
        elif ignore and "SPLIT" in ignore and player_hand[0] == player_hand[1]:
            skip += 1
            continue

        exp_move = bs.get_play(player_hand, dealer_hand[1])

        print("---------------")
        print(f"DEALER: _ {render_card(dealer_hand[1])}")
        print(f"PLAYER: {render_card(player_hand[0])} {render_card(player_hand[1])}")

        start = time.time()
        m = input("Move: ")
        move = {
            "d": Play.DOUBLE,
            "h": Play.HIT,
            "p": Play.SPLIT,
            "s": Play.STAND,
            "x": Play.SURRENDER
        }.get(m.lower(), None)
        if not move:
            try:
                move = Play(m.upper())
            except:
                pass

        move_time = round(time.time() - start, 2)

        if not move:
            print("Invalid move")
            skip += 1
            continue
        elif move == exp_move:
            print(f"{move.upper()} is Correct ({move_time} secs)")
            correct += 1
        else:
            print(f"Incorrect, expected {exp_move.value} ({move_time} secs)")

        total += 1
        total_time += move_time

    print("---------------")
    print("")
    print(f"Finished: {correct}/{total} correct{f' ({skip} skipped)' if skip else ''} \
          in {round(total_time / total, 2)} secs per move")


def strategy_practice(double_down: bool, double_after_split: bool, surrender: bool, ignore: str):
    if ignore:
        valid_ignore: set = set(["ACE", "SPLIT"])
        ignore: set = set(ignore.split(","))
        if ignore.difference(valid_ignore):
            raise Exception("Invalid ignore setting")
   
    bs = BasicStrategy()
    if double_down:
        bs.add_rule(Rule.ALLOW_DOUBLE)
    if double_after_split:
        bs.add_rule(Rule.ALLOW_DOUBLE_AFTER_SPLIT)
    if surrender:
        bs.add_rule(Rule.ALLOW_SURRENDER)

    correct = skip = total = 0
    total_time = 0
    practice = FullPractice(randomize=True)
    render_card = lambda c: str(c.value) if c < Card.TEN else c.name[0]

    for player_hand, dealer in practice:
        if ignore and "ACE" in ignore and (player_hand[0] == Card.ACE or player_hand[1] == Card.ACE):
            skip += 1
            continue
        elif ignore and "SPLIT" in ignore and player_hand[0] == player_hand[1]:
            skip += 1
            continue

        exp_move = bs.get_play(player_hand, dealer)

        print("---------------")
        print(f"DEALER: {render_card(dealer)}")
        print(f"PLAYER: {render_card(player_hand[0])} {render_card(player_hand[1])}")

        start = time.time()
        m = input("Move: ")
        move = {
            "d": Play.DOUBLE,
            "h": Play.HIT,
            "p": Play.SPLIT,
            "s": Play.STAND,
            "x": Play.SURRENDER
        }.get(m.lower(), None)
        if not move:
            try:
                move = Play(m.upper())
            except:
                pass

        move_time = round(time.time() - start, 2)

        if not move:
            print("Invalid move")
            skip += 1
            continue
        elif move == exp_move:
            print(f"{move.upper()} is Correct ({move_time} secs)")
            correct += 1
        else:
            print(f"Incorrect, expected {exp_move.value} ({move_time} secs)")

        total += 1
        total_time += move_time

    print("---------------")
    print("")
    print(f"Finished: {correct}/{total} correct{f' ({skip} skipped)' if skip else ''} \
          in {round(total_time / total, 2)} secs per move")