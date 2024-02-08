# IVA Rate Notifier 🌍💼

Este proyecto proporciona un script de Python diseñado para ayudar a negocios y contadores a monitorear y notificar cambios en las tasas de IVA para diferentes países. Utiliza la API de Vatstack para obtener las tasas actuales de IVA y compara estos datos con registros previos para detectar cambios. En caso de detectarse cambios, el script envía una notificación por correo electrónico. 📧

## Pre-requisitos 📋
Antes de utilizar este script, necesitas registrarte en [Vatstack](https://vatstack.com) para obtener tu API Key. Esta clave te permitirá realizar peticiones a la API para obtener las tasas de IVA actuales.

## Instalación 🛠️
Para usar este script, necesitarás Python 3.6 o superior. Primero, clona este repositorio en tu máquina local:

#### git clone https://github.com/<tu_usuario>/IVA-Rate-Notifier.git
#### cd IVA-Rate-Notifier


Instala las dependencias necesarias:
#### pip install -r requirements.txt

## Configuración ⚙️
Antes de ejecutar el script, necesitarás configurar algunas variables:

Copia config.sample.json a config.json y rellena tus credenciales de API y configuración de correo SMTP.
Asegúrate de tener un archivo tasas_iva.json en el formato correcto (puedes encontrar un ejemplo en el repositorio).

## Uso 🚀
Para ejecutar el script, simplemente corre:
#### python3 main.py

## Contribuir 🤝
Las contribuciones son bienvenidas. Si tienes sugerencias para mejorar este proyecto, no dudes en crear un pull request o abrir un issue.

## Licencia 📄
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.


Este `README` proporciona una guía clara y concisa sobre cómo instalar, configurar y usar tu proyecto, además de invitar a contribuciones, todo ello reforzado con el uso de iconos para hacerlo más visual y amigable para el usuario.

