# Rutas de API para el panel de administración
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime
import logging

# Importar modelos y funciones de autenticación
from database_lzl.auth import get_user_by_id
from database_lzl.models_sqlalchemy import Usuario, DocumentoNormativo, CategoriaNormativa, get_session

# Configurar logging
logger = logging.getLogger("admin_api")

# Crear router para API de administración
router = APIRouter(
    prefix="/api/admin",
    tags=["admin"]
)

# Función para verificar que el usuario es administrador
async def verify_admin(request: Request):
    user = getattr(request.state, 'user', None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )
    
    if user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    
    return user

# Endpoint para obtener estadísticas del dashboard
@router.get("/stats")
async def get_admin_stats(admin: Usuario = Depends(verify_admin)):
    """Obtiene estadísticas para el dashboard de administración"""
    session = get_session()
    
    try:
        # Contar usuarios
        total_usuarios = session.query(Usuario).count()
        usuarios_activos = session.query(Usuario).filter(Usuario.activo == True).count()
        
        # Contar documentos por categoría
        documentos_por_categoria = []
        categorias = session.query(CategoriaNormativa).all()
        
        for categoria in categorias:
            count = session.query(DocumentoNormativo).filter(
                DocumentoNormativo.id_categoria == categoria.id_categoria
            ).count()
            
            documentos_por_categoria.append({
                "categoria": categoria.nombre,
                "count": count
            })
        
        # Obtener estadísticas de documentos
        total_documentos = session.query(DocumentoNormativo).count()
        
        return {
            "usuarios": {
                "total": total_usuarios,
                "activos": usuarios_activos
            },
            "documentos": {
                "total": total_documentos,
                "por_categoria": documentos_por_categoria
            }
        }
    
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener estadísticas"
        )
    
    finally:
        session.close()

# Endpoint para listar usuarios
@router.get("/usuarios")
async def list_usuarios(admin: Usuario = Depends(verify_admin)):
    """Lista todos los usuarios registrados"""
    session = get_session()
    
    try:
        usuarios = session.query(Usuario).all()
        
        # Convertir a formato JSON
        usuarios_json = []
        for usuario in usuarios:
            usuarios_json.append({
                "id": usuario.id_usuario,
                "nombre_usuario": usuario.nombre_usuario,
                "correo": usuario.correo,
                "rol": usuario.rol,
                "activo": usuario.activo,
                "empresa": usuario.empresa,
                "membresia_activa": usuario.membresia_activa,
                "plan_membresia": usuario.plan_membresia,
                "fecha_expiracion_membresia": usuario.fecha_expiracion_membresia.isoformat() if usuario.fecha_expiracion_membresia else None,
                "fecha_creacion": usuario.fecha_creacion.isoformat() if usuario.fecha_creacion else None,
                "ultimo_ingreso": usuario.ultimo_ingreso.isoformat() if usuario.ultimo_ingreso else None
            })
        
        return {"usuarios": usuarios_json}
    
    except Exception as e:
        logger.error(f"Error al listar usuarios: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener la lista de usuarios"
        )
    
    finally:
        session.close()

# Endpoint para actualizar estado de usuario
@router.put("/usuarios/{usuario_id}/estado")
async def update_usuario_estado(
    usuario_id: int, 
    activo: bool,
    admin: Usuario = Depends(verify_admin)
):
    """Actualiza el estado (activo/inactivo) de un usuario"""
    session = get_session()
    
    try:
        # Buscar usuario
        usuario = session.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Actualizar estado
        usuario.activo = activo
        session.commit()
        
        return {"message": "Estado de usuario actualizado correctamente"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        session.rollback()
        logger.error(f"Error al actualizar estado de usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar estado de usuario"
        )
    
    finally:
        session.close()

# Endpoint para listar documentos normativos
@router.get("/documentos")
async def list_documentos(admin: Usuario = Depends(verify_admin)):
    """Lista todos los documentos normativos"""
    session = get_session()
    
    try:
        documentos = session.query(DocumentoNormativo).all()
        
        # Convertir a formato JSON
        documentos_json = []
        for doc in documentos:
            documentos_json.append({
                "id": doc.id_documento,
                "titulo": doc.titulo,
                "tipo_documento": doc.tipo_documento,
                "fecha_publicacion": doc.fecha_publicacion.isoformat() if doc.fecha_publicacion else None,
                "fecha_vigencia": doc.fecha_vigencia.isoformat() if doc.fecha_vigencia else None,
                "url_documento": doc.url_documento,
                "clave_referencia": doc.clave_referencia,
                "fecha_creacion": doc.fecha_creacion.isoformat() if doc.fecha_creacion else None
            })
        
        return {"documentos": documentos_json}
    
    except Exception as e:
        logger.error(f"Error al listar documentos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener la lista de documentos"
        )
    
    finally:
        session.close()