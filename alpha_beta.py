import base_code as game
import game_tree as gt
import math

ALPHA = -math.inf
BETA = math.inf

def Alpha_Beta(curr_node: gt.Node, alpha, beta, maximizing, root: gt.Node):
    root.visited_count += 1

    if curr_node.is_end:
        return curr_node.heristic

    if maximizing:
        value = ALPHA
        for child in curr_node.children:
            value = max(value, Alpha_Beta(child, alpha, beta, False, root))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = BETA
        for child in curr_node.children:
            value = min(value, Alpha_Beta(child, alpha, beta, True, root))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

def BestMove(root: gt.Node, maximizing = True):
    if maximizing:
        best_value = ALPHA
    else:
        best_value = BETA
    
    best_pair_index = 1
    index = 0
    for index, child in enumerate(root.children):
        value = Alpha_Beta(child, ALPHA, BETA, not maximizing, root)
        
        if maximizing:
            if value > best_value:
                best_value = value
                best_pair_index = index
        else:
            if value < best_value:
                best_value = value
                best_pair_index = index
        
    return best_pair_index


def main():
    length = 15
    best_pairs = [0] * math.ceil(length / 2) 
    for _ in range(1000):
        game_state = game.GameState(game.generateVirkne(length))

        root = gt.Node(game_state)
        
        gt.Generatecurr_node(root, 3)
        
        best_pairs[BestMove(root)-1] += 1
    
    print(best_pairs)

if __name__ == '__main__':
    main()