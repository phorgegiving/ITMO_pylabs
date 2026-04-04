import math

def graph():
    w = 80
    h = 10

    WHITE = '\033[47m'
    BLUE = '\033[44m'
    BLANK = '\033[0m'

    for row in range(h):
        for col in range(w):
            if col == 0:
                print(h-row-1, BLUE+" " + BLANK, end='')
            elif row == h-1:
                print(BLUE+" "+ BLANK, end='')
            else:
                x = col/8+0.1
                y=1/x

                calcdispy=int(h-1-y*2)

                if calcdispy == row:
                    print(WHITE+' '+BLANK, end='')
                else:
                    print(' ', end = '')
        print()


graph()
    