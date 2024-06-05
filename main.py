import PySimpleGUI as sg
import cv2
from screeninfo import get_monitors
import os


sg.theme('Dark')  

# Obtener la resolución de la pantalla del usuario
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

image_width = int(screen_width * 0.85)
image_height = int(screen_height * 0.85)

# Define el diseño de la ventana
layout = [
    [sg.Text("Photoshop Casero", size=(30, 1), font=("Helvetica", 25), justification='center')],
    [
        sg.Column(
            [
                [sg.Image(filename="", key="-IMAGE-", size=(image_width, image_height))],
                [sg.Text("", key="-DETAILS-", size=(80, 2))]
            ],
            element_justification='center'
        ),
        sg.Column(
            [
                [sg.Button("Cargar Imagen", size=(15, 1))],
                [sg.VPush()], 
                [sg.Button("Salir", size=(15, 1))]
            ],
            vertical_alignment='top',
            element_justification='center',
        )
    ]
]


window = sg.Window("Photoshop Casero", layout, size=(screen_width, screen_height))

# Bucle principal de eventos
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Salir":
        break
    elif event == "Cargar Imagen":
        filename = sg.popup_get_file("Elija una imagen", file_types=(("Archivos JPEG", "*.jpg"), ("Archivos PNG", "*.png")))
        if filename:
            image = cv2.imread(filename)
            # Redimensionar la imagen para que ocupe el 70% de la pantalla
            image = cv2.resize(image, (image_width, image_height), interpolation=cv2.INTER_AREA)
            imgbytes = cv2.imencode(".png", image)[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes)
            
            # Obtener detalles de la imagen
            height, width, channels = image.shape
            file_size = os.path.getsize(filename)  
            file_size_kb = file_size / 1024  # Convertir a kilobytes

            # Mostrar los detalles de la imagen
            details = f"Alto: {height}px, Ancho: {width}px, Canales: {channels}, Tamaño: {file_size_kb:.2f} KB"
            window["-DETAILS-"].update(details)

# Cierra la ventana
window.close()
