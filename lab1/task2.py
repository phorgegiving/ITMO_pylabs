import math

def graph():
    w = 20
    h = 20

    WHITE = '\033[47m'
    BLUE = '\033[44m'
    BLANK = '\033[0m'

    for row in range(h):
        for col in range(w):
            x = col / 8 + 0.1
            y = 1 / x

            calcdispy_up = int(w/2 - y * 2)
            calcdispy_down = int(w/2 + y * 2)

            if calcdispy_up == row:
                print(BLUE + ' ' + BLANK, end='')

            elif calcdispy_down == row:
                print(BLUE + ' ' + BLANK, end='')
            else:
                print(WHITE + ' ' + BLANK, end='')
        print()

graph()