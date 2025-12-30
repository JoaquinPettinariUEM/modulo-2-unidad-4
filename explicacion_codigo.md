## 📁 Estructura del Proyecto

Este backend está construido con **Django** y **Django Rest Framework (DRF)**, organizado de forma modular para mantener el código limpio, escalable y fácil de mantener.

A continuación se describe cada carpeta y archivo principal del proyecto:

```bash
project_root/
├── core/
│   ├── migrations/
│   ├── services/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── url.py
├── spotify_api/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── .env.copy
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
```

### 🧩 core/models.py

Contiene los modelos de base de datos, definidos usando el ORM de Django.

### 🔌 core/views.py

Contiene las vistas de la API, implementadas usando Django Rest Framework.

### 📦 core/serializers.py

Define los Serializers, que cumplen un rol similar a los schemas en otros frameworks.

### 🔀 core/urls.py

Define las rutas de la aplicación.

### ⚙️ spotify_api/settings.py

Archivo central de configuración del proyecto Django.

### 🧭 Recorrido del Código (Cómo funciona todo junto)

El punto de entrada del proyecto es manage.py, que permite ejecutar comandos administrativos de Django.

Cuando el servidor se inicia:

- Django carga la configuración desde settings.py
- Se registran las rutas en urls.py
- Una request llega a una vista en views.py
- La vista usa un serializer para validar datos
- Se interactúa con los modelos para leer o escribir en la base
- Se devuelve una respuesta JSON al cliente

Esta separación clara de responsabilidades hace que el código sea mantenible y fácil de extender.

---

## 📚 Explicación de los Endpoints

### 👤 Endpoints de Usuarios (/users)

Estos endpoints representan un CRUD sencillo, ideal para iniciar y mantener la identidad del usuario dentro de la plataforma.

Incluyen:
- Crear usuario (POST /users/)
- Listar todos los usuarios con su historial y acciones (GET /users/)
- Obtener un usuario por ID (GET /users/{user_id})
- Eliminar usuario (DELETE /users/{user_id})

El propósito principal es disponer del user_id necesario para vincular el historial y los likes/dislikes.

### 🔍 Endpoints de Búsqueda (/spotify/search)

Este endpoint es el núcleo de la integración con Spotify.

Buscar música (GET /spotify/search/?query=X&type=artist|track|album&user_id=numero)

Qué hace internamente:
- Solicita un token válido a Spotify.
- Ejecuta una búsqueda directa a la API de Spotify.
- Devuelve los resultados tal cual Spotify los entrega (rápido, sin almacenar contenido extra).
- Guarda en la base de datos la query buscada

Es un endpoint pensado para ser ágil, sin procesar información adicional.

También podemos encontrar un GET con las búsquedas de un usuario (GET /spotify/search/{user_id})

### ❤️ Endpoints de Acciones de Música (/spotify/action)

Estos permiten marcar elementos musicales como like o dislike.

- Obtener las acciones de un usuario (GET /action/{user_id})
- Registrar acción (POST /action/)
- Eliminar acción (DELETE /action/{action_id})

Características:
- Usan ActionEnum para evitar errores (solo like o dislike).
- Permiten a futuro construir recomendaciones basadas en preferencias.

---

### 🚧 Limitaciones y Posibles Mejoras

- Autorización limitada: el proyecto no implementa autenticación real de usuarios (OAuth2, JWT, sesiones, etc.). Actualmente asume que el user_id es confiable.
- Dependencia del flujo [Client Credentials](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow) de Spotify: este flujo no permite obtener información personalizada del usuario de Spotify, solo acceso a contenidos públicos. Para funcionalidades más avanzadas se requeriría OAuth completo.
- Validaciones básicas: aunque se usan enums y Pydantic, aún faltan validaciones más estrictas (tipos, rangos, formatos).
- Base de datos local: se utiliza SQLite por simplicidad, lo cual no es ideal para producción. No soporta concurrencia alta ni escalabilidad.
- Errores genéricos: algunas respuestas de error del backend podrían ser más descriptivas y consistentes.
- Servicios sin tests automatizados: actualmente no hay cobertura de tests unitarios o de integración.

## 📝 Conclusiones y Observaciones

El proyecto presenta una arquitectura clara, modular y alineada con buenas prácticas de Django y DRF.

La separación entre:
- Vistas
- Serializers
- Modelos
- Configuración

permite escalar el proyecto sin generar acoplamientos innecesarios.

El uso de Docker simplifica el setup y evita problemas de dependencias, mientras que las variables de entorno mantienen las credenciales seguras.
