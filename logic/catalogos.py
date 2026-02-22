"""
Catálogos oficiales del sistema.

Este módulo centraliza todos los valores predefinidos utilizados por el sistema
para garantizar consistencia entre la interfaz, la validación y la lógica de negocio.

NO contiene lógica.
NO realiza validaciones.
NO accede a base de datos.
"""

# =========================
# VEHÍCULOS
# =========================

ESTADOS_VEHICULO = [
    "Activo",
    "Baja temporal",
    "Reporte de robo",
    "Recuperado",
    "En corralón"
]

CLASES_VEHICULO = [
    "Sedán",
    "Motocicleta",
    "Camión",
    "Camioneta",
    "Autobús"
]

PROCEDENCIAS_VEHICULO = [
    "Nacional",
    "Importado"
]

# Nota:
# Marca y modelo se consideran atributos estructurales,
# pero el documento indica que deben validarse contra valores válidos.
# En una versión real, esto vendría de una BD o catálogo externo.
# Aquí se deja abierto para crecimiento.
# =========================


# =========================
# PROPIETARIOS
# =========================

ESTADOS_LICENCIA = [
    "Vigente",
    "Suspendida",
    "Cancelada",
    "Vencida"
]

ESTADOS_PROPIETARIO = [
    "Activo",
    "Inactivo"
]

# =========================
# INFRACCIONES
# =========================

ESTADOS_INFRACCION = [
    "Pendiente",
    "Pagada",
    "Cancelada"
]

TIPOS_INFRACCION = [
    "Exceso de velocidad",
    "Estacionamiento prohibido",
    "No portar cinturón",
    "Uso de celular",
    "Conducir en estado de ebriedad",
    "Falta de documentos",
    "Otro"
]

TIPOS_CAPTURA_INFRACCION = [
    "En sitio",
    "Fotomulta"
]

# =========================
# AGENTES DE TRÁNSITO
# =========================

ESTADOS_AGENTE = [
    "Activo",
    "Inactivo"
]

# =========================
# USUARIOS DEL SISTEMA
# =========================

ROLES_USUARIO = [
    "Administrador",
    "Operador Administrativo",
    "Agente de Tránsito",
    "Supervisor"
]