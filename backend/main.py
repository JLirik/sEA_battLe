show = []
for i in range(10):
    show.append(['0'] * 10)

f = open('map.txt')
karta = []

for e in f:
    a = e.strip()
    karta.append(a)
print(karta)
ship = 0
attempts = int(input('Введите колличество попыток: '))
while attempts > 0:
    x, y = map(int, input().split())
    if x < 10 and y < 10:
        if karta[y][x] == 'k' and show[y][x] != 'k':
            print('ранил')
            show[y][x] = 'k'
            for e in show:
                print(''.join(e))
            ship += 1
            attempts -= 1
        elif karta[y][x] == '-' and show != '0':
            print('мимо')
            show[y][x] = '-'
            for e in show:
                print(''.join(e))
            attempts -= 1
        if ship == 10:
            print('Победа')
            break
        print(f'Осталось попыток: {attempts}')
    else:
        print('Неверные координаты')


# ПЛАН:
# Создать стартовый экран (слева правила, справа войти \ авторизоваться)