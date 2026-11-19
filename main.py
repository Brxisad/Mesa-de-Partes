from datetime import datetime, timedelta

from validaciones import (validar_dni, validar_ruc, validar_nombre,
                          validar_correo, validar_celular, generar_codigo)
from persistencia import guardar_expedientes, leer_expedientes

VENTANILLA = "03"

# ---------- UTILIDADES ----------

def cabecera():
    ahora = datetime.now()
    print("\n" + "=" * 60)
    print("   MUNICIPALIDAD DISTRITAL DE CHORRILLOS")
    print("   SUBGERENCIA DE TRÁMITE DOCUMENTARIO")
    print("   Mesa de Partes Digital - Ley N.° 31170")
    print("=" * 60)
    print(f"   Fecha: {ahora.strftime('%d/%m/%Y')}   "
          f"Hora: {ahora.strftime('%H:%M')}   Ventanilla: {VENTANILLA}")
    print("=" * 60)

def cargo_recepcion(codigo, dni, nombre, tramite, folios, fecha, tipo, requisitos):
    print("\n" + "-" * 60)
    print("        CARGO DE RECEPCIÓN DE EXPEDIENTE")
    print("-" * 60)
    print(f"  N.° Expediente : {codigo}")
    print(f"  Fecha y hora   : {fecha}")
    print(f"  Tipo           : {tipo}")
    print(f"  Remitente      : {nombre}")
    print(f"  Documento      : {dni}")
    print(f"  Trámite        : {tramite}")
    print(f"  Folios         : {folios}")
    print(f"  Requisitos     : {requisitos}")
    print(f"  Estado         : REGISTRADO")
    print(f"  Ventanilla     : {VENTANILLA}")
    print("-" * 60)
    print("  Conserve este número para consultar su trámite.")
    print("-" * 60)

# ---------- OPERACIONES ----------

def recepcionar(codigos, dnis, nombres, tramites, folios, fechas, estados,
                tipos_persona, rucs, direcciones, celulares, correos,
                firmantes, requisitos, citas):
    print("\n--- RECEPCIÓN DE EXPEDIENTE ---")
    print("  Tipo de solicitante:")
    print("    1) Persona Natural")
    print("    2) Persona Jurídica")
    tipo_op = input("  Opción: ").strip()

    if tipo_op == "1":
        tipo = "Persona Natural"
        dni = input("  DNI / Carnet de extranjería (8 dígitos): ").strip()
        if not validar_dni(dni):
            print("  >> ERROR: el documento debe tener 8 dígitos numéricos.")
            return
        nombre = input("  Nombres y apellidos completos: ").strip()
        if not validar_nombre(nombre):
            print("  >> ERROR: el nombre debe tener al menos 3 caracteres.")
            return
        direccion = input("  Dirección domiciliaria: ").strip()
        celular = input("  Número de celular (9 dígitos): ").strip()
        if not validar_celular(celular):
            print("  >> ERROR: el celular debe tener 9 dígitos.")
            return
        correo = input("  Correo electrónico activo: ").strip()
        if not validar_correo(correo):
            print("  >> ERROR: el correo no tiene un formato válido.")
            return
        ruc = "-"
        firmante = "-"
    elif tipo_op == "2":
        tipo = "Persona Jurídica"
        ruc = input("  RUC de la empresa u organización (11 dígitos): ").strip()
        if not validar_ruc(ruc):
            print("  >> ERROR: el RUC debe tener 11 dígitos numéricos.")
            return
        nombre = input("  Razón social de la empresa: ").strip()
        if not validar_nombre(nombre):
            print("  >> ERROR: la razón social debe tener al menos 3 caracteres.")
            return
        dni = input("  DNI de quien firma (8 dígitos): ").strip()
        if not validar_dni(dni):
            print("  >> ERROR: el DNI debe tener 8 dígitos numéricos.")
            return
        firmante = input("  Nombre de quien firma: ").strip()
        if not validar_nombre(firmante):
            print("  >> ERROR: el nombre del firmante debe tener al menos 3 caracteres.")
            return
        direccion = input("  Dirección fiscal: ").strip()
        celular = input("  Número de celular (9 dígitos): ").strip()
        if not validar_celular(celular):
            print("  >> ERROR: el celular debe tener 9 dígitos.")
            return
        correo = input("  Correo electrónico activo: ").strip()
        if not validar_correo(correo):
            print("  >> ERROR: el correo no tiene un formato válido.")
            return
    else:
        print("  >> ERROR: tipo de solicitante no válido.")
        return

    print("\n  Tipo de trámite:")
    print("    1) Licencia de funcionamiento")
    print("    2) ITSE (Inspección Técnica de Seguridad)")
    print("    3) Solicitud de vecino")
    opcion = input("  Opción: ").strip()
    mapa = {"1": "Licencia de funcionamiento",
            "2": "ITSE",
            "3": "Solicitud de vecino"}
    if opcion not in mapa:
        print("  >> ERROR: tipo de trámite no válido.")
        return

    num_folios = input("  Número de folios presentados: ").strip()
    if not num_folios.isdigit() or int(num_folios) <= 0:
        print("  >> ERROR: los folios deben ser un número mayor a 0.")
        return

    print("\n  --- REQUISITOS / DOCUMENTOS ADJUNTOS ---")
    print("  Marque S/N si el documento está adjunto:")
    req = []
    if input("    ¿Solicitud o escrito digital de la entidad? (S/N): ").strip().upper() == "S":
        req.append("solicitud")
    if input("    ¿Pruebas, recibos, copias u otros archivos de respaldo? (S/N): ").strip().upper() == "S":
        req.append("pruebas")
    if input("    ¿Formato correspondiente? (S/N): ").strip().upper() == "S":
        req.append("formato")
    if input("    ¿Solicitud física en papel dentro del expediente? (S/N): ").strip().upper() == "S":
        req.append("sello")
    requisitos_txt = ", ".join(req) if req else "NINGUNO"

    codigo = generar_codigo(codigos)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    codigos.append(codigo); dnis.append(dni); nombres.append(nombre)
    tramites.append(mapa[opcion]); folios.append(num_folios)
    fechas.append(fecha); estados.append("REGISTRADO")
    tipos_persona.append(tipo); rucs.append(ruc)
    direcciones.append(direccion); celulares.append(celular)
    correos.append(correo); firmantes.append(firmante)
    requisitos.append(requisitos_txt); citas.append("SIN CITA")

    cargo_recepcion(codigo, dni, nombre, mapa[opcion], num_folios, fecha,
                    tipo, requisitos_txt)
    guardar_expedientes(codigos, dnis, nombres, tramites, folios, fechas, estados,
                        tipos_persona, rucs, direcciones, celulares, correos,
                        firmantes, requisitos, citas)


def consultar(codigos, dnis, nombres, tramites, folios, fechas, estados,
              tipos_persona, rucs, direcciones, celulares, correos,
              firmantes, requisitos, citas):
    print("\n--- CONSULTA DE ESTADO ---")
    buscado = input("  N.° de expediente: ").strip().upper()
    for i in range(len(codigos)):
        if codigos[i] == buscado:
            print("\n" + "-" * 60)
            print(f"  N.° Expediente : {codigos[i]}")
            print(f"  Ingresado      : {fechas[i]}")
            print(f"  Tipo           : {tipos_persona[i]}")
            print(f"  Remitente      : {nombres[i]}")
            print(f"  Documento      : {dnis[i]}")
            if tipos_persona[i] == "Persona Jurídica":
                print(f"  RUC            : {rucs[i]}")
                print(f"  Firma          : {firmantes[i]}")
            print(f"  Dirección      : {direcciones[i]}")
            print(f"  Celular        : {celulares[i]}")
            print(f"  Correo         : {correos[i]}")
            print(f"  Trámite        : {tramites[i]}")
            print(f"  Folios         : {folios[i]}")
            print(f"  Requisitos     : {requisitos[i]}")
            print(f"  Cita           : {citas[i]}")
            print(f"  ESTADO ACTUAL  : {estados[i]}")
            print("-" * 60)
            return
    print("  >> No se encontró ningún expediente con ese número.")

def ordenar_por_codigo(codigos, dnis, nombres, tramites, folios, fechas, estados,
                       tipos_persona, rucs, direcciones, celulares, correos,
                       firmantes, requisitos, citas):
    n = len(codigos)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if codigos[j] > codigos[j + 1]:
                codigos[j], codigos[j+1] = codigos[j+1], codigos[j]
                dnis[j], dnis[j+1] = dnis[j+1], dnis[j]
                nombres[j], nombres[j+1] = nombres[j+1], nombres[j]
                tramites[j], tramites[j+1] = tramites[j+1], tramites[j]
                folios[j], folios[j+1] = folios[j+1], folios[j]
                fechas[j], fechas[j+1] = fechas[j+1], fechas[j]
                estados[j], estados[j+1] = estados[j+1], estados[j]
                tipos_persona[j], tipos_persona[j+1] = tipos_persona[j+1], tipos_persona[j]
                rucs[j], rucs[j+1] = rucs[j+1], rucs[j]
                direcciones[j], direcciones[j+1] = direcciones[j+1], direcciones[j]
                celulares[j], celulares[j+1] = celulares[j+1], celulares[j]
                correos[j], correos[j+1] = correos[j+1], correos[j]
                firmantes[j], firmantes[j+1] = firmantes[j+1], firmantes[j]
                requisitos[j], requisitos[j+1] = requisitos[j+1], requisitos[j]
                citas[j], citas[j+1] = citas[j+1], citas[j]

def bandeja(codigos, dnis, nombres, tramites, folios, fechas, estados,
            tipos_persona, rucs, direcciones, celulares, correos,
            firmantes, requisitos, citas):
    if len(codigos) == 0:
        print("  >> No hay expedientes en la bandeja.")
        return
    ordenar_por_codigo(codigos, dnis, nombres, tramites, folios, fechas, estados,
                       tipos_persona, rucs, direcciones, celulares, correos,
                       firmantes, requisitos, citas)
    print("\n--- BANDEJA DE EXPEDIENTES (ordenada por N.°) ---")
    print(f"{'N.° EXPEDIENTE':<18}{'FECHA':<18}{'DOC':<12}{'TIPO':<18}{'TRÁMITE':<28}{'ESTADO'}")
    print("-" * 110)
    for i in range(len(codigos)):
        print(f"{codigos[i]:<18}{fechas[i]:<18}{dnis[i]:<12}{tipos_persona[i]:<18}{tramites[i]:<28}{estados[i]}")

def cambiar_estado(codigos, dnis, nombres, tramites, folios, fechas, estados,
                   tipos_persona, rucs, direcciones, celulares, correos,
                   firmantes, requisitos, citas):
    print("\n--- DERIVAR / CAMBIAR ESTADO ---")
    buscado = input("  N.° de expediente: ").strip().upper()
    for i in range(len(codigos)):
        if codigos[i] == buscado:
            print(f"  Estado actual: {estados[i]}")
            print("  Nuevo estado:")
            print("    1) EN REVISIÓN")
            print("    2) OBSERVADO")
            print("    3) APROBADO")
            print("    4) RECHAZADO")
            op = input("  Opción: ").strip()
            mapa = {"1": "EN REVISIÓN", "2": "OBSERVADO",
                    "3": "APROBADO", "4": "RECHAZADO"}
            if op in mapa:
                estados[i] = mapa[op]
                print(f"  >> Expediente {codigos[i]} actualizado a: {mapa[op]}")
            else:
                print("  >> ERROR: opción no válida.")
            return
    print("  >> No se encontró el expediente.")

def mostrar_reglas_anulacion():
    """Muestra las reglas de negocio de la anulación."""
    print("\n" + "=" * 60)
    print("   REGLAS PARA ANULAR UN ENVÍO A LA MUNICIPALIDAD")
    print("=" * 60)
    print("  La Mesa de Partes anula el envío si:")
    print("  1. El trámite está cancelado o el expediente anulado.")
    print("  2. Falta algún documento obligatorio (adjunto, firma, sello).")
    print("  3. Los datos son inválidos (DNI/RUC mal registrados).")
    print("  4. Hay duplicación de datos (mismo número, DNI o referencia).")
    print("  5. El destino de la municipalidad cambia o se corrige.")
    print("  6. La municipalidad rechaza o devuelve el expediente.")
    print("  7. Pasa el tiempo límite de 24 horas sin confirmación.")
    print("  8. No cumple los requisitos obligatorios del trámite.")
    print("=" * 60)

def anular(codigos, dnis, nombres, tramites, folios, fechas, estados,
           tipos_persona, rucs, direcciones, celulares, correos,
           firmantes, requisitos, citas):
    mostrar_reglas_anulacion()

    print("\n--- ANULAR EXPEDIENTE ---")
    buscado = input("  N.° de expediente a anular: ").strip().upper()

    for i in range(len(codigos)):
        if codigos[i] == buscado:
            motivos = []

            # 1. Trámite cancelado / expediente anulado
            if estados[i] in ("CANCELADO", "ANULADO"):
                motivos.append(f"El expediente ya está en estado {estados[i]}.")

            # 2. Documento faltante
            obligatorios = ["solicitud", "formato", "sello"]
            for doc in obligatorios:
                if doc not in requisitos[i].split(", "):
                    motivos.append(f"Falta el documento obligatorio: {doc}.")

            # 3. Datos inválidos
            if not dnis[i].isdigit() or len(dnis[i]) not in (8, 11):
                motivos.append("El documento (DNI/RUC) no es válido.")

            # 4. Duplicación de datos
            duplicados = [c for c in codigos if c == buscado]
            if len(duplicados) > 1:
                motivos.append("Ya existe un expediente con ese número (duplicado).")
            else:
                print(f"  >> Verificación de duplicados: no hay expedientes duplicados con el número {buscado}.")

            # 5. Cambio de destino
            destinos_validos = ["Chorrillos", "Miraflores", "San Isidro"]
            if "Chorrillos" not in destinos_validos:
                motivos.append("El destino no es válido o cambió.")

            # 6. Rechazo / devolución
            if estados[i] == "RECHAZADO":
                motivos.append("El expediente fue rechazado o devuelto por la municipalidad.")

            # 7. Tiempo límite vencido (24 horas)
            try:
                fecha_envio = datetime.strptime(fechas[i], "%d/%m/%Y %H:%M")
                limite = fecha_envio + timedelta(hours=24)
                if datetime.now() > limite:
                    motivos.append("Pasó el tiempo límite de 24 horas sin confirmación.")
            except ValueError:
                pass

            # 8. Incumplimiento de requisitos obligatorios
            if requisitos[i] == "NINGUNO":
                motivos.append("El expediente no tiene ningún requisito adjunto.")

            if motivos:
                print("\n  >> NO se puede anular el envío. Motivos:")
                for m in motivos:
                    print(f"     - {m}")
                return

            conf = input("\n  ¿Está seguro de anular este expediente? (S/N): ").strip().upper()
            if conf != "S":
                print("  >> Anulación cancelada.")
                return

            estados[i] = "ANULADO"
            print(f"  >> Expediente {codigos[i]} ANULADO.")
            return

    print("  >> No se encontró el expediente.")

def registrar_cita(codigos, dnis, nombres, tramites, folios, fechas, estados,
                   tipos_persona, rucs, direcciones, celulares, correos,
                   firmantes, requisitos, citas):
    print("\n--- REGISTRAR CITA ---")
    buscado = input("  N.° de expediente: ").strip().upper()
    for i in range(len(codigos)):
        if codigos[i] == buscado:
            fecha_cita = input("  Fecha de la cita (dd/mm/aaaa): ").strip()
            hora_cita = input("  Hora de la cita (hh:mm): ").strip()
            citas[i] = f"{fecha_cita} {hora_cita}"
            print(f"  >> Cita registrada para {codigos[i]}: {citas[i]}")
            return
    print("  >> No se encontró el expediente.")

def reporte(codigos, dnis, nombres, tramites, folios, fechas, estados,
            tipos_persona, rucs, direcciones, celulares, correos,
            firmantes, requisitos, citas):
    print("\n--- REPORTE POR TIPO DE TRÁMITE ---")
    if len(codigos) == 0:
        print("  >> No hay datos para reportar.")
        return
    conteo = {}
    for t in tramites:
        conteo[t] = conteo.get(t, 0) + 1
    for tipo, cantidad in conteo.items():
        print(f"  {tipo:<35} {cantidad} expediente(s)")
    print("-" * 50)
    print(f"  TOTAL REGISTRADO: {len(codigos)} expediente(s)")

# ---------- MENÚ PRINCIPAL ----------

def menu():
    (codigos, dnis, nombres, tramites, folios, fechas, estados,
     tipos_persona, rucs, direcciones, celulares, correos,
     firmantes, requisitos, citas) = leer_expedientes()

    while True:
        cabecera()
        print("  [1] Recepcionar expediente")
        print("  [2] Consultar estado por N.° de expediente")
        print("  [3] Bandeja de expedientes (Ordenado)")
        print("  [4] Derivar / cambiar estado")
        print("  [5] Anular expediente")
        print("  [6] Registrar cita")
        print("  [7] Reporte por tipo de trámite")
        print("  [8] Cerrar caja y salir")
        opcion = input("\n  Seleccione una opción: ").strip()

        if opcion == "1":
            recepcionar(codigos, dnis, nombres, tramites, folios, fechas, estados,
                        tipos_persona, rucs, direcciones, celulares, correos,
                        firmantes, requisitos, citas)
        elif opcion == "2":
            consultar(codigos, dnis, nombres, tramites, folios, fechas, estados,
                      tipos_persona, rucs, direcciones, celulares, correos,
                      firmantes, requisitos, citas)
        elif opcion == "3":
            bandeja(codigos, dnis, nombres, tramites, folios, fechas, estados,
                    tipos_persona, rucs, direcciones, celulares, correos,
                    firmantes, requisitos, citas)
        elif opcion == "4":
            cambiar_estado(codigos, dnis, nombres, tramites, folios, fechas, estados,
                           tipos_persona, rucs, direcciones, celulares, correos,
                           firmantes, requisitos, citas)
        elif opcion == "5":
            anular(codigos, dnis, nombres, tramites, folios, fechas, estados,
                   tipos_persona, rucs, direcciones, celulares, correos,
                   firmantes, requisitos, citas)
        elif opcion == "6":
            registrar_cita(codigos, dnis, nombres, tramites, folios, fechas, estados,
                           tipos_persona, rucs, direcciones, celulares, correos,
                           firmantes, requisitos, citas)
        elif opcion == "7":
            reporte(codigos, dnis, nombres, tramites, folios, fechas, estados,
                    tipos_persona, rucs, direcciones, celulares, correos,
                    firmantes, requisitos, citas)
        elif opcion == "8":
            guardar_expedientes(codigos, dnis, nombres, tramites, folios, fechas, estados,
                                tipos_persona, rucs, direcciones, celulares, correos,
                                firmantes, requisitos, citas)
            print("\n>> Caja cerrada. Datos guardados. Hasta luego.")
            break
        else:
            print(">> ERROR: opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
