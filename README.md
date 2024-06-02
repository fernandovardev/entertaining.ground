# Proyecto FastAPI

## Introducción
Bienvenido al proyecto FastAPI. Este proyecto proporciona una API para gestionar afinidades mágicas, grimorios y solicitudes de estudiantes. Este README te guiará a través de la configuración y uso de la API.

## Instalación

1. **Clonar el Repositorio:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Crear un Entorno Virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Ejecutar la Aplicación:**
    ```bash
    uvicorn src.main:app --reload
    ```

## Endpoints de la API

### 1. Afinidades Mágicas

#### Obtener todas las Afinidades Mágicas
- **Endpoint:** `/api/afinidades/`
- **Método:** `GET`
- **Descripción:** Obtiene todas las afinidades mágicas disponibles en la base de datos.
- **Respuesta:**
  ```json
  [
    {
      "id": 1,
      "nombre": "Fuego"
    },
    ...
  ]
  ```

#### Crear Nueva Afinidad Mágica
- **Endpoint:** `/api/afinidades/`
- **Método:** `POST`
- **Descripción:** Crea una nueva afinidad mágica con los datos proporcionados.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "id": 2,
    "nombre": "Agua"
  }
  ```
- **Respuesta:**
  ```json
  {
    "id": 2,
    "nombre": "Agua"
  }
  ```

#### Obtener Afinidad Mágica por ID
- **Endpoint:** `/api/afinidades/{afinidad_id}`
- **Método:** `GET`
- **Descripción:** Obtiene una afinidad mágica por su ID único.
- **Parámetros:**
  - `afinidad_id` (entero, requerido): ID de la afinidad mágica.
- **Respuesta:**
  ```json
  {
    "id": 1,
    "nombre": "Fuego"
  }
  ```

#### Actualizar Afinidad Mágica por ID
- **Endpoint:** `/api/afinidades/{afinidad_id}`
- **Método:** `PUT`
- **Descripción:** Actualiza los detalles de una afinidad mágica existente por su ID.
- **Parámetros:**
  - `afinidad_id` (entero, requerido): ID de la afinidad mágica.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "id": 1,
    "nombre": "Fuego"
  }
  ```
- **Respuesta:**
  ```json
  {
    "id": 1,
    "nombre": "Fuego"
  }
  ```

### 2. Grimorios

#### Obtener todos los Grimorios
- **Endpoint:** `/api/grimorios/`
- **Método:** `GET`
- **Descripción:** Obtiene todos los grimorios disponibles en la base de datos.
- **Respuesta:**
  ```json
  [
    {
      "id": 1,
      "tipo": "Grimorio de Fuego",
      "rareza": "Raro",
      "peso": 3
    },
    ...
  ]
  ```

#### Crear Nuevo Grimorio
- **Endpoint:** `/api/grimorios/`
- **Método:** `POST`
- **Descripción:** Crea un nuevo grimorio con los datos proporcionados.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "tipo": "Grimorio de Agua",
    "rareza": "Común",
    "peso": 2
  }
  ```
- **Respuesta:**
  ```json
  {
    "id": 2,
    "tipo": "Grimorio de Agua",
    "rareza": "Común",
    "peso": 2
  }
  ```

#### Obtener Grimorio por ID
- **Endpoint:** `/api/grimorios/{grimorio_id}`
- **Método:** `GET`
- **Descripción:** Obtiene un grimorio por su ID único.
- **Parámetros:**
  - `grimorio_id` (entero, requerido): ID del grimorio.
- **Respuesta:**
  ```json
  {
    "id": 1,
    "tipo": "Grimorio de Fuego",
    "rareza": "Raro",
    "peso": 3
  }
  ```

#### Actualizar Grimorio por ID
- **Endpoint:** `/api/grimorios/{grimorio_id}`
- **Método:** `PUT`
- **Descripción:** Actualiza los detalles de un grimorio existente por su ID.
- **Parámetros:**
  - `grimorio_id` (entero, requerido): ID del grimorio.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "tipo": "Grimorio de Agua",
    "rareza": "Común",
    "peso": 2
  }
  ```
- **Respuesta:**
  ```json
  {
    "id": 2,
    "tipo": "Grimorio de Agua",
    "rareza": "Común",
    "peso": 2
  }
  ```

### 3. Solicitudes

#### Obtener todas las Solicitudes
- **Endpoint:** `/api/solicitudes/`
- **Método:** `GET`
- **Descripción:** Obtiene todas las solicitudes con opción de paginación.
- **Parámetros:**
  - `skip` (entero, opcional): Número de registros a omitir (por defecto 0).
  - `limit` (entero, opcional): Número máximo de registros a devolver (por defecto 100).
- **Respuesta:**
  ```json
  [
    {
      "id": 1,
      "nombre": "Gandalf",
      "apellido": "El",
      "identificacion": "1234567890",
      "edad": 25,
      "afinidad_magica_id": 1,
      "status_id": 1,
      "assignments": []
    },
    ...
  ]
  ```

#### Crear Nueva Solicitud
- **Endpoint:** `/api/solicitudes/`
- **Método:** `POST`
- **Descripción:** Crea una nueva solicitud con los datos proporcionados.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "nombre": "Gandalf",
    "apellido": "El",
    "identificacion": "1234567890",
    "edad": 25,
    "afinidad_magica_id": 1
  }
  ```
- **Respuesta:**
  ```json
  {
    "id": 1,
    "nombre": "Gandalf",
    "apellido": "El",
    "identificacion": "1234567890",
    "edad": 25,
    "afinidad_magica_id": 1,
    "status_id": 1,
    "assignments": []
  }
  ```

#### Actualizar Solicitud por ID
- **Endpoint:** `/api/solicitudes/{id}`
- **Método:** `PUT`
- **Descripción:** Actualiza los detalles de una solicitud existente por su ID.
- **Parámetros:**
  - `id` (entero, requerido): ID de la solicitud.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "nombre": "Maria",
    "apellido": "Gomez",
    "identificacion": "0987654321",
    "edad": 30,
    "afinidad_magica_id": 2
  }
  ```
- **Respuesta:**
  ```json
  {
    "id": 1,
    "nombre": "Maria",
    "apellido": "Gomez",
    "identificacion": "0987654321",
    "edad": 30,
    "afinidad_magica_id": 2,
    "status_id": 1,
    "assignments": []
  }
  ```

#### Eliminar Solicitud por ID
- **Endpoint:** `/api/solicitudes/{id}`
- **Método:** `DELETE`
- **Descripción:** Elimina una solicitud existente por su ID.
- **Parámetros:**
  - `id` (entero, requerido): ID de la solicitud.
- **Respuesta:**
  ```json
  {
    "id": 1,
    "nombre": "Gandalf",
    "apellido": "El",
    "identificacion": "1234567890",
    "edad": 25,
    "afinidad_magica_id": 1,
    "status_id": 1,
    "assignments": []
  }
  ```

#### Actualizar Estado de la Solicitud
- **Endpoint:** `/api/solicitudes/{id}/estatus`
- **Método:** `PATCH`
- **Descripción:** Actualiza el estado de una solicitud existente por su ID.
- **Parámetros:**
  - `id` (entero, requerido): ID de la solicitud.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "status": 2
  }
  ```
- **Respuesta:**
  ```json
  {
   

 "id": 1,
    "nombre": "Gandalf",
    "apellido": "El",
    "identificacion": "1234567890",
    "edad": 25,
    "afinidad_magica_id": 1,
    "status_id": 2,
    "assignments": []
  }
  ```

### 4. Endpoints Misceláneos

#### Bienvenido al Proyecto
- **Endpoint:** `/`
- **Método:** `GET`
- **Descripción:** Página de bienvenida del proyecto.
- **Respuesta:**
  ```html
  <html>
    <body>
      <h1>Welcome to the Project</h1>
    </body>
  </html>
  ```

#### Autenticación por Acertijo
- **Endpoint:** `/riddle`
- **Método:** `GET`
- **Descripción:** Página de autenticación mediante acertijo.
- **Respuesta:**
  ```html
  <html>
    <body>
      <h1>Riddle Authentication</h1>
      <form method="post">
        <label for="answer">Answer:</label>
        <input type="text" id="answer" name="answer">
        <input type="submit" value="Submit">
      </form>
    </body>
  </html>
  ```

- **Endpoint:** `/riddle`
- **Método:** `POST`
- **Descripción:** Validación de respuesta al acertijo.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "answer": "respuesta"
  }
  ```
- **Respuesta:**
  ```html
  <html>
    <body>
      <h1>Congratulations! You've solved the riddle.</h1>
    </body>
  </html>
  ```

#### Fallo en el Acertijo
- **Endpoint:** `/riddle-fail`
- **Método:** `GET`
- **Descripción:** Página de fallo en la autenticación mediante acertijo.
- **Respuesta:**
  ```html
  <html>
    <body>
      <h1>Failure! Try again.</h1>
    </body>
  </html>
  ```

#### Página Segura
- **Endpoint:** `/secure`
- **Método:** `GET`
- **Descripción:** Página segura del proyecto.
- **Respuesta:**
  ```html
  <html>
    <body>
      <h1>Secure Page</h1>
    </body>
  </html>
  ```

#### Página de Felicitaciones
- **Endpoint:** `/congratulations/{solicitud_id}`
- **Método:** `GET`
- **Descripción:** Página de felicitación después de resolver un acertijo.
- **Parámetros:**
  - `solicitud_id` (entero, requerido): ID de la solicitud.
- **Respuesta:**
  ```html
  <html>
    <body>
      <h1>Congratulations! Your request has been approved.</h1>
    </body>
  </html>
  ```
```