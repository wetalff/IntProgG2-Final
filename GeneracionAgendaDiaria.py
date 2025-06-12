from datetime import datetime

habitos = [
    {
        "nombre": "Leer 30 minutos",
        "frecuencia": "diaria",
        "duracion": 30,
        "horario": "07:00"
    },
    {
        "nombre": "Hacer ejercicio",
        "frecuencia": "semanal",
        "duracion": 60,
        "horario": "18:00"
    },
    {
        "nombre": "Meditación",
        "frecuencia": "diaria",
        "duracion": 15,
        "horario": None
    },
    {
        "nombre": "Planificación semanal",
        "frecuencia": "semanal",
        "duracion": 45,
        "horario": "09:00"
    }
]

def generar_agenda_diaria(habitos):
    hoy = datetime.now()
    dia_semana = hoy.weekday()  # 0 = Lunes, 6 = Domingo

    print(f"Agenda para hoy: {hoy.strftime('%A, %d-%m-%Y')}\n")

    for habito in habitos:
        frecuencia = habito["frecuencia"]

        if frecuencia == "diaria" or (frecuencia == "semanal" and dia_semana == 0):
            nombre = habito["nombre"]
            duracion = habito["duracion"]
            horario = habito["horario"] if habito["horario"] else "Horario no especificado"
            print(f"- {nombre} | Duración: {duracion} min | Horario: {horario}")

generar_agenda_diaria(habitos)