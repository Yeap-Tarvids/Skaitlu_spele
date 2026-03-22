import spele_DM as game
import game_tree as gt
import math

def alpha_beta(node:gt.Node, depth:int, maximizingPlayer:bool, alpha=-math.inf, beta=math.inf):
    if depth == 0 or node.is_end:
        return node.heristic
    if maximizingPlayer:
        value = -math.inf
        for i in node.children:
            value = max(value, alpha_beta(i, depth - 1, not maximizingPlayer, alpha, beta))
            if value >= beta:
                break
            alpha = max(alpha, value)
        return value
    else:
        value = math.inf
        for i in node.children:
            value = min(value, alpha_beta(i, depth - 1, True, alpha, beta))
            if value <= alpha:
                break
            beta = min(beta, value)
        return value

def best(root:gt.Node, depth:int, maximizingPlayer:bool):
    best_value = -math.inf if maximizingPlayer else math.inf
    best_child = None
    
    for i in root.children:
        value = alpha_beta(i, depth - 1, not maximizingPlayer)
        if maximizingPlayer:
            if value > best_value:
                best_value = value
                best_child = i
        else:
            if value < best_value:
                best_value = value
                best_child = i

    return best_child

def main():
    depth = 4
    best_pairs = [0] * math.ceil(15 / 2)

    for _ in range(50):
        game_state = game.GameState(game.generateVirkne(15))
        root = gt.Node(game_state)
        gt.GenerateTree(root, depth)
        best_move = best(root, depth, maximizingPlayer=True)

        if best_move is not None:
            index = root.children.index(best_move)
            best_pairs[index] += 1

    print("Cik reizes katrs pāris tika izvēlēts kā labākais:")
    print(best_pairs)

if __name__ == "__main__":
    main()
