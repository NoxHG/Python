salario = float(input('Digite o salário: '))

if salario >= 3000:
    imposto = salario * 0.15
    print(f'Imposto: R$ {imposto:.2f}')
else:
    imposto = salario * 0.075
    print(f'Imposto: R$ {imposto:.2f}')