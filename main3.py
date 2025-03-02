from datetime import date

class Usuario:
    def __init__(self,id,nombre,email,password):
        self.id=id
        self.nombre=nombre
        self.email=email
        self.password=password
        self.directorios=[]#lista directorios

    def crear_directorio(self,nombre):
        directorio=Directorio(nombre)
        self.directorios.append(directorio)
        return directorio

    def contar_archivos(self):
        return sum(len(d.archivos) for d in self.directorios)

    def calcular_espacio(self):
        return sum(sum(a.tamano for a in d.archivos) for d in self.directorios)

class Directorio:
    def __init__(self,nombre):
        self.nombre=nombre
        self.archivos=[]#lista archivos
        self.subdirectorios=[]#lista subdirectorios

    def agregar_archivo(self,archivo):
        self.archivos.append(archivo)

    def agregar_subdirectorio(self,directorio):
        self.subdirectorios.append(directorio)

class Archivo:
    def __init__(self,nombre,tamano):
        self.nombre=nombre
        self.fecha_creacion=date.today()
        self.fecha_modificacion=self.fecha_creacion
        self.tamano=tamano

    def modificar_archivo(self,nuevo_tamano):
        self.tamano=nuevo_tamano
        self.fecha_modificacion=date.today()

class Compartir:
    def __init__(self,propietario,archivo):
        self.propietario=propietario
        self.archivo=archivo

    def es_accesible(self,usuario):
        pass#verificar acceso

class CompartirUsuario(Compartir):
    def __init__(self,propietario,archivo):
        super().__init__(propietario,archivo)
        self.usuarios_autorizados=[]#lista usuarios

    def compartir_con(self,usuario):
        self.usuarios_autorizados.append(usuario)

    def es_accesible(self,usuario):
        return usuario in self.usuarios_autorizados

class CompartirPublico(Compartir):
    def __init__(self,propietario,archivo,fecha_limite):
        super().__init__(propietario,archivo)
        self.fecha_limite=fecha_limite

    def definir_publico(self,fecha_limite):
        self.fecha_limite=fecha_limite

    def es_accesible(self,usuario):
        return date.today()<=self.fecha_limite

#MAIN
if __name__=="__main__":
    print("====INICIO====\n")

    #Crear usuario
    usuario1=Usuario(1,"Juan","juan@example.com","1234")

    #Crear directorio
    dir1=usuario1.crear_directorio("Mis Documentos")

    #Crear archivos
    archivo1=Archivo("reporte.pdf",2.5)
    archivo2=Archivo("datos.xlsx",1.2)

    #Agregar archivos
    dir1.agregar_archivo(archivo1)
    dir1.agregar_archivo(archivo2)

    #Compartir archivo
    compartir1=CompartirUsuario(usuario1,archivo1)
    usuario2=Usuario(2,"Maria","maria@example.com","5678")
    compartir1.compartir_con(usuario2)

    #Compartir publico
    compartir2=CompartirPublico(usuario1,archivo2,date(2024,4,1))

    #Mostrar accesos
    print(f"Maria acceso reporte.pdf: {compartir1.es_accesible(usuario2)}")
    print(f"Publico datos.xlsx: {compartir2.es_accesible(usuario2)}\n")

    print("====FIN====")
