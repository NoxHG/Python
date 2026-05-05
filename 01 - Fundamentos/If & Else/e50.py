vh = 18
vhd = 12
vs = 8
ref = 6
ssp = 'Volte Sempre!'

print('################################')
print('Menu de opções')
print('################################')
print('\n 1 - Hamburguer', '\n 2 - Hot Dog', '\n 3 - Suco', '\n 4 - Refrigerante' )
print('\n################################')

pd = int(input('Digite o número do produto desejado: '))

if pd == 1:
    print(f'O valor do produto é: R$ {vh:.2f}')
elif pd == 2:
    print(f'O valor do produto é: R$ {vhd:.2f}')
elif pd == 3:
    print(f'O valor do produto é: R$ {vs:.2f}')
elif pd == 4:
    print(f'O valor do produto é: R$ {ref:.2f}')
elif pd == 5:
    print(ssp)
else:
    print('Produto inválido.')
print('################################')