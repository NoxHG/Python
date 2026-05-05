i = int(input('Digite a idade: '))

if i <= 5:
    print('Gratuito')
elif i <= 6 and i <= 12:
    print('12,00')
elif i >= 16 and i <= 17:
    print('18,00')
else:
    print('25.00')