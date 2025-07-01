#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SuperHábit - Aplicación para el seguimiento y motivación de hábitos saludables

Autores: 
Diego Corrales
Steven Ottoniel
Alfredo Montalvan
Andy Rueda

Fecha: Junio 2025
Versión: 1.0

Descripción:
SuperHábit es una aplicación de consola que ayuda a los usuarios a crear,
seguir y mantener hábitos saludables a través de un sistema de seguimiento
y motivación personalizado.

Características principales:
- Registro de hábitos con frecuencia y horarios personalizados
- Seguimiento diario de cumplimiento
- Cálculo de progreso semanal y mensual
- Sistema de mensajes motivacionales
- Alertas y recordatorios
- Historial detallado de cumplimiento
- Estadísticas y recomendaciones personalizadas
"""

import sys
import os
from datetime import datetime
import pwinput

contraseña = "Final12345"

def inicio(): #Implementación de acceso al programa mediante inicio de sesión con contraseña
    intentos = 3
    while intentos > 0:
     os.system('cls' if os.name == 'nt' else 'clear')
     print("🔴🔵"*6)
     print(" " * 1 + "🔑 INICIO DE SESION 🔑 ")
     print("🔴🔵"*6)
     print("-"* 43)
     intento = pwinput.pwinput(prompt= '🔐 CONTRASEÑA: ' , mask="*")
     if intento == contraseña:
        print(" Acceso permitido\n")
        main()
        return True
     else:
        intentos -= 1
        print("-"* 43)
        print(" Contraseña incorrecta. Acceso denegado ❌")
        print("-"* 43)
        if intentos > 0:
                print(f" Te quedan {intentos} intento(s)\n")
        else:
                print(" 🔒 Se agotaron los intentos.\n")
        input("Presiona Enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')
    return False
    


# Agregar el directorio padre al path para importar módulos

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interfaz_usuario import InterfazUsuario

def mostrar_banner_inicial():
    """Muestra el banner inicial de la aplicación"""
    print("🎆" * 25)
    print(" " * 8 + "💪 BIENVENIDO A SUPERHÁBIT 💪")
    print(" " * 2 + "🌟 Tu compañero de crecimiento personal 🌟")
    print("🎆" * 25)
    print()
    print("🎯 Objetivo: Ayudarte a construir hábitos que transformen tu vida")
    print("💪 Misión: Hacer que la constancia sea tu superpoder")
    print("🌱 Visión: Crecer un 1% cada día")
    print()
    print("🚀 ¡Comencemos tu jornada de transformación personal!")
    print("🎆" * 27)
    input("\nPresiona Enter para continuar...")

def verificar_requisitos():
    """Verifica que el entorno tenga los requisitos necesarios"""
    try:
        # Verificar versión de Python
        if sys.version_info < (3, 6):
            print("⚠️ Error: Se requiere Python 3.6 o superior")
            print(f"Versión actual: {sys.version}")
            return False
        
        # Verificar que el sistema está listo (no necesitamos crear directorios)
        print("📁 Sistema de almacenamiento en memoria listo")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Error al verificar requisitos: {e}")
        return False

def main():
    """Función principal de la aplicación"""
    try:
        # Configurar codificación para Windows
        if os.name == 'nt':  # Windows
            os.system('chcp 65001 > nul')  # UTF-8
        
        # Verificar requisitos del sistema
        if not verificar_requisitos():
            input("\nPresiona Enter para salir...")
            return
        
        # Mostrar banner inicial
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_banner_inicial()
        
        # Inicializar y ejecutar la aplicación
        print("💾 Iniciando SuperHábit...")
        print("🔧 Cargando sistema de hábitos...")
        
        app = InterfazUsuario()
        
        print("✅ ¡Sistema listo!")
        print("🎉 ¡Bienvenido a tu nueva vida de hábitos saludables!")
        
        # Ejecutar la aplicación principal
        app.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego! Gracias por usar SuperHábit.")
        print("🌟 Recuerda: La constancia es la clave del éxito.")
        
    except Exception as e:
        print(f"\n\n⚠️ Error inesperado: {e}")
        print("📞 Si el problema persiste, verifica que todos los archivos estén presentes.")
        input("\nPresiona Enter para salir...")
        
    finally:
        # Mensaje de despedida
        print("\n\n🚀 ¡Gracias por usar SuperHábit!")
        print("🎆 ¡Sigue construyendo hábitos extraordinarios!")

if __name__ == "__main__":
    inicio()

