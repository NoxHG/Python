nop = [n1, op, n2] = input("Digite a operação: ", '1 = maior, 2 = menor, 3 = soma, 4 = diferenca', sep='\n').split()
n1 = float(n1)
n2 = float(n2)

if op ==1:
    print('o maior número é: ', max(n1, n2))
elif op == 2:
    print('o menor número é: ', min(n1, n2))
elif op == 3:
    print('a soma dos números é: ', n1 + n2)
elif op == 4:
    print('a diferença dos números é: ', abs(n1 - n2))
else:
    print('Operação inválida.')