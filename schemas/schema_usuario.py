from pydantic import BaseModel, Field
from typing import Optional

# ==========================================
# 1. Esquema para CREAR (Recibe datos sensibles)
# ==========================================
class UsuarioCrear(BaseModel):
    nombre_usuario: str = Field(..., min_length=4, description="Mínimo 4 caracteres")
    password: str = Field(..., min_length=6, description="Mínimo 6 caracteres")
    rol: str = Field(..., description="Debe coincidir con el catálogo de roles")
    estado: Optional[str] = "Activo"

# ==========================================
# 2. Esquema para ACTUALIZAR (Permisos)
# ==========================================
class UsuarioActualizar(BaseModel):
    # Según tu lógica actual, el administrador solo actualiza el rol y el estado
    # No permitimos cambiar el nombre de usuario ni la contraseña por esta vía
    rol: Optional[str] = None
    estado: Optional[str] = None

# ==========================================
# 3. Esquema de RESPUESTA (El filtro de seguridad)
# ==========================================
class UsuarioRespuesta(BaseModel):
    id_usuario: int
    nombre_usuario: str
    rol: str
    estado: str
    
    # FÍJATE BIEN: Aquí NO pusimos el campo 'password'. 

    class Config:
        # Esto es un superpoder de Pydantic. Le dice que puede leer datos 
        # directamente de tus tuplas de SQLite o de tus modelos internos.
        from_attributes = True