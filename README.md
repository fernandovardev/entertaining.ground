```markdown
# FastAPI Project

## Introduction
Welcome to the FastAPI project. This project provides an API for managing magical affinities, grimoires, and student requests. This README will guide you through setting up and using the API.

## Installation

1. **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application:**
    ```bash
    uvicorn src.main:app --reload
    ```

## API Endpoints

### 1. Afinidades Mágicas

#### Obtener todas las Afinidades Mágicas
- **Endpoint:** `/api/afinidades/`
- **Method:** `GET`
- **Description:** Obtiene todas las afinidades mágicas disponibles en la base de datos.
- **Response:**
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
- **Method:** `POST`
- **Description:** Crea una nueva afinidad mágica con los datos proporcionados.
- **Request Body:**
  ```json
  {
    "id": 2,
    "nombre": "Agua"
  }
  ```
- **Response:**
  ```json
  {
    "id": 2,
    "nombre": "Agua"
  }
  ```

#### Obtener Afinidad Mágica por ID
- **Endpoint:** `/api/afinidades/{afinidad_id}`
- **Method:** `GET`
- **Description:** Obtiene una afinidad mágica por su ID único.
- **Parameters:**
  - `afinidad_id` (integer, required): ID de la afinidad mágica.
- **Response:**
  ```json
  {
    "id": 1,
    "nombre": "Fuego"
  }
  ```

#### Actualizar Afinidad Mágica por ID
- **Endpoint:** `/api/afinidades/{afinidad_id}`
- **Method:** `PUT`
- **Description:** Actualiza los detalles de una afinidad mágica existente por su ID.
- **Parameters:**
  - `afinidad_id` (integer, required): ID de la afinidad mágica.
- **Request Body:**
  ```json
  {
    "id": 1,
    "nombre": "Fuego"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "nombre": "Fuego"
  }
  ```

### 2. Grimorios

#### Obtener todos los Grimorios
- **Endpoint:** `/api/grimorios/`
- **Method:** `GET`
- **Description:** Obtiene todos los grimorios disponibles en la base de datos.
- **Response:**
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
- **Method:** `POST`
- **Description:** Crea un nuevo grimorio con los datos proporcionados.
- **Request Body:**
  ```json
  {
    "tipo": "Grimorio de Agua",
    "rareza": "Común",
    "peso": 2
  }
  ```
- **Response:**
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
- **Method:** `GET`
- **Description:** Obtiene un grimorio por su ID único.
- **Parameters:**
  - `grimorio_id` (integer, required): ID del grimorio.
- **Response:**
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
- **Method:** `PUT`
- **Description:** Actualiza los detalles de un grimorio existente por su ID.
- **Parameters:**
  - `grimorio_id` (integer, required): ID del grimorio.
- **Request Body:**
  ```json
  {
    "tipo": "Grimorio de Agua",
    "rareza": "Común",
    "peso": 2
  }
  ```
- **Response:**
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
- **Method:** `GET`
- **Description:** Obtiene todas las solicitudes con opción de paginación.
- **Parameters:**
  - `skip` (integer, optional): Número de registros a omitir (por defecto 0).
  - `limit` (integer, optional): Número máximo de registros a devolver (por defecto 100).
- **Response:**
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
- **Method:** `POST`
- **Description:** Crea una nueva solicitud con los datos proporcionados.
- **Request Body:**
  ```json
  {
    "nombre": "Gandalf",
    "apellido": "El",
    "identificacion": "1234567890",
    "edad": 25,
    "afinidad_magica_id": 1
  }
  ```
- **Response:**
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
- **Method:** `PUT`
- **Description:** Actualiza los detalles de una solicitud existente por su ID.
- **Parameters:**
  - `id` (integer, required): ID de la solicitud.
- **Request Body:**
  ```json
  {
    "nombre": "Maria",
    "apellido": "Gomez",
    "identificacion": "0987654321",
    "edad": 30,
    "afinidad_magica_id": 2
  }
  ```
- **Response:**
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
- **Method:** `DELETE`
- **Description:** Elimina una solicitud existente por su ID.
- **Parameters:**
  - `id` (integer, required): ID de la solicitud.
- **Response:**
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
- **Method:** `PATCH`
- **Description:** Actualiza el estado de una solicitud existente por su ID.
- **Parameters:**
  - `id` (integer, required): ID de la solicitud.
- **Request Body:**
  ```json
  {
    "status": 2
  }
  ```
- **Response:**
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

### 4. Miscellaneous Endpoints

#### Welcome to the Project
- **

Endpoint:** `/`
- **Method:** `GET`
- **Description:** Página de bienvenida del proyecto.
- **Response:**
  ```html
  <html>
    <body>
      <h1>Welcome to the Project</h1>
    </body>
  </html>
  ```

#### Riddle Authentication
- **Endpoint:** `/riddle`
- **Method:** `GET`
- **Description:** Página de autenticación mediante acertijo.
- **Response:**
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
- **Method:** `POST`
- **Description:** Validación de respuesta al acertijo.
- **Request Body:**
  ```json
  {
    "answer": "respuesta"
  }
  ```
- **Response:**
  ```html
  <html>
    <body>
      <h1>Congratulations! You've solved the riddle.</h1>
    </body>
  </html>
  ```

#### Riddle Failure
- **Endpoint:** `/riddle-fail`
- **Method:** `GET`
- **Description:** Página de fallo en la autenticación mediante acertijo.
- **Response:**
  ```html
  <html>
    <body>
      <h1>Failure! Try again.</h1>
    </body>
  </html>
  ```

#### Secure Page
- **Endpoint:** `/secure`
- **Method:** `GET`
- **Description:** Página segura del proyecto.
- **Response:**
  ```html
  <html>
    <body>
      <h1>Secure Page</h1>
    </body>
  </html>
  ```

#### Congratulations Page
- **Endpoint:** `/congratulations/{solicitud_id}`
- **Method:** `GET`
- **Description:** Página de felicitación después de resolver un acertijo.
- **Parameters:**
  - `solicitud_id` (integer, required): ID de la solicitud.
- **Response:**
  ```html
  <html>
    <body>
      <h1>Congratulations! Your request has been approved.</h1>
    </body>
  </html>
  ```
```