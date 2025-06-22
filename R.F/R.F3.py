def validar_repeticiones(input_str):
    """Valida que las repeticiones ingresadas sean un número entero positivo"""
    try:
        repeticiones = int(input_str)
        if repeticiones < 0:
            print("Error: Las repeticiones no pueden ser negativas.")
            return None
        return repeticiones
    except ValueError:
        print("Error: Las repeticiones deben ser un número entero.")
        return None

def validar_frecuencia(frecuencia):
    """Valida que la frecuencia sea 'diaria' o 'semanal'"""
    frecuencia = frecuencia.lower()
    if frecuencia in ["diaria", "semanal"]:
        return frecuencia
    else:
        print("Error: La frecuencia debe ser 'diaria' o 'semanal'.")
        return None

def solicitar_habito():
    nombre = input("Ingrese el nombre del hábito: ")

    # Validar frecuencia
    frecuencia = None
    while frecuencia is None:
        frecuencia = validar_frecuencia(input("Ingrese la frecuencia ('diaria' o 'semanal'): "))

    # Validar repeticiones
    repeticiones = None
    while repeticiones is None:
        repeticiones = validar_repeticiones(input("Ingrese la cantidad de repeticiones deseadas: "))

    print(f"\n Hábito registrado correctamente:")
    print(f"Nombre: {nombre}")
    print(f"Frecuencia: {frecuencia}")
    print(f"Repeticiones: {repeticiones}")

# Ejecución de prueba
if __name__ == "__main__":
    solicitar_habito()