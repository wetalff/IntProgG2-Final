class Habito:
    def __init__(self, nombre, repeticiones_deseadas):
        self.nombre = nombre
        self.repeticiones_deseadas = repeticiones_deseadas
        self.repeticiones_completadas = 0

    def registrar_repeticiones(self, completadas):
        if 0 <= completadas <= self.repeticiones_deseadas:
            self.repeticiones_completadas = completadas
        else:
            print(f"Error: Las repeticiones deben estar entre 0 y {self.repeticiones_deseadas}")

    def porcentaje_cumplimiento(self):
        if self.repeticiones_deseadas == 0:
            return 0
        return (self.repeticiones_completadas / self.repeticiones_deseadas) * 100

habito = Habito("Beber agua", 5)
habito.registrar_repeticiones(4)
print(f"Cumplimiento de hoy: {habito.porcentaje_cumplimiento():.2f}%")