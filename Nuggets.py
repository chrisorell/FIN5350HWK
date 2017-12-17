def nug_num (possible):
    for a in range (0, possible //6 + 1):
        for b in range (0, possible //9 + 1):
            for c in range(0, possible //20 +1):
                if 6 * a + 9 * b + 20 * c == possible:
                    return True
    return False

def main():
    success = 0
    biggest = 0
    possible = 6
    while success != 6:
        if(nug_num (possible)):
            success += 1
        else:
            success= 0
            biggest = possible
        possible += 1
    print(biggest)
    