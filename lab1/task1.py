def flag():
    RED = '\033[41m'
    WHITE = '\033[47m'
    BLUE = '\033[44m'
    SPC = ' '
    BLANK = '\033[0m'

    height = 24
    width = 36

    strheight = height//6

    for i in range(6):
        if i == 0 or i == 5:
            print(RED+SPC*30+BLANK)
        elif i == 1 or i == 4:
            print(WHITE+SPC*30+BLANK)
        else:
            print(BLUE+SPC*30+BLANK)

flag()
