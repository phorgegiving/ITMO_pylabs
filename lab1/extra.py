open_secrets = open('sequence.txt', 'r')
stroka = ''

for word in open_secrets.read().split():
    stroka += chr(int(word))

print(stroka)