```markdown
# Concesionaria de Autos

Este proyecto es una aplicación web de tipo CRUD (Create, Read, Update, Delete)
diseñada para gestionar un concesionario de vehículos. La aplicación permite
realizar operaciones como registro de vehículos, gestión de alquileres y ventas,
y consulta de transacciones, utilizando Flask como framework backend y MySQL como base de datos.

---

## Funcionalidades

- **Gestión de vehículos**: 
  - Registro, edición y eliminación de vehículos en la base de datos.
  - Control del estado de los vehículos (disponible, alquilado, vendido).
- **Gestión de transacciones**:
  - Registro de alquileres y ventas.
  - Cálculo automático de costos según la duración del alquiler.
- **Alquiler de vehículos**:
  - Verificación de disponibilidad de vehículos.
  - Asignación de empleados para procesar reservas.
  - Actualización del estado del vehículo a "Alquilado".
- **Venta de vehículos**:
  - Registro de la transacción de venta.
  - Actualización del estado del vehículo a "Vendido".
- **Base de datos MySQL**:
  - Tablas optimizadas para manejar vehículos, clientes, empleados, transacciones y reservas.

---

## Requisitos del Sistema

Para ejecutar esta aplicación, necesitarás:

- **Python 3.12**: Versión mínima recomendada para compatibilidad.
- **MySQL**: Servidor de base de datos para almacenar la información.
- **Bibliotecas de Python**: Flask, mysql-connector-python, y otras que se incluyen en el archivo `requirements.txt`.

---

## Estructura del Proyecto

```plaintext
crud_concesionario/
│
├── app/                          # Código principal de la aplicación
│   ├── controllers/              # Controladores para manejar rutas y lógica del negocio
│   ├── views/                    # Controladores para manejar rutas
│   ├── models/                   # Modelos para interactuar con la base de datos
│   ├── templates/                # Plantillas HTML (frontend)
│   └── static/                   # Archivos estáticos (CSS, JS, imágenes)
│
├── database/                     # Conexión y configuración de la base de datos
│   └── respaldo.sql                     # Archivo para la conexión con MySQL
│
├── .gitignore                    # Archivos que no deben subirse al repositorio
├── requirements.txt              # Dependencias del proyecto
├── README.md                     # Descripción del proyecto
└── run.py                        # Archivo para iniciar la aplicación
```

---

## Instalación

Sigue estos pasos para configurar y ejecutar la aplicación en tu entorno local:

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/crud_concesionario.git
   cd crud_concesionario
   ```

2. **Crea y activa un entorno virtual**:
   - En Linux/Mac:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - En Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos**:
   - Crea una base de datos en MySQL.
   - Importa el archivo SQL (si existe) para inicializar las tablas:
     ```bash
     mysql -u tu_usuario -p nombre_base_datos < init.sql
     ```
   - Configura las credenciales de la base de datos en un archivo `.env`:
     ```plaintext
     DB_HOST=localhost
     DB_USER=tu_usuario
     DB_PASSWORD=tu_contraseña
     DB_NAME=nombre_base_datos
     ```

5. **Inicia la aplicación**:
   ```bash
   flask run
   ```

6. Accede a la aplicación en tu navegador:
   ```
   http://127.0.0.1:5001
   ```

---

## Uso de la Aplicación

### Registro de Vehículos
- Navega al módulo de "Gestión de Vehículos" para agregar, editar o eliminar vehículos.
- Verifica la disponibilidad y los detalles de cada vehículo.

### Alquiler de Vehículos
- Selecciona un vehículo disponible para alquilar.
- Ingresa las fechas de inicio y fin del alquiler.
- La aplicación calcula automáticamente el costo total del alquiler.

### Venta de Vehículos
- Cambia el estado de un vehículo a "Vendido" al realizar una venta.
- Registra la transacción correspondiente en la base de datos.

---

## Configuración de la Base de Datos

Este proyecto incluye un respaldo de la base de datos con la estructura y datos iniciales. Sigue estos pasos para importar el respaldo y configurar la base de datos:

### **1. Requisitos**
- MySQL instalado en tu máquina.
- MySQL Workbench (opcional, pero recomendado).

### **2. Importar el respaldo usando MySQL Workbench**
1. Abre MySQL Workbench y conéctate a tu servidor.
2. Ve a **Server > Data Import**.
3. Selecciona **`Import from Self-Contained File`** y elige el archivo:
   ```
   database/respaldo.sql
   ```
4. Selecciona la base de datos objetivo:
   - Si no tienes una base de datos, crea una nueva:
     ```sql
     CREATE DATABASE concesionaria_Autos;
     ```
   - Selecciona esta base de datos en el menú.
5. Haz clic en **Start Import**.
6. Verifica que las tablas y datos se hayan importado correctamente.

### **3. Importar el respaldo usando la línea de comandos**
1. Asegúrate de estar en la carpeta del proyecto.
2. Usa el siguiente comando:
   ```bash
   mysql -u tu_usuario -p concesionaria_Autos < database/respaldo.sql
   ```
3. Introduce tu contraseña cuando te la pida.

---

## Tecnologías Utilizadas

- **Backend**:
  - Flask: Framework web ligero en Python.
  - MySQL: Sistema de gestión de bases de datos relacional.

- **Frontend**:
  - HTML5, CSS3: Para las plantillas de usuario.
  - JavaScript: Para validaciones y cálculos en tiempo real.

- **Herramientas adicionales**:
  - Entorno virtual de Python (`venv`) para manejo de dependencias.
  - MySQL Workbench (opcional) para gestionar la base de datos.

---

## Licencia

Este proyecto está bajo la licencia **MIT**. Siéntete libre de usar, modificar y distribuir el código según los términos de la licencia.

---
