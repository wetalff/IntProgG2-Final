# SUPERHÁBIT - AVANCE
# GRUPO C
# Introducción a la Programación
# Funcionalidades implementadas: RF-001, RF-002, RF-003, RF-004

import datetime

# ════════════════════════════════════════════════════════════════════
# Lista de hábitos y cumplimiento
# Cada hábito es una lista: [nombre, frecuencia, duración, horario, veces_por_dia]
# Cada cumplimiento es una lista de porcentajes (uno por día o semana)
# ════════════════════════════════════════════════════════════════════
habitos = []
cumplimiento = []

# ════════════════════════════════════════════════════════════════════
# Registro de hábitos por el usuario (RF-001) - versión mejorada
# ════════════════════════════════════════════════════════════════════
print("BIENVENIDO A SUPERHÁBIT - Seguimiento de hábitos personales\n")

while True:
    print("--- REGISTRO DE HÁBITO ---")
    nombre = input("Nombre del hábito: ")

    frecuencia = input("Frecuencia (diaria/semanal): ").lower()
    while frecuencia not in ["diaria", "semanal"]:
        print("⚠️ Ingresa solo 'diaria' o 'semanal'.")
        frecuencia = input("Frecuencia (diaria/semanal): ").lower()

    duracion = input("Duración estimada (ej: 30 minutos): ")

    veces_por_dia = 1
    horarios = ""

    if frecuencia == "diaria":
        rep = input("¿Cuántas veces deseas realizarlo al día?: ")
        if rep.isdigit() and int(rep) > 0:
            veces_por_dia = int(rep)

        # Pedir horarios para cada repetición si son más de una
        if veces_por_dia > 1:
            print(f"Ingresa el horario sugerido para cada una de las {veces_por_dia} repeticiones:")
            lista_horarios = []
            for i in range(veces_por_dia):
                h = input(f"Horario sugerido para la repetición {i+1}: ")
                lista_horarios.append(h)
            horarios = ", ".join(lista_horarios)
        else:
            horarios = input("Horario sugerido (opcional): ")

    elif frecuencia == "semanal":
        horarios = input("Horario sugerido (opcional): ")

    # Guardar el hábito
    nuevo = [nombre, frecuencia, duracion, horarios, veces_por_dia]
    habitos.append(nuevo)
    cumplimiento.append([])

    continuar = input("¿Agregar otro hábito? (s/n): ").lower()
    if continuar != "s":
        break


# ════════════════════════════════════════════════════════════════════
# Mostrar hábitos del día (RF-002)
# ════════════════════════════════════════════════════════════════════
print("\nAGENDA DEL DÍA:")

# Obtener el día actual (0 = lunes, 6 = domingo)
hoy = datetime.date.today()
dia_semana = hoy.weekday()

for i in range(len(habitos)):
    h = habitos[i]

    nombre = h[0]
    frecuencia = h[1]
    duracion = h[2]
    horario = h[3]
    veces = h[4]

    # Mostrar el hábito si es diario o si es lunes (para los semanales)
    if frecuencia == "diaria" or (frecuencia == "semanal" and dia_semana == 0):
        # Mostrar "x2", "x3", etc. si se repite más de una vez
        veces_txt = f" x{veces}" if frecuencia == "diaria" and veces > 1 else ""
        # Mostrar el horario si fue ingresado
        horario_txt = f" - Horario: {horario}" if horario != "" else ""

        print(f"{i+1}. {nombre}{veces_txt} ({duracion}){horario_txt}")


# ════════════════════════════════════════════════════════════════════
# Marcar hábitos completados (RF-003) — versión modificada
# ════════════════════════════════════════════════════════════════════
print("\nMARCA TUS HÁBITOS DE HOY:")

for i in range(len(habitos)):
    h = habitos[i]
    frecuencia = h[1]
    veces = h[4]

    if frecuencia == "diaria":
        entrada = input(f"¿Cuántas veces hiciste '{h[0]}' hoy? (0-{veces}): ")
        if entrada.isdigit():
            hechas = int(entrada)
            if hechas > veces:
                hechas = veces
            porcentaje = int((hechas / veces) * 100)
        else:
            porcentaje = 0
        cumplimiento[i].append(porcentaje)

    elif frecuencia == "semanal":
        respuesta = input(f"¿Completaste '{h[0]}' esta semana? (s/n): ").lower()
        porcentaje = 100 if respuesta == "s" else 0
        cumplimiento[i].append(porcentaje)

# ════════════════════════════════════════════════════════════════════
# Mostrar progreso (RF-004)
# ════════════════════════════════════════════════════════════════════
print("\nPROGRESO SEMANAL:")

for i in range(len(habitos)):
    h = habitos[i]
    nombre = h[0]
    frecuencia = h[1]
    registros = cumplimiento[i]

    if frecuencia == "diaria":
        if len(registros) > 0:
            promedio = sum(registros) / len(registros)
        else:
            promedio = 0
        print(f"{nombre}: {int(promedio)}% promedio diario")
    
    elif frecuencia == "semanal":
        if len(registros) > 0 and registros[-1] == 100:
            print(f"{nombre}: completado esta semana")
        else:
            print(f"{nombre}: pendiente esta semana")