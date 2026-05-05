A = 4
B = 10
C = 4
D = True
E = False

print(A == C)
print(B > A and B > C)
print(A != C or B == 10)
print(not D)
print(D and not E)
print(A < B and C > A)
print(A < B > C)
print(A >= 1 and A <= 10)
print(not E and A + 1 < B or D)


#10. Usando operadores lógicos e relacionais, escreva uma expressão em Python que resulte em True 
# somente quando A for um número par e estiver entre 1 e 9 (inclusive). 
# Use o açúcar sintático de encadeamento na parte da comparação de intervalo.

#Dica: um número é par quando o resto da divisão por 2 é igual a zero (A % 2 == 0).

A = input("Digite um número entre 1 e 9: ")
A = int(A)
print(A % 2 == 0 and 1 <= A <= 9)

F = 0
G = -3
I = [1, 2, 3, 4, 5]

print()