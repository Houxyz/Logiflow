# Middleware de autenticación para LogiXport
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
import jwt
from typing import Optional, Callable, Dict, Any
import logging

# Importar funciones de autenticación
from database_lzl.auth import get_user_by_id, SECRET_KEY, ALGORITHM

# Configurar logging
logger = logging.getLogger("auth_middleware")

class AuthMiddleware:
    """
    Middleware para verificar la autenticación en rutas protegidas.
    """
    
    async def __call__(self, request: Request, call_next: Callable):
        """
        Procesa la solicitud y verifica la autenticación si es necesaria.
        """
        # Rutas que no requieren autenticación
        public_paths = [
            "/",
            "/login",
            "/register",
            "/information",
            "/static",
            "/templates",
            "/auth/login",
            "/auth/verify",
            "/api/token"
        ]
        
        # Verificar si la ruta actual es pública
        current_path = request.url.path
        for path in public_paths:
            if current_path.startswith(path):
                # Ruta pública, continuar sin verificar autenticación
                return await call_next(request)
        
        # Verificar token en cookies o encabezado de autorización
        token = self._get_token_from_request(request)
        
        if not token:
            # Si es una solicitud de API, devolver error 401
            if current_path.startswith("/api") or current_path.startswith("/auth"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No se proporcionó token de autenticación",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            # Si es una solicitud web, redirigir a login
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        # Verificar token y obtener usuario
        user = await self._get_user_from_token(token)
        if not user:
            # Si es una solicitud de API, devolver error 401
            if current_path.startswith("/api") or current_path.startswith("/auth"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido o expirado",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            # Si es una solicitud web, redirigir a login
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        # Verificar permisos para rutas de administrador
        if current_path.startswith("/admin") and user.rol != "admin":
            # Si no es administrador, denegar acceso
            if current_path.startswith("/api") or current_path.startswith("/auth"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para acceder a este recurso"
                )
            # Si es una solicitud web, redirigir a dashboard
            return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        
        # Agregar usuario a la solicitud para que esté disponible en los endpoints
        request.state.user = user
        
        # Continuar con la solicitud
        return await call_next(request)
    
    def _get_token_from_request(self, request: Request) -> Optional[str]:
        """
        Obtiene el token JWT de la solicitud (cookie o encabezado).
        """
        # Intentar obtener token del encabezado de autorización
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.replace("Bearer ", "")
        
        # Intentar obtener token de las cookies
        token = request.cookies.get("access_token")
        if token:
            return token
        
        return None
    
    async def _get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica el token JWT y obtiene la información del usuario.
        """
        try:
            # Decodificar el token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            usuario_id: int = payload.get("sub")
            
            if usuario_id is None:
                return None
            
            # Obtener usuario de la base de datos
            usuario = get_user_by_id(usuario_id)
            if usuario is None or not usuario.activo:
                return None
            
            return usuario
        except jwt.PyJWTError as e:
            logger.error(f"Error al decodificar token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error al obtener usuario desde token: {e}")
            return None