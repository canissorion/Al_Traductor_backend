import uvicorn  # pyright: ignore
from app import create_app

app = create_app()

if __name__ == "__main__":
    # TODO(davideliseo): Agregar la configuración de producción.
    uvicorn.run(  # pyright: ignore
        "main:app",
        host="0.0.0.0",
        port=8000,
        debug=False,
        reload=False,
        log_level="info",
    )
