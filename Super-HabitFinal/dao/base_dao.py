from typing import List, Dict, Any, Optional
import csv
import os
from datetime import datetime

class BaseDAO:
    """Clase base para el manejo de datos usando almacenamiento en memoria"""
    
    # Almacenamiento compartido en memoria para todas las instancias
    _almacenamiento_global = {}
    _datos_cargados = False
    
    def __init__(self, nombre_coleccion: str):
        self.nombre_coleccion = nombre_coleccion
        self._archivo_datos = f'{nombre_coleccion}.csv'
        
        # Solo cargar datos una vez al inicio
        if not BaseDAO._datos_cargados:
            self._cargar_todos_los_datos()
            BaseDAO._datos_cargados = True
        
        if nombre_coleccion not in BaseDAO._almacenamiento_global:
            BaseDAO._almacenamiento_global[nombre_coleccion] = []
        self.datos = BaseDAO._almacenamiento_global[nombre_coleccion]
        self._siguiente_id = self._obtener_siguiente_id()
    
    def _cargar_todos_los_datos(self):
        """Carga todos los archivos de datos disponibles"""
        archivos_datos = {
            'habitos.csv': 'habitos',
            'registros.csv': 'registros'
        }
        
        for archivo, nombre_coleccion in archivos_datos.items():
            if os.path.exists(archivo):
                try:
                    elementos = self._cargar_csv(archivo)
                    if nombre_coleccion not in BaseDAO._almacenamiento_global:
                        BaseDAO._almacenamiento_global[nombre_coleccion] = []
                    BaseDAO._almacenamiento_global[nombre_coleccion] = elementos
                except Exception:
                    # Si hay error al cargar este archivo, continuar con el siguiente
                    continue
    
    def _obtener_siguiente_id(self) -> int:
        """Obtiene el siguiente ID disponible"""
        if not self.datos:
            return 1
        return max(item.get('id', 0) for item in self.datos) + 1
    
    def _generar_id(self) -> int:
        """Genera un nuevo ID único"""
        nuevo_id = self._siguiente_id
        self._siguiente_id += 1
        return nuevo_id
    
    def _cargar_csv(self, archivo: str) -> List[Dict[str, Any]]:
        """Carga datos desde un archivo CSV"""
        elementos = []
        try:
            with open(archivo, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convertir tipos de datos apropiados
                    elemento = self._convertir_tipos_csv(row)
                    elementos.append(elemento)
        except Exception:
            pass  # Si no se puede leer, retornar lista vacía
        return elementos
    
    def _convertir_tipos_csv(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Convierte strings de CSV a tipos de datos apropiados"""
        elemento = {}
        for key, value in row.items():
            if not value:  # Valor vacío
                elemento[key] = None
            elif key == 'id' or key.endswith('_id'):
                elemento[key] = int(value)
            elif key in ['duracion']:
                elemento[key] = int(value)
            elif key in ['activo', 'completado']:
                elemento[key] = value.lower() == 'true'
            elif key in ['fecha_creacion', 'fecha_registro'] and value:
                try:
                    # Si ya es datetime, mantenerlo
                    if isinstance(value, datetime):
                        elemento[key] = value
                    else:
                        elemento[key] = datetime.fromisoformat(value)
                except:
                    elemento[key] = value
            elif key == 'fecha' and value:
                try:
                    # Para fechas simples (solo fecha, no datetime)
                    from datetime import datetime as dt
                    if isinstance(value, str):
                        if 'T' in value:
                            elemento[key] = dt.fromisoformat(value)
                        else:
                            elemento[key] = dt.fromisoformat(value + 'T00:00:00')
                    else:
                        elemento[key] = value
                except:
                    elemento[key] = value
            else:
                elemento[key] = value
        return elemento
    
    def _guardar_datos(self):
        """Guarda los datos actuales en un archivo CSV"""
        try:
            if not self.datos:
                return  # No crear archivo vacío
            
            # Obtener campos del primer elemento
            campos = list(self.datos[0].keys())
            
            with open(self._archivo_datos, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader()
                
                for elemento in self.datos:
                    # Convertir datetime a string para CSV
                    elemento_csv = self._convertir_para_csv(elemento)
                    writer.writerow(elemento_csv)
                    
        except Exception as e:
            print(f"⚠️ Error al guardar datos: {e}")
    
    def _convertir_para_csv(self, elemento: Dict[str, Any]) -> Dict[str, str]:
        """Convierte tipos de datos a strings para CSV"""
        elemento_csv = {}
        for key, value in elemento.items():
            if value is None:
                elemento_csv[key] = ''
            elif isinstance(value, datetime):
                if key == 'fecha':
                    # Solo fecha para registros
                    elemento_csv[key] = value.date().isoformat()
                else:
                    # Datetime completo
                    elemento_csv[key] = value.isoformat()
            elif isinstance(value, bool):
                elemento_csv[key] = str(value)
            else:
                elemento_csv[key] = str(value)
        return elemento_csv
    
    def obtener_todos(self) -> List[Dict[str, Any]]:
        """Obtiene todos los elementos"""
        return self.datos.copy()
    
    def obtener_por_id(self, id_elemento: int) -> Optional[Dict[str, Any]]:
        """Obtiene un elemento por su ID"""
        for item in self.datos:
            if item.get('id') == id_elemento:
                return item.copy()
        return None
    
    def crear(self, elemento: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo elemento"""
        elemento['id'] = self._generar_id()
        self.datos.append(elemento)
        self._guardar_datos()
        return elemento.copy()
    
    def actualizar(self, id_elemento: int, elemento: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un elemento existente"""
        for i, item in enumerate(self.datos):
            if item.get('id') == id_elemento:
                elemento['id'] = id_elemento
                self.datos[i] = elemento
                self._guardar_datos()
                return elemento.copy()
        return None
    
    def eliminar(self, id_elemento: int) -> bool:
        """Elimina un elemento por su ID"""
        for i, item in enumerate(self.datos):
            if item.get('id') == id_elemento:
                del self.datos[i]
                self._guardar_datos()
                return True
        return False

