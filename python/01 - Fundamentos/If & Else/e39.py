salario = int(input('Digite o salário: '))

if salario <= 1500:
    print('Reajute:', salario * 0.15)
elif salario <= 2500:
    print('Reajuste:', salario * 0.10)
elif salario <= 6000:
    print('Reajuste:', salario * 0.07)
else:
    print('Reajuste:', salario * 0.03)