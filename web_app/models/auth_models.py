# Modelos Pydantic para autenticación
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    """
    Modelo para la solicitud de inicio de sesión.
    """
    email: EmailStr
    password: str
    remember_me: Optional[bool] = False

class UserResponse(BaseModel):
    """
    Modelo para la respuesta con información del usuario.
    """
    id_usuario: int
    correo: EmailStr
    nombre_usuario: Optional[str] = None
    rol: str
    empresa: Optional[str] = None
    membresia_activa: bool
    plan_membresia: Optional[str] = None
    fecha_expiracion_membresia: Optional[datetime] = None
    ultimo_ingreso: Optional[datetime] = None
    avatar: Optional[str] = None

class TokenResponse(BaseModel):
    """
    Modelo para la respuesta con el token de acceso.
    """
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Tiempo de expiración en segundos
    user: UserResponse

class ErrorResponse(BaseModel):
    """
    Modelo para respuestas de error.
    """
    detail: str
    status_code: int = 400