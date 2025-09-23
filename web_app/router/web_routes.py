from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Configurar plantillas
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "web_app" / "templates"))

# Crear router para páginas web
router = APIRouter(tags=["web_pages"])

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Página de inicio (landing) con redirección a dashboard si el usuario está autenticado"""
    # Verificar si el usuario está autenticado
    user = getattr(request.state, 'user', None)
    if user:
        # Si el usuario está autenticado, redirigir al dashboard
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    # Si no está autenticado, mostrar la página de inicio
    return templates.TemplateResponse("pages/landing.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de inicio de sesión con redirección a dashboard si el usuario está autenticado"""
    # Verificar si el usuario está autenticado
    user = getattr(request.state, 'user', None)
    if user:
        # Si el usuario está autenticado, redirigir al dashboard
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    # Si no está autenticado, mostrar la página de login
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Página de registro con redirección a dashboard si el usuario está autenticado"""
    # Verificar si el usuario está autenticado
    user = getattr(request.state, 'user', None)
    if user:
        # Si el usuario está autenticado, redirigir al dashboard
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    # Si no está autenticado, mostrar la página de registro
    return templates.TemplateResponse("pages/register.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Página del panel de control (requiere autenticación)"""
    # La verificación de autenticación ya se realiza en el middleware
    # Obtener información del usuario desde request.state
    user = getattr(request.state, 'user', None)
    
    # Determinar qué plantilla mostrar según el rol del usuario
    if user and user.rol == 'admin':
        return templates.TemplateResponse("panel_admin/dashboard-admin.html", {
            "request": request,
            "user": user
        })
    else:
        # Para usuarios regulares, mostrar el dashboard de usuario
        return templates.TemplateResponse("pages/index.html", {
            "request": request,
            "user": user
        })

@router.get("/information", response_class=HTMLResponse)
async def information_page(request: Request):
    """Página de información"""
    return templates.TemplateResponse("pages/information.html", {"request": request})

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Panel de administración (requiere autenticación de administrador)"""
    # La verificación de autenticación ya se realiza en el middleware
    # Obtener información del usuario desde request.state
    user = getattr(request.state, 'user', None)
    
    # Pasar datos del usuario al template
    return templates.TemplateResponse("panel_admin/dashboard-admin.html", {
        "request": request,
        "user": user
    })

# Redirecciones para rutas antiguas
@router.get("/templates/pages/{page_name}.html", response_class=RedirectResponse)
async def redirect_old_routes(page_name: str):
    """Redirecciona las rutas antiguas a las nuevas rutas"""
    routes_map = {
        "landing": "/",
        "login": "/login",
        "register": "/register",
        "information": "/information"
    }
    
    if page_name in routes_map:
        return RedirectResponse(url=routes_map[page_name], status_code=status.HTTP_301_MOVED_PERMANENTLY)
    else:
        # Si no existe una redirección específica, redirigir a la página principal
        return RedirectResponse(url="/", status_code=status.HTTP_301_MOVED_PERMANENTLY)

# Ruta adicional para /landing que redirecciona a la página principal
@router.get("/landing", response_class=RedirectResponse)
async def landing_redirect():
    """Redirecciona /landing a la página principal"""
    return RedirectResponse(url="/", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.get("/logout", response_class=HTMLResponse)
async def logout_page(request: Request):
    """Página de cierre de sesión"""
    return templates.TemplateResponse("pages/logout.html", {"request": request})