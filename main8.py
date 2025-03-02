from datetime import date, timedelta
from abc import ABC, abstractmethod

# Clase Integrante
class Integrante:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email
        self.puntaje = 0

    def asignarTarea(self, tarea: 'Tarea', fecha: date):
        tarea.asignarIntegrante(self, fecha)

# Clase Líder Técnico
class LiderTecnico(Integrante):
    def __init__(self, nombre: str, email: str):
        super().__init__(nombre, email)

    def crearTablero(self, nombre: str):
        return Tablero(nombre, self)

    def crearLista(self, tablero: 'Tablero', nombreLista: str):
        tablero.crearLista(nombreLista)

# Clase Desarrollador
class Desarrollador(Integrante):
    def __init__(self, nombre: str, email: str):
        super().__init__(nombre, email)

    def completarTarea(self, tarea: 'Tarea', fecha: date):
        tarea.finalizarTarea(fecha)

# Clase Tablero
class Tablero:
    def __init__(self, nombre: str, lider: LiderTecnico):
        self.nombre = nombre
        self.lider = lider
        self.listas = []
        self.backlog = ListaTareas("Backlog")
        self.listas.append(self.backlog)

    def crearLista(self, nombreLista: str):
        lista = ListaTareas(nombreLista)
        self.listas.append(lista)

    def listarTareasPendientes(self):
        return sorted(
            [t for lista in self.listas for t in lista.tareas if t.fechaFinalizacion is None], 
            key=lambda t: t.fechaCreacion
        )

    def cerrarSprint(self):
        fecha_limite = date.today() - timedelta(days=15)
        for lista in self.listas:
            for tarea in lista.tareas:
                if tarea.fechaFinalizacion and tarea.fechaFinalizacion >= fecha_limite:
                    tarea.integrante.puntaje += tarea.calcularPuntaje()
                    if isinstance(tarea.integrante, LiderTecnico) and tarea.fechaFinalizacion <= tarea.fechaTope:
                        self.lider.puntaje += 1

# Clase Lista de Tareas
class ListaTareas:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tareas = []

    def agregarTarea(self, tarea: 'Tarea'):
        self.tareas.append(tarea)

    def moverTarea(self, tarea: 'Tarea', listaDestino: 'ListaTareas'):
        if tarea in self.tareas:
            self.tareas.remove(tarea)
            listaDestino.agregarTarea(tarea)

# Clase Asignación
class Asignacion:
    def __init__(self, integrante: Integrante, fechaInicio: date):
        self.integrante = integrante
        self.fechaInicio = fechaInicio
        self.fechaFin = None

# Clase Tarea (Abstracta)
class Tarea(ABC):
    def __init__(self, titulo: str, descripcion: str, complejidad: int, fechaTope: date):
        self.titulo = titulo
        self.descripcion = descripcion
        self.complejidad = complejidad
        self.fechaCreacion = date.today()
        self.fechaTope = fechaTope
        self.fechaFinalizacion = None
        self.historialAsignaciones = []
        self.integrante = None

    def asignarIntegrante(self, integrante: Integrante, fecha: date):
        if self.integrante:
            self.historialAsignaciones[-1].fechaFin = fecha
        self.integrante = integrante
        self.historialAsignaciones.append(Asignacion(integrante, fecha))

    def finalizarTarea(self, fecha: date):
        self.fechaFinalizacion = fecha

    @abstractmethod
    def calcularPuntaje(self):
        pass

# Clase Tarea de Diseño de Interfaz de Usuario
class TareaDIU(Tarea):
    def calcularPuntaje(self):
        return 2 * self.complejidad if self.fechaFinalizacion <= self.fechaTope else 1

# Clase Tarea de Programación
class TareaProgramacion(Tarea):
    def calcularPuntaje(self):
        return self.complejidad ** 2 if self.fechaFinalizacion <= self.fechaTope else 0

# MAIN
if __name__ == "__main__":
    print("=== INICIO DEL SISTEMA ===\n")

    # Crear líder técnico
    print("Creando líder técnico...")
    lider = LiderTecnico("Carlos", "carlos@empresa.com")
    print(f"Líder registrado: {lider.nombre}\n")

    # Crear tablero
    print("Creando tablero...")
    tablero = lider.crearTablero("Proyecto App Web")
    print(f"Tablero '{tablero.nombre}' creado con Backlog por defecto\n")

    # Crear listas adicionales
    print("Creando listas...")
    tablero.crearLista("En Progreso")
    tablero.crearLista("Finalizadas")
    print("Listas creadas: Backlog, En Progreso, Finalizadas\n")

    # Crear desarrolladores
    print("Registrando desarrolladores...")
    dev1 = Desarrollador("Ana", "ana@empresa.com")
    dev2 = Desarrollador("Luis", "luis@empresa.com")
    print(f"Desarrolladores registrados: {dev1.nombre}, {dev2.nombre}\n")

    # Crear tareas
    print("Creando tareas...")
    tarea1 = TareaDIU("Diseñar landing page", "Diseño en Figma", 3, date(2024, 4, 5))
    tarea2 = TareaProgramacion("Implementar backend", "API en Django", 5, date(2024, 4,10))

    # Agregar tareas al backlog
    tablero.backlog.agregarTarea(tarea1)
    tablero.backlog.agregarTarea(tarea2)
    print("Tareas agregadas al Backlog\n")

    # Asignar tareas a desarrolladores
    print("Asignando tareas...")
    dev1.asignarTarea(tarea1, date(2024, 3, 20))
    dev2.asignarTarea(tarea2, date(2024, 3, 22))
    print(f"Tarea '{tarea1.titulo}' asignada a {dev1.nombre}")
    print(f"Tarea '{tarea2.titulo}' asignada a {dev2.nombre}\n")

    # Mover tareas a "En Progreso"
    print("Moviendo tareas a 'En Progreso'...")
    tablero.backlog.moverTarea(tarea1, tablero.listas[1])
    tablero.backlog.moverTarea(tarea2, tablero.listas[1])
    print("Tareas en progreso\n")

    # Finalizar tareas
    print("Finalizando tareas...")
    dev1.completarTarea(tarea1, date(2024, 4, 3))  # A tiempo
    dev2.completarTarea(tarea2, date(2024, 4, 12))  # Fuera de tiempo
    print(f"Tarea '{tarea1.titulo}' finalizada el {tarea1.fechaFinalizacion}")
    print(f"Tarea '{tarea2.titulo}' finalizada el {tarea2.fechaFinalizacion}\n")

    # Cerrar sprint
    print("Cerrando sprint...")
    tablero.cerrarSprint()
    print(f"Puntaje final de {dev1.nombre}: {dev1.puntaje}")
    print(f"Puntaje final de {dev2.nombre}: {dev2.puntaje}")
    print(f"Puntaje final de líder {lider.nombre}: {lider.puntaje}\n")

    # Listar tareas pendientes
    print("Tareas pendientes:")
    tareas_pendientes = tablero.listarTareasPendientes()
    for tarea in tareas_pendientes:
        print(f"Tarea: {tarea.titulo}, Creación: {tarea.fechaCreacion}")

    print("\n=== FIN DEL SISTEMA ===")
