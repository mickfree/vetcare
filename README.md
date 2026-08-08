# VetCare API

VetCare es una API REST para administrar una clínica veterinaria. Permite registrar usuarios, mascotas, servicios veterinarios, citas e historias clínicas.

## Tecnologías utilizadas

| Tecnología | Uso en el proyecto |
|---|---|
| Django | Framework principal y ORM |
| Django REST Framework | Construcción de la API REST |
| Simple JWT | Autenticación mediante tokens JWT |
| drf-spectacular | Generación de OpenAPI, Swagger y ReDoc |
| PostgreSQL / psycopg2 | Base de datos objetivo para producción |
| dj-database-url | Lectura de la conexión de base de datos desde una URL |
| python-dotenv | Variables de entorno locales |
| Gunicorn | Servidor WSGI para producción y Render |
| WhiteNoise | Archivos estáticos en producción |
| django-cors-headers | Acceso a la API desde un frontend externo |
| pytest / pytest-django | Pruebas automatizadas |
| pytest-cov / coverage | Medición de cobertura de pruebas |
| Faker | Generación de datos para pruebas |

Las versiones exactas están declaradas en `requirements.txt`.

## Estructura

```text
vetcare/
├── config/              Configuración principal y rutas globales
├── users/               Usuarios, registro y autenticación
├── pets/                Mascotas de los clientes
├── services/            Servicios veterinarios
├── appointments/        Citas veterinarias
├── medical_records/     Historias clínicas
├── manage.py
├── requirements.txt
├── schema.yml
└── README.md
```

## Requisitos

- Python 3.12 o superior.

## Instalación en Windows

Abrir PowerShell y ejecutar:

```powershell
cd G:\Example\tecsup-projects\vetcare
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Variables de entorno

Para producción se recomienda crear un archivo `.env` basado en este ejemplo:

```env
SECRET_KEY=una-clave-segura
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgresql://usuario:password@localhost:5432/vetcare
```


## Migraciones

Como el proyecto utiliza un usuario personalizado, `AUTH_USER_MODEL` debe estar configurado antes de ejecutar las primeras migraciones.

```powershell
python manage.py makemigrations
python manage.py migrate
```

Crear un administrador es opcional:

```powershell
python manage.py createsuperuser
```

## Ejecutar el proyecto

Puerto predeterminado:

```powershell
python manage.py runserver
```

Puerto personalizado:

```powershell
python manage.py runserver 8080
```

Direcciones principales usando el puerto `8080`:

| Recurso | Dirección |
|---|---|
| API | `http://127.0.0.1:8080/api/v1/` |
| Swagger | `http://127.0.0.1:8080/api/docs/swagger/` |
| ReDoc | `http://127.0.0.1:8080/api/docs/redoc/` |
| Esquema OpenAPI | `http://127.0.0.1:8080/api/schema/` |
| Administración | `http://127.0.0.1:8080/admin/` |

## Autenticación

Con excepción del registro y el inicio de sesión, los endpoints requieren un access token JWT.

Registrar un usuario:

```http
POST /api/v1/auth/register/
Content-Type: application/json

{
  "username": "maria",
  "first_name": "María",
  "last_name": "Torres",
  "email": "maria@example.com",
  "password": "ClaveSegura123",
  "phone": "999888777",
  "address": "Av. Principal 123"
}
```

Iniciar sesión:

```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "username": "maria",
  "password": "ClaveSegura123"
}
```

Respuesta aproximada:

```json
{
  "refresh": "token-refresh",
  "access": "token-access"
}
```

Enviar el token en las rutas protegidas:

```http
Authorization: Bearer token-access
```

En Swagger se puede presionar **Authorize** e ingresar:

```text
Bearer token-access
```

## Endpoints

Todos los endpoints usan el prefijo `/api/v1/`.

| Método | Endpoint | Autenticación | Descripción | Ejemplo de body |
|---|---|---:|---|---|
| `POST` | `/auth/register/` | No | Registra un cliente | `{"username":"maria","email":"maria@example.com","password":"ClaveSegura123"}` |
| `POST` | `/auth/login/` | No | Obtiene los tokens JWT | `{"username":"maria","password":"ClaveSegura123"}` |
| `GET` | `/users/` | Sí | Lista los usuarios | Sin body |
| `POST` | `/users/` | Sí | Crea un usuario | `{"username":"doctor1","email":"doctor@example.com","password":"ClaveSegura123","role":"VET"}` |
| `GET` | `/users/{id}/` | Sí | Consulta un usuario | Sin body |
| `PUT` | `/users/{id}/` | Sí | Reemplaza los datos de un usuario | `{"username":"doctor1","email":"doctor@example.com","role":"VET","is_active":true}` |
| `PATCH` | `/users/{id}/` | Sí | Actualiza algunos datos | `{"phone":"987654321"}` |
| `DELETE` | `/users/{id}/` | Sí | Elimina un usuario | Sin body |
| `GET` | `/pets/` | Sí | Lista las mascotas del usuario autenticado | Sin body |
| `POST` | `/pets/` | Sí | Registra una mascota | `{"name":"Firulais","species":"DOG","breed":"Labrador","birth_date":"2022-05-10","weight":"24.50","sex":"MALE"}` |
| `GET` | `/pets/{id}/` | Sí | Consulta una mascota propia | Sin body |
| `PUT` | `/pets/{id}/` | Sí | Reemplaza los datos de una mascota | `{"name":"Firulais","species":"DOG","breed":"Labrador","birth_date":"2022-05-10","weight":"25.00","sex":"MALE","is_active":true}` |
| `PATCH` | `/pets/{id}/` | Sí | Actualiza algunos datos de la mascota | `{"weight":"25.00"}` |
| `DELETE` | `/pets/{id}/` | Sí | Elimina una mascota | Sin body |
| `GET` | `/services/` | Sí | Lista los servicios veterinarios | Sin body |
| `POST` | `/services/` | Sí | Crea un servicio | `{"name":"Consulta general","description":"Evaluación médica","duration_minutes":30,"price":"50.00"}` |
| `GET` | `/services/{id}/` | Sí | Consulta un servicio | Sin body |
| `PUT` | `/services/{id}/` | Sí | Reemplaza un servicio | `{"name":"Consulta general","description":"Evaluación completa","duration_minutes":45,"price":"60.00","is_active":true}` |
| `PATCH` | `/services/{id}/` | Sí | Actualiza parcialmente un servicio | `{"price":"55.00"}` |
| `DELETE` | `/services/{id}/` | Sí | Elimina un servicio | Sin body |
| `GET` | `/appointments/` | Sí | Lista las citas visibles para el usuario | Sin body |
| `POST` | `/appointments/` | Sí | Programa una cita | `{"pet":1,"veterinarian":2,"service":1,"scheduled_at":"2026-08-15T15:00:00Z","reason":"Control anual"}` |
| `GET` | `/appointments/{id}/` | Sí | Consulta una cita | Sin body |
| `PUT` | `/appointments/{id}/` | Sí | Reemplaza una cita | `{"pet":1,"veterinarian":2,"service":1,"scheduled_at":"2026-08-16T15:00:00Z","status":"CONFIRMED","reason":"Control anual","observations":""}` |
| `PATCH` | `/appointments/{id}/` | Sí | Cambia campos como el estado | `{"status":"COMPLETED","observations":"Mascota atendida"}` |
| `DELETE` | `/appointments/{id}/` | Sí | Elimina una cita | Sin body |
| `GET` | `/medical-records/` | Sí | Lista las historias clínicas visibles | Sin body |
| `POST` | `/medical-records/` | Sí | Crea una historia para una cita completada | `{"appointment":1,"diagnosis":"Dermatitis leve","treatment":"Tratamiento tópico","prescription":"Aplicar crema cada 12 horas","notes":"Control en siete días"}` |
| `GET` | `/medical-records/{id}/` | Sí | Consulta una historia clínica | Sin body |
| `PUT` | `/medical-records/{id}/` | Sí | Reemplaza una historia clínica | `{"appointment":1,"diagnosis":"Dermatitis","treatment":"Tratamiento tópico","prescription":"Aplicar cada 12 horas","notes":"Evolución favorable"}` |
| `PATCH` | `/medical-records/{id}/` | Sí | Actualiza parcialmente una historia | `{"notes":"Paciente recuperado"}` |
| `DELETE` | `/medical-records/{id}/` | Sí | Elimina una historia clínica | Sin body |


## Validaciones principales

- El correo electrónico de un usuario debe ser único.
- La contraseña de registro debe tener al menos ocho caracteres.
- La fecha de nacimiento de una mascota no puede estar en el futuro.
- El peso de una mascota debe ser mayor que cero.
- Un usuario solo puede consultar y modificar sus propias mascotas.
- Un servicio debe durar entre 15 y 240 minutos.
- El precio de un servicio no puede ser negativo.
- Una cita debe programarse en el futuro.
- La mascota seleccionada debe pertenecer al cliente autenticado.
- El usuario seleccionado como veterinario debe tener el rol `VET`.
- No se pueden registrar dos citas para el mismo veterinario en la misma fecha y hora.
- Una historia clínica solo puede registrarse para una cita completada.
- La historia clínica debe ser creada por el veterinario asignado a la cita.

## Generar la documentación OpenAPI

```powershell
python manage.py spectacular --file schema.yml --validate
```

## Pruebas

Cuando se agreguen pruebas, podrán ejecutarse con:

```powershell
python -m pytest -v
```
