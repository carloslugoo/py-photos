import cv2

# Ruta al archivo de la imagen
image_path = 'D:/Prog/py-photos/tracking/images/images3.jpg'  # Reemplaza con la ruta de tu imagen

# Cargar la imagen
image = cv2.imread(image_path)

# Verificar si la imagen se cargó correctamente
if image is None:
    print("Error al cargar la imagen")
    exit()

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Cargar el clasificador en cascada de Haar para autos
car_cascade = cv2.CascadeClassifier('D:/Prog/py-photos/tracking/cars.xml')  
# Detectar autos en la imagen
cars = car_cascade.detectMultiScale(gray, 1.1, 1)

# Dibujar rectángulos alrededor de los autos detectados
for (x, y, w, h) in cars:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Mostrar la imagen con las detecciones
cv2.imshow('Detección de Vehículos', image)

# Esperar a que el usuario presione una tecla y cerrar la ventana
cv2.waitKey(0)
cv2.destroyAllWindows()