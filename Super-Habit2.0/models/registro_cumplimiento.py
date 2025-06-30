from datetime import datetime
from typing import Optional

class RegistroCumplimiento:
    """Clase que representa el registro de cumplimiento de un hábito"""
    
    def __init__(self, habito_id: int, fecha: datetime, completado: bool = False, 
                 registro_id: Optional[int] = None, nota: Optional[str] = None):
        self.id = registro_id
        self.habito_id = habito_id
        self.fecha = fecha
        self.completado = completado
        self.fecha_completado = datetime.now() if completado else None
        self.nota = nota
        
    def marcar_completado(self, nota: Optional[str] = None):
        """Marca el hábito como completado"""
        self.completado = True
        self.fecha_completado = datetime.now()
        if nota:
            self.nota = nota
    
    def desmarcar_completado(self):
        """Desmarca el hábito como completado"""
        self.completado = False
        self.fecha_completado = None
    
    def __str__(self):
        estado = "✅ Completado" if self.completado else "❌ Pendiente"
        return f"Hábito {self.habito_id} - {self.fecha.strftime('%Y-%m-%d')} - {estado}"
    
    def to_dict(self):
        """Convierte el registro a diccionario para almacenamiento"""
        return {
            'id': self.id,
            'habito_id': self.habito_id,
            'fecha': self.fecha.date().isoformat(),
            'completado': self.completado,
            'fecha_completado': self.fecha_completado.isoformat() if self.fecha_completado else None,
            'nota': self.nota
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un registro desde un diccionario"""
        fecha = datetime.fromisoformat(data['fecha'] + 'T00:00:00')
        
        registro = cls(
            habito_id=data['habito_id'],
            fecha=fecha,
            completado=data['completado'],
            registro_id=data.get('id'),
            nota=data.get('nota')
        )
        
        if data.get('fecha_completado'):
            registro.fecha_completado = datetime.fromisoformat(data['fecha_completado'])
        
        return registro

