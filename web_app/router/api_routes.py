from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional, List
from pydantic import BaseModel

# Importar módulos de base de datos
from database_lzl.db_models import User, Shipment

# Crear router para API
router = APIRouter(
    prefix="/api",
    tags=["api"]
)

# Configurar seguridad OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

# Modelos Pydantic para validación de datos
class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class ShipmentCreate(BaseModel):
    origin: str
    destination: str
    status: str
    client_id: int
    details: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# Rutas de autenticación
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint para obtener token de acceso"""
    user = User.get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Aquí se implementaría la verificación de contraseña
    # y generación de token JWT
    return {"access_token": "dummy_token", "token_type": "bearer"}

# Rutas de usuarios
@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Crear un nuevo usuario"""
    result = User.create_user(user.username, user.password, user.email)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear usuario"
        )
    return {"message": "Usuario creado exitosamente"}

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """Obtener información del usuario actual"""
    # Aquí se implementaría la decodificación del token
    # y la obtención de la información del usuario
    return {"username": "current_user", "email": "user@example.com"}

# Rutas de envíos
@router.post("/shipments", status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment: ShipmentCreate, token: str = Depends(oauth2_scheme)):
    """Crear un nuevo envío"""
    result = Shipment.create_shipment(
        shipment.origin,
        shipment.destination,
        shipment.status,
        shipment.client_id,
        shipment.details
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear envío"
        )
    return {"message": "Envío creado exitosamente", "id": result[0][0]}

@router.get("/shipments/{client_id}")
async def get_client_shipments(client_id: int, token: str = Depends(oauth2_scheme)):
    """Obtener todos los envíos de un cliente"""
    shipments = Shipment.get_shipments_by_client(client_id)
    if not shipments:
        return {"shipments": []}
    return {"shipments": shipments}

@router.put("/shipments/{shipment_id}/status")
async def update_shipment_status(shipment_id: int, new_status: str, token: str = Depends(oauth2_scheme)):
    """Actualizar el estado de un envío"""
    result = Shipment.update_shipment_status(shipment_id, new_status)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar estado del envío"
        )
    return {"message": "Estado del envío actualizado exitosamente"}