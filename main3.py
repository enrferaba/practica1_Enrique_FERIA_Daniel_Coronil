from datetime import date

class Usuario:
    def __init__(self,id,nombre,email,contrasena):
        self.id=id
        self.nombre=nombre
        self.email=email
        self.contrasena=contrasena
        self.directorios=[]

    def obtenerCantidadArchivos(self):
        return sum(len(d.obtenerArchivos())for d in self.directorios)

    def obtenerTamañoTotalArchivos(self):
        return sum(a.obtenerTamaño()for d in self.directorios for a in d.obtenerArchivos())

    def agregarDirectorio(self,directorio):
        self.directorios.append(directorio)

class Directorio:
    def __init__(self,nombre):
        self.nombre=nombre
        self.archivos=[]
        self.subdirectorios=[]

    def agregarArchivo(self,archivo):
        self.archivos.append(archivo)

    def agregarSubdirectorio(self,directorio):
        self.subdirectorios.append(directorio)

    def obtenerArchivos(self):
        return self.archivos

    def obtenerSubdirectorios(self):
        return self.subdirectorios

class Archivo:
    def __init__(self,nombre,creacion,modificacion,tamano,compartir=None):
        self.nombre=nombre
        self.creacion=creacion
        self.modificacion=modificacion
        self.tamano=tamano
        self.compartir=compartir

    def obtenerTamaño(self):
        return self.tamano

class Compartir:
    def acceder(self,usuario):
        raise NotImplementedError

class CompartirUsuario(Compartir):
    def __init__(self):
        self.usuariosPermitidos=[]

    def agregarUsuario(self,usuario):
        self.usuariosPermitidos.append(usuario)

    def acceder(self,usuario):
        return usuario in self.usuariosPermitidos

class CompartirPublico(Compartir):
    def __init__(self,limite):
        self.limite=limite

    def acceder(self,usuario):
        return date.today()<=self.limite

# Main con pruebas
usuario1=Usuario(1,"Alice","alice@mail.com","1234")
usuario2=Usuario(2,"Bob","bob@mail.com","5678")

directorio1=Directorio("Documentos")
directorio2=Directorio("Imagenes")

archivo1=Archivo("notas.txt",date(2024,3,1),date(2024,3,3),15.5)
archivo2=Archivo("foto.jpg",date(2024,2,28),date(2024,3,2),220.3)

directorio1.agregarArchivo(archivo1)
directorio2.agregarArchivo(archivo2)

usuario1.agregarDirectorio(directorio1)
usuario1.agregarDirectorio(directorio2)

compartirU=CompartirUsuario()
compartirU.agregarUsuario(usuario2)
archivo1.compartir=compartirU

compartirP=CompartirPublico(date(2024,3,10))
archivo2.compartir=compartirP

print("Cantidad archivos usuario1:",usuario1.obtenerCantidadArchivos())
print("Tamano total usuario1:",usuario1.obtenerTamañoTotalArchivos())
print("Usuario2 accede a notas.txt:",archivo1.compartir.acceder(usuario2))
print("Usuario2 accede a foto.jpg:",archivo2.compartir.acceder(usuario2))
