from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
import os
from pathlib import Path

# Importar módulos de base de datos
from database_lzl.db_connection import connect_to_database, test_connection

# Importar routers
from web_app.router.web_routes import router as web_router
from web_app.router.api_routes import router as api_router
from web_app.router.auth_routes import router as auth_router
from web_app.router.admin_api import router as admin_api_router

# Importar middleware de autenticación
from web_app.middleware.auth_middleware import AuthMiddleware

# Crear la aplicación FastAPI
app = FastAPI(
    title="LogiXport",
    description="Sistema de gestión logística",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware de autenticación
app.middleware("http")(AuthMiddleware())

# Configurar directorios de plantillas y archivos estáticos
BASE_DIR = Path(__file__).resolve().parent

# Configurar Jinja2Templates para las páginas de error
templates = Jinja2Templates(directory=str(BASE_DIR / "web_app" / "templates"))

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "web_app" / "templates" / "style")), name="static")
# Montar la carpeta templates como estática para acceder a los recursos
app.mount("/templates", StaticFiles(directory=str(BASE_DIR / "web_app" / "templates")), name="templates")

# Incluir routers
app.include_router(web_router)
app.include_router(api_router)
app.include_router(auth_router)
app.include_router(admin_api_router)

# Manejadores de errores personalizados
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Manejador personalizado para errores HTTP"""
    if exc.status_code == 404:
        return templates.TemplateResponse("pages/error_404.html", {"request": request}, status_code=404)
    elif exc.status_code == 500:
        return templates.TemplateResponse("pages/error_500.html", {"request": request}, status_code=500)
    # Para otros códigos de error, usar el manejador predeterminado
    raise exc

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejador personalizado para errores de validación"""
    # Los errores de validación se muestran como error 500
    return templates.TemplateResponse("pages/error_500.html", {"request": request}, status_code=500)

# Manejador para excepciones no controladas (error 500)
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Manejador para excepciones generales no controladas"""
    return templates.TemplateResponse("pages/error_500.html", {"request": request}, status_code=500)

# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    # Probar conexión a la base de datos antes de iniciar
    if test_connection():
        print("Conexión a la base de datos exitosa. Iniciando servidor...")
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    else:
        print("Error al conectar con la base de datos. Verifique la configuración.")
