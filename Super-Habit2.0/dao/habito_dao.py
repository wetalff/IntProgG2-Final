from typing import List, Optional
from datetime import datetime
from dao.base_dao import BaseDAO
from models.habito import Habito

class HabitoDAO(BaseDAO):
    """DAO para el manejo de hábitos"""
    
    def __init__(self):
        super().__init__('habitos')
    
    def crear_habito(self, habito: Habito) -> Habito:
        """Crea un nuevo hábito"""
        datos_habito = habito.to_dict()
        datos_guardados = self.crear(datos_habito)
        habito.id = datos_guardados['id']
        return habito
    
    def obtener_habito(self, habito_id: int) -> Optional[Habito]:
        """Obtiene un hábito por su ID"""
        datos = self.obtener_por_id(habito_id)
        if datos:
            return Habito.from_dict(datos)
        return None
    
    def obtener_todos_habitos(self) -> List[Habito]:
        """Obtiene todos los hábitos"""
        return [Habito.from_dict(datos) for datos in self.obtener_todos()]
    
    def obtener_habitos_activos(self) -> List[Habito]:
        """Obtiene todos los hábitos activos"""
        habitos = self.obtener_todos_habitos()
        return [h for h in habitos if h.activo]
    
    def obtener_habitos_por_frecuencia(self, frecuencia: str) -> List[Habito]:
        """Obtiene hábitos por frecuencia (diaria o semanal)"""
        habitos = self.obtener_habitos_activos()
        return [h for h in habitos if h.frecuencia == frecuencia.lower()]
    
    def actualizar_habito(self, habito: Habito) -> bool:
        """Actualiza un hábito existente"""
        if habito.id is None:
            return False
        
        datos_habito = habito.to_dict()
        resultado = self.actualizar(habito.id, datos_habito)
        return resultado is not None
    
    def desactivar_habito(self, habito_id: int) -> bool:
        """Desactiva un hábito (no lo elimina)"""
        habito = self.obtener_habito(habito_id)
        if habito:
            habito.activo = False
            return self.actualizar_habito(habito)
        return False
    
    def eliminar_habito(self, habito_id: int) -> bool:
        """Elimina permanentemente un hábito"""
        return self.eliminar(habito_id)

