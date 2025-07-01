import random
from datetime import date, timedelta
from typing import List, Dict
from models.habito import Habito

class GeneradorMensajes:
    """Clase para generar mensajes motivacionales y alertas"""
    
    def __init__(self):
        self.calculadora = None  # Se inicializará en lazy loading
        
        # Mensajes motivacionales por categoría
        self.mensajes_motivacion = {
            'inicio': [
                "¡Es un gran día para formar nuevos hábitos! 🌟",
                "Cada pequeño paso cuenta hacia tu objetivo 💪",
                "¡Tú puedes! Hoy es el día perfecto para empezar 🚀",
                "Los grandes cambios empiezan con pequeñas acciones ✨",
                "¡Confía en el proceso y sé constante! 🎯"
            ],
            'progreso': [
                "¡Excelente progreso! Sigues en el camino correcto 🔥",
                "¡Vas muy bien! Tu constancia está dando frutos 🌱",
                "¡Increíble! Cada día te acercas más a tu meta 🏆",
                "Tu dedicación es admirable, ¡sigue así! ⭐",
                "¡Fantástico! Estás construyendo hábitos sólidos 🏗️"
            ],
            'racha': [
                "¡Qué racha tan impresionante! 🔥🔥🔥",
                "¡Imparable! Tu constancia es inspiradora 💫",
                "¡Eres una máquina de hábitos! 🤖",
                "¡Esta racha es épica! No te detengas 🚀",
                "¡Wow! Tu disciplina es de otro nivel 👑"
            ],
            'completado': [
                "¡Hábito completado! Un paso más hacia el éxito ✅",
                "¡Misión cumplida! Te sientes genial, ¿verdad? 😊",
                "¡Perfecto! Otro día más de crecimiento personal 🌿",
                "¡Bien hecho! Tu yo del futuro te lo agradecerá 🙏",
                "¡Excelente! Cada día eres una mejor versión de ti 💎"
            ],
            'alerta_suave': [
                "Hey, ¿qué tal si revisamos tus hábitos pendientes? 🤔",
                "Recuerda: la constancia es la clave del éxito 🗝️",
                "¡No olvides tus hábitos de hoy! Aún hay tiempo ⏰",
                "Un pequeño esfuerzo hoy, grandes resultados mañana 📈",
                "¿Lista/o para continuar con tus hábitos? 💪"
            ],
            'alerta_fuerte': [
                "⚠️ ¡Alerta! Tienes hábitos pendientes importantes",
                "🚨 No dejes que la pereza gane. ¡Tú eres más fuerte!",
                "⚡ ¡Es momento de actuar! Tus hábitos te esperan",
                "🔔 Recordatorio: Tu futuro depende de las acciones de hoy",
                "📢 ¡No rompas tu racha! Completa tus hábitos"
            ]
        }
        
        self.mensajes_metas = {
            'semanal_alcanzada': [
                "🎉 ¡Meta semanal alcanzada! ¡Eres increíble!",
                "🏆 ¡Semana perfecta! Tu dedicación es admirable",
                "⭐ ¡Objetivo semanal completado! ¡Celebra este logro!",
                "🎊 ¡Qué semana tan productiva! Sigues creciendo",
                "💪 ¡Meta semanal conseguida! Eres imparable"
            ],
            'mensual_alcanzada': [
                "🎆 ¡META MENSUAL COMPLETADA! ¡Eres una estrella!",
                "👑 ¡Un mes perfecto! Tu constancia es legendaria",
                "🌟 ¡Objetivo mensual logrado! ¡Qué disciplina!",
                "🎁 ¡Mes completado! Te mereces una recompensa",
                "🚀 ¡Meta mensual alcanzada! Rumbo al siguiente nivel"
            ]
        }

    def obtener_mensaje_motivacional(self, categoria: str = 'inicio') -> str:
        """Obtiene un mensaje motivacional aleatorio de una categoría"""
        if categoria in self.mensajes_motivacion:
            return random.choice(self.mensajes_motivacion[categoria])
        return random.choice(self.mensajes_motivacion['inicio'])
    
    def generar_mensaje_diario(self, habitos: List[Habito]) -> str:
        """Genera un mensaje motivacional para comenzar el día"""
        if not habitos:
            return "¡Buen día! Considera agregar algunos hábitos para mejorar tu día a día 🌞"
        
        # Por ahora generar mensaje básico, se mejorará con más lógica
        return self.obtener_mensaje_motivacional('inicio')
    
    def generar_mensaje_habito_completado(self, habito: Habito, racha: int = 0) -> str:
        """Genera un mensaje cuando se completa un hábito"""
        mensaje_base = self.obtener_mensaje_motivacional('completado')
        
        if racha >= 7:
            mensaje_racha = self.obtener_mensaje_motivacional('racha')
            return f"{mensaje_base}\n{mensaje_racha} (Racha: {racha} días)"
        elif racha >= 3:
            return f"{mensaje_base}\n¡Llevas {racha} días seguidos! 🔥"
        else:
            return mensaje_base
    
    def generar_alerta_habitos_pendientes(self, habitos_pendientes: List[Habito]) -> str:
        """Genera alertas para hábitos pendientes"""
        if not habitos_pendientes:
            return "¡Perfecto! No tienes hábitos pendientes 🎉"
        
        cantidad = len(habitos_pendientes)
        
        if cantidad == 1:
            habito = habitos_pendientes[0]
            return f"{self.obtener_mensaje_motivacional('alerta_suave')}\n📝 Pendiente: {habito.nombre}"
        elif cantidad <= 3:
            mensaje = self.obtener_mensaje_motivacional('alerta_suave')
            lista_habitos = "\n".join([f"📝 {h.nombre}" for h in habitos_pendientes])
            return f"{mensaje}\n\nHábitos pendientes:\n{lista_habitos}"
        else:
            mensaje = self.obtener_mensaje_motivacional('alerta_fuerte')
            return f"{mensaje}\n\n¡Tienes {cantidad} hábitos pendientes! Es momento de actuar 💪"
    
    def generar_mensaje_meta_alcanzada(self, habito: Habito, tipo_meta: str, completados: int = 0, objetivo: int = 0, porcentaje: float = 0) -> str:
        """Genera mensaje cuando se alcanza una meta semanal o mensual"""
        if tipo_meta == 'semanal':
            mensaje = random.choice(self.mensajes_metas['semanal_alcanzada'])
        else:  # mensual
            mensaje = random.choice(self.mensajes_metas['mensual_alcanzada'])
        
        return f"{mensaje}\n\n📊 {habito.nombre}\n✅ {completados}/{objetivo} ({porcentaje:.0f}%)"
    
    def generar_recomendacion_mejora(self, habito: Habito, porcentaje_exito: float = 0) -> str:
        """Genera recomendaciones basadas en el desempeño"""
        if porcentaje_exito >= 80:
            return f"🌟 ¡Excelente trabajo con '{habito.nombre}'! Tu tasa de éxito es del {porcentaje_exito:.0f}%. ¡Mantén ese ritmo!"
        elif porcentaje_exito >= 60:
            return f"👍 Buen progreso con '{habito.nombre}' ({porcentaje_exito:.0f}% de éxito). ¡Puedes llegar al 80%!"
        elif porcentaje_exito >= 40:
            return f"💡 Sugerencia para '{habito.nombre}': Intenta asociarlo con otro hábito que ya tengas establecido."
        else:
            return f"🎯 Enfócate en '{habito.nombre}': Empieza con sesiones más cortas o cambia el horario para mayor consistencia."
    
    def generar_mensaje_resumen_semanal(self, habitos: List[Habito], metas_alcanzadas: int = 0, total_metas: int = 0) -> str:
        """Genera un resumen motivacional semanal"""
        if not habitos:
            return "¡Considera agregar algunos hábitos para la próxima semana! 📝"
        
        # Si no se proporcionan datos, usar valores por defecto
        if total_metas == 0:
            total_metas = len(habitos)
            metas_alcanzadas = max(0, int(total_metas * 0.7))  # Asumir 70% de éxito
        
        porcentaje_general = (metas_alcanzadas / total_metas * 100) if total_metas > 0 else 0
        
        if porcentaje_general >= 80:
            emoji = "🎉"
            mensaje = "¡Semana espectacular!"
        elif porcentaje_general >= 60:
            emoji = "👏"
            mensaje = "¡Buena semana!"
        elif porcentaje_general >= 40:
            emoji = "💪"
            mensaje = "Semana con progreso"
        else:
            emoji = "🎯"
            mensaje = "La próxima semana será mejor"
        
        return f"{emoji} {mensaje}\n\n📊 Resumen semanal:\n✅ {metas_alcanzadas}/{total_metas} metas alcanzadas\n📈 {porcentaje_general:.0f}% de éxito general"
    
    def obtener_consejo_del_dia(self) -> str:
        """Obtiene un consejo motivacional del día"""
        consejos = [
            "💡 Consejo del día: La constancia vence al talento cuando el talento no es constante.",
            "🧠 Recuerda: Los hábitos son como músculos, se fortalecen con el uso diario.",
            "⚡ Tip: Si un hábito te parece difícil, hazlo más pequeño, no lo abandones.",
            "🎯 Enfoque: Es mejor hacer un hábito imperfectamente que no hacerlo en absoluto.",
            "🌱 Crecimiento: Cada día que practicas un hábito, tu cerebro se adapta un poco más.",
            "🔥 Motivación: No necesitas motivación para empezar, necesitas disciplina para continuar.",
            "📈 Progreso: Los pequeños cambios diarios llevan a grandes transformaciones.",
            "🎊 Celebra: Reconoce cada pequeña victoria en tu camino hacia el cambio.",
            "⏰ Tiempo: El mejor momento para plantar un árbol fue hace 20 años. El segundo mejor momento es ahora.",
            "💪 Fortaleza: Tu yo del futuro te agradecerá los esfuerzos que haces hoy."
        ]
        
        return random.choice(consejos)

