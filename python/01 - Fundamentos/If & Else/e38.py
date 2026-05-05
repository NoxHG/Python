n1 = int(input('Digite o primeiro número: '))
op = input('Digite a operação (+, -, *, /): ')
n2 = int(input('Digite o segundo número: '))

if op == '+':
    print(n1 + n2)
elif op == '-':
    print(n1 - n2)
elif op == '*':
    print(n1 * n2)
elif op == '/':
    if n2 != 0:
        print(n1 / n2)
    else:
        print('Erro: divisão por zero')
else:
    print('Operação inválida')
