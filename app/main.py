from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine


app = FastAPI(
    title="API - Sistema de Repostería",
    version="1.0.0",
)


@app.on_event("startup")
def verificar_conexion():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("==============================================")
        print("CONEXIÓN ESTABLECIDA CON LA BASE DE DATOS")
        print("PostgreSQL conectado correctamente")
        print("==============================================")

    except Exception as e:
        print("==============================================")
        print("ERROR: NO SE PUDO CONECTAR A LA BASE DE DATOS")
        print(f"Detalle: {e}")
        print("==============================================")


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok"
    }