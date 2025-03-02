from datetime import date

class Usuario:
    def __init__(self,id,nombre,email,clave):
        self.id=id
        self.nombre=nombre
        self.email=email
        self.clave=clave
        self.bono_disponible=0.0#bono total

    def inscribirse(self,curso):
        if isinstance(curso,CursoEnVivo) and curso.fecha_inicio<=date.today():
            print(f"{self.nombre} no puede inscribirse en {curso.nombre}. Inscripcion cerrada desde {curso.fecha_inicio}.")
            return False
        print(f"{self.nombre} inscrito en {curso.nombre}")
        return True

    def valorar_curso(self,curso,puntaje,comentario):
        if 1<=puntaje<=5:
            curso.valoraciones.append(Valoracion(puntaje,date.today(),comentario))
            print(f"{self.nombre} valoro {curso.nombre} {puntaje}/5")
        else:
            print("Puntaje invalido.")

    def aplicar_bono(self,monto):
        descuento=min(monto*0.5,self.bono_disponible)
        self.bono_disponible-=descuento
        return monto-descuento

    def mostrar(self):
        print(f"Usuario:{self.nombre},Email:{self.email},Bono:{self.bono_disponible:.2f}")

class Curso:
    def __init__(self,id,nombre,descripcion):
        self.id=id
        self.nombre=nombre
        self.descripcion=descripcion
        self.valoraciones=[]#lista valoraciones

    def obtener_valoracion_promedio(self):
        return sum(v.puntaje for v in self.valoraciones)/len(self.valoraciones) if self.valoraciones else 0

    def mostrar(self):
        print(f"Curso:{self.nombre},Valoracion:{self.obtener_valoracion_promedio():.2f}")

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
        self.inscritos=[]#lista inscritos

    def calcular_costo(self):
        return 100#precio fijo

    def aplicar_bono_inscritos(self):
        if len(self.inscritos)>=self.min_inscritos:
            bono=(self.porcentaje_bono/100)*self.calcular_costo()
            for usuario in self.inscritos:
                usuario.bono_disponible+=bono
            print(f"Bono {bono:.2f} aplicado.")

class Valoracion:
    def __init__(self,puntaje,fecha,comentario):
        self.puntaje=puntaje
        self.fecha=fecha
        self.comentario=comentario

class Inscripcion:
    def __init__(self,usuario,curso,fecha,monto_pagado):
        self.usuario=usuario
        self.curso=curso
        self.fecha=fecha
        self.monto_pagado=monto_pagado

    def calcular_monto_final(self):
        return self.monto_pagado

    def mostrar(self):
        print(f"Inscripcion:{self.usuario.nombre} en {self.curso.nombre},Monto:{self.monto_pagado:.2f}")

#MAIN
if __name__=="__main__":
    print("====INICIO====\n")

    #Crear usuario
    print("Creando usuario...\n")
    usuario1=Usuario(1,"Juan","juan@example.com","1234")
    usuario1.mostrar()
    print("\n")

    #Crear cursos
    print("Creando cursos...\n")
    curso1=CursoGrabado(101,"Python Basico","Curso Python",50)
    curso2=CursoEnVivo(102,"Python Avanzado","Curso avanzado",20,date(2024,3,1),10,10)#Fecha pasada

    curso1.mostrar()
    curso2.mostrar()
    print("\n")

    #Inscripcion grabado
    print("Inscribiendo en grabado...\n")
    if usuario1.inscribirse(curso1):
        inscripcion1=Inscripcion(usuario1,curso1,date.today(),usuario1.aplicar_bono(curso1.calcular_costo()))
        inscripcion1.mostrar()
    print("\n")

    #Inscripcion en vivo
    print("Inscribiendo en vivo...\n")
    if usuario1.inscribirse(curso2):
        curso2.inscritos.append(usuario1)
        inscripcion2=Inscripcion(usuario1,curso2,date.today(),usuario1.aplicar_bono(curso2.calcular_costo()))
        inscripcion2.mostrar()
    print("\n")

    #Valorar curso
    print("Valorando curso...\n")
    usuario1.valorar_curso(curso1,4,"Buen curso")
    usuario1.valorar_curso(curso1,6,"No valido")#Debe fallar
    print("\n")

    #Aplicar bono
    print("Aplicando bono...\n")
    curso2.aplicar_bono_inscritos()
    usuario1.mostrar()
    print("\n")

    print("====FIN====")
