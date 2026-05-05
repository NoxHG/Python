print('IMC CALCULATOR V2')
peso = float(input('Digite o peso: '))
altura = float(input('Digite a altura: '))
imc = peso / (altura ** 2)

if imc < 18.5:
    print('Abaixo do peso')
elif imc < 25:
    print('Peso normal')
elif imc < 30:
    print('Sobrepeso')
elif imc >= 30:
    print('Obesidade')
