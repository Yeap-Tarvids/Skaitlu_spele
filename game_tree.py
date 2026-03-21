import base_code as game

class Node:
    def __init__(self, data: game.GameState):
        self.data = data
        self.heristic = 0
        self.children = []

    def addChild(self, child):
        self.children.append(child)
        return
    

def GenerateTree(root: Node, depth):
    if root.data.Has_finished() or depth == 0:
        return

    for index in range(1, root.data.Pair_count()+1):
        sub_game = root.data.Copy()
        sub_game.SumPair(index)
        child = Node(sub_game)
        GenerateTree(child, depth-1)
        root.addChild(child)
    
    return 


def printTree(root: Node, indent = 0):
    if root is None:
        return
    
    prefix = '\t'*indent
    print(f'{prefix}{root.data.virkne}')
    for child in root.children:
        printTree(child, indent+1)


def main():
    gameState = game.GameState(game.GenerateVirkne(5))

    root = Node(gameState)

    GenerateTree(root, 10)

    printTree(root)



if __name__ == "__main__":
    main()