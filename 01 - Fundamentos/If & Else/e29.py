print('IMC CALCULATOR')

altura = float(input('Digite a altura em metros: '))
peso = float(input('Digite o peso em kg: '))

imc = peso / (altura ** 2)

if imc < 25:
    print('Peso normal')
elif imc < 30:
    print('Acima do peso')