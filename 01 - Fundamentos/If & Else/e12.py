nome = input('Digite seu nome: ')
p = nome.find('a')
p = nome.find('A')

if p == 0:
    print('O nome começa com a letra A')
else:
    print('O nome não começa com a letra A')