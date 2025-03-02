from datetime import datetime,date
from abc import ABC,abstractmethod

class CreadorRecurso:
    def __init__(self,nombre,email,contrasena,puntos=0):
        self.nombre=nombre
        self.email=email
        self.contrasena=contrasena
        self.puntos=puntos
        self.recursos=[]  # rec list

    def registrarRecurso(self,recurso):
        self.recursos.append(recurso)

class Usuario:
    def __init__(self,nombre,email,contrasena):
        self.nombre=nombre
        self.email=email
        self.contrasena=contrasena

    @staticmethod
    def registrarUsuario(nombre,email,contrasena):
        return Usuario(nombre,email,contrasena)

class Recurso:
    def __init__(self,descripcion,imagenPrevisualizacion,urlDescarga,fechaCarga,precioBase,creador,estrategia):
        self.descripcion=descripcion
        self.imagenPrevisualizacion=imagenPrevisualizacion
        self.urlDescarga=urlDescarga
        self.fechaCarga=fechaCarga
        self.precioBase=precioBase
        self.creador=creador
        self.estrategia=estrategia

    def getPrecioFinal(self,fechaCompra):
        return self.estrategia.calcularPrecio(self,fechaCompra)

class EstrategiaComercializacion(ABC):
    @abstractmethod
    def calcularPrecio(self,recurso,fechaCompra):
        pass
    @abstractmethod
    def calcularPuntos(self,costo):
        pass

class Normal(EstrategiaComercializacion):
    def calcularPrecio(self,recurso,fechaCompra):
        return recurso.precioBase
    def calcularPuntos(self,costo):
        return int(costo*10)

class Oferta(EstrategiaComercializacion):
    def __init__(self,fechaLimite,porcentaje):
        self.fechaLimite=fechaLimite
        self.porcentaje=porcentaje
    def calcularPrecio(self,recurso,fechaCompra):
        if fechaCompra<=self.fechaLimite:
            return recurso.precioBase*(1-self.porcentaje/100)
        return recurso.precioBase
    def calcularPuntos(self,costo):
        if date.today()<=self.fechaLimite:
            return int(costo*5)
        return int(costo*10)

class CrowdBased(EstrategiaComercializacion):
    def __init__(self,cantidadMinima):
        self.cantidadMinima=cantidadMinima
    def calcularPrecio(self,recurso,fechaCompra):
        return recurso.precioBase
    def calcularPuntos(self,costo):
        return int(costo*50/self.cantidadMinima)

class Compra:
    def __init__(self,usuario,recurso,fechaCompra):
        self.usuario=usuario
        self.recurso=recurso
        self.fechaCompra=fechaCompra
        self.costoFinal=0
        self.puntosObtenidos=0
    def calcularCostoFinal(self):
        self.costoFinal=self.recurso.getPrecioFinal(self.fechaCompra)
        return self.costoFinal
    def calcularPuntosTotales(self):
        self.puntosObtenidos=self.recurso.estrategia.calcularPuntos(self.costoFinal)
        return self.puntosObtenidos
    def registrarCompra(self):
        self.calcularCostoFinal()
        self.calcularPuntosTotales()
        self.recurso.creador.puntos += self.puntosObtenidos

class Payment:
    def processPayment(self,credit_card_number,amount):
        return True if len(credit_card_number)==16 and amount>0 else False

# MAIN
if __name__=="__main__":
    print("==== INICIO ====\n")

    # Crear creador
    print("Creando creador...")
    creador = CreadorRecurso("Alice","alice@ejemplo.com","pass123")
    print("Creador:", creador.nombre)

    # Crear estrategias
    print("\nCreando estrategias...")
    estrNorm = Normal()
    estrOferta = Oferta(date(2024,3,15),10)
    estrCrowd = CrowdBased(20)

    # Crear recursos
    print("\nCreando recursos...")
    recurso1 = Recurso("Recurso Normal","img1.jpg","url1",date(2024,3,1),100.0,creador,estrNorm)
    recurso2 = Recurso("Recurso Oferta","img2.jpg","url2",date(2024,3,2),150.0,creador,estrOferta)
    recurso3 = Recurso("Recurso Crowd","img3.jpg","url3",date(2024,3,3),200.0,creador,estrCrowd)
    creador.registrarRecurso(recurso1)
    creador.registrarRecurso(recurso2)
    creador.registrarRecurso(recurso3)
    print("Recursos creados:", len(creador.recursos))

    # Crear usuarios
    print("\nCreando usuarios...")
    usuarioA = Usuario.registrarUsuario("Bob","bob@ejemplo.com","bobpass")
    usuarioB = Usuario.registrarUsuario("Carol","carol@ejemplo.com","carolpass")
    print("Usuarios registrados: Bob y Carol")

    # Crear compras
    print("\nProcesando compras...")
    compra1 = Compra(usuarioA,recurso1,date(2024,3,10))
    compra2 = Compra(usuarioB,recurso2,date(2024,3,12))
    compra3 = Compra(usuarioA,recurso3,date(2024,3,14))
    compra1.registrarCompra()
    compra2.registrarCompra()
    compra3.registrarCompra()

    # Mostrar compras
    print("\nDetalles de compras:")
    for i, compra in enumerate([compra1,compra2,compra3],1):
        print(f"Compra{i}: Costo {compra.costoFinal}€, Puntos {compra.puntosObtenidos}")

    # Procesar pagos
    print("\nProcesando pagos...")
    payment = Payment()
    pagos = [
        payment.processPayment("1234567812345678", compra1.costoFinal),
        payment.processPayment("8765432187654321", compra2.costoFinal),
        payment.processPayment("1234876512348765", compra3.costoFinal)
    ]
    
    # Mostrar pagos
    print("\nResultados de pagos:")
    for i, pago in enumerate(pagos,1):
        print(f"Pago{i}: {'OK' if pago else 'FAIL'}")

    # Mostrar puntos creador
    print("\nTotal puntos creador:", creador.puntos)

    # Cambio estrategia
    print("\nCambio estrategia recurso2 a Normal")
    recurso2.estrategia = estrNorm
    compra4 = Compra(usuarioB,recurso2,date(2024,3,16))
    compra4.registrarCompra()
    pago4 = payment.processPayment("8765432187654321", compra4.costoFinal)
    # Mostrar nueva compra
    print("\nProcesando nueva compra...")
    print(f"Usuario: {compra4.usuario.nombre}")
    print(f"Recurso: {compra4.recurso.descripcion}")
    print(f"Costo final: {compra4.costoFinal}€")
    print(f"Puntos obtenidos: {compra4.puntosObtenidos}")
    print(f"Estado pago: {'OK' if pago4 else 'FAIL'}")

    print("\n==== FIN DEL SISTEMA ====")
