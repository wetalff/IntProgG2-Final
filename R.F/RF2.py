"""Se agregara la funcionalidad para que el sistema registre el historial de cumplimiento diario por cada hábito. Esto se logra almacenando los porcentajes diarios (en el caso de hábitos diarios) o un valor binario semanal (para hábitos semanales). El historial queda disponible en memoria mientras se ejecuta el programa, como preparación para la futura persistencia de datos."""


habitos = [
    ["Beber agua", "diario", 8],
    ["Leer libro", "diario", 1],
    ["Salir a correr", "semanal"],
    ["Limpiar habitación", "semanal"]
]


historial = [[habito[0], []] for habito in habitos]

def registrar_dia():
    print("\nRegistro de hábitos para el día:\n")
    for i, habito in enumerate(habitos):
        nombre = habito[0]
        tipo = habito[1]
        if tipo == "diario":
            objetivo = habito[2]
            while True:
                try:
                    realizado = int(input(f"¿Cuántas veces realizaste '{nombre}' hoy? "))
                    if realizado < 0:
                        print("Ingresa un número positivo.")
                        continue
                    break
                except ValueError:
                    print("Por favor ingresa un número válido.")
            porcentaje = min(100, int((realizado / objetivo) * 100))
            historial[i][1].append(porcentaje)
        else:  # semanal
            while True:
                resp = input(f"¿Completaste el hábito semanal '{nombre}' hoy? (s/n): ").lower()
                if resp in ("s", "n"):
                    cumplimiento = 1 if resp == "s" else 0
                    historial[i][1].append(cumplimiento)
                    break
                else:
                    print("Responde con 's' o 'n'.")

def mostrar_historial():
    print("\nHistorial acumulado de hábitos:")
    for hab, datos in historial:
        print(f"- {hab}: {datos}")



seguir = "s"
while seguir == "s":
    registrar_dia()
    mostrar_historial()
    seguir = input("\n¿Registrar otro día? (s/n): ").lower()

print("\nPrograma terminado.")