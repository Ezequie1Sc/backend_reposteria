# Backend - Sistema de Repostería

API REST construida con FastAPI, SQLAlchemy y PostgreSQL.

## Arquitectura

Router → Schema → Service → Repository → Model → PostgreSQL

## Estructura

- `app/core`: configuración, base de datos y seguridad.
- `app/modules`: módulos de negocio.
- `app/api/v1`: versión de la API.
- `alembic`: migraciones.
- `tests`: pruebas unitarias e integración.

## Ejecución

1. Crear un entorno virtual.
2. Instalar `requirements.txt`.
3. Copiar `.env.example` a `.env`.
4. Configurar `DATABASE_URL`.
5. Ejecutar:

```bash
uvicorn app.main:app --reload
```

Documentación:
- `/docs`
- `/redoc`
