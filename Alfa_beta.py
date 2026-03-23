import random
import math
import time

class GameState:
    def __init__(self, virkne, score=0, bank=0):
        self.virkne = virkne
        self.punkti = score
        self.banka = bank

    def PrintState(self):
        print("Šī brīža sekvence:", end=" ")
        for i in range(0, len(self.virkne), 2):
            print(self.virkne[i:i+2], end=" ")
        print(f"\nPunkti: {self.punkti} Banka: {self.banka}")

    def sumPair(self, pairIndex):
        totalPairs = math.ceil(len(self.virkne)/2)

        if pairIndex not in range(1, totalPairs+1):
            return False

        if pairIndex == totalPairs and len(self.virkne) % 2 == 1:
            self.punkti -= 1
            self.virkne = self.virkne[:-1]
            return True

        left = (pairIndex-1)*2
        a, b = self.virkne[left], self.virkne[left+1]

        summa = a + b
        self.punkti += 1

        if summa > 6:
            summa -= 6
            self.banka += 1

        self.virkne[left] = summa
        self.virkne = self.virkne[:left+1] + self.virkne[left+2:]

        return True

class Node:
    def __init__(self, state, move=None):
        self.state = state
        self.move = move
        self.children = []
        self.value = None


def clone(state):
    return GameState(state.virkne.copy(), state.punkti, state.banka)


def get_moves(state):
    return list(range(1, math.ceil(len(state.virkne)/2)+1))


def generate_tree(node, depth):
    if depth == 0 or len(node.state.virkne) == 1:
        return 1

    count = 1

    for move in get_moves(node.state):
        new_state = clone(node.state)
        new_state.sumPair(move)

        child = Node(new_state, move)
        node.children.append(child)

        count += generate_tree(child, depth-1)

    return count

def evaluate(state):
    val = state.punkti + 2*state.banka

    if state.virkne[0] % 2 == 0:
        val += 3
    else:
        val -= 3

    val -= len(state.virkne)

    return val


# ---------------- ALPHA-BETA ---------------- #

def alphabeta(node, depth, alpha, beta, maximizing):
    if depth == 0 or not node.children:
        node.value = evaluate(node.state)
        return node.value

    if maximizing:
        val = -math.inf
        for c in node.children:
            val = max(val, alphabeta(c, depth-1, alpha, beta, False))
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        node.value = val
        return val
    else:
        val = math.inf
        for c in node.children:
            val = min(val, alphabeta(c, depth-1, alpha, beta, True))
            beta = min(beta, val)
            if beta <= alpha:
                break
        node.value = val
        return val


def best_move(node):
    best = None
    best_val = math.inf

    for c in node.children:
        if c.value < best_val:
            best_val = c.value
            best = c.move

    return best

def get_sequence_length():
    while True:
        user_input = input("Ievadi virknes garumu (15-25): ")

        try:
            length = int(user_input)
        except ValueError:
            print("Kļūda: ievadi skaitli!")
            continue

        if 15 <= length <= 25:
            return length
        else:
            print("Kļūda: garumam jābūt no 15 līdz 25!")


# ---------------- GAME ---------------- #

def generate_seq(n):
    return [random.randint(1, 6) for _ in range(n)]


def play_game(starter, depth=3, show=True):
    length = get_sequence_length()  # ✅ NEW
    state = GameState(generate_seq(length))

    print(f"\nĢenerētā virkne ({length} skaitļi):")

    player = starter

    total_nodes = 0
    total_time = 0

    while len(state.virkne) > 1:
        if show:
            state.PrintState()

        if player:
            if show:
                print("Spēlētājs:")
            move = int(input("Ievadi indeksu: "))
        else:
            if show:
                print("Dators domā...")

            root = Node(clone(state))
            t0 = time.time()

            nodes = generate_tree(root, depth)
            total_nodes += nodes

            alphabeta(root, depth, -math.inf, math.inf, False)

            move = best_move(root)
            total_time += time.time() - t0

            if show:
                print("AI izvēlējās:", move)

        state.sumPair(move)
        player = not player

    return state, total_nodes, total_time

def run_experiments():
    wins = 0
    total_nodes = 0
    total_time = 0

    for _ in range(10):
        state, nodes, t = play_game(False, show=False)

        total_nodes += nodes
        total_time += t

        if (state.punkti + state.banka) % 2 == 1:
            wins += 1

    print("\n--- EKSPERIMENTI (Alpha-Beta) ---")
    print("AI uzvaras:", wins)
    print("Vidējais laiks:", total_time/10)
    print("Vidējās virsotnes:", total_nodes/10)

def main():
    while True:
        starter = input("Kas sāk? (1-cilvēks, 2-dators): ") == "1"

        play_game(starter)

        if input("Atkārtot? (y/n): ") != "y":
            break

        if input("Veikt eksperimentus? (y/n): ") == "y":
            run_experiments()


if __name__ == "__main__":
    main()