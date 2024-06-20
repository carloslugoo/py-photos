## Detección de Vehículos en Video y Imagenes con Python (OpenCV-TensorFlow)
Este proyecto utiliza OpenCV para detectar vehículos en movimiento en un video y tambien la detección de vehiculos en imagenes, excluyendo las luces de los autos en escenas nocturnas.
En el caso del video, el usuario puede seleccionar una región de interés (ROI) en el primer cuadro del video, y el programa realizará la detección de vehículos dentro de esta región. 
En caso de imagenes, solo es necesario cargar la imagen correspondiente.<br>
## Requisitos <br>
Python 3.x <br>
OpenCV <br>
## Instalación
Clone the project
```bash
  git clone https://github.com/carloslugoo/python-cv.git
```
Dependencias
```bash
pip install opencv-python
pip install PySimpleGUI==4.60.5
pip install tensorflow #Solo GPU
```
## Uso
Puedes utilizar cualquier video con una cámara estable. Ejemplos en el repositorio. <br>
`En caso de disponer de GPU:` <br>
Descarga el modelo ssd_mobilenet_v2 y sus archivos asociados desde [Tensorflow Detection Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md) y colócalo en la carpeta models. <br>
- Ejecutar gui.py 
```bash
cd tracking
python gui.py
```
`Sino:`
```bash
cd tracking
python gui-nogpu.py
```
## Resultados
Selección de punto de intéres:
![image](https://github.com/carloslugoo/python-cv/assets/112581880/0e879dee-582e-4034-b8cd-4037326550fe)
Detección de los vehiculos en video:
![image](https://github.com/carloslugoo/python-cv/assets/112581880/fdc241f7-0c90-4028-8bec-29bccf9eabc5)
Detección de los vehiculos en imagenes:
![image](https://github.com/carloslugoo/python-cv/assets/112581880/5587dab6-f5f7-4134-85d7-e9f87323bf64)
Pequeña interfaz para seleccionar los archivos: <br>
![image](https://github.com/carloslugoo/python-cv/assets/112581880/ab8465b8-31e1-4615-b6fe-c63ebee2422b)

