# ============================================================
#  VALIDACIONES - MESA DE PARTES DIGITAL (CHORRILLOS)
# ============================================================

import re
from datetime import datetime

LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"

# ---------- 1. IDENTIDAD Y DATOS PERSONALES ----------

def validar_dni(dni):
    """8 dígitos numéricos, solo ASCII."""
    return dni.isascii() and dni.isdigit() and len(dni) == 8

def validar_ruc(ruc):
    """11 dígitos numéricos, solo ASCII."""
    return ruc.isascii() and ruc.isdigit() and len(ruc) == 11

def validar_nombre(nombre):
    """Mínimo 3 caracteres, solo letras (con tildes y ñ) y espacios simples."""
    n = nombre.strip()
    return len(n) >= 3 and re.fullmatch(rf"[{LETRAS}]+( [{LETRAS}]+)*", n) is not None

def validar_razon_social(razon):
    """Mínimo 3 caracteres, letras/números y . , & ' - , con al menos una letra."""
    r = razon.strip()
    return (len(r) >= 3
            and re.fullmatch(rf"[{LETRAS}0-9 .,&'\-]+", r) is not None
            and re.search(rf"[{LETRAS}]", r) is not None)

def validar_direccion(direccion):
    """Mínimo 5 caracteres, letras/números y . , # ° / - , con al menos una letra."""
    d = direccion.strip()
    return (len(d) >= 5
            and re.fullmatch(rf"[{LETRAS}0-9 .,#°/\-]+", d) is not None
            and re.search(rf"[{LETRAS}]", d) is not None)

def validar_correo(correo):
    """Estructura usuario@dominio.ext con extensión de 2+ letras."""
    return re.fullmatch(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}",
                        correo) is not None

def validar_celular(celular):
    """9 dígitos y empieza con 9 (celulares en Perú)."""
    return (celular.isascii() and celular.isdigit()
            and len(celular) == 9 and celular.startswith("9"))

# ---------- 2. CITA: FECHA Y HORA ----------

HORA_APERTURA = datetime.strptime("08:00 AM", "%I:%M %p").time()
HORA_CIERRE = datetime.strptime("10:00 PM", "%I:%M %p").time()

def validar_fecha_cita(fecha_txt):
    """Devuelve None si es válida, o el mensaje de error."""
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", fecha_txt) is None:
        return "la fecha debe tener el formato dd/mm/aaaa."
    try:
        fecha = datetime.strptime(fecha_txt, "%d/%m/%Y")
    except ValueError:
        return "la fecha no existe en el calendario."
    if fecha.year < 2026:
        return "no se aceptan fechas anteriores al año 2026."
    if fecha.date() < datetime.now().date():
        return "no se aceptan fechas pasadas."
    return None

def convertir_hora_12(hora_txt):
    """Convierte 'hh:mm AM/PM' en datetime. Devuelve None si no es válida."""
    m = re.fullmatch(r"([0-9]{1,2}):([0-9]{2}) ?(AM|PM)", hora_txt.strip().upper())
    if m is None:
        return None
    try:
        return datetime.strptime(f"{int(m.group(1)):02d}:{m.group(2)} {m.group(3)}",
                                 "%I:%M %p")
    except ValueError:
        return None

def validar_hora_cita(hora_txt, fecha_txt):
    """Devuelve None si es válida, o el mensaje de error."""
    hora = convertir_hora_12(hora_txt)
    if hora is None:
        return ("la hora debe tener el formato hh:mm AM/PM (ejemplo: 09:30 AM) "
                "y ser una hora válida.")
    if hora.time() < HORA_APERTURA:
        return "la hora es antes del inicio de atención. El horario es de 08:00 AM a 10:00 PM."
    if hora.time() > HORA_CIERRE:
        return "la hora es después del cierre de atención. El horario es de 08:00 AM a 10:00 PM."
    fecha = datetime.strptime(fecha_txt, "%d/%m/%Y")
    if datetime.combine(fecha.date(), hora.time()) < datetime.now():
        return "la hora indicada ya pasó."
    return None

# ---------- 3. VALIDACIONES DENTRO DE recepcionar() ----------

# Tipo de solicitante: solo "1" o "2"
if tipo_op not in ("1", "2"):
    print("  >> ERROR: tipo de solicitante no válido.")
    return

# Tipo de trámite: debe estar en el diccionario
mapa = {"1": "Licencia de funcionamiento",
        "2": "ITSE",
        "3": "Solicitud de vecino"}
if opcion not in mapa:
    print("  >> ERROR: tipo de trámite no válido.")
    return

# Número de folios: dígitos y mayor a 0
if not (num_folios.isascii() and num_folios.isdigit()) or int(num_folios) <= 0:
    print("  >> ERROR: los folios deben ser un número mayor a 0.")
    return

# Requisitos S/N: cada respuesta debe ser exactamente S o N
resp = input(f"    {texto} (S/N): ").strip().upper()
if resp not in ("S", "N"):
    print("  >> ERROR: responda únicamente S o N.")
    return

# ---------- 4. REGLAS DE NEGOCIO DE anular() ----------

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

# 5. Cambio de destino
destinos_validos = ["Chorrillos", "Miraflores", "San Isidro"]
if "Chorrillos" not in destinos_validos:
    motivos.append("El destino no es válido o cambió.")

# 6. Rechazo / devolución
if estados[i] == "RECHAZADO":
    motivos.append("El expediente fue rechazado o devuelto por la municipalidad.")

# 7. Tiempo límite vencido (24 horas)
fecha_envio = datetime.strptime(fechas[i], "%d/%m/%Y %I:%M %p")
limite = fecha_envio + timedelta(hours=24)
if datetime.now() > limite:
    motivos.append("Pasó el tiempo límite de 24 horas sin confirmación.")

# 8. Incumplimiento de requisitos obligatorios
if requisitos[i] == "NINGUNO":
    motivos.append("El expediente no tiene ningún requisito adjunto")
