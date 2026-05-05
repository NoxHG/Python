kwh = int(input('Digite a quantia de consumo de energia em kWh: '))

if kwh >= 100:
    valor = kwh * 0.40
    print(f'O valor a ser pago é: R$ {valor:.2f}')
elif kwh >= 101:
    valor = kwh * 0.50
    print(f'O valor a ser pago é: R$ {valor:.2f}')
elif kwh >= 201:
    valor = kwh * 0.65
    print(f'O valor a ser pago é: R$ {valor:.2f}')
else:
    valor = kwh * 0.85
    print(f'O valor a ser pago é: R$ {valor:.2f}')
