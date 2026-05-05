nota = int(input("Digite a nota do aluno: "))

if nota >= 90:
    print('Excelente')
if nota >= 70:
    print('Bom')
if nota >= 50:
    print('Regular')
if nota < 50:
    print('Insuficiente')
else:
    print('Nota inválida.')