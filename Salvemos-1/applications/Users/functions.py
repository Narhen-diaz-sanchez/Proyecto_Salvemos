"""Funciones extra de la aplicación users"""
import random
import string


def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Funcion que genera el código aleatorio de seis digitos"""
    return ''.join(random.choice(chars) for _ in range(size))
