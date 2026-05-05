v = input('insira uma vogal:')

if v.lower() in 'aeiou':
    print('vogal')
elif v.lower() in 'bcdfghjklmnpqrstvwxyz':
    print('consoante')
elif v.lower() in '0123456789':
    print('número')
else:
    print('caractere especial')