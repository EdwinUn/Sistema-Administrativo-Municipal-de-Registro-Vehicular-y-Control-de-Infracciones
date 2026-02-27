from pydantic import BaseModel, Field, model_validator
from typing import Optional

# ==========================================
# 1. Esquema para CREAR (Registro de la multa)
# ==========================================
class InfraccionCrear(BaseModel):
    vin_infractor: str = Field(..., min_length=17, max_length=17, description="VIN de 17 caracteres")
    id_agente: int = Field(..., gt=0, description="ID interno del agente emisor")
    
    # Validamos que siempre manden el formato correcto para no romper SQLite
    fecha: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Formato YYYY-MM-DD")
    hora: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="Formato HH:MM")
    
    lugar: str = Field(..., min_length=5, description="Lugar exacto del hecho")
    tipo_infraccion: str = Field(..., description="Del catálogo de tipos")
    motivo: str = Field(..., min_length=5, description="Artículo o descripción")
    
    # El monto debe ser estrictamente mayor a cero (gt = greater than)
    monto: float = Field(..., gt=0, description="Cantidad económica de la multa")
    
    tipo_captura: str = Field(..., description="'En sitio' o 'Fotomulta'")
    licencia_conductor: Optional[str] = Field(None, min_length=5)

    # ¡LA MAGIA DE PYDANTIC! Validación inter-campos (Regla de negocio 4.2.vii)
    @model_validator(mode='after')
    def validar_licencia_en_sitio(self):
        if self.tipo_captura == "En sitio" and not self.licencia_conductor:
            raise ValueError("Para infracciones 'En sitio', el número de licencia del conductor es obligatorio.")
        return self

# ==========================================
# 2. Esquema para ACTUALIZAR ESTADO (Cobro/Cancelación)
# ==========================================
class InfraccionActualizarEstado(BaseModel):
    # Cuando el operador quiera cobrar una multa, el frontend solo enviará el nuevo estado.
    # El Folio viajará en la URL (ej. PUT /api/infracciones/INF-2026...)
    nuevo_estado: str = Field(..., description="'Pagada' o 'Cancelada'")

# ==========================================
# 3. Esquema de RESPUESTA (Consulta)
# ==========================================
class InfraccionRespuesta(BaseModel):
    folio: str
    vin_infractor: str
    id_agente: int
    fecha: str
    hora: str
    lugar: str
    tipo_infraccion: str
    motivo: str
    monto: float
    licencia_conductor: Optional[str] = None
    estado: str

    class Config:
        from_attributes = True