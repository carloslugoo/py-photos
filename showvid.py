import cv2

import os

# Ruta a la carpeta en Google Drive
folder_path = 'D:/Prog/py-photos/tracking/'

# Lista todos los archivos y carpetas en la ruta especificada
files = os.listdir(folder_path)

# Imprime los nombres de los archivos y carpetas
for file in files:
    print(file)

# Ruta del archivo de video
video_path = "/tracking/video.mp4"

# Captura de video
cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)

# Verifica si el archivo de video se abrió correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir el archivo de video.")
    exit()

# Loop para leer y mostrar los frames del video
while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Muestra el frame en una ventana llamada "Video"
    cv2.imshow("Video", frame)
    
    # Espera 25 ms y verifica si se presiona la tecla 'Esc' (código ASCII 27)
    if cv2.waitKey(25) & 0xFF == 27:
        break

# Libera el objeto VideoCapture y cierra todas las ventanas
cap.release()
cv2.destroyAllWindows()
