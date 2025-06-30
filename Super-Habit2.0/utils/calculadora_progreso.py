from datetime import date, timedelta, datetime
from typing import List, Dict, Tuple
from models.habito import Habito
from models.registro_cumplimiento import RegistroCumplimiento
from dao.registro_dao import RegistroDAO

class CalculadoraProgreso:
    """Clase para calcular el progreso de hábitos"""
    
    def __init__(self):
        self.registro_dao = RegistroDAO()
    
    def calcular_progreso_semanal(self, habito: Habito) -> Dict[str, float]:
        """Calcula el progreso semanal de un hábito"""
        hoy = date.today()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        
        registros = self.registro_dao.obtener_registros_por_periodo(inicio_semana, fin_semana)
        registros_habito = [r for r in registros if r.habito_id == habito.id and r.completado]
        
        if habito.frecuencia == 'diaria':
            objetivo = 7  # 7 días a la semana
        else:  # semanal
            objetivo = 1  # 1 vez a la semana
        
        completados = len(registros_habito)
        porcentaje = (completados / objetivo) * 100 if objetivo > 0 else 0
        
        return {
            'completados': completados,
            'objetivo': objetivo,
            'porcentaje': min(porcentaje, 100),
            'periodo': f"{inicio_semana.strftime('%d/%m')} - {fin_semana.strftime('%d/%m')}"
        }
    
    def calcular_progreso_mensual(self, habito: Habito) -> Dict[str, float]:
        """Calcula el progreso mensual de un hábito"""
        hoy = date.today()
        inicio_mes = hoy.replace(day=1)
        
        # Calcular el último día del mes
        if hoy.month == 12:
            fin_mes = hoy.replace(year=hoy.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            fin_mes = hoy.replace(month=hoy.month + 1, day=1) - timedelta(days=1)
        
        registros = self.registro_dao.obtener_registros_por_periodo(inicio_mes, fin_mes)
        registros_habito = [r for r in registros if r.habito_id == habito.id and r.completado]
        
        dias_mes = (fin_mes - inicio_mes).days + 1
        
        if habito.frecuencia == 'diaria':
            objetivo = dias_mes
        else:  # semanal
            # Aproximadamente 4 semanas por mes
            objetivo = dias_mes // 7
        
        completados = len(registros_habito)
        porcentaje = (completados / objetivo) * 100 if objetivo > 0 else 0
        
        return {
            'completados': completados,
            'objetivo': objetivo,
            'porcentaje': min(porcentaje, 100),
            'periodo': f"{inicio_mes.strftime('%B %Y')}"
        }
    
    def calcular_racha_actual(self, habito: Habito) -> int:
        """Calcula la racha actual de cumplimiento"""
        return self.registro_dao.calcular_racha_actual(habito.id)
    
    def calcular_estadisticas_generales(self, habito: Habito) -> Dict[str, any]:
        """Calcula estadísticas generales de un hábito"""
        registros = self.registro_dao.obtener_registros_por_habito(habito.id)
        registros_completados = [r for r in registros if r.completado]
        
        total_dias = len(registros)
        dias_completados = len(registros_completados)
        
        porcentaje_exito = (dias_completados / total_dias * 100) if total_dias > 0 else 0
        racha_actual = self.calcular_racha_actual(habito)
        
        # Calcular la racha más larga
        racha_maxima = self._calcular_racha_maxima(registros_completados)
        
        return {
            'total_dias': total_dias,
            'dias_completados': dias_completados,
            'porcentaje_exito': porcentaje_exito,
            'racha_actual': racha_actual,
            'racha_maxima': racha_maxima,
            'fecha_creacion': habito.fecha_creacion.strftime('%d/%m/%Y')
        }
    
    def _calcular_racha_maxima(self, registros_completados: List[RegistroCumplimiento]) -> int:
        """Calcula la racha máxima de días consecutivos"""
        if not registros_completados:
            return 0
        
        # Ordenar por fecha
        registros_ordenados = sorted(registros_completados, key=lambda r: r.fecha)
        
        racha_maxima = 1
        racha_actual = 1
        
        for i in range(1, len(registros_ordenados)):
            fecha_anterior = registros_ordenados[i-1].fecha.date()
            fecha_actual = registros_ordenados[i].fecha.date()
            
            # Verificar si son días consecutivos
            if fecha_actual == fecha_anterior + timedelta(days=1):
                racha_actual += 1
                racha_maxima = max(racha_maxima, racha_actual)
            else:
                racha_actual = 1
        
        return racha_maxima
    
    def obtener_resumen_diario(self, fecha: date = None) -> Dict[str, any]:
        """Obtiene un resumen del progreso del día"""
        if fecha is None:
            fecha = date.today()
        
        registros = self.registro_dao.obtener_registros_por_fecha(fecha)
        
        total_habitos = len(registros)
        completados = len([r for r in registros if r.completado])
        pendientes = total_habitos - completados
        
        porcentaje = (completados / total_habitos * 100) if total_habitos > 0 else 0
        
        return {
            'fecha': fecha.strftime('%d/%m/%Y'),
            'total_habitos': total_habitos,
            'completados': completados,
            'pendientes': pendientes,
            'porcentaje': porcentaje
        }

