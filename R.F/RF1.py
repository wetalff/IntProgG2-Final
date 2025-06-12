"""Se implementara la interacción con el usuario para registrar qué hábitos fueron cumplidos en el día. Si el hábito es diario, se solicita cuántas veces fue realizado ese día, comparándolo contra el objetivo para calcular un porcentaje. Si es semanal, se pregunta si se completó o no. Esta información se almacena en listas anidadas para mantener el historial de cumplimiento sin el uso de diccionarios."""

# Lista de hábitos: [nombre, tipo, objetivo]
habitos = [
    ["Beber agua", "diario", 8],     # objetivo: 8 vasos por día
    ["Ejercicio", "semanal", 1],     # objetivo: 1 vez por semana
    ["Leer", "diario", 30],          # objetivo: 30 minutos por día
    ["Lavar ropa", "semanal", 1]
]

# Historial de cumplimiento: lista por hábito, cada entrada es una sublista con los datos del día
# Formato para diario: [[día, veces_realizado, porcentaje]]
# Formato para semanal: [[semana, completado (1 o 0)]]
historial = [[] for _ in habitos]

def registrar_cumplimiento(dia, semana):
    for i, habito in enumerate(habitos):
        nombre, tipo, objetivo = habito
        print(f"\nHábito: {nombre} ({tipo})")

        if tipo == "diario":
            realizado = int(input(f"¿Cuántas veces hiciste '{nombre}' el día {dia}? "))
            porcentaje = min(100, int((realizado / objetivo) * 100))
            historial[i].append([dia, realizado, porcentaje])
        elif tipo == "semanal":
            completado = input(f"¿Completaste '{nombre}' en la semana {semana}? (s/n): ").strip().lower()
            historial[i].append([semana, 1 if completado == "s" else 0])

def mostrar_historial():
    print("\n=== HISTORIAL DE HÁBITOS ===")
    for i, habito in enumerate(habitos):
        nombre, tipo, _ = habito
        print(f"\n{name_format(nombre)} ({tipo}):")
        for registro in historial[i]:
            if tipo == "diario":
                dia, realizado, porcentaje = registro
                print(f"  Día {dia}: realizado {realizado} veces ({porcentaje}%)")
            else:
                semana, completado = registro
                print(f"  Semana {semana}: {'Completado' if completado else 'No completado'}")

def name_format(nombre):
    return nombre[0].upper() + nombre[1:]

# Ejemplo de uso
dia_actual = 1
semana_actual = 1

# Repetimos el registro por varios días
while True:
    print("\n--- Registro de hábitos ---")
    registrar_cumplimiento(dia_actual, semana_actual)

    mostrar_historial()

    continuar = input("\n¿Registrar otro día? (s/n): ").strip().lower()
    if continuar != "s":
        break
    dia_actual += 1
    if dia_actual % 7 == 1:
        semana_actual += 1