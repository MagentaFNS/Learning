def hanoi(n,source,target,auxiliary):
    """
    n - количество дисков
    source - откуда берем (стержень A)
    target - куда кладем (стержень C)
    auxiliary - вспомогательный стержень (стержень B)
    """
    if n == 1:
        print(f"Переместить диск 1 с {source} на {target}")
        return
    
    hanoi(n-1,source,auxiliary,target)
    print(f"Переместить диск {n} с {source} на {target}")
    hanoi(n - 1, auxiliary, target, source)

print("Для 3 дисков:")
hanoi(3, 'A', 'C', 'B')