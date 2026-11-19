import os

RUTA = os.path.join(os.path.expanduser("~"), "expedientes.txt")

# ---------- PERSISTENCIA ----------

def guardar_expedientes(codigos, dnis, nombres, tramites, folios, fechas, estados,
                        tipos_persona, rucs, direcciones, celulares, correos,
                        firmantes, requisitos, citas):
    with open(RUTA, "w", encoding="utf-8") as archivo:
        for i in range(len(codigos)):
            linea = (f"{codigos[i]}|{dnis[i]}|{nombres[i]}|{tramites[i]}|"
                     f"{folios[i]}|{fechas[i]}|{estados[i]}|{tipos_persona[i]}|"
                     f"{rucs[i]}|{direcciones[i]}|{celulares[i]}|{correos[i]}|"
                     f"{firmantes[i]}|{requisitos[i]}|{citas[i]}\n")
            archivo.write(linea)

def leer_expedientes():
    codigos, dnis, nombres, tramites, folios, fechas, estados = [], [], [], [], [], [], []
    tipos_persona, rucs, direcciones, celulares, correos = [], [], [], [], []
    firmantes, requisitos, citas = [], [], []
    if not os.path.exists(RUTA):
        return (codigos, dnis, nombres, tramites, folios, fechas, estados,
                tipos_persona, rucs, direcciones, celulares, correos,
                firmantes, requisitos, citas)
    with open(RUTA, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split("|")
            if len(partes) == 15:
                codigos.append(partes[0]); dnis.append(partes[1])
                nombres.append(partes[2]); tramites.append(partes[3])
                folios.append(partes[4]); fechas.append(partes[5])
                estados.append(partes[6]); tipos_persona.append(partes[7])
                rucs.append(partes[8]); direcciones.append(partes[9])
                celulares.append(partes[10]); correos.append(partes[11])
                firmantes.append(partes[12]); requisitos.append(partes[13])
                citas.append(partes[14])
    return (codigos, dnis, nombres, tramites, folios, fechas, estados,
            tipos_persona, rucs, direcciones, celulares, correos,
            firmantes, requisitos, citas)
