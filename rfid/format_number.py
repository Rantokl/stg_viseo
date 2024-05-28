def format_numero_telephone(numero):
    numero_numerique = ''.join(filter(str.isdigit, numero))
    numero = numero_numerique[:10]
    if numero_numerique.startswith('261'):
        numero = numero_numerique[3:]

    if numero.startswith('0'):
        numero = numero[1:]



    numero = '261' + numero

    numero += '@c.us'

    return numero