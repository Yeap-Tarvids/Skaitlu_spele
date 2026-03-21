import random
import math


class GameState:
    def __init__(self, virkne: list[int], score=0, bank=0):
        self.virkne = virkne
        self.punkti = score
        self.banka = bank

    def PrintState(self):
        print("Šī brīža sekvence:", end=" ")
        for i in range(0, len(self.virkne), 2):
            print(f'{self.virkne[i:i+2]} ', end="")
        print(f"\nPunkti: {self.punkti} Banka: {self.banka}")

    def sumPair(self, pairIndex):
        totalPairs = math.ceil(len(self.virkne) / 2)

        if pairIndex not in range(1, totalPairs + 1):
            return False

        seq = self.virkne

        if pairIndex == totalPairs and len(self.virkne) % 2 == 1:
            self.punkti -= 1
            self.virkne = seq[:len(self.virkne) - 1]
            return True

        leftIndex = (pairIndex - 1) * 2
        summa = self.virkne[leftIndex] + self.virkne[leftIndex + 1]
        self.punkti += 1

        if summa > 6:
            summa -= 6
            self.banka += 1

        seq[leftIndex] = summa
        self.virkne = seq[:leftIndex + 1] + seq[leftIndex + 2:]

        return True

    def winCon(self):
        if ((self.punkti + self.banka) % 2 == 0) and self.virkne[0] % 2 == 0:
            print("Player 1 wins!")
        elif ((self.punkti + self.banka) % 2 == 1) and self.virkne[0] % 2 == 1:
            print("Player 2 wins!")
        else:
            print("Draw!")


# ---------------- AI ---------------- #

def clone_state(state):
    return GameState(state.virkne.copy(), state.punkti, state.banka)


def get_moves(state):
    return list(range(1, math.ceil(len(state.virkne) / 2) + 1))


def evaluate(state):
    return state.punkti + 2 * state.banka


def alphabeta(state, depth, alpha, beta, maximizing):
    if len(state.virkne) == 1 or depth == 0:
        return evaluate(state)

    moves = get_moves(state)

    if maximizing:
        value = -math.inf
        for m in moves:
            new_state = clone_state(state)
            new_state.sumPair(m)
            value = max(value, alphabeta(new_state, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = math.inf
        for m in moves:
            new_state = clone_state(state)
            new_state.sumPair(m)
            value = min(value, alphabeta(new_state, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def best_move(state):
    best = None
    best_val = math.inf

    for m in get_moves(state):
        new_state = clone_state(state)
        new_state.sumPair(m)
        val = alphabeta(new_state, 3, -math.inf, math.inf, True)

        if val < best_val:
            best_val = val
            best = m

    return best


# ---------------- GAME ---------------- #

def generateVirkne(length):
    return [random.randint(1, 6) for _ in range(length)]


def main():
    while True:
        length = input("Ievadi virknes garumu (15-25): ")
        try:
            length = int(length)
            if 15 <= length <= 25:
                break
        except:
            pass

    game = GameState(generateVirkne(length))

    playerOne = True

    while len(game.virkne) > 1:
        game.PrintState()

        if playerOne:
            print("Spēlētāja 1 kārta")
            move = input("Ievadi pāra indeksu: ")

            try:
                move = int(move)
            except:
                print("Nepareiza ievade")
                continue

        else:
            print("Spēlētāja 2 (AI) kārta")
            move = best_move(game)
            print(f"AI izvēlējās: {move}")

        success = game.sumPair(move)

        if not success:
            print("Nepareizs gājiens")
            continue 

        playerOne = not playerOne

    game.PrintState()
    game.winCon()


if __name__ == "__main__":
    main()