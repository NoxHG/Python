#Triangulos

a = float(input("Digite o valor do lado a: "))
b = float(input("Digite o valor do lado b: "))
c = float(input("Digite o valor do lado c: "))

if a < b + c and b < a + c and c < a + b:
    print("Os lados formam um triângulo.")
else:
    print("Os lados não formam um triângulo.")

if a == b == c:
    print("O triângulo é equilátero.")
elif a == b or b == c or a == c:
    print("O triângulo é isósceles.")
else:
    print("O triângulo é escaleno.")