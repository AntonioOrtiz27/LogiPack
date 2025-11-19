🚚 LogiPack – Sistema de Gestión de Entregas

Aplicación web desarrollada con Flask para la gestión integral de paquetes, transportes y entregas en la empresa logística LogiPack.

📦 Descripción General

Este proyecto implementa una plataforma que permite a despachantes y repartidores gestionar el flujo completo de envíos: desde el registro del paquete hasta su entrega final. Incluye módulos para registro, asignación, salida y llegada de transportes.

⭐ Funcionalidades Principales
🏢 Selección de Sucursal

Pantalla inicial donde el despachante selecciona la sucursal en la que operará.

Información organizada por número, provincia y localidad, disponible en una lista desplegable.

📬 Registro de Paquetes

Formularios para la recepción de nuevos pedidos.

Se registran: peso, nombre del destinatario y dirección.

Generación automática de un número único de envío.

Los paquetes se marcan inicialmente como no entregados.

🚛 Gestión de Transportes

Módulo para registrar la salida de transportes:

Selección de sucursal de destino.

Asignación de paquetes a trasladar.

Registro de fecha y hora de salida.

Módulo para registrar la llegada del transporte:

Actualización de fecha y hora mediante formulario de confirmación.

📦➡️🧍‍♂️ Asignación de Paquetes y Entregas (Repartidores)

El despachante puede asignar paquetes a repartidores.

Los repartidores acceden con número y DNI para:

Registrar la entrega de los paquetes.

Indicar observaciones en caso de no poder entregar.

🛠️ Tecnologías e Infraestructura
🔧 Backend

Flask para la gestión de rutas y manejo de solicitudes (GET/POST).

SQLAlchemy para la persistencia de datos mediante modelos que representan:

Sucursales

Transportes

Repartidores

Paquetes

🗂️ Organización del Proyecto

app.py: lógica principal de la aplicación.

Modelos: representan las entidades del sistema.

config.py: parámetros de configuración.

templates/: vistas HTML.

static/: archivos CSS y otros recursos.

Estructura modular siguiendo buenas prácticas de desarrollo web.
