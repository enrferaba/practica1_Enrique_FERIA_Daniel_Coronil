from datetime import date
from abc import ABC,abstractmethod

# Clase Tren
class Tren:
    def __init__(self,numSerie:str,marca:str,fechaIncorporacion:date,kilometraje:float):
        self.numSerie=numSerie
        self.marca=marca
        self.fechaIncorporacion=fechaIncorporacion
        self.kilometraje=kilometraje
        self.modelo=None
        self.viajes=[]
        self.mantenimientos=[]

    def registrarViaje(self,km:float,fecha:date)->None:
        self.kilometraje+=km
        self.viajes.append(RegistroViaje(fecha,km))

    def agregarMantenimiento(self,mant:'MantenimientoRealizado')->None:
        self.mantenimientos.append(mant)

# Clase ModeloTren
class ModeloTren:
    def __init__(self,nombre:str):
        self.nombre=nombre
        self.planMantenimiento=None

    def getNombre(self)->str:
        return self.nombre

    def setPlan(self,plan:'PlanMantenimiento')->None:
        self.planMantenimiento=plan

# Clase PlanMantenimiento
class PlanMantenimiento:
    def __init__(self,version:str):
        self.version=version
        self.tareas=[]

    def agregarTarea(self,tarea:'TareaMantenimiento')->None:
        self.tareas.append(tarea)

    def eliminarTarea(self,tarea:'TareaMantenimiento')->None:
        if tarea in self.tareas:
            self.tareas.remove(tarea)

# Clase abstracta TareaMantenimiento
class TareaMantenimiento(ABC):
    def __init__(self,id:int,duracion:float,costoBase:float):
        self.id=id
        self.duracion=duracion
        self.costoBase=costoBase
        self.repuestos=[]

    @abstractmethod
    def calcularCosto(self)->float:
        pass

    def agregarRepuesto(self,rep:'Repuesto')->None:
        self.repuestos.append(rep)

# Clase TareaPorTiempo
class TareaPorTiempo(TareaMantenimiento):
    def __init__(self,id:int,duracion:float,costoBase:float,frecuenciaDias:int):
        super().__init__(id,duracion,costoBase)
        self.frecuenciaDias=frecuenciaDias

    def calcularCosto(self)->float:
        return self.costoBase+sum(rep.getCosto() for rep in self.repuestos)

# Clase TareaPorRodadura
class TareaPorRodadura(TareaMantenimiento):
    def __init__(self,id:int,duracion:float,costoBase:float,kmRequeridos:float):
        super().__init__(id,duracion,costoBase)
        self.kmRequeridos=kmRequeridos

    def calcularCosto(self,km:float)->float:
        extra=(km-self.kmRequeridos)*0.05*self.costoBase if km>self.kmRequeridos else 0
        return self.costoBase+extra+sum(rep.getCosto() for rep in self.repuestos)

# Clase Repuesto
class Repuesto:
    def __init__(self,nombre:str,costo:float):
        self.nombre=nombre
        self.costo=costo

    def getCosto(self)->float:
        return self.costo

# Clase RegistroViaje
class RegistroViaje:
    def __init__(self,fecha:date,kmRecorridos:float):
        self.fecha=fecha
        self.kmRecorridos=kmRecorridos

# Clase TareaRealizada
class TareaRealizada:
    def __init__(self,tarea:TareaMantenimiento,fecha:date,descripcion:str,costo:float):
        self.tarea=tarea
        self.fecha=fecha
        self.descripcion=descripcion
        self.costo=costo

    def calcularCostoReal(self)->float:
        return self.costo

# Clase MantenimientoRealizado
class MantenimientoRealizado:
    def __init__(self,fecha:date):
        self.fecha=fecha
        self.tareasRealizadas=[]

    def calcularCostoFinal(self)->float:
        return sum(tr.calcularCostoReal() for tr in self.tareasRealizadas)

    def agregarTareaRealizada(self,tr:TareaRealizada)->None:
        self.tareasRealizadas.append(tr)

# MAIN
from datetime import date

# MAIN
if __name__=="__main__":
    print("===INICIO===")

    # Crear modelo
    print("\nCreando modelo...")
    modelo1=ModeloTren("AVE")
    print("Modelo:",modelo1.getNombre())

    # Crear plan mantenimiento
    print("\nCreando plan mantenimiento...")
    plan1=PlanMantenimiento("V1")
    modelo1.setPlan(plan1)
    print("Plan asignado:",plan1.version)

    # Crear tareas
    print("\nCreando tareas...")
    tarea1=TareaPorTiempo(1,2,100,180)
    tarea2=TareaPorRodadura(2,3,200,5000)
    print("Tarea tiempo creada, frecuencia:",tarea1.frecuenciaDias,"dias")
    print("Tarea rodadura creada, km requeridos:",tarea2.kmRequeridos)

    # Agregar tareas al plan
    plan1.agregarTarea(tarea1)
    plan1.agregarTarea(tarea2)
    print("Tareas agregadas al plan")

    # Crear tren
    print("\nCreando tren...")
    tren1=Tren("12345","Renfe",date(2020,5,10),10000)
    tren1.modelo=modelo1
    print("Tren creado, serie:",tren1.numSerie,", marca:",tren1.marca)

    # Registrar viajes
    print("\nRegistrando viajes...")
    tren1.registrarViaje(300,date(2024,3,1))
    tren1.registrarViaje(500,date(2024,3,5))
    print("Viajes registrados, kilometraje total:",tren1.kilometraje)

    # Crear repuestos
    print("\nCreando repuestos...")
    repuesto1=Repuesto("Filtro",50)
    repuesto2=Repuesto("Aceite",30)
    tarea1.agregarRepuesto(repuesto1)
    tarea2.agregarRepuesto(repuesto2)
    print("Repuestos asignados a tareas")

    # Crear mantenimiento
    print("\nCreando mantenimiento realizado...")
    mantenimiento=MantenimientoRealizado(date(2024,3,10))

    # Crear tareas realizadas
    tareaRealizada1=TareaRealizada(tarea1,date(2024,3,10),"Cambio filtro",tarea1.calcularCosto())
    tareaRealizada2=TareaRealizada(tarea2,date(2024,3,10),"Ajuste frenos",tarea2.calcularCosto(tren1.kilometraje))
    print("Tareas realizadas creadas")

    # Agregar tareas al mantenimiento
    mantenimiento.agregarTareaRealizada(tareaRealizada1)
    mantenimiento.agregarTareaRealizada(tareaRealizada2)
    print("Tareas agregadas al mantenimiento")

    # Registrar mantenimiento en el tren
    tren1.agregarMantenimiento(mantenimiento)
    print("Mantenimiento registrado en tren")

    # Mostrar resumen mantenimiento
    print("\n===RESUMEN MANTENIMIENTO===")
    print("Fecha:",mantenimiento.fecha)
    for t in mantenimiento.tareasRealizadas:
        print("Tarea:",t.descripcion,"- Costo:",t.calcularCostoReal())

    print("Costo total mantenimiento:",mantenimiento.calcularCostoFinal())

    print("\n===FIN===")