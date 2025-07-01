from typing import List, Dict, Any, Optional
import pickle
import os

class BaseDAO:
    """Clase base para el manejo de datos usando almacenamiento en memoria"""
    
    # Almacenamiento compartido en memoria para todas las instancias
    _almacenamiento_global = {}
    _datos_cargados = False
    
    def __init__(self, nombre_coleccion: str):
        self.nombre_coleccion = nombre_coleccion
        self._archivo_datos = f'{nombre_coleccion}.pkl'
        
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
        archivos_datos = ['habitos.pkl', 'registros.pkl']
        
        for archivo in archivos_datos:
            if os.path.exists(archivo):
                try:
                    with open(archivo, 'rb') as f:
                        datos_archivo = pickle.load(f)
                        # Merge datos de este archivo con el almacenamiento global
                        for coleccion, elementos in datos_archivo.items():
                            if coleccion not in BaseDAO._almacenamiento_global:
                                BaseDAO._almacenamiento_global[coleccion] = []
                            BaseDAO._almacenamiento_global[coleccion] = elementos
                except (pickle.PickleError, EOFError, FileNotFoundError):
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
    
    def _guardar_datos(self):
        """Guarda los datos actuales en un archivo usando pickle"""
        try:
            # Guardar solo los datos de esta colección en su archivo específico
            datos_a_guardar = {self.nombre_coleccion: self.datos}
            with open(self._archivo_datos, 'wb') as f:
                pickle.dump(datos_a_guardar, f)
        except Exception as e:
            print(f"⚠️ Error al guardar datos: {e}")
    
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

