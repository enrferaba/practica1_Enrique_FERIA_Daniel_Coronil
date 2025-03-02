from datetime import date
from abc import ABC, abstractmethod

# Clase Proyectista
class Proyectista:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email
        self.proyectos = []

    def registrarProyecto(self, nombre: str, descripcion: str, fechaCierre: date, categorias: list) -> 'Proyecto':
        proyecto = Proyecto(nombre, descripcion, fechaCierre, categorias, self)
        self.proyectos.append(proyecto)
        return proyecto

# Clase Freelancer
class Freelancer:
    def __init__(self, nombre: str, email: str, precioHora: float, categorias: list):
        self.nombre = nombre
        self.email = email
        self.precioHora = precioHora
        self.categorias = categorias
        self.ofertas = []

    def registrarOferta(self, proyecto: 'Proyecto', oferta: 'Oferta') -> None:
        proyecto.registrarOferta(oferta)
        self.ofertas.append(oferta)

# Clase Proyecto
class Proyecto:
    def __init__(self, nombre: str, descripcion: str, fechaCierre: date, categorias: list, proyectista: Proyectista):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaCierre = fechaCierre
        self.categorias = categorias
        self.ofertas = []
        self.freelancerAsignado = None
        self.finalizado = False
        self.proyectista = proyectista

    def registrarOferta(self, oferta: 'Oferta') -> None:
        if date.today() <= self.fechaCierre:
            self.ofertas.append(oferta)
            print(f"Oferta registrada: {oferta.freelancer.nombre}, Precio: {oferta.calcularPrecio()}")
        else:
            print(f"No se puede registrar oferta. Fecha cierre: {self.fechaCierre}, Hoy: {date.today()}")

    def asignarOferta(self, oferta: 'Oferta') -> None:
        if oferta in self.ofertas:
            self.freelancerAsignado = oferta.freelancer

    def finalizarProyecto(self, puntaje: int, fechaFinalizacion: date) -> None:
        if self.freelancerAsignado and not self.finalizado:
            self.finalizado = True
            print(f"Proyecto {self.nombre} finalizado con puntaje {puntaje}.")

# Clase abstracta Oferta
class Oferta(ABC):
    def __init__(self, freelancer: Freelancer, fechaOferta: date):
        self.freelancer = freelancer
        self.fechaOferta = fechaOferta

    @abstractmethod
    def calcularPrecio(self) -> float:
        pass

    @abstractmethod
    def calcularTiempoEntrega(self, fechaInicio: date) -> int:
        pass

    def calcularPuntaje(self, fechaInicio: date) -> float:
        dias = self.calcularTiempoEntrega(fechaInicio)
        return self.calcularPrecio() / dias if dias > 0 else float('inf')

# Clase OfertaPorHora
class OfertaPorHora(Oferta):
    def __init__(self, freelancer: Freelancer, fechaOferta: date, horasEstimadas: int, fechaEntrega: date):
        super().__init__(freelancer, fechaOferta)
        self.horasEstimadas = horasEstimadas
        self.fechaEntrega = fechaEntrega

    def calcularPrecio(self) -> float:
        return self.horasEstimadas * self.freelancer.precioHora

    def calcularTiempoEntrega(self, fechaInicio: date) -> int:
        return (self.fechaEntrega - fechaInicio).days

# Clase OfertaPorPosicion
class OfertaPorPosicion(Oferta):
    def __init__(self, freelancer: Freelancer, fechaOferta: date, salarioMensual: float, mesesDuracion: int):
        super().__init__(freelancer, fechaOferta)
        self.salarioMensual = salarioMensual
        self.mesesDuracion = mesesDuracion

    def calcularPrecio(self) -> float:
        return self.salarioMensual * self.mesesDuracion

    def calcularTiempoEntrega(self, fechaInicio: date) -> int:
        return self.mesesDuracion * 30  # Aproximadamente 30 días por mes

# Clase Plataforma
class Plataforma:
    def __init__(self):
        self.proyectos = []
        self.freelancers = []

    def registrarProyectista(self, nombre: str, email: str) -> Proyectista:
        return Proyectista(nombre, email)

    def registrarFreelancer(self, nombre: str, email: str, precioHora: float, categorias: list) -> Freelancer:
        freelancer = Freelancer(nombre, email, precioHora, categorias)
        self.freelancers.append(freelancer)
        return freelancer

    def registrarProyecto(self, proyectista: Proyectista, nombre: str, descripcion: str, fechaCierre: date, categorias: list) -> Proyecto:
        proyecto = proyectista.registrarProyecto(nombre, descripcion, fechaCierre, categorias)
        self.proyectos.append(proyecto)
        return proyecto

    def buscarProyectosPorCategoria(self, categoria: str) -> list:
        return [p for p in self.proyectos if categoria in p.categorias]

    def buscarFreelancersPorCategoria(self, categoria: str) -> list:
        return [f for f in self.freelancers if categoria in f.categorias]

    def recomendarOfertas(self, proyecto: Proyecto) -> list:
        return sorted(proyecto.ofertas, key=lambda x: x.calcularPuntaje(proyecto.fechaCierre))

    def asignarOferta(self, proyecto: Proyecto, oferta: Oferta) -> None:
        proyecto.asignarOferta(oferta)

    def obtenerFreelancerAsignado(self, proyecto: Proyecto) -> Freelancer:
        return proyecto.freelancerAsignado

# MAIN
if __name__ == "__main__":
    print("===INICIO===")

    # Crear plataforma
    plataforma = Plataforma()

    # Registrar proyectista
    print("\nRegistrando proyectista...")
    proyectista = plataforma.registrarProyectista("Carlos", "carlos@example.com")
    print("Proyectista registrado:", proyectista.nombre)

    # Registrar freelancers
    print("\nRegistrando freelancers...")
    freelancer1 = plataforma.registrarFreelancer("Ana", "ana@example.com", 25, ["Desarrollo Web", "Diseño Gráfico"])
    freelancer2 = plataforma.registrarFreelancer("Luis", "luis@example.com", 30, ["Desarrollo Web", "Backend"])
    print("Freelancers registrados:", freelancer1.nombre, "y", freelancer2.nombre)

    # Registrar proyectos
    print("\nRegistrando proyectos...")
    proyecto1 = plataforma.registrarProyecto(proyectista, "Web App", "Desarrollo de una aplicación web", date(2024, 3, 25), ["Desarrollo Web"])
    print("Proyecto registrado:", proyecto1.nombre)

    # Registrar ofertas
    print("\nRegistrando ofertas...")
    oferta1 = OfertaPorHora(freelancer1, date(2024, 3, 20), 40, date(2024, 4, 1))
    oferta2 = OfertaPorPosicion(freelancer2, date(2024, 3, 22), 1500, 2)

    freelancer1.registrarOferta(proyecto1, oferta1)
    freelancer2.registrarOferta(proyecto1, oferta2)
    print("Ofertas registradas en proyecto:", proyecto1.nombre)

    # Verificar ofertas registradas
    print("\nOfertas registradas en proyecto:", proyecto1.nombre)
    if proyecto1.ofertas:
        for oferta in proyecto1.ofertas:
            print(f"Freelancer: {oferta.freelancer.nombre}, Precio: {oferta.calcularPrecio()}")
    else:
        print("No hay ofertas registradas.")

    # Recomendar ofertas
    print("\nRecomendando ofertas para proyecto:", proyecto1.nombre)
    mejores_ofertas = plataforma.recomendarOfertas(proyecto1)

    if mejores_ofertas:
        print("Mejor oferta seleccionada:", mejores_ofertas[0].freelancer.nombre, "- Precio:", mejores_ofertas[0].calcularPrecio())
        plataforma.asignarOferta(proyecto1, mejores_ofertas[0])
        print("Oferta asignada a:", plataforma.obtenerFreelancerAsignado(proyecto1).nombre)
    else:
        print("No hay ofertas disponibles para asignar.")

    # Finalizar proyecto
    print("\nFinalizando proyecto...")
    proyecto1.finalizarProyecto(45, date(2024, 4, 1))
    print("Proyecto", proyecto1.nombre, "finalizado.")

    print("\n===FIN===")
