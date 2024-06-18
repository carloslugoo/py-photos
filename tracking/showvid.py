import cv2
from Rastreador import Rastreador

# Manos a la obra: creamos un objeto de la clase Rastreador
seguimiento = Rastreador()

video_path = "D:/Prog/py-photos/tracking/video.mp4"
# Realizamos la lectura del video
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: No se pudo abrir el archivo de video.")
    exit()

# Cambiando la detección de objetos con cámara estable
deteccion = cv2.createBackgroundSubtractorMOG2(history=10000, varThreshold=12)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame del video.")
        break
    frame = cv2.resize(frame, (1280, 720))  # Redimensionamos el video

    # Suponiendo que el video tiene una resolución de 1280x720
    zona = frame[360:720, 0:1280]


    # Creamos una máscara en los fotogramas con el fin de que nuestros objetos sean blancos
    mascara = deteccion.apply(zona)
    _, mascara = cv2.threshold(mascara, 254, 255, cv2.THRESH_BINARY)

    # Con este umbral buscamos los contornos
    contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Contornos detectados: {len(contornos)}")

    detecciones = []

    # Dibujamos todos los contornos en el frame, de azul claro con 2 de grosor
    for cont in contornos:
        # Eliminamos los contornos pequeños
        area = cv2.contourArea(cont)
        if area > 800:  # Si el área es mayor a 800 píxeles
            x, y, ancho, alto = cv2.boundingRect(cont)
            cv2.rectangle(zona, (x, y), (x + ancho, y + alto), (255, 255, 0), 3)  # Dibujamos el rectángulo
            detecciones.append([x, y, ancho, alto])  # Almacenamos la información de las detecciones
    print(f"Detecciones: {len(detecciones)}")

    # Seguimiento de los objetos
    info_id = seguimiento.rastreo(detecciones)
    for inf in info_id:
        x, y, ancho, alto, id = inf
        cv2.putText(zona, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
        cv2.rectangle(zona, (x, y), (x + ancho, y + alto), (255, 255, 0), 3)  # Dibujamos el rectángulo

    print(f"Info ID: {info_id}")
    cv2.imshow("Zona de Interes", zona)
    cv2.imshow("Carretera", frame)
    cv2.imshow("Mascara", mascara)
    key = cv2.waitKey(5)
    if key == 27:  # Presiona 'Esc' para salir
        break

cap.release()
cv2.destroyAllWindows()
