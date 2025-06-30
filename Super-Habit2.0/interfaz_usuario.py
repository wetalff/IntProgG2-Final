import os
import sys
from datetime import datetime, date, time
from typing import Optional
from gestor_superhabit import GestorSuperHabit

class InterfazUsuario:
    """Interfaz de usuario para la aplicación SuperHábit"""
    
    def __init__(self):
        self.gestor = GestorSuperHabit()
        self.ejecutando = True
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausar(self):
        """Pausa la ejecución hasta que el usuario presione Enter"""
        input("\nPresiona Enter para continuar...")
    
    def _solicitar_opcion_menu(self, mensaje: str, min_opcion: int, max_opcion: int) -> str:
        """Solicita una opción del menú con validación"""
        while True:
            try:
                opcion = input(mensaje).strip()
                if not opcion:
                    print("⚠️ Por favor, ingresa una opción válida.")
                    continue
                
                opcion_num = int(opcion)
                if min_opcion <= opcion_num <= max_opcion:
                    return str(opcion_num)
                else:
                    print(f"⚠️ Por favor, ingresa un número entre {min_opcion} y {max_opcion}.")
                    
            except ValueError:
                print("⚠️ Por favor, ingresa un número válido.")
    
    def _solicitar_numero_entero(self, mensaje: str, minimo: int = None, maximo: int = None) -> int:
        """Solicita un número entero con validación"""
        while True:
            try:
                valor = input(mensaje).strip()
                if not valor:
                    print("⚠️ Por favor, ingresa un valor.")
                    continue
                
                numero = int(valor)
                
                if minimo is not None and numero < minimo:
                    print(f"⚠️ El valor debe ser mayor o igual a {minimo}.")
                    continue
                    
                if maximo is not None and numero > maximo:
                    print(f"⚠️ El valor debe ser menor o igual a {maximo}.")
                    continue
                    
                return numero
                
            except ValueError:
                print("⚠️ Por favor, ingresa un número válido.")
    
    def _solicitar_texto_no_vacio(self, mensaje: str) -> str:
        """Solicita un texto que no esté vacío"""
        while True:
            texto = input(mensaje).strip()
            if texto:
                return texto
            print("⚠️ Este campo no puede estar vacío. Por favor, ingresa un valor.")
    
    def mostrar_titulo(self, titulo: str):
        """Muestra un título formateado"""
        print("\n" + "="*50)
        print(f"  {titulo}")
        print("="*50)
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        self.limpiar_pantalla()
        print("🌟" * 20)
        print("    💪 SUPERHÁBIT - Tu Compañero de Hábitos 💪")
        print("🌟" * 20)
        
        # Mostrar mensaje de bienvenida
        mensaje_bienvenida = self.gestor.obtener_mensaje_bienvenida()
        print(f"\n🌅 {mensaje_bienvenida}")
        
        print("\n🗺️ MENÚ PRINCIPAL:")
        print("\n1. 📅 Ver agenda de hoy")
        print("2. ➕ Agregar nuevo hábito")
        print("3. ✅ Marcar hábito como completado")
        print("4. 📈 Ver progreso de hábitos")
        print("5. 📊 Ver resumen general")
        print("6. ⚙️ Gestionar hábitos")
        print("7. 📁 Ver historial")
        print("8. 📢 Ver recordatorios")
        print("9. 🚪 Salir")
        
        return self._solicitar_opcion_menu("🎯 Selecciona una opción (1-9): ", 1, 9)
    
    def ejecutar(self):
        """Ejecuta la aplicación principal"""
        while self.ejecutando:
            try:
                opcion = self.mostrar_menu_principal()
                
                if opcion == '1':
                    self.mostrar_agenda_hoy()
                elif opcion == '2':
                    self.agregar_habito()
                elif opcion == '3':
                    self.marcar_habito_completado()
                elif opcion == '4':
                    self.mostrar_progreso_habitos()
                elif opcion == '5':
                    self.mostrar_resumen_general()
                elif opcion == '6':
                    self.gestionar_habitos()
                elif opcion == '7':
                    self.mostrar_historial()
                elif opcion == '8':
                    self.mostrar_recordatorios()
                elif opcion == '9':
                    self.salir()
                else:
                    print("⚠️ Opción no válida. Por favor, selecciona una opción del 1 al 9.")
                    self.pausar()
                    
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n⚠️ Error inesperado: {e}")
                self.pausar()
    
    def mostrar_agenda_hoy(self):
        """Muestra la agenda del día actual"""
        self.limpiar_pantalla()
        self.mostrar_titulo("📅 AGENDA DE HOY")
        
        agenda = self.gestor.generar_agenda_diaria()
        
        print(f"\n📆 Fecha: {agenda['fecha']}")
        
        if not agenda['habitos']:
            print("\n🎆 ¡No tienes hábitos programados para hoy!")
            print("💡 Considera agregar algunos hábitos para empezar tu jornada de crecimiento personal.")
        else:
            print(f"\n📊 Resumen: {agenda['resumen']['completados']}/{agenda['resumen']['total']} hábitos completados ({agenda['resumen']['porcentaje']:.0f}%)")
            
            print("\n🗺️ HÁBITOS DEL DÍA:")
            print("-" * 60)
            
            for i, item in enumerate(agenda['habitos'], 1):
                habito = item['habito']
                estado = "✅" if item['completado'] else "❌"
                horario = f" a las {item['horario_sugerido']}" if item['horario_sugerido'] else ""
                racha = f" (🔥 Racha: {item['racha_actual']} días)" if item['racha_actual'] > 0 else ""
                
                print(f"{i}. {estado} {habito.nombre}")
                print(f"   ⏱️ {item['duracion']} minutos{horario}{racha}")
                print(f"   🔄 Frecuencia: {habito.frecuencia.capitalize()}")
                print()
        
        self.pausar()
    
    def agregar_habito(self):
        """Permite agregar un nuevo hábito"""
        self.limpiar_pantalla()
        self.mostrar_titulo("➕ AGREGAR NUEVO HÁBITO")
        
        try:
            print("📝 Complete la información del nuevo hábito:\n")
            
            # Solicitar nombre con validación
            nombre = self._solicitar_texto_no_vacio("🏷️ Nombre del hábito: ")
            
            # Solicitar frecuencia con validación
            print("\n🔄 Frecuencia:")
            print("1. Diaria")
            print("2. Semanal")
            opcion_freq = self._solicitar_opcion_menu("Selecciona (1-2): ", 1, 2)
            
            if opcion_freq == '1':
                frecuencia = 'diaria'
            else:  # opcion_freq == '2'
                frecuencia = 'semanal'
            
            # Solicitar duración con validación
            duracion = self._solicitar_numero_entero("\n⏱️ Duración estimada (en minutos): ", minimo=1, maximo=1440)
            
            # Solicitar horario sugerido (opcional)
            horario = self._solicitar_horario_mejorado()
            
            # Crear hábito
            habito = self.gestor.crear_habito(nombre, frecuencia, duracion, horario if horario else None)
            
            print(f"\n✨ ¡Hábito '{habito.nombre}' creado exitosamente!")
            print(f"🔄 Frecuencia: {habito.frecuencia.capitalize()}")
            print(f"⏱️ Duración: {habito.duracion} minutos")
            if habito.horario_sugerido:
                print(f"🕰️ Horario sugerido: {habito.horario_sugerido.strftime('%H:%M')}")
            
            print("\n💪 ¡Es hora de empezar a construir este hábito!")
            
        except ValueError as e:
            print(f"\n⚠️ Error: {e}")
        
        self.pausar()
    
    def _validar_horario(self, horario: str) -> bool:
        """Valida el formato de horario HH:MM"""
        try:
            partes = horario.split(':')
            if len(partes) != 2:
                return False
            hora, minuto = int(partes[0]), int(partes[1])
            return 0 <= hora <= 23 and 0 <= minuto <= 59
        except ValueError:
            return False
    
    def _solicitar_horario(self) -> str:
        """Solicita horario con opción de AM/PM"""
        print("\n🕰️ Horario sugerido (opcional):")
        print("1. Usar formato 24 horas (HH:MM, ej: 14:30)")
        print("2. Usar formato 12 horas con AM/PM (ej: 2:30 PM)")
        print("3. No especificar horario")
        
        opcion = input("Selecciona una opción (1-3): ").strip()
        
        if opcion == '1':
            horario = input("Ingresa el horario (HH:MM): ").strip()
            if horario and not self._validar_horario(horario):
                print("⚠️ Formato de horario inválido. Usa HH:MM (ej: 08:30)")
                return False
            return horario
        
        elif opcion == '2':
            return self._solicitar_horario_12h()
        
        elif opcion == '3':
            return ""
        
        else:
            print("⚠️ Opción no válida.")
            return False
    
    def _solicitar_horario_12h(self) -> str:
        """Solicita horario en formato 12 horas con AM/PM"""
        try:
            hora = int(input("Hora (1-12): "))
            if not (1 <= hora <= 12):
                print("⚠️ La hora debe estar entre 1 y 12.")
                return False
            
            minuto = int(input("Minutos (0-59): "))
            if not (0 <= minuto <= 59):
                print("⚠️ Los minutos deben estar entre 0 y 59.")
                return False
            
            print("AM o PM:")
            print("1. AM")
            print("2. PM")
            opcion_ampm = input("Selecciona (1-2): ").strip()
            
            if opcion_ampm == '1':
                periodo = 'AM'
            elif opcion_ampm == '2':
                periodo = 'PM'
            else:
                print("⚠️ Opción no válida.")
                return False
            
            # Convertir a formato 24 horas
            if periodo == 'AM':
                if hora == 12:
                    hora_24 = 0
                else:
                    hora_24 = hora
            else:  # PM
                if hora == 12:
                    hora_24 = 12
                else:
                    hora_24 = hora + 12
            
            return f"{hora_24:02d}:{minuto:02d}"
            
        except ValueError:
            print("⚠️ Ingresa números válidos.")
            return False
    
    def _solicitar_horario_mejorado(self) -> str:
        """Solicita horario con validación mejorada"""
        print("\n🕰️ Horario sugerido (opcional):")
        print("1. Usar formato 24 horas (HH:MM, ej: 14:30)")
        print("2. Usar formato 12 horas con AM/PM (ej: 2:30 PM)")
        print("3. No especificar horario")
        
        opcion = self._solicitar_opcion_menu("Selecciona una opción (1-3): ", 1, 3)
        
        if opcion == '1':
            while True:
                horario = input("Ingresa el horario (HH:MM): ").strip()
                if not horario:
                    return ""
                if self._validar_horario(horario):
                    return horario
                print("⚠️ Formato de horario inválido. Usa HH:MM (ej: 08:30)")
        
        elif opcion == '2':
            while True:
                resultado = self._solicitar_horario_12h()
                if resultado is not False:
                    return resultado
                print("⚠️ Intenta nuevamente.")
        
        else:  # opcion == '3'
            return ""
    
    def marcar_habito_completado(self):
        """Permite marcar un hábito como completado"""
        self.limpiar_pantalla()
        self.mostrar_titulo("✅ MARCAR HÁBITO COMPLETADO")
        
        habitos_pendientes = self.gestor.obtener_habitos_pendientes_hoy()
        
        if not habitos_pendientes:
            print("\n🎉 ¡Felicitaciones! No tienes hábitos pendientes para hoy.")
            print("🎆 ¡Has completado todos tus hábitos del día!")
            self.pausar()
            return
        
        print("\n🗺️ HÁBITOS PENDIENTES PARA HOY:")
        print("-" * 40)
        
        for i, habito in enumerate(habitos_pendientes, 1):
            horario = f" (sugerido: {habito.horario_sugerido.strftime('%H:%M')})" if habito.horario_sugerido else ""
            print(f"{i}. {habito.nombre} - {habito.duracion} min{horario}")
        
        # Usar validación mejorada
        opcion = self._solicitar_opcion_menu(f"\n🎯 Selecciona el hábito a completar (1-{len(habitos_pendientes)}): ", 1, len(habitos_pendientes))
        
        habito_seleccionado = habitos_pendientes[int(opcion) - 1]
        
        # Solicitar nota opcional
        nota = input("\n📝 Agregar nota (opcional): ").strip()
        nota = nota if nota else None
        
        # Marcar como completado
        mensaje = self.gestor.marcar_habito_completado(habito_seleccionado.id, nota=nota)
        
        print(f"\n{mensaje}")
        
        self.pausar()
    
    def mostrar_progreso_habitos(self):
        """Muestra el progreso de todos los hábitos"""
        self.limpiar_pantalla()
        self.mostrar_titulo("📈 PROGRESO DE HÁBITOS")
        
        habitos = self.gestor.obtener_habitos_activos()
        
        if not habitos:
            print("\n💭 No tienes hábitos registrados aún.")
            print("💡 ¡Agrega tu primer hábito para empezar a ver tu progreso!")
            self.pausar()
            return
        
        print("\n🗺️ Selecciona un hábito para ver su progreso detallado:")
        print("-" * 50)
        
        for i, habito in enumerate(habitos, 1):
            estadisticas = self.gestor.calculadora_progreso.calcular_estadisticas_generales(habito)
            print(f"{i}. {habito.nombre} - Éxito: {estadisticas['porcentaje_exito']:.0f}% - Racha: {estadisticas['racha_actual']} días")
        
        print(f"{len(habitos) + 1}. Volver al menú principal")
        
        opcion = self._solicitar_opcion_menu(f"\n🎯 Selecciona una opción (1-{len(habitos) + 1}): ", 1, len(habitos) + 1)
        
        if 1 <= int(opcion) <= len(habitos):
            self.mostrar_progreso_detallado(habitos[int(opcion) - 1].id)
        else:  # opcion == len(habitos) + 1
            return
    
    def mostrar_progreso_detallado(self, habito_id: int):
        """Muestra el progreso detallado de un hábito específico"""
        self.limpiar_pantalla()
        
        progreso = self.gestor.obtener_progreso_habito(habito_id)
        if not progreso:
            print("⚠️ Hábito no encontrado.")
            self.pausar()
            return
        
        habito = progreso['habito']
        stats = progreso['estadisticas_generales']
        semanal = progreso['progreso_semanal']
        mensual = progreso['progreso_mensual']
        
        self.mostrar_titulo(f"📈 PROGRESO DETALLADO: {habito.nombre.upper()}")
        
        print(f"\n🏷️ Información del hábito:")
        print(f"   🔄 Frecuencia: {habito.frecuencia.capitalize()}")
        print(f"   ⏱️ Duración: {habito.duracion} minutos")
        if habito.horario_sugerido:
            print(f"   🕰️ Horario sugerido: {habito.horario_sugerido.strftime('%H:%M')}")
        print(f"   📅 Creado: {stats['fecha_creacion']}")
        
        print(f"\n📊 Estadísticas generales:")
        print(f"   📈 Tasa de éxito: {stats['porcentaje_exito']:.1f}%")
        print(f"   📅 Total de días: {stats['total_dias']}")
        print(f"   ✅ Días completados: {stats['dias_completados']}")
        print(f"   🔥 Racha actual: {stats['racha_actual']} días")
        print(f"   🏆 Racha máxima: {stats['racha_maxima']} días")
        
        print(f"\n📅 Progreso semanal ({semanal['periodo']}):")
        self._mostrar_barra_progreso(semanal['porcentaje'])
        print(f"   ✅ {semanal['completados']}/{semanal['objetivo']} objetivos alcanzados")
        
        print(f"\n📆 Progreso mensual ({mensual['periodo']}):")
        self._mostrar_barra_progreso(mensual['porcentaje'])
        print(f"   ✅ {mensual['completados']}/{mensual['objetivo']} objetivos alcanzados")
        
        print(f"\n💡 Recomendación:")
        print(f"   {progreso['recomendacion']}")
        
        self.pausar()
    
    def _mostrar_barra_progreso(self, porcentaje: float):
        """Muestra una barra de progreso visual"""
        ancho_barra = 30
        progreso_completo = int((porcentaje / 100) * ancho_barra)
        progreso_incompleto = ancho_barra - progreso_completo
        
        barra = "█" * progreso_completo + "░" * progreso_incompleto
        print(f"   [{barra}] {porcentaje:.1f}%")
    
    def mostrar_resumen_general(self):
        """Muestra un resumen general de todos los hábitos"""
        self.limpiar_pantalla()
        self.mostrar_titulo("📊 RESUMEN GENERAL")
        
        resumen = self.gestor.obtener_resumen_general()
        
        if resumen['total_habitos'] == 0:
            print(f"\n{resumen['mensaje']}")
            self.pausar()
            return
        
        print(f"\n📊 Total de hábitos activos: {resumen['total_habitos']}")
        
        # Resumen del día
        diario = resumen['resumen_diario']
        print(f"\n📅 Resumen de hoy ({diario['fecha']}):")
        if diario['total_habitos'] > 0:
            self._mostrar_barra_progreso(diario['porcentaje'])
            print(f"   ✅ Completados: {diario['completados']}")
            print(f"   ⏳ Pendientes: {diario['pendientes']}")
        else:
            print("   💭 No hay hábitos programados para hoy")
        
        # Top 5 hábitos
        if resumen['habitos_ranking']:
            print(f"\n🏆 Top 5 hábitos (por tasa de éxito):")
            for i, item in enumerate(resumen['habitos_ranking'], 1):
                habito = item['habito']
                print(f"   {i}. {habito.nombre} - {item['porcentaje_exito']:.0f}% (🔥 {item['racha_actual']} días)")
        
        # Mensaje semanal
        print(f"\n{resumen['mensaje_semanal']}")
        
        # Consejo del día
        print(f"\n{resumen['consejo_del_dia']}")
        
        self.pausar()
    
    def gestionar_habitos(self):
        """Menú para gestionar hábitos existentes"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_titulo("⚙️ GESTIONAR HÁBITOS")
            
            habitos = self.gestor.obtener_habitos_activos()
            
            if not habitos:
                print("\n💭 No tienes hábitos registrados aún.")
                print("💡 ¡Agrega tu primer hábito desde el menú principal!")
                self.pausar()
                return
            
            print("\n🗺️ HÁBITOS ACTIVOS:")
            print("-" * 50)
            
            for i, habito in enumerate(habitos, 1):
                horario = f" a las {habito.horario_sugerido.strftime('%H:%M')}" if habito.horario_sugerido else ""
                print(f"{i}. {habito.nombre} ({habito.frecuencia}, {habito.duracion} min{horario})")
            
            print(f"\n{len(habitos) + 1}. Volver al menú principal")
            
            opcion = self._solicitar_opcion_menu(f"\n🎯 Selecciona un hábito para gestionar (1-{len(habitos) + 1}): ", 1, len(habitos) + 1)
            
            if 1 <= int(opcion) <= len(habitos):
                self.gestionar_habito_individual(habitos[int(opcion) - 1])
            else:  # opcion == len(habitos) + 1
                return
    
    def gestionar_habito_individual(self, habito):
        """Gestiona un hábito individual"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_titulo(f"⚙️ GESTIONAR: {habito.nombre.upper()}")
            
            print(f"\n🏷️ Información actual:")
            print(f"   Nombre: {habito.nombre}")
            print(f"   Frecuencia: {habito.frecuencia.capitalize()}")
            print(f"   Duración: {habito.duracion} minutos")
            print(f"   Horario: {habito.horario_sugerido.strftime('%H:%M') if habito.horario_sugerido else 'No definido'}")
            
            print("\n🗺️ Opciones:")
            print("1. ✏️ Editar hábito")
            print("2. ⏸️ Desactivar hábito")
            print("3. 🗑️ Eliminar hábito permanentemente")
            print("4. ⬅️ Volver")
            
            opcion = self._solicitar_opcion_menu("\n🎯 Selecciona una opción (1-4): ", 1, 4)
            
            if opcion == '1':
                self.editar_habito(habito)
                break
            elif opcion == '2':
                if self.confirmar_accion(f"desactivar el hábito '{habito.nombre}'"):
                    if self.gestor.desactivar_habito(habito.id):
                        print(f"\n✅ Hábito '{habito.nombre}' desactivado exitosamente.")
                    else:
                        print(f"\n⚠️ Error al desactivar el hábito.")
                    self.pausar()
                break
            elif opcion == '3':
                if self.confirmar_accion(f"eliminar PERMANENTEMENTE el hábito '{habito.nombre}'"):
                    if self.gestor.eliminar_habito(habito.id):
                        print(f"\n✅ Hábito '{habito.nombre}' eliminado permanentemente.")
                    else:
                        print(f"\n⚠️ Error al eliminar el hábito.")
                    self.pausar()
                break
            elif opcion == '4':
                break
            else:
                print("⚠️ Opción no válida.")
                self.pausar()
    
    def editar_habito(self, habito):
        """Permite editar un hábito existente"""
        self.limpiar_pantalla()
        self.mostrar_titulo(f"✏️ EDITAR HÁBITO: {habito.nombre.upper()}")
        
        print("\n📝 Deja en blanco para mantener el valor actual\n")
        
        try:
            # Editar nombre
            nuevo_nombre = input(f"Nuevo nombre [{habito.nombre}]: ").strip()
            
            # Editar frecuencia
            print(f"\nFrecuencia actual: {habito.frecuencia.capitalize()}")
            print("1. Diaria")
            print("2. Semanal")
            print("3. Mantener actual")
            opcion_freq = input("Selecciona (1-3): ").strip()
            
            nueva_frecuencia = None
            if opcion_freq == '1':
                nueva_frecuencia = 'diaria'
            elif opcion_freq == '2':
                nueva_frecuencia = 'semanal'
            
            # Editar duración
            nueva_duracion_str = input(f"Nueva duración en minutos [{habito.duracion}]: ").strip()
            nueva_duracion = None
            if nueva_duracion_str:
                try:
                    nueva_duracion = int(nueva_duracion_str)
                    if nueva_duracion <= 0:
                        print("⚠️ La duración debe ser mayor a 0.")
                        self.pausar()
                        return
                except ValueError:
                    print("⚠️ Ingresa un número válido.")
                    self.pausar()
                    return
            
            # Editar horario
            horario_actual = habito.horario_sugerido.strftime('%H:%M') if habito.horario_sugerido else 'No definido'
            nuevo_horario = input(f"Nuevo horario sugerido [{horario_actual}]: ").strip()
            
            if nuevo_horario and not self._validar_horario(nuevo_horario):
                print("⚠️ Formato de horario inválido. Usa HH:MM (ej: 08:30)")
                self.pausar()
                return
            
            # Aplicar cambios
            if self.gestor.actualizar_habito(
                habito.id,
                nombre=nuevo_nombre if nuevo_nombre else None,
                frecuencia=nueva_frecuencia,
                duracion=nueva_duracion,
                horario_sugerido=nuevo_horario if nuevo_horario else None
            ):
                print(f"\n✅ Hábito actualizado exitosamente!")
            else:
                print(f"\n⚠️ Error al actualizar el hábito.")
            
        except ValueError as e:
            print(f"\n⚠️ Error: {e}")
        
        self.pausar()
    
    def confirmar_accion(self, accion: str) -> bool:
        """Solicita confirmación para una acción"""
        respuesta = input(f"\n⚠️ ¿Estás seguro de que quieres {accion}? (s/N): ").strip().lower()
        return respuesta in ['s', 'si', 'sí', 'yes', 'y']
    
    def mostrar_historial(self):
        """Muestra el historial de cumplimiento"""
        self.limpiar_pantalla()
        self.mostrar_titulo("📁 HISTORIAL DE CUMPLIMIENTO")
        
        habitos = self.gestor.obtener_habitos_activos()
        
        if not habitos:
            print("\n💭 No tienes hábitos registrados aún.")
            self.pausar()
            return
        
        print("\n🗺️ Selecciona un hábito para ver su historial:")
        print("-" * 40)
        
        for i, habito in enumerate(habitos, 1):
            print(f"{i}. {habito.nombre}")
        
        print(f"{len(habitos) + 1}. Volver al menú principal")
        
        opcion = self._solicitar_opcion_menu(f"\n🎯 Selecciona una opción (1-{len(habitos) + 1}): ", 1, len(habitos) + 1)
        
        if 1 <= int(opcion) <= len(habitos):
            self.mostrar_historial_habito(habitos[int(opcion) - 1])
        else:  # opcion == len(habitos) + 1
            return
    
    def mostrar_historial_habito(self, habito):
        """Muestra el historial de un hábito específico con opciones mejoradas"""
        self.limpiar_pantalla()
        self.mostrar_titulo(f"📁 HISTORIAL: {habito.nombre.upper()}")
        
        print("\n📊 Selecciona el período de historial:")
        print("1. Últimos 7 días")
        print("2. Últimos 30 días")
        print("3. Últimos 90 días")
        print("4. Todo el historial")
        print("5. Período personalizado")
        
        opcion = self._solicitar_opcion_menu("\nSelecciona una opción (1-5): ", 1, 5)
        
        if opcion == '1':
            dias = 7
        elif opcion == '2':
            dias = 30
        elif opcion == '3':
            dias = 90
        elif opcion == '4':
            dias = 365  # Un año como máximo
        else:  # opcion == '5'
            dias = self._solicitar_numero_entero("\n📅 ¿Cuántos días mostrar?: ", minimo=1, maximo=365)
        
        historial = self.gestor.obtener_historial_habito(habito.id, dias)
        
        if not historial:
            print("\n💭 No hay historial disponible para este hábito.")
            self.pausar()
            return
        
        # Calcular estadísticas detalladas
        completados = sum(1 for dia in historial if dia['completado'])
        total = len(historial)
        porcentaje = (completados / total * 100) if total > 0 else 0
        
        # Calcular racha actual y máxima
        racha_actual = 0
        racha_maxima = 0
        racha_temp = 0
        
        for dia in reversed(historial):
            if dia['completado']:
                racha_temp += 1
                if racha_actual == 0:  # Solo contar la racha actual desde el final
                    racha_actual = racha_temp
            else:
                if racha_temp > racha_maxima:
                    racha_maxima = racha_temp
                racha_temp = 0
                if racha_actual == 0:  # Si no hay racha actual, seguir buscando
                    pass
                else:
                    break  # Ya encontramos la racha actual
        
        if racha_temp > racha_maxima:
            racha_maxima = racha_temp
        
        print(f"\n📊 RESUMEN DEL PERÍODO ({dias} días):")
        print("-" * 50)
        print(f"📈 Tasa de cumplimiento: {completados}/{total} días ({porcentaje:.1f}%)")
        self._mostrar_barra_progreso(porcentaje)
        print(f"🔥 Racha actual: {racha_actual} días")
        print(f"🏆 Racha máxima: {racha_maxima} días")
        
        # Mostrar análisis de tendencias
        if len(historial) >= 14:
            primera_mitad = historial[:len(historial)//2]
            segunda_mitad = historial[len(historial)//2:]
            
            porc_primera = (sum(1 for d in primera_mitad if d['completado']) / len(primera_mitad) * 100)
            porc_segunda = (sum(1 for d in segunda_mitad if d['completado']) / len(segunda_mitad) * 100)
            
            if porc_segunda > porc_primera + 10:
                print("📈 ¡Tendencia positiva! Has mejorado tu constancia recientemente.")
            elif porc_primera > porc_segunda + 10:
                print("📉 Tendencia decreciente. ¡Puedes retomar el ritmo!")
            else:
                print("➡️ Tendencia estable en el período.")
        
        # Mostrar calendario visual para períodos cortos
        if dias <= 30:
            print(f"\n📅 CALENDARIO VISUAL:")
            print("-" * 50)
            
            # Agrupar por semanas
            import datetime
            for i in range(0, len(historial), 7):
                semana = historial[i:i+7]
                print(f"\nSemana {i//7 + 1}:")
                for dia in semana:
                    estado = "✅" if dia['completado'] else "❌"
                    fecha_obj = datetime.datetime.strptime(dia['fecha'], '%d/%m/%Y')
                    dia_semana = fecha_obj.strftime('%a')
                    nota = f" ({dia['nota'][:20]}...)" if dia['nota'] and len(dia['nota']) > 20 else f" ({dia['nota']})" if dia['nota'] else ""
                    print(f"  {dia_semana} {dia['fecha']}: {estado}{nota}")
        else:
            # Para períodos largos, mostrar solo resumen por semanas
            print(f"\n📅 ÚLTIMOS 21 DÍAS DETALLADOS:")
            print("-" * 50)
            for dia in historial[-21:]:
                estado = "✅" if dia['completado'] else "❌"
                nota = f" - {dia['nota']}" if dia['nota'] else ""
                print(f"   {dia['fecha']} {estado}{nota}")
            
            if len(historial) > 21:
                print(f"\n📝 ... y {len(historial) - 21} días más (usa período más corto para ver detalles)")
        
        # Mostrar días con notas
        dias_con_notas = [d for d in historial if d['nota']]
        if dias_con_notas:
            print(f"\n📝 NOTAS DESTACADAS:")
            print("-" * 50)
            for dia in dias_con_notas[-5:]:  # Últimas 5 notas
                print(f"   {dia['fecha']}: {dia['nota']}")
        
        self.pausar()
    
    def mostrar_recordatorios(self):
        """Muestra recordatorios y alertas"""
        self.limpiar_pantalla()
        self.mostrar_titulo("📢 RECORDATORIOS Y ALERTAS")
        
        recordatorios = self.gestor.generar_recordatorios()
        print(f"\n{recordatorios}")
        
        # Mostrar consejo del día
        print("\n" + "-" * 50)
        consejo = self.gestor.generador_mensajes.obtener_consejo_del_dia()
        print(f"\n{consejo}")
        
        self.pausar()
    
    def salir(self):
        """Maneja la salida de la aplicación"""
        self.limpiar_pantalla()
        print("🌟" * 20)
        print("    👋 ¡HASTA LUEGO!")
        print("🌟" * 20)
        
        # Mostrar mensaje de despedida motivacional
        habitos = self.gestor.obtener_habitos_activos()
        if habitos:
            resumen = self.gestor.obtener_resumen_general()
            if resumen['resumen_diario']['porcentaje'] >= 80:
                print("\n🎆 ¡Excelente trabajo hoy! Sigues construyendo hábitos sólidos.")
            elif resumen['resumen_diario']['completados'] > 0:
                print("\n💪 ¡Buen progreso! Cada pequeño paso cuenta hacia tus objetivos.")
            else:
                print("\n🌅 Mañana es una nueva oportunidad para crecer. ¡Tú puedes!")
        
        print("\n🚀 Recuerda: Los grandes cambios empiezan con pequeñas acciones diarias.")
        print("🌟 ¡Nos vemos pronto en tu jornada de crecimiento personal!")
        
        self.ejecutando = False

