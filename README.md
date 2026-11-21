

CAMPUSVOZ

Prototipo de navegación universitaria accesible | Hackatón
========================================================

1. DESCRIPCIÓN

CampusVoz es un prototipo de aplicación web orientado a mejorar la
accesibilidad y la orientación dentro del entorno universitario, especialmente
para personas con discapacidad visual.

La aplicación permite seleccionar destinos del campus y consultar su ubicación
o recorrido en un mapa. Se diseñó considerando el uso de controles accesibles
y la posibilidad de incorporar indicaciones auditivas y reportes de incidencias.

Este proyecto es un prototipo de hackatón. No reemplaza un sistema de movilidad
asistida ni garantiza rutas interiores seguras o navegación autónoma para
personas ciegas.

2. FUNCIONES DEL PROTOTIPO

- Selección de destinos universitarios mediante botones.
- Ubicaciones de referencia: Biblioteca, Casino, Entrada 1 y Entrada 2.
- Visualización de mapas/rutas según la integración implementada.
- Interfaz desarrollada con Flet (Python).
- Consideraciones de accesibilidad para lectores de pantalla como TalkBack.
- Integración técnica con Supabase para almacenamiento de datos, según las
  funciones configuradas en el proyecto.
- Integración con servicios HTTP mediante FastAPI, si se ejecuta el servidor.

Nota: el comportamiento exacto de audio, GPS, reportes y rutas depende de los
módulos efectivamente integrados y de los permisos del dispositivo/navegador.

3. TECNOLOGÍAS

Python 3
Flet
Flet Map
Flet Geolocator
Flet Audio Recorder
SpeechRecognition
OpenStreetMap
Valhalla Routing API

4. REQUISITOS PREVIOS

Antes de ejecutar el proyecto, es necesario contar con:

Python 3 instalado.
pip, el gestor de paquetes de Python.
Conexión a Internet.
Un micrófono para utilizar las funciones de reconocimiento de voz.

Se recomienda utilizar Python 3.13, que fue la versión utilizada durante el desarrollo.



------ INSTALACIÓN ----------


1. DESCARGAR EL REPOSITORIO

Clonar el repositorio desde GitHub:

git clone https://github.com/tofiaxd/hackaton.git

También es posible descargar el proyecto directamente como archivo ZIP desde GitHub.



2. ABRIR CARPETA DEL PROYECTO

Abrir una terminal y posicionarse en la carpeta principal del proyecto:

cd ruta\de\la\carpeta\campus_voz



3. CREAR ENTORNO VIRTUAL (recomendado)

Para mantener las dependencias del proyecto separadas de otras instalaciones de Python, se recomienda crear un entorno virtual:

py -m venv venv

Activarlo con:

.\venv\Scripts\Activate.ps1

Si se utiliza CMD en lugar de PowerShell:

venv\Scripts\activate.bat



4. INSTALAR DEPENDENCIAS

El proyecto incluye un archivo requirements.txt con las dependencias necesarias.

Para instalarlas, ejecutar:

py -m pip install -r requirements.txt



5. EJECUTAR

Una vez instaladas las dependencias, ejecutar:

flet run

La aplicación debería iniciarse y mostrar la pantalla de inicio de sesión.


------------ CONSIDERACIONES -------------

Para utilizar el reconocimiento de voz, es necesario permitir el acceso al micrófono.
Las funciones de reconocimiento de voz requieren conexión a Internet.
El mapa utiliza OpenStreetMap y el cálculo de rutas peatonales utiliza Valhalla.
La precisión de la ubicación GPS puede variar según el dispositivo y el entorno.
Los reportes de alertas se mantienen durante la ejecución de la aplicación; no cuentan con almacenamiento permanente.
