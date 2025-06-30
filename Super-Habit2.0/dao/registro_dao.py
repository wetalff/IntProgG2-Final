from typing import List, Optional
from datetime import datetime, date, timedelta
from dao.base_dao import BaseDAO
from models.registro_cumplimiento import RegistroCumplimiento

class RegistroDAO(BaseDAO):
    """DAO para el manejo de registros de cumplimiento"""
    
    def __init__(self):
        super().__init__('registros')
    
    def crear_registro(self, registro: RegistroCumplimiento) -> RegistroCumplimiento:
        """Crea un nuevo registro de cumplimiento"""
        datos_registro = registro.to_dict()
        datos_guardados = self.crear(datos_registro)
        registro.id = datos_guardados['id']
        return registro
    
    def obtener_registro(self, registro_id: int) -> Optional[RegistroCumplimiento]:
        """Obtiene un registro por su ID"""
        datos = self.obtener_por_id(registro_id)
        if datos:
            return RegistroCumplimiento.from_dict(datos)
        return None
    
    def obtener_registro_por_habito_fecha(self, habito_id: int, fecha: date) -> Optional[RegistroCumplimiento]:
        """Obtiene un registro específico por hábito y fecha"""
        for datos in self.obtener_todos():
            if (datos['habito_id'] == habito_id and 
                datos['fecha'] == fecha.isoformat()):
                return RegistroCumplimiento.from_dict(datos)
        return None
    
    def obtener_registros_por_habito(self, habito_id: int) -> List[RegistroCumplimiento]:
        """Obtiene todos los registros de un hábito"""
        registros = []
        for datos in self.obtener_todos():
            if datos['habito_id'] == habito_id:
                registros.append(RegistroCumplimiento.from_dict(datos))
        return sorted(registros, key=lambda r: r.fecha)
    
    def obtener_registros_por_fecha(self, fecha: date) -> List[RegistroCumplimiento]:
        """Obtiene todos los registros de una fecha específica"""
        registros = []
        fecha_str = fecha.isoformat()
        for datos in self.obtener_todos():
            if datos['fecha'] == fecha_str:
                registros.append(RegistroCumplimiento.from_dict(datos))
        return registros
    
    def obtener_registros_por_periodo(self, fecha_inicio: date, fecha_fin: date) -> List[RegistroCumplimiento]:
        """Obtiene registros en un período de tiempo"""
        registros = []
        for datos in self.obtener_todos():
            fecha_registro = datetime.fromisoformat(datos['fecha'] + 'T00:00:00').date()
            if fecha_inicio <= fecha_registro <= fecha_fin:
                registros.append(RegistroCumplimiento.from_dict(datos))
        return sorted(registros, key=lambda r: r.fecha)
    
    def obtener_registros_completados_por_habito(self, habito_id: int) -> List[RegistroCumplimiento]:
        """Obtiene todos los registros completados de un hábito"""
        registros = self.obtener_registros_por_habito(habito_id)
        return [r for r in registros if r.completado]
    
    def actualizar_registro(self, registro: RegistroCumplimiento) -> bool:
        """Actualiza un registro existente"""
        if registro.id is None:
            return False
        
        datos_registro = registro.to_dict()
        resultado = self.actualizar(registro.id, datos_registro)
        return resultado is not None
    
    def marcar_habito_completado(self, habito_id: int, fecha: date, nota: Optional[str] = None) -> RegistroCumplimiento:
        """Marca un hábito como completado en una fecha específica"""
        registro = self.obtener_registro_por_habito_fecha(habito_id, fecha)
        
        if registro:
            # Actualizar registro existente
            registro.marcar_completado(nota)
            self.actualizar_registro(registro)
        else:
            # Crear nuevo registro
            fecha_datetime = datetime.combine(fecha, datetime.min.time())
            registro = RegistroCumplimiento(habito_id, fecha_datetime, True, nota=nota)
            registro = self.crear_registro(registro)
        
        return registro
    
    def desmarcar_habito_completado(self, habito_id: int, fecha: date) -> bool:
        """Desmarca un hábito como completado"""
        registro = self.obtener_registro_por_habito_fecha(habito_id, fecha)
        
        if registro:
            registro.desmarcar_completado()
            return self.actualizar_registro(registro)
        
        return False
    
    def calcular_racha_actual(self, habito_id: int) -> int:
        """Calcula la racha actual de días consecutivos completados"""
        registros = self.obtener_registros_completados_por_habito(habito_id)
        if not registros:
            return 0
        
        # Ordenar por fecha descendente
        registros.sort(key=lambda r: r.fecha, reverse=True)
        
        racha = 0
        fecha_actual = date.today()
        
        for registro in registros:
            fecha_registro = registro.fecha.date()
            if fecha_registro == fecha_actual:
                racha += 1
                fecha_actual -= timedelta(days=1)
            else:
                break
        
        return racha

