

def expo(m, d, n):
    moduluuu = m
    dinb = bin(d)[2:]
    i = 0
    j = 0
    k = 1
    while True:
        if i == 0:
            if int(dinb[:j+1],base=2) == d:
                break
            checker_2 = int(dinb[0:j+2],base=2)
            if k * 2 <= checker_2:
                moduluuu = (moduluuu**2)% n
                k*=2
                i+=1
                j+=1
                continue

        if int(dinb[:j],base=2) == d:
            break
        checker_2 = int(dinb[0:j+1],base=2)
        if k * 2 < checker_2:
            moduluuu = (moduluuu**2)% n
            k*=2
            i+=1
            continue

        if dinb[j] == '1':
            moduluuu = (moduluuu * m) % n
            k+=1
        if dinb[j] == '0':
            moduluuu = (moduluuu**2)% n
            k*=2
        i+=1
        j+=1
    return moduluuu



