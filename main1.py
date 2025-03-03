from datetime import date,timedelta

class Usuario:
    def __init__(self,id,nombre,email):
        self.id=id
        self.nombre=nombre
        self.email=email

    def mostrar(self):
        print(f"Usuario: {self.nombre}, Email: {self.email}")

class Propiedad:
    def __init__(self,id,precio_noche):
        self.id=id
        self.precio_noche=precio_noche
        self.reglas=[]#lista reglas

    def agregar_regla(self,regla):
        self.reglas.append(regla)#agregar regla

    def es_disponible(self,inicio,fin,reservas):
        for reserva in reservas:
            if not(fin<=reserva.inicio or inicio>=reserva.fin):
                return False
        return True#verificar disponibilidad

    def mostrar(self):
        print(f"Propiedad ID: {self.id}, Precio por noche: {self.precio_noche}")

class Reserva:
    def __init__(self,usuario,propiedad,inicio,fin):
        self.usuario=usuario
        self.propiedad=propiedad
        self.inicio=inicio
        self.fin=fin
        self.precio_final=0#inicializar precio

    def calcular_precio(self):
        dias_reserva=(self.fin-self.inicio).days
        precio_base=self.propiedad.precio_noche*dias_reserva#calculo base
        reglas_ordenadas=sorted(self.propiedad.reglas,key=lambda r:r.get_prioridad())#orden reglas
        for regla in reglas_ordenadas:
            precio_base=regla.aplicar(self,precio_base)#aplicar reglas
        self.precio_final=precio_base
        return self.precio_final#retornar precio final

    def es_valido(self,inicio,fin,reservas):
        return self.propiedad.es_disponible(inicio,fin,reservas)#validar reserva

    def mostrar(self):
        print(f"Reserva de {self.usuario.nombre} en propiedad {self.propiedad.id}")
        print(f"Desde {self.inicio} hasta {self.fin}")
        print(f"Precio final: {self.precio_final:.2f}")

class Regla:
    def aplicar(self,reserva,precio):
        pass

    def get_prioridad(self):
        pass

class ReglaRangoFechas(Regla):
    def __init__(self,fecha_inicio,fecha_fin,porcentaje):
        self.fecha_inicio=fecha_inicio
        self.fecha_fin=fecha_fin
        self.porcentaje=porcentaje#porcentaje ajuste

    def aplicar(self,reserva,precio):
        dias_afectados=sum(1 for d in range((reserva.fin-reserva.inicio).days) 
            if reserva.inicio+timedelta(days=d)>=self.fecha_inicio and 
            reserva.inicio+timedelta(days=d)<=self.fecha_fin)
        if dias_afectados>0:
            ajuste=(self.porcentaje/100)*reserva.propiedad.precio_noche*dias_afectados
            precio+=ajuste#ajustar precio
        return precio

    def get_prioridad(self):
        return 1#prioridad alta

class ReglaPorEstancia(Regla):
    def __init__(self,dia_minimo,porcentaje):
        self.dia_minimo=dia_minimo
        self.porcentaje=porcentaje#porcentaje descuento

    def aplicar(self,reserva,precio):
        dias_reserva=(reserva.fin-reserva.inicio).days
        if dias_reserva>self.dia_minimo:
            descuento=(self.porcentaje/100)*precio
            precio-=descuento#aplicar descuento
        return precio

    def get_prioridad(self):
        return 2#prioridad baja

#ejemplo de uso
if __name__=="__main__":
    print("==== INICIO DEL SISTEMA ====\n")

    # Crear usuario
    usuario1=Usuario(1,"Juan","juan@example.com")
    usuario1.mostrar()
    print()

    # Crear propiedad
    propiedad1=Propiedad(101,100)#precio noche 100
    propiedad1.mostrar()
    print()

    # Definir reglas
    print("Definiendo reglas de precio...\n")
    regla1=ReglaRangoFechas(date(2024,1,1),date(2024,2,28),10)#aumenta 10%
    regla2=ReglaPorEstancia(10,5)#descuento 5%

    propiedad1.agregar_regla(regla1)
    propiedad1.agregar_regla(regla2)

    # Crear reserva
    print("Generando reserva...\n")
    reserva1=Reserva(usuario1,propiedad1,date(2024,1,5),date(2024,1,20))#reserva 15 dias

    # Calcular precio
    print("Calculando precio final...\n")
    reserva1.calcular_precio()

    # Mostrar datos de la reserva
    reserva1.mostrar()
    print("\n==== FIN DEL SISTEMA ====")
