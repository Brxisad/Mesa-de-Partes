from datetime import datetime

def validar_dni(dni):
    return dni.isdigit() and len(dni) == 8

def validar_ruc(ruc):
    return ruc.isdigit() and len(ruc) == 11

def validar_nombre(nombre):
    return len(nombre.strip()) >= 3

def validar_correo(correo):
    return "@" in correo and "." in correo.split("@")[-1]

def validar_celular(celular):
    return celular.isdigit() and len(celular) == 9

def generar_codigo(codigos):
    anio = datetime.now().year
    return f"{anio}-{len(codigos) + 1:05d}-MCH"
