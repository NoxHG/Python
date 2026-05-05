m = int(input('Insira o número do mês: '))

if m == 12 or m == 1 or m == 2:
    print('Verão')
elif m == 3 or m == 4 or m == 5:
    print('Outono')
elif m == 6 or m == 7 or m == 8:
    print('Inverno')
elif m == 9 or m == 10 or m == 11:
    print('Primavera')
else:
    print('Mês inválido')