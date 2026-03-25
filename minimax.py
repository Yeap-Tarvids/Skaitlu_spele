import math
import game_tree as GT
import base_code as game

def minimax(curr_node: GT.Node, maximizing: bool, root: GT.Node, depth=0):
    root.visited_count += 1
    if curr_node.is_end:
        return curr_node.heristic
    if maximizing:
        value = -math.inf
        for child in curr_node.children:
            value = max(value, minimax(child, not maximizing, root,depth+1))
        return value
    else:
        value = math.inf
        for child in curr_node.children:
            value = min(value, minimax(child, not maximizing, root,depth+1))
        return value

def ai_move(root: GT.Node, ai_is_player1: bool):
    best = 0
    move = 0
    root.visited_count = 0
    for index, child in enumerate(root.children):
        value = minimax(child, not ai_is_player1, root)
        if value > best:
            best = value
            move = index

            
    return move

def main():
    length = 15
    best_pairs = [0] * math.ceil(length / 2) 
    for _ in range(10000):
        game_state = game.GameState(game.generateVirkne(length))

        root = GT.Node(game_state)
        
        GT.GenerateTree(root, 3)
        
        best_pairs[ai_move(root, True)-1] += 1
    
    print(best_pairs)

if __name__ == '__main__':
    main()