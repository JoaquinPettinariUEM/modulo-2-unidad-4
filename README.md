# 📖 Backend – Setup desde cero (Django + Docker)

Este documento explica cómo levantar el proyecto desde cero luego de clonar el repositorio.  
Los pasos están pensados para un usuario externo que no conoce el entorno.

⚠️ **Importante:**  
La aplicación **NO funciona si no se crea el archivo `.env` antes de ejecutar Docker Compose**.

---

## 🚀 Levantar aplicación con Docker Compose

Este proyecto se puede levantar fácilmente usando Docker Compose, sin necesidad de instalar Python ni dependencias en tu máquina local.

---

## 📚 Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado en tu sistema  
  (incluye Docker Compose).

Verificar instalación:
```bash
docker compose version
```

## 🔧 Cómo crear tu archivo .env
Copiá el archivo de ejemplo:
```bash
cp .env.copy .env
```

Reemplaza los valores por los tuyos
```bash
SECRET_KEY=django_secret_key
SPOTIFY_CLIENT_ID=tu_client_id_de_spotify
SPOTIFY_CLIENT_SECRET=tu_client_secret_de_spotify
```


## 🚀 Levantar la aplicación.

Desde la raíz del proyecto (donde está docker-compose.yml), ejecuta:
```bash
Por primera vez usar:
docker compose up --build

Después usar:
docker compose up
```

## Entrega del proyecto:

[Explicación del código, estructura del proyecto y conclusiones](https://github.com/JoaquinPettinariUEM/modulo-2-unidad-4/blob/main/explicacion_codigo.md)
