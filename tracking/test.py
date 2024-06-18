import cv2

# Inicializar el objeto para la sustracción de fondo MOG2
fgbg = cv2.createBackgroundSubtractorMOG2()

# Capturar video desde la cámara
cap = cv2.VideoCapture('D:/Prog/py-photos/tracking/video1.mp4')  # Puedes cambiar 'video.mp4' por 0 para capturar desde la cámara en vivo

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Aplicar la sustracción de fondo
    fgmask = fgbg.apply(frame)
    
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
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Mostrar el video con las detecciones
    cv2.imshow('Frame', frame)
    cv2.imshow('Foreground Mask', fgmask)
    
    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # Presionar Esc para salir
        break

cap.release()
cv2.destroyAllWindows()
