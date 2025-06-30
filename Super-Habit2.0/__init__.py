"""
SuperHábit - Aplicación para el seguimiento y motivación de hábitos saludables

Este paquete contiene todos los módulos necesarios para ejecutar la aplicación
SuperHábit, incluyendo modelos de datos, acceso a datos, utilidades y la
interfaz de usuario.

Módulos principales:
- models: Clases de datos (Habito, RegistroCumplimiento)
- dao: Acceso a datos (HabitoDAO, RegistroDAO)
- utils: Utilidades (CalculadoraProgreso, GeneradorMensajes)
- gestor_superhabit: Lógica de negocio principal
- interfaz_usuario: Interfaz de consola
- main: Punto de entrada de la aplicación

Versión: 1.0
Autor: Tu nombre
Fecha: Junio 2025
"""

__version__ = "1.0.0"
__author__ = "Tu nombre"
__email__ = "tu.email@example.com"
__description__ = "Aplicación para el seguimiento y motivación de hábitos saludables"

# Importaciones principales para facilitar el uso del paquete
from .gestor_superhabit import GestorSuperHabit
from .interfaz_usuario import InterfazUsuario

# Importaciones de modelos
from .models import Habito, RegistroCumplimiento

# Importaciones de DAOs
from .dao import HabitoDAO, RegistroDAO

# Importaciones de utilidades
from .utils import CalculadoraProgreso, GeneradorMensajes

__all__ = [
    'GestorSuperHabit',
    'InterfazUsuario',
    'Habito',
    'RegistroCumplimiento',
    'HabitoDAO',
    'RegistroDAO',
    'CalculadoraProgreso',
    'GeneradorMensajes'
]

