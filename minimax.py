## 1. variants by Ed
max_depth = 3
def heuristic(numSeq, firstMove):
    towardEven = firstMove #Стремится к четному или нет
    seq = numSeq #Числовая последовательность
    count = 0
    for i in seq:
        if(i%2 == 0 and towardEven): # +1 если число четное и стремится к четному и наоборот
            count = count + 1
    score = (count / len(seq)) * 2 - 1 # Нормализация чисел для более удобного добавления бонусов
    if(seq[0]%2 == 0 and towardEven):# Бонус если число после обьединения четное и стремится к четному и наоборот
        fnumBonus = 0.5
    else:
        fnumBonus = -0.5
    if (len(seq)%2 != 0): # Смотрит на наличие числа без пары 
        if (seq[-1]%2 == 0 and towardEven):# Бонус если последнее число четное а стремится к нечетному (Вычитаение неугодного)
            delBonus = -0.3
        else:
            delBonus = 0.3
    return score + fnumBonus + delBonus

