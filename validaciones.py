# ---------- VALIDACIONES ----------

LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"

def validar_dni(dni):
    return dni.isascii() and dni.isdigit() and len(dni) == 8

def validar_ruc(ruc):
    return ruc.isascii() and ruc.isdigit() and len(ruc) == 11

def validar_nombre(nombre):
    # Solo letras (con tildes y ñ) y espacios entre palabras. Sin números ni símbolos.
    n = nombre.strip()
    return len(n) >= 3 and re.fullmatch(rf"[{LETRAS}]+( [{LETRAS}]+)*", n) is not None

def validar_razon_social(razon):
    # Letras, números y signos propios de una empresa (S.A.C., E.I.R.L., &, -)
    r = razon.strip()
    return (len(r) >= 3
            and re.fullmatch(rf"[{LETRAS}0-9 .,&'\-]+", r) is not None
            and re.search(rf"[{LETRAS}]", r) is not None)

def validar_direccion(direccion):
    # Letras, números y signos propios de una dirección (Av. Los Pinos #123, Mz. A-5)
    d = direccion.strip()
    return (len(d) >= 5
            and re.fullmatch(rf"[{LETRAS}0-9 .,#°/\-]+", d) is not None
            and re.search(rf"[{LETRAS}]", d) is not None)

def validar_correo(correo):
    return re.fullmatch(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}",
                        correo) is not None

def validar_celular(celular):
    # 9 dígitos y los celulares en Perú empiezan con 9
    return (celular.isascii() and celular.isdigit()
            and len(celular) == 9 and celular.startswith("9"))

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

HORA_APERTURA = datetime.strptime("08:00 AM", "%I:%M %p").time()
HORA_CIERRE = datetime.strptime("10:00 PM", "%I:%M %p").time()

def formatear_hora_12(dt):
    """Devuelve la hora en formato 12 horas: 08:30 AM / 10:00 PM."""
    h = dt.hour % 12 or 12
    return f"{h:02d}:{dt.minute:02d} {'AM' if dt.hour < 12 else 'PM'}"

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

def generar_codigo(codigos):
    anio = datetime.now().year
    return f"{anio}-{len(codigos) + 1:05d}-MCH"
