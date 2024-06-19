## Detección de Vehículos en Video con Python (OpenCV)
Este proyecto utiliza OpenCV para detectar vehículos en movimiento en un video, excluyendo las luces de los autos en escenas nocturnas.
El usuario puede seleccionar una región de interés (ROI) en el primer cuadro del video, y el programa realizará la detección de vehículos dentro de esta región. <br>
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
pip install opencv-python PySimpleGUI==4.60.5
```
## Uso
Puedes utilizar cualquier video con una cámara estable. <br>
Ejecutar gui.py
```bash
cd tracking
python gui.py
```
## Resultados
Selección de punto de intéres:
![image](https://github.com/carloslugoo/python-cv/assets/112581880/0e879dee-582e-4034-b8cd-4037326550fe)
Detección de los vehiculos:
![image](https://github.com/carloslugoo/python-cv/assets/112581880/fdc241f7-0c90-4028-8bec-29bccf9eabc5)
