#Числа больше 5 и меньше 5, отрицательные отбросить
WHITE = '\033[47m'
BLUE = '\033[44m'
BLANK = '\033[0m'

f=open('sequence.txt')
t=[]
for l in f:
    t.append(float(l))

b5 = 0
l5 = 0

for i in t:
    if i>5:
        b5+=1
    elif 0<=i<5:
        l5 +=1
#print(l5, b5)

p1 = b5/(b5+l5)*100
p2 = l5/(b5+l5)*100

#print(p1, p2)

print(WHITE+int(p1)*' '+BLANK+ BLUE+int(p2)*' '+BLANK, end='')
print()
print((int(p1/2.5))*" ", '>5', p1, '%', (7)*" ", '<5', p2, '%')
#os.system("cls")