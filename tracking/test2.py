import cv2

# Ruta al archivo de video
video_path = 'D:/Prog/py-photos/tracking/video1.mp4'  # Reemplaza con la ruta de tu video

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

# Función para manejar la selección del usuario
def draw_rectangle(event, x, y, flags, params):
    global start_x, start_y, end_x, end_y, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            frame_copy = frame.copy()
            cv2.rectangle(frame_copy, (start_x, start_y), (x, y), (0, 255, 0), 2)
            cv2.imshow('Selecciona el rectángulo', frame_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_x, end_y = x, y
        print(f"Coordenadas del rectángulo seleccionado: ({start_x}, {start_y}), ({end_x}, {end_y})")

# Mostrar la imagen original y permitir que el usuario seleccione un rectángulo
cv2.imshow('Selecciona el rectángulo', frame)
cv2.setMouseCallback('Selecciona el rectángulo', draw_rectangle)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Presiona 'q' para salir
        break
    elif key == ord('c'):  # Presiona 'c' para continuar con el rectángulo seleccionado
        break

cv2.destroyAllWindows()

# Liberar los recursos
cap.release()
