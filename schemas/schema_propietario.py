from pydantic import BaseModel, Field
from typing import Optional

# ==========================================
# 1. Esquema para CREAR un Propietario
# ==========================================
class PropietarioCrear(BaseModel):
    # Usamos min_length=5 como lo tenías en tu validador
    nombre_completo: str = Field(..., min_length=5, description="Nombre completo del propietario")
    
    # Pydantic puede validar expresiones regulares (pattern). ¡Usamos la misma que ya tenías!
    curp: str = Field(..., 
                      min_length=18, 
                      max_length=18, 
                      pattern=r"^[A-Z]{4}\d{6}[HMX][A-Z]{2}[A-Z]{3}[A-Z0-9]\d$", 
                      description="CURP válida de 18 caracteres")
    
    direccion: str = Field(..., min_length=10, description="Dirección completa")
    
    # Forzamos a que sean exactamente 10 dígitos numéricos
    telefono: str = Field(..., 
                          min_length=10, 
                          max_length=10, 
                          pattern=r"^\d+$", 
                          description="Teléfono a 10 dígitos")
    
    # Validación de correo usando la misma regla del validador
    correo_electronico: str = Field(..., 
                                    pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$", 
                                    description="Formato de correo válido")
    
    estado_licencia: str = Field(..., description="Estado de la licencia")
    
    # El estado por defecto siempre será "Activo" al nacer
    estado: Optional[str] = "Activo"

# ==========================================
# 2. Esquema para ACTUALIZAR un Propietario
# ==========================================
class PropietarioActualizar(BaseModel):
    # Fíjate que NO incluimos 'nombre_completo' ni 'curp' aquí.
    # Así garantizamos que el frontend jamás pueda modificar esos datos inmutables.
    
    direccion: Optional[str] = Field(None, min_length=10)
    
    telefono: Optional[str] = Field(None, 
                                    min_length=10, 
                                    max_length=10, 
                                    pattern=r"^\d+$")
    
    correo_electronico: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    
    estado_licencia: Optional[str] = None
    estado: Optional[str] = None