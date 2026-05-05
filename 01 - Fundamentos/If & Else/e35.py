vel = float(input('Digite a velocidade: '))

if vel <= 80:
    print('Sem multa')
elif vel <= 100:
    print('Multa leve: R$ 130')
elif vel <= 120:
    print('Multa Média: R$ 195')
else:
    print('Multa grave: R$ 293 + suspensão')