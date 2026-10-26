# Sistema Web de Votaciones · Festival de la Leyenda Vallenata 2027

Entrega 2 · Desarrollo Web · Fundación Universitaria del Área Andina.
Versión inicial construida con **Python, Django (patrón MVT) y MySQL**, a partir del análisis y diseño de la Entrega 1.

## Qué incluye esta versión

- Proyecto Django con dos aplicaciones: `festival` (ediciones, categorías, votaciones y opciones) y `cuentas` (registro, inicio y cierre de sesión).
- Modelo relacional en MySQL: **Edición → Categoría → Votación → Opción**, con migraciones y restricciones de integridad.
- Administración de los cuatro elementos mediante **Django Admin**.
- Autenticación con el sistema nativo de Django (`django.contrib.auth`).
- Interfaz pública responsive (HTML5, CSS3, **Bootstrap 5** incluido localmente y JavaScript) con datos reales de MySQL: edición vigente, estados Abierta/Próximamente/Cerrada/Publicada y cuenta regresiva.
- Registro e inicio de sesión por correo, con consentimiento de datos (texto pendiente de validación).
- Reglas de administración: no se abre una votación sin opciones, advertencia al desactivar categorías con votaciones abiertas y registro de auditoría de solo lectura.
- Interfaz propia para gestionar ediciones (`/gestion/ediciones/`, solo personal).
- Perfil «Administrador» (grupo con permisos concretos), cambios de estado válidos (Borrador → Abierta → Cerrada → Resultados publicados), eliminación restringida y panel con actividad reciente.
- 53 pruebas automatizadas y un comando para cargar datos de prueba.

Fuera de alcance en esta entrega (siguiente fase): emisión de votos (el botón «Votar» está deshabilitado), control de duplicados, resultados y despliegue. Las decisiones pendientes de validación con la Fundación (edición vigente, mínimo de opciones, datos del votante) usan un criterio provisional marcado en el código.

## Requisitos

- Python 3.10 o superior
- MySQL 8.x (o MariaDB 10.5+) en ejecución
- Git

## Instalación y ejecución (Windows, PowerShell)

```powershell
# 1. Clonar y entrar al proyecto
git clone <URL_DEL_REPOSITORIO>
cd festival_votaciones

# 2. Entorno virtual y dependencias
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Crear la base de datos y un usuario en MySQL (ejecutar en el cliente mysql como root)
#    CREATE DATABASE festival_votaciones CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
#    CREATE USER 'festival_user'@'localhost' IDENTIFIED BY 'TU_CONTRASEÑA';
#    GRANT ALL PRIVILEGES ON festival_votaciones.* TO 'festival_user'@'localhost';
#    GRANT ALL PRIVILEGES ON test_festival_votaciones.* TO 'festival_user'@'localhost';  -- para correr las pruebas
#    FLUSH PRIVILEGES;

# 4. Configuración local (el archivo .env NO se sube a git)
copy .env.example .env
#    Editar .env y poner la contraseña real de MySQL (DB_PASSWORD)

# 5. Tablas, datos de prueba y administrador
python manage.py migrate
python manage.py cargar_datos_prueba          # use --limpiar para reiniciar los datos de prueba
python manage.py createsuperuser

# 6. Servidor de desarrollo
python manage.py runserver
```

En Linux/macOS cambie la activación por `source venv/bin/activate` y `copy` por `cp`.

Abra <http://127.0.0.1:8000/> (sitio público) y <http://127.0.0.1:8000/admin/> (administración).

> Si `pip install mysqlclient` falla en Windows, actualice pip (`python -m pip install -U pip`) para usar la rueda precompilada; en Linux instale antes `libmysqlclient-dev` (o `libmariadb-dev`) y `pkg-config`.

## Pruebas

```powershell
python manage.py test
```

Cubre relaciones y restricciones de los modelos, estados públicos, visibilidad (borradores y elementos inactivos devuelven 404), registro/login/logout por correo y las reglas y auditoría del administrador.

## Estructura

```
festival_votaciones/
├── manage.py
├── requirements.txt
├── .env.example            # plantilla de configuración (sin secretos)
├── config/                 # settings, urls raíz, wsgi
├── festival/               # modelos, admin, vistas, urls, pruebas, comando de datos de prueba
├── cuentas/                # registro, login, logout
├── templates/              # base.html, festival/*, registration/*
└── static/                 # css/estilos.css, js/app.js, vendor/bootstrap (local)
```

## Rutas principales

| Ruta | Descripción |
|---|---|
| `/` | Edición vigente y sus categorías |
| `/ediciones/` | Ediciones activas |
| `/gestion/` | Panel del personal con actividad reciente (auditoría) |
| `/gestion/ediciones/` | Gestión de ediciones (solo personal): listar, crear, editar, activar/desactivar |
| `/ediciones/<id>/` | Categorías de una edición |
| `/categorias/<id>/` | Votaciones de una categoría |
| `/votaciones/<id>/` | Opciones de una votación (los borradores devuelven 404) |
| `/cuentas/registro/`, `/cuentas/ingresar/`, `/cuentas/salir/` | Autenticación (el cierre de sesión es por POST) |
| `/admin/` | Django Admin (solo personal autorizado) |

## Perfiles y permisos

Al ejecutar `python manage.py migrate` se crea el grupo **Administrador** (permisos sobre ediciones, categorías, votaciones y opciones, y consulta de la auditoría; sin eliminar ediciones ni categorías). Para dar acceso a una persona del equipo: en `/admin/` cree el usuario, marque *Es staff* y asígnelo a ese grupo. Un usuario *staff* sin el grupo no puede gestionar contenido. El superusuario tiene todos los permisos.

## Seguridad

- Contraseña de MySQL, `SECRET_KEY` y demás valores sensibles se leen de variables de entorno (`.env`), nunca del código.
- Contraseñas de usuarios almacenadas con hash PBKDF2 (nativo de Django); protección CSRF activa en todos los formularios.
- Todos los datos incluidos son **datos de prueba**; ningún participante corresponde a una persona real.
- `DJANGO_DEBUG` está en `False` por defecto; para desarrollo local el `.env` debe tener `DJANGO_DEBUG=True` (ya viene en `.env.example`).
- Antes de desplegar: `DJANGO_SECRET_KEY` propia, `DJANGO_ALLOWED_HOSTS` definido y `DJANGO_HTTPS=True` (activa redirección a HTTPS, cookies seguras y HSTS). Verifique con `python manage.py check --deploy`.
