from datetime import datetime, date

class Usuario:
    def __init__(self,dni,nombre,apellido,tarjeta_credito,abono):
        self.dni=dni
        self.nombre=nombre
        self.apellido=apellido
        self.tarjeta_credito=tarjeta_credito
        self.abono=abono

    def cambiar_abono(self,nuevo_abono):
        self.abono=nuevo_abono

class Estacion:
    def __init__(self,id,geoposicion,capacidad):
        self.id=id
        self.geoposicion=geoposicion
        self.capacidad=capacidad
        self.estacionamientos=[]#lista estacionamientos
        self.usoBicicletas=[]#lista usos

    def estacionamientos_disponibles(self):
        return sum(1 for e in self.estacionamientos if not e.bicicleta)

    def bicicletas_disponibles(self):
        return sum(1 for e in self.estacionamientos if e.bicicleta)

class Estacionamiento:
    def __init__(self,id):
        self.id=id
        self.bicicleta=None#bicicleta asignada
        self.cerrado=False#estado

    def bloquear(self):
        self.cerrado=True

    def desbloquear(self):
        self.cerrado=False

class Bicicleta:
    def __init__(self,id):
        self.id=id

    def asignar_estacionamiento(self,estacionamiento):
        estacionamiento.bicicleta=self

class Abono:
    def calcular_costo(self,minutos):
        pass#metodo base

class AbonoAnual(Abono):
    def __init__(self,fecha_inicio):
        self.fecha_inicio=fecha_inicio

    def calcular_costo(self,minutos):
        return 0 if minutos<=30 else (minutos-30)*0.50

class AbonoPrepago(Abono):
    def __init__(self,saldo):
        self.saldo=saldo

    def recargar(self,monto):
        self.saldo+=monto

    def calcular_costo(self,minutos):
        costo=minutos*0.20
        if self.saldo>=costo:
            self.saldo-=costo
            return costo
        return 0

class AbonoTuristico(Abono):
    def __init__(self,fecha_inicio,duracion):
        self.fecha_inicio=fecha_inicio
        self.duracion=duracion

    def calcular_costo(self,minutos):
        return 0 if minutos<=120 else (minutos-120)*1.00

class UsoBicicleta:
    def __init__(self,usuario,bicicleta,estacion_origen,estacion_destino,fecha_inicio,fecha_fin):
        self.usuario=usuario
        self.bicicleta=bicicleta
        self.estacion_origen=estacion_origen
        self.estacion_destino=estacion_destino
        self.fecha_inicio=fecha_inicio
        self.fecha_fin=fecha_fin

    def calcular_costo(self):
        minutos=(self.fecha_fin-self.fecha_inicio).seconds//60
        return self.usuario.abono.calcular_costo(minutos)

class Payment:
    def processPayment(self,credit_card_number,amount):
        return True if len(credit_card_number)==16 and amount>0 else False

from datetime import datetime,date

# MAIN
if __name__=="__main__":
    print("==== INICIO DEL SISTEMA ====\n")
    # Crear abonos
    abono1=AbonoAnual(date(2024,3,1))
    abono2=AbonoPrepago(10)
    abono3=AbonoTuristico(date(2024,3,5),7)
    # Crear usuarios
    usuario1=Usuario("12345678A","Juan","Perez","1111222233334444",abono1)
    usuario2=Usuario("87654321B","Maria","Lopez","5555666677778888",abono2)
    usuario3=Usuario("65432178C","Carlos","Garcia","9999888877776666",abono3)
    # Crear estaciones
    estacion1=Estacion(1,"40.4168,-3.7038",20)
    estacion2=Estacion(2,"40.4170,-3.7040",15)
    estacion3=Estacion(3,"40.4180,-3.7050",10)
    # Crear estacionamientos
    estac1=Estacionamiento(1)
    estac2=Estacionamiento(2)
    estac3=Estacionamiento(3)
    estac4=Estacionamiento(4)
    estacion1.estacionamientos.append(estac1)
    estacion1.estacionamientos.append(estac2)
    estacion2.estacionamientos.append(estac3)
    estacion3.estacionamientos.append(estac4)
    # Asignar bicicletas
    bici1=Bicicleta(101)
    bici2=Bicicleta(102)
    bici3=Bicicleta(103)
    bici4=Bicicleta(104)
    bici1.asignar_estacionamiento(estac1)
    bici2.asignar_estacionamiento(estac3)
    bici3.asignar_estacionamiento(estac2)
    # Bloquear estac4
    estac4.bloquear()
    # Mostrar disponibles
    print(f"Estacion 1: {estacion1.bicicletas_disponibles()} disponibles")
    print(f"Estacion 2: {estacion2.bicicletas_disponibles()} disponibles")
    print(f"Estacion 3: {estacion3.bicicletas_disponibles()} disponibles\n")
    # Crear viajes
    uso1=UsoBicicleta(usuario1,bici1,estacion1,estacion2,datetime(2024,3,10,8,30,0),datetime(2024,3,10,9,0,0))
    uso2=UsoBicicleta(usuario2,bici2,estacion2,estacion3,datetime(2024,3,10,9,15,0),datetime(2024,3,10,9,45,0))
    uso3=UsoBicicleta(usuario3,bici3,estacion1,estacion3,datetime(2024,3,10,10,0,0),datetime(2024,3,10,10,50,0))
    uso4=UsoBicicleta(usuario1,bici4,estacion3,estacion1,datetime(2024,3,10,11,0,0),datetime(2024,3,10,11,30,0))
    # Registrar usos
    estacion1.usoBicicletas.append(uso1)
    estacion2.usoBicicletas.append(uso2)
    estacion3.usoBicicletas.append(uso3)
    estacion1.usoBicicletas.append(uso4)
    # Calcular costos
    print(f"Costo Juan viaje1: {uso1.calcular_costo()}€")
    print(f"Costo Maria viaje: {uso2.calcular_costo()}€")
    print(f"Costo Carlos viaje: {uso3.calcular_costo()}€")
    print(f"Costo Juan viaje2: {uso4.calcular_costo()}€\n")
    # Recargar saldo
    print("Maria recarga 5€")
    usuario2.abono.recargar(5)
    print(f"Maria saldo: {usuario2.abono.saldo}€\n")
    # Cambiar abono
    print("Carlos cambia abono")
    usuario3.cambiar_abono(abono1)
    uso5=UsoBicicleta(usuario3,bici3,estacion3,estacion2,datetime(2024,3,11,8,0,0),datetime(2024,3,11,9,0,0))
    estacion3.usoBicicletas.append(uso5)
    print(f"Costo Carlos viaje nuevo: {uso5.calcular_costo()}€\n")
    # Procesar pago
    payment=Payment()
    if payment.processPayment(usuario1.tarjeta_credito,uso1.calcular_costo()):
        print("Pago Juan OK")
    else:
        print("Pago Juan FAIL")
    # Mas viajes
    uso6=UsoBicicleta(usuario2,bici4,estacion2,estacion1,datetime(2024,3,11,10,0,0),datetime(2024,3,11,10,30,0))
    uso7=UsoBicicleta(usuario1,bici1,estacion1,estacion3,datetime(2024,3,11,11,0,0),datetime(2024,3,11,11,40,0))
    estacion2.usoBicicletas.append(uso6)
    estacion1.usoBicicletas.append(uso7)
    print(f"Costo Maria viaje2: {uso6.calcular_costo()}€")
    print(f"Costo Juan viaje3: {uso7.calcular_costo()}€\n")
    # Mostrar usos en Estacion1
    print("Usos Estacion1:")
    for uso in estacion1.usoBicicletas:
        print(f"Usuario: {uso.usuario.nombre}, Costo: {uso.calcular_costo()}€")
    print("\n==== FIN DEL SISTEMA ====")
