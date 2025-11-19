# 🚚 LogiPack – Sistema de Gestión de Entregas  
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)

Aplicación web desarrollada con **Flask** para la gestión integral de paquetes, transportes y entregas en la empresa logística *LogiPack*.

---

## 📦 Descripción General  
Este proyecto implementa una plataforma que permite a despachantes y repartidores gestionar el flujo completo de envíos: desde el registro del paquete hasta su entrega final. Incluye módulos para registro, asignación, salida y llegada de transportes.

---

## Funcionalidades Principales

### Selección de Sucursal  
- Pantalla inicial donde el **despachante** selecciona la sucursal donde operará.  
- Información organizada por:  
  - Número  
  - Provincia  
  - Localidad  
- Presentación mediante una lista desplegable ordenada.

### 📬 Registro de Paquetes  
- Formularios para la recepción de nuevos pedidos.  
- Datos registrados:  
  - Peso  
  - Nombre del destinatario  
  - Dirección  
- Generación automática de un **número único de envío**.  
- Estado inicial del paquete: **No entregado**.

### 🚛 Gestión de Transportes  
- Registro de **salida de transportes**:  
  - Selección de sucursal de destino  
  - Asignación de paquetes a trasladar  
  - Fecha y hora de salida  
- Registro de **llegada de transportes**:  
  - Actualización de fecha y hora mediante formulario de confirmación

### 📦➡️🧍‍♂️ Asignación de Paquetes y Entregas (Repartidores)  
- Asignación de paquetes a repartidores realizada por el despachante.  
- Acceso de repartidores mediante **número y DNI**.  
- Funcionalidades:  
  - Registrar la **entrega** de paquetes  
  - Registrar **observaciones** en caso de no entrega

---

## Tecnologías e Infraestructura

### Backend  
- **Flask** para manejo de rutas y peticiones (GET/POST).  
- **SQLAlchemy** para persistencia de datos.  
- Modelos del sistema:  
  - Sucursales  
  - Transportes  
  - Repartidores  
  - Paquetes  

### Organización del Proyecto  
- `app.py`: Lógica principal del sistema  
- `models/`: Modelos de base de datos  
- `config.py`: Configuración  
- `templates/`: Archivos HTML  
- `static/`: CSS y recursos estáticos  
- Estructura modular siguiendo buenas prácticas de desarrollo web

---

##  Diagrama del Sistema

```mermaid
flowchart TD

    subgraph Usuario
        D[Despachante]
        R[Repartidor]
    end

    subgraph Sistema_LogiPack
        A[Selección de Sucursal]
        B[Registro de Paquetes]
        C[Gestión de Transportes]
        D1[Asignación de Paquetes]
        E[Registro de Entregas]
    end

    subgraph Base_de_Datos
        S[Sucursales]
        P[Paquetes]
        T[Transportes]
        RP[Repartidores]
    end

    D --> A
    D --> B
    D --> C
    D --> D1

    R --> E

    A --> S
    B --> P
    C --> T
    D1 --> RP
    E --> P

