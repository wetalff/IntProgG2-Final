from datetime import datetime, time
from typing import Optional

class Habito:
    """Clase que representa un hábito del usuario"""
    
    def __init__(self, nombre: str, frecuencia: str, duracion: int, 
                 horario_sugerido: Optional[time] = None, habito_id: Optional[int] = None):
        self.id = habito_id
        self.nombre = nombre
        self.frecuencia = frecuencia.lower()  # 'diaria' o 'semanal'
        self.duracion = duracion  # en minutos
        self.horario_sugerido = horario_sugerido
        self.fecha_creacion = datetime.now()
        self.activo = True
        
    def __str__(self):
        horario_str = f" a las {self.horario_sugerido.strftime('%H:%M')}" if self.horario_sugerido else ""
        return f"{self.nombre} ({self.frecuencia}, {self.duracion} min{horario_str})"
    
    def to_dict(self):
        """Convierte el hábito a diccionario para almacenamiento"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'frecuencia': self.frecuencia,
            'duracion': self.duracion,
            'horario_sugerido': self.horario_sugerido.strftime('%H:%M') if self.horario_sugerido else None,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un hábito desde un diccionario"""
        horario = None
        if data.get('horario_sugerido'):
            hour, minute = map(int, data['horario_sugerido'].split(':'))
            horario = time(hour, minute)
            
        habito = cls(
            nombre=data['nombre'],
            frecuencia=data['frecuencia'],
            duracion=data['duracion'],
            horario_sugerido=horario,
            habito_id=data.get('id')
        )
        
        if data.get('fecha_creacion'):
            habito.fecha_creacion = datetime.fromisoformat(data['fecha_creacion'])
        
        habito.activo = data.get('activo', True)
        return habito

