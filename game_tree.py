import base_code as game

class Node:
    def __init__(self, data: game.GameState):
        self.parent = None
        self.data = data
        self.heristic = 0
        self.children = []
        self.children_count = 0
        self.visited_count = 0
        self.is_end = False
        self.index = 0

    def addChild(self, child):
        child.parent = self
        self.children.append(child)
        return

def GenerateTree(curr_node: Node, depth, root: Node):
    root.children_count += 1
    if curr_node.data.Has_finished() or depth == 0:
        return True

    for index in range(1, curr_node.data.Pair_count()+1):
        sub_game = curr_node.data.Copy()
        sub_game.sumPair(index)
        child = Node(sub_game)
        end = GenerateTree(child, depth-1, root)
        curr_node.addChild(child)
        child.index = index
        if end:
            child.is_end = True
            child.heristic = evalState(child.data)
    
    return None

def evalState(game_state: game.GameState):
    parity_value = evalSequence(game_state.get_virkne()) % 2 # Kāda, visticammāk, būs virknes paritāte (vai virknei būs visticamāk pāra vai nepāra gala rezultāts)
    score_total = game_state.punkti + game_state.banka
    if parity_value == 1 and score_total % 2 == 1: # Ja pozīcija būs visticamāk labāka spēlētājam, kas uzsāka spēli
        return 1000 + score_total
    elif parity_value == 0 and score_total % 2 == 0: # Ja pozīcija būs visticamāk sliktāka spēlētājam, kas uzsāka spēli
        return -1000 + score_total
    else: # Ja pozīcija visticamāk būs neizšķirts rezultāts
        return score_total 

def evalSequence(seq):
    while len(seq) > 1:
        newSeq = []
        for i in range(0, len(seq)-1, 2):
            newSeq.append((seq[i]+seq[i+1])%2)
        seq = newSeq
    return seq[0]

def main():
    gameState = game.GameState(game.generateVirkne(10))

    curr_node = Node(gameState)

    GenerateTree(curr_node, 4)



if __name__ == "__main__":
    main()