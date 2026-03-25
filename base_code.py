import random
import math

# Bāzes kods

class GameState:
    def __init__(self, virkne: list[int], score = 0, bank = 0):
        self.virkne = virkne
        self.punkti = score
        self.banka = bank

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
            return 1
        elif ((self.punkti+self.banka) % 2 == 1) and self.get_virkne()[0]%2 == 1:
            return -1
        else:
            return 0

    def Has_finished(self):
        return len(self.virkne) <= 1
    
    def get_virkne(self):
        return self.virkne
    
    def Pair_count(self):
        return math.ceil(len(self.virkne)/2)
    
    def Copy(self):
        return GameState(self.virkne.copy(), self.punkti, self.banka)

def generateVirkne(length):
    virkne = []
    for _ in range(length):
        virkne.append(random.randint(1, 6))

    return virkne