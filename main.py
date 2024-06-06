import PySimpleGUI as sg
import cv2
import imutils
from screeninfo import get_monitors
import os

# Establecer el tema elegido
sg.theme('Dark')  

# Obtener la resolución de la pantalla del usuario
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

image_width = int(screen_width * 0.50)
image_height = int(screen_height * 0.50)

# Define el diseño de la ventana
layout = [
    [
        sg.Column(
            [   
                [sg.Text("", key="-DETAILS-", size=(80, 2))],
                [sg.Text("Imagen Original", size=(80, 2))],
                [sg.Image(filename="", key="-IMAGE-ORIGINAL-", size=(image_width, image_height))]
            ],
            element_justification='center'
        ),
        sg.VSeparator(),
        sg.Column(
            [   
                [sg.Text("", key="-DETAILSMOD-", size=(80, 2))],
                [sg.Text("Imagen Modificada", size=(80, 2))],
                [sg.Image(filename="", key="-IMAGE-MODIFIED-", size=(image_width, image_height))]
            ],
            element_justification='center'
        )
    ],
    [
        sg.Column(
            [   
            [sg.Button("Cargar Imagen", size=(15, 1))], 
            [sg.Button("Guardar imagen", size=(15, 1))],
            [sg.Button("Deshacer cambios", size=(15, 1))],
            [sg.Button("Salir", size=(15, 1))]
            ],
        ),
        sg.Column(
            [   
            [sg.Text("Translación X:", size=(10, 1)), sg.InputText("0", key="-TRANSLATE-X-", size=(5, 1)),
            sg.Text("Translación Y:", size=(10, 1)), sg.InputText("0", key="-TRANSLATE-Y-", size=(5, 1)), 
            sg.Button("Aplicar translación", size=(15, 1))],
            [sg.Text("Rotación:", size=(10, 1)), sg.InputText("0", key="-ROTATE-ANGLE-", size=(5, 1)), 
            sg.Button("Aplicar rotación", size=(15, 1))],
            [sg.Text("Nueva altura:", size=(10, 1)), sg.InputText("0", key="-NEW-HEIGHT-", size=(5, 1)),
            sg.Text("Nuevo ancho:", size=(10, 1)), sg.InputText("0", key="-NEW-WIDTH-", size=(5, 1)), 
            sg.Button("Aplicar tamaño", size=(15, 1))],
            [sg.Button("Aplicar espejado", size=(15, 1))],
            [sg.Text("Recorte X1:", size=(10, 1)), sg.InputText("0", key="-CROP-X1-", size=(5, 1)),
            sg.Text("Y1:", size=(5, 1)), sg.InputText("0", key="-CROP-Y1-", size=(5, 1)),
            sg.Text("X2:", size=(5, 1)), sg.InputText("0", key="-CROP-X2-", size=(5, 1)),
            sg.Text("Y2:", size=(5, 1)), sg.InputText("0", key="-CROP-Y2-", size=(5, 1)),
            sg.Button("Aplicar recorte", size=(15, 1))]
            ],
            element_justification='right'
        ),
    ]
]

# Crea la ventana con el tamaño de la resolución de la pantalla del usuario
window = sg.Window("PyPhotoEditor", layout, size=(screen_width, screen_height))

# Imagen cargada
loaded_image = None
# Imagen modificada
modified_image = None

# Bucle principal de eventos
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Salir":
        break
    elif event == "Cargar Imagen":
        filename = sg.popup_get_file("Elija una imagen", file_types=(("Archivos JPEG", "*.jpg"), ("Archivos PNG", "*.png")))
        if filename:
            loaded_image = cv2.imread(filename)
            modified_image = loaded_image.copy()  # Copia de la imagen original
            image_resized = cv2.resize(loaded_image, (image_width, image_height), interpolation=cv2.INTER_AREA)
            imgbytes = cv2.imencode(".png", image_resized)[1].tobytes()
            window["-IMAGE-ORIGINAL-"].update(data=imgbytes)
            
            # Obtener detalles de la imagen
            height, width, channels = loaded_image.shape
            file_size = os.path.getsize(filename)  
            file_size_kb = file_size / 1024  # Convertir a kilobytes

            # Mostrar los detalles de la imagen
            details = f"Alto: {height}px, Ancho: {width}px, Canales: {channels}, Tamaño: {file_size_kb:.2f} KB"
            window["-DETAILS-"].update(details)
            
            # Mostrar la imagen modificada inicial (igual a la original)
            window["-IMAGE-MODIFIED-"].update(data=imgbytes)
    elif event == "Aplicar translación":
        if loaded_image is not None:
            try:
                # Obtener valores de translación
                translate_x = int(values["-TRANSLATE-X-"])
                translate_y = int(values["-TRANSLATE-Y-"])
                
                # Aplicar la translación a la imagen original
                modified_image = imutils.translate(modified_image, translate_x, translate_y)
                
                # Mostrar la imagen modificada
                modified_image_resized = cv2.resize(modified_image, (image_width, image_height), interpolation=cv2.INTER_AREA)
                imgbytes = cv2.imencode(".png", modified_image_resized)[1].tobytes()
                
                # Actualizar la ventana con la imagen modificada
                window["-IMAGE-MODIFIED-"].update(data=imgbytes)
                
                # Actualizar los detalles de la imagen modificada
                height, width, _ = modified_image.shape
                details = f"Alto: {height}px, Ancho: {width}px"
                window["-DETAILSMOD-"].update(details)
            except ValueError:
                sg.popup("Por favor, ingrese valores válidos para la translación.")
    elif event == "Aplicar rotación":
        if loaded_image is not None:
            try:
                # Obtener el ángulo de rotación
                angle = int(values["-ROTATE-ANGLE-"])
                
                # Obtener el centro de la imagen
                (h, w) = loaded_image.shape[:2]
                center = (w // 2, h // 2)
                
                # Obtener la matriz de rotación
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                
                # Aplicar la rotación a la imagen original
                modified_image = cv2.warpAffine(modified_image, M, (w, h))
                
                # Mostrar la imagen modificada
                modified_image_resized = cv2.resize(modified_image, (image_width, image_height), interpolation=cv2.INTER_AREA)
                imgbytes = cv2.imencode(".png", modified_image_resized)[1].tobytes()
                
                # Actualizar la ventana con la imagen modificada
                window["-IMAGE-MODIFIED-"].update(data=imgbytes)
                
                # Actualizar los detalles de la imagen modificada
                height, width, _ = modified_image.shape
                details = f"Alto: {height}px, Ancho: {width}px"
                window["-DETAILSMOD-"].update(details)
            except ValueError:
                sg.popup("Por favor, ingrese valores válidos para la rotación.")
    elif event == "Aplicar tamaño":
        if loaded_image is not None:
            try:
                # Obtener los valores de ancho y alto especificados por el usuario
                new_width = int(values["-NEW-WIDTH-"])
                new_height = int(values["-NEW-HEIGHT-"])
                
                # Aplicar el cambio de tamaño a la imagen modificada
                modified_image = cv2.resize(modified_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
                
                # Mostrar la imagen modificada
                modified_image_resized = cv2.resize(modified_image, (image_width, image_height), interpolation=cv2.INTER_AREA)
                imgbytes = cv2.imencode(".png", modified_image_resized)[1].tobytes()
                window["-IMAGE-MODIFIED-"].update(data=imgbytes)
                
                # Actualizar los detalles de la imagen modificada
                height, width, _ = modified_image.shape
                details = f"Alto: {height}px, Ancho: {width}px"
                window["-DETAILSMOD-"].update(details)
            except ValueError:
                sg.popup("Por favor, ingrese valores válidos para el ancho y el alto.")
    elif event == "Aplicar espejado":
        if loaded_image is not None:
            # Aplicar espejado horizontal a la imagen modificada
            modified_image = cv2.flip(modified_image, 1)
            
            # Mostrar la imagen modificada
            modified_image_resized = cv2.resize(modified_image, (image_width, image_height), interpolation=cv2.INTER_AREA)
            imgbytes = cv2.imencode(".png", modified_image_resized)[1].tobytes()
            window["-IMAGE-MODIFIED-"].update(data=imgbytes)
            
            # Actualizar los detalles de la imagen modificada
            height, width, _ = modified_image.shape
            details = f"Alto: {height}px, Ancho: {width}px"
            window["-DETAILSMOD-"].update(details)
    elif event == "Aplicar recorte":
        if loaded_image is not None:
            try:
                # Obtener los valores de las coordenadas de recorte
                x1 = int(values["-CROP-X1-"])
                y1 = int(values["-CROP-Y1-"])
                x2 = int(values["-CROP-X2-"])
                y2 = int(values["-CROP-Y2-"])
                
                # Aplicar el recorte a la imagen modificada
                modified_image = modified_image[y1:y2, x1:x2]
                
                # Mostrar la imagen modificada
                modified_image_resized = cv2.resize(modified_image, (image_width, image_height), interpolation=cv2.INTER_AREA)
                imgbytes = cv2.imencode(".png", modified_image_resized)[1].tobytes()
                window["-IMAGE-MODIFIED-"].update(data=imgbytes)
                
                # Actualizar los detalles de la imagen modificada
                height, width, _ = modified_image.shape
                details = f"Alto: {height}px, Ancho: {width}px"
                window["-DETAILSMOD-"].update(details)
            except ValueError:
                sg.popup("Por favor, ingrese valores válidos para el recorte.")
    elif event == "Deshacer cambios":
        if loaded_image is not None:
            # Restaurar la imagen modificada a la original
            modified_image = loaded_image.copy()
            image_resized = cv2.resize(modified_image, (image_width, image_height), interpolation=cv2.INTER_AREA)
            imgbytes = cv2.imencode(".png", image_resized)[1].tobytes()
            window["-IMAGE-MODIFIED-"].update(data=imgbytes)
    elif event == "Guardar imagen":
        if modified_image is not None:
            save_filename = sg.popup_get_file("Guardar imagen como", save_as=True, file_types=(("Archivos PNG", "*.png"), ("Archivos JPEG", "*.jpg")))
            if save_filename:
                # Guardar la imagen modificada
                cv2.imwrite(save_filename, modified_image)
                sg.popup("Imagen guardada con éxito.")
    
# Cierra la ventana
window.close()
