from collections import Counter
from itertools import combinations

RANKS = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}


HAND_RANKS = {
    "Carta Alta": 1,
    "Um Par": 2,
    "Dois Pares": 3,
    "Trinca": 4,
    "Sequência": 5,
    "Flush": 6,
    "Full House": 7,
    "Quadra": 8,
    "Straight Flush": 9,
    "Royal Flush": 10
}


def evaluate_five_cards(cards):

    values = []
    suits = []

    for card in cards:
        suit = card[-1]
        rank = card[:-1]

        suits.append(suit)
        values.append(RANKS[rank])

    values.sort()

    counter = Counter(values)
    counts = sorted(counter.values(), reverse=True)

    is_flush = len(set(suits)) == 1

    unique_values = sorted(set(values))

    is_straight = False

    if len(unique_values) == 5:

        if unique_values == list(
            range(unique_values[0], unique_values[0] + 5)
        ):
            is_straight = True

        elif unique_values == [2, 3, 4, 5, 14]:
            is_straight = True

    # Royal Flush

    if is_flush and unique_values == [10, 11, 12, 13, 14]:
        return {
            "hand": "Royal Flush",
            "strength": 100,
            "recommendation":
                "Mão máxima. Aposte agressivamente."
        }

    # Straight Flush

    if is_flush and is_straight:
        return {
            "hand": "Straight Flush",
            "strength": 95,
            "recommendation":
                "Mão extremamente forte."
        }

    # Quadra

    if counts[0] == 4:
        return {
            "hand": "Quadra",
            "strength": 90,
            "recommendation":
                "Excelente mão."
        }

    # Full House

    if counts[0] == 3 and counts[1] == 2:
        return {
            "hand": "Full House",
            "strength": 85,
            "recommendation":
                "Mão muito forte."
        }

    # Flush

    if is_flush:
        return {
            "hand": "Flush",
            "strength": 80,
            "recommendation":
                "Grande chance de vitória."
        }

    # Sequência

    if is_straight:
        return {
            "hand": "Sequência",
            "strength": 75,
            "recommendation":
                "Mão forte."
        }

    # Trinca

    if counts[0] == 3:
        return {
            "hand": "Trinca",
            "strength": 60,
            "recommendation":
                "Boa mão."
        }

    # Dois Pares

    if counts[0] == 2 and counts[1] == 2:
        return {
            "hand": "Dois Pares",
            "strength": 50,
            "recommendation":
                "Jogue com cautela."
        }

    # Um Par

    if counts[0] == 2:
        return {
            "hand": "Um Par",
            "strength": 40,
            "recommendation":
                "Mão razoável."
        }

    highest = max(values)

    if highest == 14:
        return {
            "hand": "Carta Alta",
            "strength": 30,
            "recommendation":
                "Mão fraca, mas possui Ás."
        }

    if highest >= 11:
        return {
            "hand": "Carta Alta",
            "strength": 20,
            "recommendation":
                "Possui carta alta, mas sem combinações."
        }

    return {
        "hand": "Carta Alta",
        "strength": 10,
        "recommendation":
            "Considere desistir."
    }


def analyze_hand(cards):

    if len(cards) < 5:
        return {
            "hand": "Cartas insuficientes",
            "strength": 0,
            "recommendation":
                "Envie uma mão com 5 cartas."
        }

    best_result = None
    best_rank = -1

    for combo in combinations(cards, 5):

        result = evaluate_five_cards(combo)

        rank = HAND_RANKS[result["hand"]]

        if rank > best_rank:
            best_rank = rank
            best_result = result

    return best_result