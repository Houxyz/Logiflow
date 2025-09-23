# Rutas de autenticación para LogiXport
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
import jwt
from datetime import datetime, timedelta

# Importar modelos y funciones de autenticación
from database_lzl.auth import (
    authenticate_user, create_access_token, update_last_login,
    get_user_by_id, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
)
from web_app.models.auth_models import LoginRequest, TokenResponse, UserResponse, ErrorResponse

# Crear router para autenticación
router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

# Configurar OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Función para obtener el usuario actual a partir del token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Obtiene el usuario actual a partir del token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: int = payload.get("sub")
        
        if usuario_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Obtener usuario de la base de datos
    usuario = get_user_by_id(usuario_id)
    if usuario is None:
        raise credentials_exception
    
    # Verificar si el usuario está activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return usuario

# Endpoint para inicio de sesión
@router.post("/login", response_model=TokenResponse)
async def login(request: Request, login_data: LoginRequest):
    """
    Endpoint para iniciar sesión y obtener un token JWT.
    """
    # Autenticar usuario
    usuario = authenticate_user(login_data.email, login_data.password)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar si el usuario está activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Crear datos para el token
    token_data = {
        "sub": usuario.id_usuario,
        "email": usuario.correo,
        "role": usuario.rol
    }
    
    # Establecer tiempo de expiración
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if login_data.remember_me:
        # Si el usuario marcó "recordarme", extender el tiempo de expiración (7 días)
        expires_delta = timedelta(days=7)
    
    # Crear token de acceso
    access_token = create_access_token(
        data=token_data,
        expires_delta=expires_delta
    )
    
    # Actualizar información de último ingreso
    client_host = request.client.host if request.client else None
    update_last_login(usuario.id_usuario, client_host)
    
    # Crear respuesta de usuario
    user_response = UserResponse(
        id_usuario=usuario.id_usuario,
        correo=usuario.correo,
        nombre_usuario=usuario.nombre_usuario,
        rol=usuario.rol,
        empresa=usuario.empresa,
        membresia_activa=usuario.membresia_activa,
        plan_membresia=usuario.plan_membresia,
        fecha_expiracion_membresia=usuario.fecha_expiracion_membresia,
        ultimo_ingreso=usuario.ultimo_ingreso,
        avatar=usuario.avatar
    )
    
    # Crear respuesta con token
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_delta.total_seconds(),
        user=user_response
    )

# Endpoint para obtener información del usuario actual
@router.get("/me", response_model=UserResponse)
async def get_user_info(current_user = Depends(get_current_user)):
    """
    Endpoint para obtener información del usuario autenticado.
    """
    return UserResponse(
        id_usuario=current_user.id_usuario,
        correo=current_user.correo,
        nombre_usuario=current_user.nombre_usuario,
        rol=current_user.rol,
        empresa=current_user.empresa,
        membresia_activa=current_user.membresia_activa,
        plan_membresia=current_user.plan_membresia,
        fecha_expiracion_membresia=current_user.fecha_expiracion_membresia,
        ultimo_ingreso=current_user.ultimo_ingreso,
        avatar=current_user.avatar
    )

# Endpoint para verificar si el token es válido
@router.get("/verify")
async def verify_token(current_user = Depends(get_current_user)):
    """
    Endpoint para verificar si el token JWT es válido.
    """
    return {"valid": True, "user_id": current_user.id_usuario}

# Endpoint para cerrar sesión (solo para documentación, ya que JWT es stateless)
@router.post("/logout")
async def logout():
    """
    Endpoint para cerrar sesión.
    En JWT, el cierre de sesión se maneja del lado del cliente eliminando el token.
    """
    return {"message": "Sesión cerrada exitosamente"}