import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
import pyrebase
import pywhatkit as pw
from datetime import datetime
import time
from time import gmtime, strftime
import pyautogui as pg
from geopy.geocoders import Nominatim
import geocoder
from geopy.exc import GeocoderTimedOut
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

Window.size = (720, 900)  # establece el tamaño de la ventana en pixeles

ENLACE=''
# Configuración de Firebase
config = {
  'apiKey': "AIzaSyD2Jmtv9TvQZ2Q91CCZ1whlt7WHwt7LL7w",
  'authDomain': "emergenciasep.firebaseapp.com",
  'projectId': "emergenciasep",
  "databaseURL": "https://emergenciasep-default-rtdb.firebaseio.com",
  'storageBucket': "emergenciasep.appspot.com",
  'messagingSenderId': "375827931921",
  'appId': "1:375827931921:web:93297ecdcb22796a1022b0",
  'measurementId': "G-1RVF3JHFBY"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
Builder.load_file('main.kv')
class ScreenManagement(ScreenManager):
    pass

class MainScreen(Screen):
    nombre_usuario = StringProperty('')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        
    # Función que se ejecuta al presionar el botón
    def comprobar_usuario(self, instance):
        # Obtener los usuarios de la base de datos
        usuarios = db.child("users").get().val()
        # Obtener el nombre de usuario ingresado por el usuario
        nombre_usuario = self.ids.test.text
        # Comprobar si el usuario existe en la base de datos
        if nombre_usuario in usuarios:
            print("El usuario ya existe en Firebase")
            self.manager.get_screen("second").nombre_usuario = nombre_usuario
            print(nombre_usuario)
            self.manager.current = "second"
        else:
            print("El usuario no existe en Firebase")
    pass

class SecondScreen(Screen):
    print("Cambio")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Creamos un Layout principal vertical
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=10)
        # Creamos un Layout para los textos superior
        self.mensajeria = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.1))
        self.texto_superior = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        # Creamos un Layout para los textos a la izquierda
        self.opciones_izquierda_superior = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))
        # Creamos un Layout para los botones de opcionestextos a la derecha
        self.opciones_derecha_superior = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))
        # Creamos un Layout para los botones de opciones
        self.opciones_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        # Creamos un Layout para los botones de opciones a la izquierda
        self.opciones_izquierda_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))
        # Creamos un Layout para los botones de opciones a la derecha
        self.opciones_derecha_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))
        # Creamos un botón rojo para enviar el mensaje
        self.btn_enviar = Button(background_normal='alerta_roja.png',background_down='alerta_roja.png',size_hint=(1, 0.65), font_size=30)
        # Creamos un Label para la fecha y hora
        self.lbl_fecha_hora = Label(text='Fecha y hora:', font_size=20, size_hint=(0.8, 0.1))
        # Creamos un Label para el nombre del usuario
        self.lbl_usuario = Label(text="", font_size=30, size_hint=(1, 0.1))
        # Creamos los botones de opciones
        self.btn_opcion1 = ToggleButton(text='Lesiones corporales', size_hint=(1, None), height=50,font_size=25)
        self.btn_opcion2 = ToggleButton(text='Daños a terceros', size_hint=(1, None), height=50,font_size=25)
        self.btn_opcion3 = ToggleButton(text='Choque de vehículos', size_hint=(1, None), height=50,font_size=25)
        self.btn_opcion4 = ToggleButton(text='Propiedad de 3ero dañada', size_hint=(1, None), height=50,font_size=25)
        self.btn_opcion5 = ToggleButton(text='Daño material', size_hint=(1, None), height=50,font_size=25)
        self.btn_opcion6 = ToggleButton(text='Accidente ambiental', size_hint=(1, None), height=50,font_size=25)
        # Agregamos los widgets a los layouts correspondientes
        self.opciones_izquierda_superior.add_widget(self.lbl_usuario)
        # Crear Label para la fecha y hora
        self.lbl_fecha_hora = Label(text="", font_size=30, size_hint=(1, 0.1))
        self.opciones_derecha_superior.add_widget(self.lbl_fecha_hora)
        # Iniciar el reloj para actualizar el Label cada segundo
        Clock.schedule_interval(self.update_fecha_hora, 1)  
        self.lbl_mensaje_enviado = Label(text="Selecciona consecuencias y pulsa ALERTA", font_size=30, size_hint=(1, None), height=20, opacity=1, color=(1, 1, 1, 1), valign='middle')
        self.separacion = Label(text="       ", font_size=30, size_hint=(1, None), height=60, opacity=1, color=(1, 1, 1, 1), valign='middle')
        self.texto_superior.add_widget(self.opciones_izquierda_superior)
        self.texto_superior.add_widget(self.opciones_derecha_superior)
        self.opciones_izquierda_layout.add_widget(self.btn_opcion1)
        self.opciones_izquierda_layout.add_widget(self.btn_opcion2)
        self.opciones_izquierda_layout.add_widget(self.btn_opcion5)
        self.opciones_derecha_layout.add_widget(self.btn_opcion3)
        self.opciones_derecha_layout.add_widget(self.btn_opcion4)
        self.opciones_derecha_layout.add_widget(self.btn_opcion6)
        self.opciones_layout.add_widget(self.opciones_izquierda_layout)
        self.opciones_layout.add_widget(self.opciones_derecha_layout)
        self.btn_enviar.bind(on_press=self.cambiar_imagen)
        self.layout.add_widget(self.texto_superior)
        self.layout.add_widget(self.btn_enviar)
        self.layout.add_widget(self.separacion)
        self.layout.add_widget(self.opciones_layout)
        self.layout.add_widget(self.mensajeria)
        self.mensajeria.add_widget(self.lbl_mensaje_enviado)
        # Agregando el layout al screen
        self.add_widget(self.layout)
        #numeros_telefono = ['+51920478074', '+51989266134', '+51914238612', '+51993523727']
        numeros_telefono = ['+51920478074', '+51993523727']
        # Creamos la función que se ejecutará cuando se presione el botón
        lat=""
        longt=""
        def get_location():
            global lat,longt,ENLACE
            g = geocoder.ip('me')
            lat=g.latlng[0]
            longt=g.latlng[1]
            ENLACE='https://maps.google.com/?ll='+str(lat)+','+str(longt)+'&z=24'
            #print(ENLACE)  
        def llamada():
            global localidad
            if localidad=="Lima":
                lead = '+51993523727'
            else:
                lead = '+51920478074'

            # Obtener texto concatenado de los botones ToggleButton seleccionados
            texto_mensaje= 'https://call.whatsapp.com/voice/69dbRR1ZjSrsrC2ETWjTc6'
            print(texto_mensaje)
            
            # Enviamos el mensaje de WhatsApp a los destinatarios especificados
            pw.sendwhatmsg_instantly(lead, texto_mensaje)
            
            # Esperamos un tiempo antes de cerrar la ventana
            time.sleep(10)
            
            # Cerramos la ventana de WhatsApp
            pg.hotkey('ctrl', 'w')

        # Asignamos la función enviar_mensaje al botón de enviar
        def enviar_mensaje():
            global ENLACE, localidad
            usuario = self.nombre_usuario
            localidad = db.child("users").child(usuario).child("Sede").get().val()
            print(localidad)
            # Obtener texto concatenado de los botones ToggleButton seleccionados
            now =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            opciones_seleccionadas = []
            if self.btn_opcion1.state == 'down':
                opciones_seleccionadas.append(self.btn_opcion1.text)
            if self.btn_opcion2.state == 'down':
                opciones_seleccionadas.append(self.btn_opcion2.text)
            if self.btn_opcion3.state == 'down':
                opciones_seleccionadas.append(self.btn_opcion3.text)
            if self.btn_opcion4.state == 'down':
                opciones_seleccionadas.append(self.btn_opcion4.text)
            Concat=(', '.join(opciones_seleccionadas))
            get_location()
            texto= '*ALERTA!* \n El trabajador '+ usuario +' a sufrido un accidente con fecha y hora: '+str(now)+' Las consecuencias conocidas: '    
            texto_mensaje = texto+Concat +'.\n El accidente se ha reportado aproximadamente desde: '+str(ENLACE)
            # Enviamos el mensaje de WhatsApp a los destinatarios especificados
            first = True
            if opciones_seleccionadas:
                self.lbl_mensaje_enviado.text = "Mensaje enviado"
                self.resetear_toggle()
                print(texto_mensaje)
                for lead in numeros_telefono:
                    time.sleep(5)
                    pw.sendwhatmsg_instantly(f"+{lead}", texto_mensaje)
                    if first:
                        time.sleep(7)
                        first=False
                    width,height = pg.size()
                    pg.click(width/2,height/2)
                    time.sleep(8)
                    pg.press('enter')
                    time.sleep(8)
                llamada()
            else: 
                print("Selecciona consecuencias conocidas") 
                self.lbl_mensaje_enviado.text = "Selecciona consecuencias conocidas"
                self.lbl_mensaje_enviado.opacity = 1                 

        self.btn_enviar.bind(on_press=lambda x: enviar_mensaje())
    def on_enter(self, *args):
        if hasattr(self, "nombre_usuario"):
            self.lbl_usuario.text = f"Bienvenido, {self.nombre_usuario}"
    def update_fecha_hora(self, dt):
                # Obtener la fecha y hora actual
                now = datetime.now()
                fecha_hora_str = now.strftime("%d/%m/%Y %H:%M:%S")
                # Actualizar el texto del Label
                self.lbl_fecha_hora.text = fecha_hora_str
    def resetear_toggle(self):
        self.btn_opcion1.state = 'normal'
        self.btn_opcion2.state = 'normal'
        self.btn_opcion3.state = 'normal'
        self.btn_opcion4.state = 'normal'
        self.btn_opcion5.state = 'normal'
        self.btn_opcion6.state = 'normal'
        self.lbl_mensaje_enviado.opacity = 1
    def cambiar_imagen(self, instance):
        if instance.background_normal == 'alerta_roja.png':
            instance.background_normal = 'alerta_pulso.png'
        else:
            instance.background_normal = 'alerta_roja.png'
            instance.background_down = 'alerta_pulso.png'
        
        # Programa el restablecimiento de la imagen después de 2 segundos
        Clock.schedule_once(lambda dt: self.restablecer_imagen(instance), 2)

    def restablecer_imagen(self, instance):
        instance.background_normal = 'alerta_roja.png'
        instance.background_down = 'alerta_pulso.png'

class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainScreen(name='main'))
        screen_manager.add_widget(SecondScreen(name='second'))
        return screen_manager

if __name__ == '__main__':
    MyApp().run()