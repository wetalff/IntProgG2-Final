from datetime import datetime, date, time, timedelta
from typing import List, Optional, Dict
from models import Habito, RegistroCumplimiento
from dao import HabitoDAO, RegistroDAO
from utils import CalculadoraProgreso, GeneradorMensajes

class GestorSuperHabit:
    """Clase principal para gestionar la aplicación SuperHábit"""
    
    def __init__(self):
        self.habito_dao = HabitoDAO()
        self.registro_dao = RegistroDAO()
        self.calculadora_progreso = CalculadoraProgreso()
        self.generador_mensajes = GeneradorMensajes()
    
    # ===== GESTIÓN DE HÁBITOS =====
    
    def crear_habito(self, nombre: str, frecuencia: str, duracion: int, 
                     horario_sugerido: Optional[str] = None) -> Habito:
        """Crea un nuevo hábito"""
        # Validar entrada
        if not nombre.strip():
            raise ValueError("El nombre del hábito no puede estar vacío")
        
        if frecuencia.lower() not in ['diaria', 'semanal']:
            raise ValueError("La frecuencia debe ser 'diaria' o 'semanal'")
        
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor a 0 minutos")
        
        # Procesar horario sugerido
        horario_obj = None
        if horario_sugerido:
            try:
                hora, minuto = map(int, horario_sugerido.split(':'))
                horario_obj = time(hora, minuto)
            except (ValueError, AttributeError):
                raise ValueError("Formato de horario inválido. Usa HH:MM (ej: 08:30)")
        
        # Crear y guardar hábito
        habito = Habito(nombre.strip(), frecuencia.lower(), duracion, horario_obj)
        return self.habito_dao.crear_habito(habito)
    
    def obtener_habitos_activos(self) -> List[Habito]:
        """Obtiene todos los hábitos activos"""
        return self.habito_dao.obtener_habitos_activos()
    
    def obtener_habito(self, habito_id: int) -> Optional[Habito]:
        """Obtiene un hábito por su ID"""
        return self.habito_dao.obtener_habito(habito_id)
    
    def actualizar_habito(self, habito_id: int, nombre: Optional[str] = None,
                         frecuencia: Optional[str] = None, duracion: Optional[int] = None,
                         horario_sugerido: Optional[str] = None) -> bool:
        """Actualiza un hábito existente"""
        habito = self.habito_dao.obtener_habito(habito_id)
        if not habito:
            return False
        
        # Actualizar campos si se proporcionan
        if nombre is not None:
            if not nombre.strip():
                raise ValueError("El nombre del hábito no puede estar vacío")
            habito.nombre = nombre.strip()
        
        if frecuencia is not None:
            if frecuencia.lower() not in ['diaria', 'semanal']:
                raise ValueError("La frecuencia debe ser 'diaria' o 'semanal'")
            habito.frecuencia = frecuencia.lower()
        
        if duracion is not None:
            if duracion <= 0:
                raise ValueError("La duración debe ser mayor a 0 minutos")
            habito.duracion = duracion
        
        if horario_sugerido is not None:
            if horario_sugerido.strip():
                try:
                    hora, minuto = map(int, horario_sugerido.split(':'))
                    habito.horario_sugerido = time(hora, minuto)
                except (ValueError, AttributeError):
                    raise ValueError("Formato de horario inválido. Usa HH:MM (ej: 08:30)")
            else:
                habito.horario_sugerido = None
        
        return self.habito_dao.actualizar_habito(habito)
    
    def desactivar_habito(self, habito_id: int) -> bool:
        """Desactiva un hábito"""
        return self.habito_dao.desactivar_habito(habito_id)
    
    def eliminar_habito(self, habito_id: int) -> bool:
        """Elimina permanentemente un hábito"""
        return self.habito_dao.eliminar_habito(habito_id)
    
    # ===== GESTIÓN DE CUMPLIMIENTO =====
    
    def marcar_habito_completado(self, habito_id: int, fecha: Optional[date] = None, 
                                nota: Optional[str] = None) -> str:
        """Marca un hábito como completado y retorna mensaje motivacional"""
        if fecha is None:
            fecha = date.today()
        
        habito = self.habito_dao.obtener_habito(habito_id)
        if not habito:
            raise ValueError("Hábito no encontrado")
        
        # Marcar como completado
        registro = self.registro_dao.marcar_habito_completado(habito_id, fecha, nota)
        
        # Calcular racha actual para el mensaje
        racha_actual = self.calculadora_progreso.calcular_racha_actual(habito)
        
        # Generar mensaje motivacional
        mensaje = self.generador_mensajes.generar_mensaje_habito_completado(habito, racha_actual)
        
        # Verificar si se alcanzó una meta
        progreso_semanal = self.calculadora_progreso.calcular_progreso_semanal(habito)
        progreso_mensual = self.calculadora_progreso.calcular_progreso_mensual(habito)
        
        if progreso_semanal['porcentaje'] >= 100:
            mensaje += "\n\n" + self.generador_mensajes.generar_mensaje_meta_alcanzada(habito, 'semanal')
        
        if progreso_mensual['porcentaje'] >= 100:
            mensaje += "\n\n" + self.generador_mensajes.generar_mensaje_meta_alcanzada(habito, 'mensual')
        
        return mensaje
    
    def desmarcar_habito_completado(self, habito_id: int, fecha: Optional[date] = None) -> bool:
        """Desmarca un hábito como completado"""
        if fecha is None:
            fecha = date.today()
        
        return self.registro_dao.desmarcar_habito_completado(habito_id, fecha)
    
    def obtener_estado_habito_hoy(self, habito_id: int) -> bool:
        """Verifica si un hábito está completado hoy"""
        registro = self.registro_dao.obtener_registro_por_habito_fecha(habito_id, date.today())
        return registro is not None and registro.completado
    
    # ===== GENERACIÓN DE AGENDA Y RECORDATORIOS =====
    
    def generar_agenda_diaria(self, fecha: Optional[date] = None) -> Dict[str, any]:
        """Genera la agenda diaria con hábitos y su estado"""
        if fecha is None:
            fecha = date.today()
        
        habitos_activos = self.obtener_habitos_activos()
        agenda = {
            'fecha': fecha.strftime('%d/%m/%Y'),
            'habitos': [],
            'resumen': None
        }
        
        for habito in habitos_activos:
            # Verificar si el hábito aplica para esta fecha
            aplica_hoy = self._habito_aplica_fecha(habito, fecha)
            
            if aplica_hoy:
                registro = self.registro_dao.obtener_registro_por_habito_fecha(habito.id, fecha)
                completado = registro is not None and registro.completado
                
                item_agenda = {
                    'habito': habito,
                    'completado': completado,
                    'horario_sugerido': habito.horario_sugerido.strftime('%H:%M') if habito.horario_sugerido else None,
                    'duracion': habito.duracion,
                    'racha_actual': self.calculadora_progreso.calcular_racha_actual(habito)
                }
                
                agenda['habitos'].append(item_agenda)
        
        # Generar resumen
        total = len(agenda['habitos'])
        completados = sum(1 for item in agenda['habitos'] if item['completado'])
        agenda['resumen'] = {
            'total': total,
            'completados': completados,
            'pendientes': total - completados,
            'porcentaje': (completados / total * 100) if total > 0 else 0
        }
        
        return agenda
    
    def _habito_aplica_fecha(self, habito: Habito, fecha: date) -> bool:
        """Determina si un hábito aplica para una fecha específica"""
        if habito.frecuencia == 'diaria':
            return True
        elif habito.frecuencia == 'semanal':
            # Para hábitos semanales, verificar si ya se completó esta semana
            inicio_semana = fecha - timedelta(days=fecha.weekday())
            fin_semana = inicio_semana + timedelta(days=6)
            
            registros_semana = self.registro_dao.obtener_registros_por_periodo(inicio_semana, fin_semana)
            registros_habito = [r for r in registros_semana if r.habito_id == habito.id and r.completado]
            
            # Si ya se completó esta semana, no mostrar hoy
            return len(registros_habito) == 0
        
        return False
    
    def obtener_habitos_pendientes_hoy(self) -> List[Habito]:
        """Obtiene los hábitos pendientes para hoy"""
        agenda = self.generar_agenda_diaria()
        return [item['habito'] for item in agenda['habitos'] if not item['completado']]
    
    def generar_recordatorios(self) -> str:
        """Genera recordatorios y alertas para el usuario"""
        habitos_pendientes = self.obtener_habitos_pendientes_hoy()
        return self.generador_mensajes.generar_alerta_habitos_pendientes(habitos_pendientes)
    
    # ===== REPORTES Y ESTADÍSTICAS =====
    
    def obtener_progreso_habito(self, habito_id: int) -> Dict[str, any]:
        """Obtiene el progreso completo de un hábito"""
        habito = self.habito_dao.obtener_habito(habito_id)
        if not habito:
            return None
        
        estadisticas = self.calculadora_progreso.calcular_estadisticas_generales(habito)
        progreso_semanal = self.calculadora_progreso.calcular_progreso_semanal(habito)
        progreso_mensual = self.calculadora_progreso.calcular_progreso_mensual(habito)
        
        return {
            'habito': habito,
            'estadisticas_generales': estadisticas,
            'progreso_semanal': progreso_semanal,
            'progreso_mensual': progreso_mensual,
            'recomendacion': self.generador_mensajes.generar_recomendacion_mejora(habito, estadisticas['porcentaje_exito'])
        }
    
    def obtener_resumen_general(self) -> Dict[str, any]:
        """Obtiene un resumen general de todos los hábitos"""
        habitos = self.obtener_habitos_activos()
        
        if not habitos:
            return {
                'total_habitos': 0,
                'mensaje': "No tienes hábitos registrados. ¡Comienza agregando uno! 🌟"
            }
        
        # Calcular estadísticas generales
        total_habitos = len(habitos)
        habitos_con_progreso = []
        
        for habito in habitos:
            estadisticas = self.calculadora_progreso.calcular_estadisticas_generales(habito)
            habitos_con_progreso.append({
                'habito': habito,
                'porcentaje_exito': estadisticas['porcentaje_exito'],
                'racha_actual': estadisticas['racha_actual']
            })
        
        # Ordenar por porcentaje de éxito
        habitos_con_progreso.sort(key=lambda x: x['porcentaje_exito'], reverse=True)
        
        # Obtener resumen del día
        resumen_diario = self.calculadora_progreso.obtener_resumen_diario()
        
        # Mensaje semanal
        mensaje_semanal = self.generador_mensajes.generar_mensaje_resumen_semanal(habitos)
        
        return {
            'total_habitos': total_habitos,
            'resumen_diario': resumen_diario,
            'habitos_ranking': habitos_con_progreso[:5],  # Top 5
            'mensaje_semanal': mensaje_semanal,
            'consejo_del_dia': self.generador_mensajes.obtener_consejo_del_dia()
        }
    
    def obtener_historial_habito(self, habito_id: int, dias: int = 30) -> List[Dict[str, any]]:
        """Obtiene el historial de cumplimiento de un hábito"""
        habito = self.habito_dao.obtener_habito(habito_id)
        if not habito:
            return []
        
        fecha_fin = date.today()
        fecha_inicio = fecha_fin - timedelta(days=dias)
        
        registros = self.registro_dao.obtener_registros_por_periodo(fecha_inicio, fecha_fin)
        registros_habito = [r for r in registros if r.habito_id == habito_id]
        
        # Crear historial día por día
        historial = []
        fecha_actual = fecha_inicio
        
        while fecha_actual <= fecha_fin:
            registro_dia = next((r for r in registros_habito if r.fecha.date() == fecha_actual), None)
            
            item = {
                'fecha': fecha_actual.strftime('%d/%m/%Y'),
                'completado': registro_dia.completado if registro_dia else False,
                'nota': registro_dia.nota if registro_dia else None
            }
            
            historial.append(item)
            fecha_actual += timedelta(days=1)
        
        return historial
    
    # ===== MENSAJES Y MOTIVACIÓN =====
    
    def obtener_mensaje_bienvenida(self) -> str:
        """Obtiene un mensaje de bienvenida personalizado"""
        habitos = self.obtener_habitos_activos()
        return self.generador_mensajes.generar_mensaje_diario(habitos)

