from pydantic import BaseModel, Field
from typing import Optional

# Este esquema es el molde para cuando el Frontend quiera REGISTRAR un vehículo nuevo
class VehiculoCrear(BaseModel):
    vin: str = Field(..., min_length=17, max_length=17, description="Identificador único de 17 caracteres")
    placa: str = Field(..., min_length=6, max_length=10)
    marca: str
    modelo: str
    anio: int = Field(..., ge=1899, le=2030, description="Año de fabricación")
    color: str
    clase: str
    procedencia: str
    id_propietario: int
    estado_legal: Optional[str] = "Activo"

# Este esquema es el molde para cuando el Frontend quiera ACTUALIZAR un vehículo (Solo placa, color, estado)
class VehiculoActualizar(BaseModel):
    placa: Optional[str] = None
    color: Optional[str] = None
    estado_legal: Optional[str] = None