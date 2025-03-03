from datetime import date

class Estacion:
    def __init__(self,geoposicion,capacidad):
        self.geoposicion=geoposicion
        self.capacidad=capacidad
        self.bicicletas=[]

    def bicicletasDisponibles(self):
        return len(self.bicicletas)

    def estacionamientosDisponibles(self):
        return self.capacidad-len(self.bicicletas)

    def agregarBicicleta(self,bicicleta):
        if len(self.bicicletas)<self.capacidad:
            self.bicicletas.append(bicicleta)

    def retirarBicicleta(self,bicicleta):
        if bicicleta in self.bicicletas:
            self.bicicletas.remove(bicicleta)

class Bicicleta:
    def __init__(self,id):
        self.id=id

    def obtenerID(self):
        return self.id

class Usuario:
    def __init__(self,id,nombre,dni,tarjetaCredito,abono):
        self.id=id
        self.nombre=nombre
        self.dni=dni
        self.tarjetaCredito=tarjetaCredito
        self.abono=abono
        self.usos=[]

    def registrarUso(self,bicicleta,estacion):
        if estacion.bicicletasDisponibles()>0:
            estacion.retirarBicicleta(bicicleta)
            uso=UsoBicicleta(self,bicicleta,estacion)
            self.usos.append(uso)
            return uso
        return None

    def devolverBicicleta(self,uso,estacion):
        uso.finalizarUso(estacion)
        estacion.agregarBicicleta(uso.bicicleta)

class Abono:
    def calcularCosto(self,tiempoUso):
        raise NotImplementedError

class AbonoAnual(Abono):
    def __init__(self,fechaInicio):
        self.fechaInicio=fechaInicio

    def calcularCosto(self,tiempoUso):
        return 2*((tiempoUso-30)//5)if tiempoUso>30 else 0

class AbonoPrepago(Abono):
    def __init__(self,saldo):
        self.saldo=saldo

    def agregarSaldo(self,monto):
        self.saldo+=monto

    def calcularCosto(self,tiempoUso):
        return 5*((tiempoUso+14)//15)

class AbonoTuristico(Abono):
    def __init__(self,fechaInicio):
        self.fechaInicio=fechaInicio

    def calcularCosto(self,tiempoUso):
        return 10*((tiempoUso-120)//15)if tiempoUso>120 else 0

class UsoBicicleta:
    def __init__(self,usuario,bicicleta,estacionInicio):
        self.usuario=usuario
        self.bicicleta=bicicleta
        self.estacionInicio=estacionInicio
        self.estacionFin=None
        self.tiempoUso=0

    def finalizarUso(self,estacionFin):
        self.estacionFin=estacionFin
        self.tiempoUso=30
        costo=self.usuario.abono.calcularCosto(self.tiempoUso)
        Payment().processPayment(self.usuario.tarjetaCredito,costo)

class Payment:
    def processPayment(self,credit_card_number,amount):
        return True if amount>0 else False

# Main con pruebas
usuario1=Usuario(1,"Alice","12345678","4111111111111111",AbonoAnual(date(2024,3,1)))
usuario2=Usuario(2,"Bob","87654321","4222222222222222",AbonoPrepago(50))

estacion1=Estacion("Centro",5)
estacion2=Estacion("Parque",5)

bici1=Bicicleta(101)
bici2=Bicicleta(102)

estacion1.agregarBicicleta(bici1)
estacion1.agregarBicicleta(bici2)

uso1=usuario1.registrarUso(bici1,estacion1)
usuario1.devolverBicicleta(uso1,estacion2)

uso2=usuario2.registrarUso(bici2,estacion1)
usuario2.devolverBicicleta(uso2,estacion2)

print("Bicicletas en estacion1:",estacion1.bicicletasDisponibles())
print("Bicicletas en estacion2:",estacion2.bicicletasDisponibles())
print("Pago usuario1 exitoso:",Payment().processPayment(usuario1.tarjetaCredito,10))
print("Pago usuario2 exitoso:",Payment().processPayment(usuario2.tarjetaCredito,5))
