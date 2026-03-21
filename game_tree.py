import base_code as game

class Node:
    def __init__(self, data: game.GameState):
        self.parent = None
        self.data = data
        self.heristic = 0
        self.children = []
        self.is_end = False

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
        if end:
            child.is_end = True
            child.heristic = evalState(child.data)
    
    return None


def printTree(root: Node, indent = 0):
    if root is None:
        return
    
    prefix = '\t'*indent
    print(f'{prefix}{root.data.virkne} | heur: {root.heristic}')
    for child in root.children:
        printTree(child, indent+1)

def isEven(x):
    return x % 2 == 0

def isOdd(x):
    return x % 2 == 1

def evalState(game_state: game.GameState):
    parity = evalSequence(game_state.get_virkne()) # virknes paritāte (virknei būs visticamāk pāra vai nepāra gala rezultāts)
    parity_value = 0
    match parity:
        case 1, 0 :
            parity_value = parity
        case _:
            parity_value = (parity % 2)
    score_value = game_state.punkti
    bank_value = game_state.banka
    evalValue = 0
    if isOdd(parity_value) and isOdd(score_value+bank_value):
        evalValue = (50*parity_value) + score_value + bank_value
    elif isEven(parity_value) and isEven(score_value+bank_value):
        evalValue = ((50*parity_value) + score_value + bank_value) * -1
    else:
        evalValue = 0
    return evalValue

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