import base_code as game
import game_tree as gt
import math

ALPHA = -math.inf
BETA = math.inf

def Alpha_Beta(tree: gt.Node, alpha, beta, maximizing):
    if tree.is_end:
        return tree.heristic

    if maximizing:
        value = ALPHA
        for child in tree.children:
            value = max(value, Alpha_Beta(child, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = BETA
        for child in tree.children:
            value = min(value, Alpha_Beta(child, alpha, beta, True))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

def BestMove(root: gt.Node, maximizing = True):
    best_value = ALPHA
    best_pair_index = 1
    index = 0
    for child in root.children:
        value = Alpha_Beta(child, ALPHA, BETA, not maximizing)
        
        if value > best_value:
            best_value = value
            best_pair_index = index
        
        index += 1
    return best_pair_index


def main():
    length = 15
    best_pairs = [0] * math.ceil(length / 2) 
    for _ in range(1000):
        game_state = game.GameState(game.generateVirkne(length))

        root = gt.Node(game_state)
        
        gt.GenerateTree(root, 3)
        
        best_pairs[BestMove(root)-1] += 1
    
    print(best_pairs)

if __name__ == '__main__':
    main()