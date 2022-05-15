def check_password_difficulty(password_to_check):
    with open("password_lists.txt", "r") as file:
        for password in file:
            if password.rstrip() == password_to_check:
                return False
    mayusc_amount = len([i for i in password_to_check if i.isupper()])
    minusc_amount = len([i for i in password_to_check if i.islower()])
    digit_amount = len([i for i in password_to_check if i.isdigit()])
    special_amount = len([i for i in password_to_check if i in "!#$%&()=+-."])
    password_length = True if len(password_to_check) >= 6 and len(password_to_check) <= 20 else False
    if mayusc_amount and minusc_amount and digit_amount and special_amount and password_length:
        return True
    else:
        return False


def verificar_existencia(id_componente, Tipo):
    if id_componente == 0:
        return False
    if Tipo.query.get(id_componente) is None:
        return False
    return True


def retornar_tipo(id_componente, Tipo):
    return Tipo.query.get(id_componente)


def agregar_a_lista(componente, lista):
    lista.append(componente.name)
    lista.append(componente.price)


def sumar_a_precio_total(componente, precio_total):
    precio_total += componente.price
    return precio_total


def verificar_todo(id, Tipo, lista, precio_total):
    if verificar_existencia(id, Tipo):
        componente = retornar_tipo(id, Tipo)
        agregar_a_lista(componente, lista)
        precio_total = sumar_a_precio_total(componente, precio_total)
    return precio_total
