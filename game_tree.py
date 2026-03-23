import base_code as game

class Node:
    def __init__(self, data: game.GameState):
        self.parent = None
        self.data = data
        self.heristic = 0
        self.children = []
        self.is_end = False
        self.index = 0

    def addChild(self, child):
        child.parent = self
        self.children.append(child)
        return

def GenerateTree(root: Node, depth):
    if root.data.Has_finished() or depth == 0:
        return True

    for index in range(1, root.data.Pair_count()+1):
        sub_game = root.data.Copy()
        sub_game.sumPair(index)
        child = Node(sub_game)
        end = GenerateTree(child, depth-1)
        root.addChild(child)
        child.index = index
        if end:
            child.is_end = True
            child.heristic = evalState(child.data)
    
    return None

def printTree(root: Node, indent = 0):
    if root is None:
        return
    
    prefix = '\t'*indent
    print(f'{prefix}{root.data.virkne}')
    for child in root.children:
        printTree(child, indent+1)

def evalState(game_state: game.GameState):
    parity_value = evalSequence(game_state.get_virkne()) % 2 # Kāda, visticammāk, būs virknes paritāte (vai virknei būs visticamāk pāra vai nepāra gala rezultāts)
    score_total = game_state.punkti + game_state.banka
    if parity_value == 1 and score_total % 2 == 1:
        return 1000 + score_total
    elif parity_value == 0 and score_total % 2 == 0:
        return -1000 + score_total
    else:
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

    root = Node(gameState)

    GenerateTree(root, 4)

    printTree(root)



if __name__ == "__main__":
    main()