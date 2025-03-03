from datetime import date

class Usuario:
    def __init__(self,id,nombre,email,clave):
        self.id=id
        self.nombre=nombre
        self.email=email
        self.clave=clave
        self.bono_disponible=0.0
        self.inscripciones=[]

    def inscribirse(self,curso):
        if isinstance(curso,CursoEnVivo) and curso.fecha_inicio<=date.today():
            print(f"No se puede inscribir en {curso.nombre}. Inscripcion cerrada.")
            return False
        inscripcion=Inscripcion(self,curso,date.today())
        self.inscripciones.append(inscripcion)
        if isinstance(curso,CursoEnVivo):
            curso.inscritos+=1
        print(f"Inscrito en {curso.nombre}")
        return True

    def valorar_curso(self,curso,puntaje,comentario):
        if 1<=puntaje<=5 and curso in [i.curso for i in self.inscripciones]:
            curso.valoraciones.append(Valoracion(puntaje,date.today(),comentario))
            print(f"Valorado {curso.nombre} con {puntaje}/5")
        else:
            print("Valoracion invalida.")

    def aplicar_bono(self,monto):
        descuento=min(monto*0.5,self.bono_disponible)
        self.bono_disponible-=descuento
        return monto-descuento

class Curso:
    def __init__(self,id,nombre,descripcion):
        self.id=id
        self.nombre=nombre
        self.descripcion=descripcion
        self.valoraciones=[]

    def obtener_valoracion_promedio(self):
        return sum(v.puntaje for v in self.valoraciones)/len(self.valoraciones) if self.valoraciones else 0

    def calcular_costo(self):
        raise NotImplementedError

class CursoGrabado(Curso):
    def __init__(self,id,nombre,descripcion,precio):
        super().__init__(id,nombre,descripcion)
        self.precio=precio

    def calcular_costo(self):
        return self.precio

class CursoEnVivo(Curso):
    def __init__(self,id,nombre,descripcion,cupo_maximo,fecha_inicio,min_inscritos,porcentaje_bono):
        super().__init__(id,nombre,descripcion)
        self.cupo_maximo=cupo_maximo
        self.fecha_inicio=fecha_inicio
        self.min_inscritos=min_inscritos
        self.porcentaje_bono=porcentaje_bono
        self.inscritos=0

    def calcular_costo(self):
        return 100

    def aplicar_bono_inscritos(self):
        return (self.porcentaje_bono/100)*self.calcular_costo() if self.inscritos>=self.min_inscritos else 0

class Valoracion:
    def __init__(self,puntaje,fecha,comentario):
        self.puntaje=puntaje
        self.fecha=fecha
        self.comentario=comentario

class Inscripcion:
    def __init__(self,usuario,curso,fecha):
        self.usuario=usuario
        self.curso=curso
        self.fecha=fecha
        self.monto_pagado=self.calcular_monto_final()

    def calcular_monto_final(self):
        costo=self.curso.calcular_costo()
        descuento=self.usuario.aplicar_bono(costo)
        return costo-descuento

# MAIN
if __name__=="__main__":
    usuario1=Usuario(1,"Juan","juan@example.com","1234")

    curso1=CursoGrabado(101,"Python Basico","Curso Python",50)
    curso2=CursoEnVivo(102,"Python Avanzado","Curso avanzado",20,date(2024,3,10),10,10)

    if usuario1.inscribirse(curso1):
        print(f"Pago curso1: {usuario1.inscripciones[-1].monto_pagado}")

    if usuario1.inscribirse(curso2):
        print(f"Pago curso2: {usuario1.inscripciones[-1].monto_pagado}")

    usuario1.valorar_curso(curso1,4,"Buen curso")
    usuario1.valorar_curso(curso1,6,"No valido")

    bono=curso2.aplicar_bono_inscritos()
    usuario1.bono_disponible+=bono

    print("Valoracion curso1:",curso1.obtener_valoracion_promedio())
    print("Bono disponible usuario1:",usuario1.bono_disponible)
