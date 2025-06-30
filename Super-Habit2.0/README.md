# 💪 SuperHábit - Tu Compañero de Crecimiento Personal

> **Una aplicación innovadora para fomentar buenos hábitos utilizando recordatorios e incentivos motivacionales**

## 🎯 Descripción del Proyecto

SuperHábit es una aplicación de consola desarrollada en Python que ayuda a los usuarios a crear, seguir y mantener hábitos saludables. Inspirada en la gamificación de aplicaciones como Duolingo, pero enfocada en el desarrollo personal y la formación de hábitos positivos.

## ✨ Características Principales

### 🏗️ Registro de Hábitos
- **Personalización completa**: Nombre, frecuencia (diaria/semanal), duración y horario sugerido
- **Validación de entrada**: Sistema robusto para evitar datos incorrectos
- **Flexibilidad**: Posibilidad de editar hábitos existentes

### 📊 Seguimiento y Progreso
- **Agenda diaria**: Visualización clara de hábitos del día
- **Progreso semanal y mensual**: Cálculos automáticos con barras de progreso visuales
- **Rachas**: Seguimiento de días consecutivos completados
- **Estadísticas detalladas**: Tasas de éxito, total de días, rachas máximas

### 🎮 Sistema de Motivación
- **Mensajes dinámicos**: Más de 50 mensajes motivacionales categorizados
- **Celebración de logros**: Reconocimiento automático de metas alcanzadas
- **Consejos personalizados**: Recomendaciones basadas en el desempeño
- **Alertas inteligentes**: Recordatorios suaves y enérgicos según el contexto

### 📈 Reportes y Análisis
- **Historial detallado**: Seguimiento día por día con notas opcionales
- **Ranking de hábitos**: Top 5 por tasa de éxito
- **Resumen semanal**: Análisis integral del progreso
- **Recomendaciones**: Sugerencias para mejorar la consistencia

## 🏗️ Arquitectura del Sistema

### 📁 Estructura Modular
```
superhabit/
├── models/                 # Modelos de datos
│   ├── __init__.py
│   ├── habito.py          # Clase Habito
│   └── registro_cumplimiento.py
├── dao/                   # Acceso a datos
│   ├── __init__.py
│   ├── base_dao.py        # DAO base con operaciones CRUD
│   ├── habito_dao.py      # DAO específico para hábitos
│   └── registro_dao.py    # DAO para registros
├── utils/                 # Utilidades
│   ├── __init__.py
│   ├── calculadora_progreso.py
│   └── generador_mensajes.py
├── data/                  # Almacenamiento JSON
│   ├── habitos.json
│   └── registros.json
├── gestor_superhabit.py   # Lógica de negocio principal
├── interfaz_usuario.py    # Interfaz de consola
├── main.py               # Punto de entrada
└── README.md
```

### 🔧 Componentes Principales

#### **Modelos de Datos**
- `Habito`: Representa un hábito con todas sus propiedades
- `RegistroCumplimiento`: Registra el cumplimiento diario de hábitos

#### **Capa de Acceso a Datos (DAO)**
- `BaseDAO`: Operaciones CRUD genéricas con persistencia JSON
- `HabitoDAO`: Operaciones específicas para hábitos
- `RegistroDAO`: Gestión de registros de cumplimiento

#### **Utilidades**
- `CalculadoraProgreso`: Cálculos estadísticos y métricas
- `GeneradorMensajes`: Sistema de motivación y mensajes

#### **Gestor Principal**
- `GestorSuperHabit`: Coordina toda la lógica de negocio
- `InterfazUsuario`: Interfaz de consola interactiva

## 🚀 Instalación y Uso

### Requisitos
- Python 3.6 o superior
- Sistema operativo: Windows, macOS, Linux

### Instalación
1. **Clonar/Descargar el proyecto**
   ```bash
   # Si tienes git instalado
   git clone [URL_DEL_REPOSITORIO]
   
   # O simplemente descarga todos los archivos en una carpeta
   ```

2. **Navegar al directorio**
   ```bash
   cd superhabit
   ```

3. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

### Uso Básico

1. **🏠 Menú Principal**: Navega usando las opciones numeradas (1-9)

2. **➕ Agregar Hábito**:
   - Ingresa el nombre del hábito
   - Selecciona frecuencia (diaria o semanal)
   - Define duración en minutos
   - Opcionalmente, establece un horario sugerido

3. **📅 Ver Agenda Diaria**:
   - Muestra todos los hábitos programados para hoy
   - Indica estado de cumplimiento
   - Muestra rachas actuales

4. **✅ Marcar Completado**:
   - Selecciona el hábito completado
   - Opcionalmente agrega una nota
   - Recibe mensaje motivacional personalizado

5. **📈 Ver Progreso**:
   - Estadísticas detalladas por hábito
   - Progreso semanal y mensual
   - Recomendaciones personalizadas

## 🎯 Funcionalidades Detalladas

### Sistema de Frecuencias
- **Diaria**: El hábito aparece todos los días
- **Semanal**: El hábito aparece una vez por semana (desaparece al completarse)

### Cálculo de Progreso
- **Semanal**: Lunes a Domingo
- **Mensual**: Primer día al último día del mes
- **Rachas**: Días consecutivos completados

### Sistema de Mensajes
- **Inicio**: Motivación para comenzar el día
- **Progreso**: Celebración del avance
- **Racha**: Reconocimiento de consistencia
- **Completado**: Felicitación por logro
- **Alertas**: Recordatorios suaves y enérgicos
- **Metas**: Celebración de objetivos alcanzados

### Persistencia de Datos
- **Formato JSON**: Fácil de leer y modificar
- **Backup automático**: Los datos se guardan inmediatamente
- **Estructura robusta**: Manejo de errores y validaciones

## 📊 Métricas y Estadísticas

### Por Hábito
- Tasa de éxito general
- Total de días registrados
- Días completados
- Racha actual
- Racha máxima alcanzada
- Progreso semanal/mensual

### Generales
- Resumen diario del usuario
- Ranking de hábitos por tasa de éxito
- Progreso semanal consolidado
- Recomendaciones basadas en patrones

## 🎨 Experiencia de Usuario

### Interfaz Visual
- **Emojis**: Interfaz amigable y atractiva
- **Barras de progreso**: Visualización clara del avance
- **Colores**: Estados diferenciados (✅ completado, ❌ pendiente)
- **Navegación intuitiva**: Menús numerados y flujo lógico

### Mensajes Motivacionales
- **Personalización**: Basados en el progreso individual
- **Variedad**: Más de 50 mensajes únicos
- **Contextualización**: Diferentes según el momento y situación
- **Positividad**: Enfoque en el crecimiento y la mejora continua

## 🔧 Características Técnicas

### Arquitectura
- **Patrón DAO**: Separación clara entre datos y lógica
- **Modularidad**: Componentes independientes y reutilizables
- **Escalabilidad**: Fácil agregar nuevas funcionalidades
- **Mantenibilidad**: Código limpio y bien documentado

### Validaciones
- **Entrada de datos**: Validación robusta de todos los inputs
- **Formato de tiempo**: Verificación de horarios HH:MM
- **Rangos**: Validación de duraciones y fechas
- **Existencia**: Verificación de hábitos y registros

### Manejo de Errores
- **Excepciones**: Captura y manejo elegante de errores
- **Mensajes informativos**: Explicaciones claras para el usuario
- **Recuperación**: Continuidad sin pérdida de datos
- **Logging**: Información para debugging

## 🚀 Posibles Mejoras Futuras

### Funcionalidades
- [ ] Integración con calendario
- [ ] Notificaciones del sistema
- [ ] Exportación de datos
- [ ] Interfaz gráfica (GUI)
- [ ] Sincronización en la nube
- [ ] Análisis de tendencias avanzado

### Técnicas
- [ ] Base de datos SQLite
- [ ] API REST
- [ ] Aplicación web
- [ ] Aplicación móvil
- [ ] Machine Learning para recomendaciones

## 👨‍💻 Desarrollo

### Requisitos de Desarrollo
- Python 3.6+
- Editor de código (VS Code, PyCharm, etc.)
- Git (opcional)

### Contribuciones
Este proyecto fue desarrollado como proyecto final para la clase de Introducción a la Programación. Las contribuciones y mejoras son bienvenidas.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo los términos de la licencia educativa.

## 🙏 Agradecimientos

- Inspirado en la gamificación de Duolingo
- Basado en principios de formación de hábitos de "Atomic Habits" por James Clear
- Desarrollado para fomentar el crecimiento personal y la disciplina

---

**¡Gracias por usar SuperHábit! 💪🌟**

*"Los grandes cambios empiezan con pequeñas acciones diarias"* 🚀

