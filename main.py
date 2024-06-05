import PySimpleGUI as sg
import cv2
#Libreria para saber la resolucion del monitor del usuario
from screeninfo import get_monitors

# Obtener la resolución de la pantalla del usuario
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height


# Define el diseño de la ventana
layout = [
    [sg.Text("PyPhotos", size=(30, 1), font=("Helvetica", 25))],
    [sg.Image(filename="", key="-IMAGE-")],
    [sg.Button("Cargar imagen"), sg.Button("Salir")]
]

# Crea la ventana
window = sg.Window("Photoshop Casero", layout, size=(screen_width, screen_height))

# Bucle principal de eventos
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Salir":
        break
    elif event == "Cargar imagen":
        # Lógica para cargar una imagen usando OpenCV
        filename = sg.popup_get_file("Elija una imagen", file_types=(("Archivos JPEG", "*.jpg"), ("Archivos PNG", "*.png")))
        if filename:
            image = cv2.imread(filename)
            # Convierte la imagen de OpenCV a un formato que PySimpleGUI pueda mostrar
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            imgbytes = cv2.imencode(".png", image)[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes)

# Cierra la ventana
window.close()
