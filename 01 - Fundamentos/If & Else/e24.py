n1 = int(input('Digite um número: '))
n2 = int(input('Digite outro número: '))

if n1 == 0 or n2 == 0:
    print('Divisão por zero não é permitida')
else:
    div = n1 / n2
    print(f'O resultado da divisão é: {div:.2f}')