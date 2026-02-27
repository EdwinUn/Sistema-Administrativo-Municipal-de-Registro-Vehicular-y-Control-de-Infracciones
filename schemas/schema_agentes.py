from pydantic import BaseModel, Field
from typing import Optional

# ==========================================
# 1. Esquema para CREAR (Registro de Agente)
# ==========================================
class AgenteCrear(BaseModel):
    # La placa oficial no puede estar vacía
    numero_placa: str = Field(..., min_length=3, description="Número de identificación oficial")
    
    # Validamos el nombre igual que en tu Validador (solo letras y espacios, mín 5 caracteres)
    nombre_completo: str = Field(
        ..., 
        min_length=5, 
        pattern=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$',
        description="Nombre completo sin números ni símbolos"
    )
    
    # El cargo debe tener al menos 3 caracteres según tu regla de negocio
    cargo: str = Field(..., min_length=3, description="Puesto o rango del agente")
    
    # Por defecto, un agente nuevo nace como Activo
    estado: Optional[str] = "Activo"

# ==========================================
# 2. Esquema para ACTUALIZAR (Modificación)
# ==========================================
class AgenteActualizar(BaseModel):
    # OMITIMOS 'numero_placa' y 'nombre_completo' porque son inmutables.
    # Así garantizamos que por error nadie pueda cambiarle la identidad a un agente oficial.
    
    cargo: Optional[str] = Field(None, min_length=3)
    estado: Optional[str] = None

# ==========================================
# 3. Esquema de RESPUESTA (Consulta)
# ==========================================
class AgenteRespuesta(BaseModel):
    id_agente: int
    numero_placa: str
    nombre_completo: str
    cargo: str
    estado: str

    class Config:
        from_attributes = True