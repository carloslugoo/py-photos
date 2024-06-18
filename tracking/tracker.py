import cv2
import numpy as np

# Ruta al archivo de video
video_path = 'D:/Prog/py-photos/tracking/videos/cars2.mp4'  # Reemplaza con la ruta de tu video

# Abrir el archivo de video
cap = cv2.VideoCapture(video_path)

# Verificar si el archivo se abrió correctamente
if not cap.isOpened():
    print("Error al abrir el archivo de video")
    exit()

# Leer el primer frame
ret, frame = cap.read()

# Verificar si la lectura del frame fue exitosa
if not ret:
    print("Error al leer el primer frame")
    exit()

# Variables globales para manejar la selección del usuario
start_x, start_y = -1, -1
end_x, end_y = -1, -1
drawing = False
rectangle_selected = False
window_name = 'Selecciona el rectángulo'

# Función para manejar la selección del usuario
def draw_rectangle(event, x, y, flags, params):
    global start_x, start_y, end_x, end_y, drawing, rectangle_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            frame_copy = frame.copy()
            cv2.rectangle(frame_copy, (start_x, start_y), (x, y), (0, 255, 0), 2)
            cv2.imshow(window_name, frame_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_x, end_y = x, y
        rectangle_selected = True
        cv2.destroyWindow(window_name)  # Destruir la ventana después de seleccionar el rectángulo

# Mostrar la imagen original y permitir que el usuario seleccione un rectángulo
cv2.imshow(window_name, frame)
cv2.setMouseCallback(window_name, draw_rectangle)

# Esperar hasta que el usuario haya seleccionado el rectángulo
while not rectangle_selected:
    cv2.waitKey(1)

# Imprimir las coordenadas del rectángulo seleccionado
print(f"Coordenadas del rectángulo seleccionado: ({start_x}, {start_y}), ({end_x}, {end_y})")

# Inicializar el objeto para la sustracción de fondo MOG2
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Extraer la región de interés (ROI)
    roi = frame[start_y:end_y, start_x:end_x]

    # Convertir a escala de grises
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Aplicar un umbral alto para crear una máscara de las áreas brillantes
    _, bright_areas = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Invertir la máscara para excluir las áreas brillantes
    bright_areas_inv = cv2.bitwise_not(bright_areas)

    # Aplicar la sustracción de fondo en la región seleccionada
    fgmask = fgbg.apply(roi)

    # Aplicar la máscara de áreas no brillantes a la máscara de sustracción de fondo
    fgmask = cv2.bitwise_and(fgmask, bright_areas_inv)

    # Aplicar operaciones morfológicas para eliminar el ruido
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    
    # Encontrar contornos de los objetos en movimiento
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Filtrar contornos pequeños para eliminar el ruido
        if cv2.contourArea(contour) < 500:
            continue
        
        # Dibujar rectángulo alrededor del objeto en movimiento
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x + start_x, y + start_y), (x + w + start_x, y + h + start_y), (0, 255, 0), 2)
    
    # Mostrar el video con las detecciones
    cv2.imshow('Frame', frame)
    cv2.imshow('Foreground Mask', fgmask)
    
    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # Presionar Esc para salir
        break

cap.release()
cv2.destroyAllWindows()
