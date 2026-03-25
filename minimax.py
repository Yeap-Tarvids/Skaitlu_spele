import math
import game_tree as GT
import base_code as game

def minimax(root: GT.Node, maximizing: bool):
    if root.is_end:
        return root.heristic
    if maximizing:
        value = -math.inf
        for child in root.children:
            value = max(value, minimax(child, not maximizing))
        return value
    else:
        value = math.inf
        for child in root.children:
            value = min(value, minimax(child, not maximizing))
        return value

def ai_move(root: GT.Node, ai_is_player1: bool):
    best = 0
    move = 0
    for index, child in enumerate(root.children):
        value = minimax(child, not ai_is_player1)
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