import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# creates dictionary with keys 0-51 paired to a card e.g. 2S, TD, QH. (two of spades, ten of diamonds, queen of hearts)
values = [str(i) for i in range(2, 10)] + ["T", "J", "Q", "K", "A"]
suits = ["S", "H", "D", "C"]
deck = {}
for i in range(4):
    for j, v in enumerate(values):
        deck[i * 13 + j] = v + suits[i]


# create N hands of 5 cards randomly with no duplicates in a hand
def create_hands(n):
    hands = [[deck[j] for j in random.sample(range(52), 5)] for i in range(n)]
    print("Unsorted Poker hands:")
    for hand in hands:
        print("                       "+" ".join(hand))
    return hands


# sorts a set of hands based on poker ranking from best to worst
def sort_hands(hands):
    sorted_hands = []
    # format/order card set for easier ranking
    formatted_hands = {i: sorted([[int(card[0].replace("T", "10")
                                    .replace("J", "11")
                                    .replace("Q", "12")
                                    .replace("K", "13")
                                    .replace("A", "14")),
                            card[1]] for card in hand]) for i, hand in enumerate(hands)}

    # royal flush
    royal_flushes = []
    for key, hand in formatted_hands.items():
        # Condition for card set to be a royal flush. No further ranking is required as all royal flushes are equal
        if [card[0] for card in hand] == [10, 11, 12, 13, 14] and len(set([card[1] for card in hand])) == 1:
            royal_flushes.append(key)
    for key in royal_flushes:
        # add card set to the ranked list and remove it from the formatted list
        sorted_hands.append([hands[key], " Royal flush"])
        formatted_hands.pop(key)
    # straight flush
    straight_flushes = []
    for key, hand in formatted_hands.items():
        # Flush part
        if len(set([card[1] for card in hand])) == 1:
            # straight part
            if len(set([card[0] for card in hand])) == 5:
                # Condition for a straight flush. Ascending and same suit. Except for Ace, 1, 2, 3, 4
                if max([card[0] for card in hand]) - min([card[0] for card in hand]) == 4:
                    straight_flushes.append([hand, key])
                # Condition for straight flush with a low ace
                if [card[0] for card in hand] == [2, 3, 4, 5, 14]:
                    straight_flushes.append([hand, key])
    # sorts on first card rank of straight
    straight_flushes.sort(reverse=True)
    for key in straight_flushes:
        # add card set to the ranked list and remove it from the formatted list
        sorted_hands.append([hands[key[1]], " Straight flush"])
        formatted_hands.pop(key[1])
    # four of a kind
    fours = []
    for key, hand in formatted_hands.items():
        num_list = [card[0] for card in hand]
        for n in num_list:
            # Condition for four of a kind
            if num_list.count(n) == 4:
                for m in num_list:
                    # Add rank and kicker rank for sorting all four of a kinds later
                    if num_list.count(m) == 1:
                        fours.append([n, m, key])
                        break
                break
    # sorts on fours first, and then on the additional card rank
    fours.sort(reverse=True)
    for key in fours:
        # add card set to the ranked list and remove it from the formatted list
        sorted_hands.append([hands[key[2]], " Four of a kind"])
        formatted_hands.pop(key[2])
    # Full house
    full_houses = []
    for key, hand in formatted_hands.items():
        num_list = [card[0] for card in hand]
        for n in num_list:
            # check for 3 the same ranked cards
            if num_list.count(n) == 3:
                for m in num_list:
                    # check for 2 of the same ranked cards
                    if num_list.count(m) == 2:
                        # adds ranking. Threes first, doubles second
                        full_houses.append([n, m, key])
                        break
                break
    # sorts based on threes first, then on doubles
    full_houses.sort(reverse=True)
    for key in full_houses:
        sorted_hands.append([hands[key[2]], " Full House"])
        formatted_hands.pop(key[2])
    # flush
    flushes = []
    for key, hand in formatted_hands.items():
        if len(set([card[1] for card in hand])) == 1:
            # num_list adds ranking from high to low
            num_list = [card[0] for card in hand]
            num_list.sort(reverse=True)
            flushes.append([num_list, key])
    # sorts flushes from ranking/num_list
    flushes.sort(reverse=True)
    for key in flushes:
        sorted_hands.append([hands[key[1]], " Flush"])
        formatted_hands.pop(key[1])
    # straight
    straights = []
    for key, hand in formatted_hands.items():
        if len(set([card[0] for card in hand])) == 5:
            # Condition for a straight . Ascending and same suit. Except for Ace, 1, 2, 3, 4
            if max([card[0] for card in hand]) - min([card[0] for card in hand]) == 4:
                straights.append([hand, key])
            # Condition for straight flush with a low ace
            if [card[0] for card in hand] == [2, 3, 4, 5, 14]:
                straights.append([hand, key])
    # sorts all straights based on hand ranking from high to low
    straights.sort(reverse=True)
    for key in straights:
        sorted_hands.append([hands[key[1]], " Straight"])
        formatted_hands.pop(key[1])
    # three of a kind
    threes = []
    for key, hand in formatted_hands.items():
        num_list = [card[0] for card in hand]
        for n in num_list:
            # Condition for three of a kind
            if num_list.count(n) == 3:
                # ranking. Adds rank of threes first, and then adds other two cards from high to low
                rank_list = [n, sorted((list(set(num_list))), reverse=True)]
                rank_list[1].remove(n)
                threes.append([rank_list, key])
                break
    # sorts all threes
    threes.sort(reverse=True)
    for key in threes:
        sorted_hands.append([hands[key[1]], " Three of a kind"])
        formatted_hands.pop(key[1])
    # two pair
    two_pair = []
    for key, hand in formatted_hands.items():
        num_list = [card[0] for card in hand]
        rankings = []
        for num in num_list:
            if num_list.count(num) == 2:
                # adds doubles to rankings
                rankings.append(num)
        if len(rankings) == 4:
            # removes duplicates from doubles. Then ranks them from high to low
            rankings = sorted(list(set(rankings)), reverse=True)
            for num in num_list:
                if num not in rankings:
                    # adds last non double rank to rankings
                    rankings.append(num)
            two_pair.append([rankings, key])
    # sort all two pairs
    two_pair.sort(reverse=True)
    for key in two_pair:
        sorted_hands.append([hands[key[1]], " Two pair"])
        formatted_hands.pop(key[1])
    # pair
    pair = []
    for key, hand in formatted_hands.items():
        num_list = [card[0] for card in hand]
        rankings = []
        for num in num_list:
            if num_list.count(num) == 2:
                # adds pair to ranking
                rankings.append(num)
                break
        # if there is a pair found. continue here
        if len(rankings) == 1:
            # second order will be all other card ranks added after sorted from high to low
            second_order = []
            for num in num_list:
                if num not in rankings:
                    second_order.append(num)
            second_order.sort(reverse=True)
            rankings.append(second_order)
            pair.append([rankings, key])
    # sort all pairs
    pair.sort(reverse=True)
    for key in pair:
        sorted_hands.append([hands[key[1]], " Pair"])
        formatted_hands.pop(key[1])
    # high card
    highs = []
    for key, hand in formatted_hands.items():
        # num_list takes care of ranking
        num_list = [card[0] for card in hand]
        num_list.sort(reverse=True)
        highs.append([num_list, key])
    # sort all high cards
    highs.sort(reverse=True)
    for key in highs:
        sorted_hands.append([hands[key[1]], " High card"])
        formatted_hands.pop(key[1])
    for hand in sorted_hands:
        print(" ".join(hand[0]) + hand[1])
    return sorted_hands


sorted_hands_random = sort_hands(create_hands(10000))


df = pd.DataFrame({"Card": [i[1] for i in sorted_hands_random]})
input_df = df.groupby("Card").size().reset_index(name='Frequency').sort_values(by=['Frequency'])

sns.set_style("whitegrid")
sns.set_context("poster", 0.5)

f, ax = plt.subplots(figsize=[12, 7])
ax = sns.barplot(data=input_df, x="Card", y="Frequency")
ax.set_title("Total poker hands")

plt.show()
plt.close("all")

# test set
print("\n\n\nTest set\n")
sort_hands([["TC", "JC", "KC", "AC", "QC"],     # royal flush
            ["TC", "JC", "KC", "QC", "9C"],     # straight flush
            ["2C", "4C", "AC", "3C", "5C"],     # straight flush
            ["7C", "9C", "8C", "TC", "JC"],     # straight flush
            ["7C", "9H", "8C", "TS", "JH"],     # straight
            ["7C", "7D", "6C", "7C", "3H"],     # Three of a kind
            ["3S", "3C", "QC", "3C", "QC"],     # Full house
            ["4H", "4C", "6C", "4C", "6C"],     # Full house
            ["7C", "7D", "KC", "7S", "5H"],     # Three of a kind
            ["QC", "9H", "KC", "TS", "JH"],     # straight
            ["3C", "2H", "4C", "AS", "5H"],     # straight
            ["7C", "7C", "6C", "7C", "6C"],     # Full house
            ["KC", "KD", "KC", "2C", "3H"],     # Three of a kind
            ["7C", "4C", "6C", "3C", "5C"],     # straight flush
            ["TC", "JC", "KC", "QC", "8C"],     # flush
            ["4C", "4C", "6S", "4C", "4C"],     # four of a kind
            ["AC", "TD", "KC", "TC", "TH"],     # Three of a kind
            ["QH", "QC", "QS", "2C", "QC"],     # four of a kind
            ["QH", "9H", "5H", "2H", "QH"],     # Flush
            ["QH", "9H", "5H", "4H", "QH"],     # Flush
            ["7H", "4H", "7H", "AS", "4H"],     # two pair
            ["QH", "QH", "5H", "2S", "2H"],     # two pair
            ["QH", "QH", "6H", "2S", "2H"],     # two pair
            ["8H", "8H", "5H", "5S", "QH"],     # two pair
            ["QH", "9H", "5H", "3H", "QH"],     # Flush
            ["4C", "4C", "9S", "4C", "4C"],     # four of a kind
            ["4C", "4C", "3S", "4C", "4C"],     # four of a kind
            ])
