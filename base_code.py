import random
import math

# Bāzes kods

class GameState:
    def __init__(self, virkne: list[int], score = 0, bank = 0):
        self.virkne = virkne
        self.punkti = score
        self.banka = bank
    
    def PrintState(self):
        for i in range(0, len(self.virkne), 2):
            print(f'{self.virkne[i:i+2]} ', end="")
        print(f"\nPunkti: {self.punkti}\nBanka: {self.banka}")

    def sumPair(self, pairIndex):
        totalPairs = math.ceil(len(self.virkne)/2)
        if pairIndex not in range(1, totalPairs+1) or len(self.virkne) <= 1:
            return -1
        
        seq = self.virkne

        if (pairIndex ==  totalPairs and len(self.virkne)%2 == 1):
            self.punkti -= 1
            self.virkne = seq[:len(self.virkne)-1]
            return
        
        leftIndex = (pairIndex-1)*2
        summa = self.virkne[leftIndex] + self.virkne[leftIndex+1]
        self.punkti += 1

        if (summa > 6):
            summa -= 6
            self.banka += 1
        
        seq[leftIndex] = summa
        self.virkne = seq[:leftIndex+1] + seq[leftIndex+2:]

    def winCon(self):
        if ((self.punkti+self.banka) % 2 == 0) and self.get_virkne()[0]%2 == 0:
            print("\033[0;34mPlayer 1 wins!\033[0m")
            return 1
        elif ((self.punkti+self.banka) % 2 == 1) and self.get_virkne()[0]%2 == 1:
            print("\033[0;32mPlayer 2 wins!\033[0m")
            return -1
        else:
            print("\033[1;33mDraw!\033[0m")
            return 0

    def Has_finished(self):
        return len(self.virkne) <= 1
    
    def get_virkne(self):
        return self.virkne
    
    def set_virkne(self, new_virkne):
        self.virkne = new_virkne


def generateVirkne(length):
    virkne = []
    for _ in range(length):
        virkne.append(random.randint(1, 6))

    return virkne


def main():
    lengthRun = True
    while lengthRun:
        length = input("Input the length of the sequence (15-25): ")
        try:
            length = int(length)
        except ValueError:
            print("Invalid input: Not a integer value")
            continue
        if not 15 <= length <= 25:
            print("Invalid input: Not in the range")
            continue
        break

    
    
    obj = GameState(generateVirkne(length))
    playerOne = True

    while len(obj.virkne) > 1:
        obj.PrintState()
        print("================")

        if playerOne:
            print('\033[0;34m', end='')
        else:
            print('\033[0;32m', end='')

        userInput = input("Input the index of the pair to sum: ")
        
        print('\033[0m', end='')
        try:
            index = int(userInput)
        except ValueError:
            
            print("Invalid input: Not a integer value")
            continue

        if index not in range(1, math.ceil(len(obj.virkne)/2)+1):
            print("Invalid input: Not a valid index")
            continue
        obj.sumPair(index)
        playerOne = not playerOne
    
    obj.PrintState()
    print("================")
    
    obj.winCon()

if __name__ == "__main__":
    main()