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
    "Autobús",
    "Hatchback"
]

PROCEDENCIAS_VEHICULO = [
    "Nacional",
    "Importado"
]

# =========================
# MARCAS, MODELOS Y SUS CLASES PERMITIDAS (Cascada Doble)
# =========================
# Diccionario donde la clave es la Marca y el valor es otro diccionario.
# Cada Modelo contiene una LISTA con las clases en las que se fabrica.

#TODO MEJORAR porque por ejemplo puedo poner un aveo hatchback que no existe realmente
MARCAS_MODELOS_VEHICULO = {
    "Nissan": {
        "Versa": ["Sedán"], "Sentra": ["Sedán"], "March": ["Hatchback"], 
        "Tsuru": ["Sedán"], "Altima": ["Sedán"], "Kicks": ["Camioneta"], 
        "Frontier": ["Camioneta"], "NP300": ["Camioneta"]
    },
    "Chevrolet": {
        "Aveo": ["Sedán", "Hatchback"], "Chevy": ["Sedán", "Hatchback"], 
        "Beat": ["Sedán", "Hatchback"], "Spark": ["Hatchback"], 
        "Onix": ["Sedán"], "Trax": ["Camioneta"], 
        "Silverado": ["Camioneta"], "Colorado": ["Camioneta"]
    },
    "Volkswagen": {
        "Jetta": ["Sedán"], "Vento": ["Sedán"], "Gol": ["Hatchback"], 
        "Polo": ["Hatchback"], "Virtus": ["Sedán"], "Tiguan": ["Camioneta"], 
        "Saveiro": ["Camioneta"], "Taos": ["Camioneta"]
    },
    "Toyota": {
        "Corolla": ["Sedán"], "Yaris": ["Sedán", "Hatchback"], "Camry": ["Sedán"], 
        "Prius": ["Sedán", "Hatchback"], "RAV4": ["Camioneta"], 
        "Hilux": ["Camioneta"], "Tacoma": ["Camioneta"], "Avanza": ["Camioneta"]
    },
    "Honda": {
        "Civic": ["Sedán", "Hatchback"], "City": ["Sedán", "Hatchback"], 
        "Accord": ["Sedán"], "CR-V": ["Camioneta"], 
        "HR-V": ["Camioneta"], "BR-V": ["Camioneta"]
    },
    "Ford": {
        "Figo": ["Sedán", "Hatchback"], "Fiesta": ["Sedán", "Hatchback"], 
        "Focus": ["Sedán", "Hatchback"], "Mustang": ["Sedán"], 
        "Escape": ["Camioneta"], "Ranger": ["Camioneta"], 
        "F-150": ["Camioneta"], "Explorer": ["Camioneta"]
    },
    "Mazda": {
        "Mazda 2": ["Sedán", "Hatchback"], "Mazda 3": ["Sedán", "Hatchback"], 
        "Mazda 6": ["Sedán"], "CX-3": ["Camioneta"], 
        "CX-5": ["Camioneta"], "CX-30": ["Camioneta"]
    },
    "Kia": {
        "Rio": ["Sedán", "Hatchback"], "Forte": ["Sedán", "Hatchback"], 
        "Soul": ["Camioneta"], "Seltos": ["Camioneta"], 
        "Sportage": ["Camioneta"], "Sorento": ["Camioneta"]
    },
    "Hyundai": {
        "Grand i10": ["Sedán", "Hatchback"], "Accent": ["Sedán", "Hatchback"], 
        "Elantra": ["Sedán"], "Tucson": ["Camioneta"], "Creta": ["Camioneta"]
    },
    "Yamaha": {
        "FZ25": ["Motocicleta"], "MT-07": ["Motocicleta"], 
        "R6": ["Motocicleta"], "Crypton": ["Motocicleta"]
    },
    "Mercedes-Benz": {
        "Sprinter": ["Camioneta"], "Clase C": ["Sedán"], 
        "Actros": ["Camión"], "Marcopolo": ["Autobús"]
    }
}
# =========================
# COLORES DE VEHÍCULO
# =========================
# Catálogo cerrado para evitar discrepancias ortográficas o descriptivas en la base de datos.
#PENDIENTE A MEJORAR
COLORES_VEHICULO = [
    "Blanco",
    "Negro",
    "Gris",
    "Plateado",
    "Rojo",
    "Azul",
    "Verde",
    "Amarillo",
    "Naranja",
    "Marrón",
    "Beige",
    "Vino",
    "Dorado",
    "Turquesa",
    "Morado",
    "Rosa",
    "Otro"
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

TABULADOR_INFRACCIONES = {
    # --- ORIGINALES ---
    "EXCESO_VELOCIDAD": {
        "descripcion": "Exceso de velocidad",
        "articulo": "Art. 64",
        "multa": {"min": 1200.00, "max": 2500.00},
        "puntos": 3,
        "corralon": False
    },
    "ESTACIONAMIENTO_PROHIBIDO": {
        "descripcion": "Estacionamiento prohibido",
        "articulo": "Art. 75",
        "multa": {"min": 600.00, "max": 1200.00},
        "puntos": 1,
        "corralon": True
    },
    "CINTURON_SEGURIDAD": {
        "descripcion": "No portar cinturón",
        "articulo": "Art. 52",
        "multa": {"min": 900.00, "max": 1500.00},
        "puntos": 2,
        "corralon": False
    },
    "USO_CELULAR": {
        "descripcion": "Uso de celular",
        "articulo": "Art. 53",
        "multa": {"min": 2000.00, "max": 3500.00},
        "puntos": 4,
        "corralon": False
    },
    "ALCOHOL_EBRIEDAD": {
        "descripcion": "Conducir en estado de ebriedad",
        "articulo": "Art. 99",
        "multa": {"min": 4500.00, "max": 7000.00},
        "puntos": 6,
        "corralon": True,
        "suspension_licencia": True
    },
    "FALTA_DOCUMENTOS": {
        "descripcion": "Falta de documentos (Tarjeta/Licencia)",
        "articulo": "Art. 34",
        "multa": {"min": 800.00, "max": 1500.00},
        "puntos": 0,
        "corralon": True
    },

    # --- NUEVAS INCORPORACIONES REALISTAS ---
    "SEMAFORO_ROJO": {
        "descripcion": "No respetar luz roja de semáforo",
        "articulo": "Art. 147",
        "multa": {"min": 1600.00, "max": 2800.00},
        "puntos": 4,
        "corralon": False
    },
    "SENTIDO_CONTRARIO": {
        "descripcion": "Circular en sentido contrario",
        "articulo": "Art. 141",
        "multa": {"min": 1300.00, "max": 2200.00},
        "puntos": 4,
        "corralon": False
    },
    "SIN_PLACAS": {
        "descripcion": "Circular sin placas o placas ocultas",
        "articulo": "Art. 38",
        "multa": {"min": 2500.00, "max": 4000.00},
        "puntos": 0,
        "corralon": True
    },
    "VIDRIOS_POLARIZADOS": {
        "descripcion": "Vidrios con opacidad no permitida",
        "articulo": "Art. 36",
        "multa": {"min": 800.00, "max": 1600.00},
        "puntos": 0,
        "corralon": False
    },
    "LUGAR_DISCAPACITADOS": {
        "descripcion": "Obstruir cajón para personas con discapacidad",
        "articulo": "Art. 211",
        "multa": {"min": 3200.00, "max": 5400.00},
        "puntos": 3,
        "corralon": True
    },
    "CASCO_MOTOCICLETA": {
        "descripcion": "No portar casco protector (Motociclistas)",
        "articulo": "Art. 222",
        "multa": {"min": 500.00, "max": 1100.00},
        "puntos": 2,
        "corralon": True
    },
    "VUELTA_PROHIBIDA": {
        "descripcion": "Realizar vuelta en U o prohibida",
        "articulo": "Art. 150",
        "multa": {"min": 850.00, "max": 1700.00},
        "puntos": 2,
        "corralon": False
    },
    "LUCES_DEFECTUOSAS": {
        "descripcion": "Circular sin luces o luces fundidas",
        "articulo": "Art. 30",
        "multa": {"min": 450.00, "max": 950.00},
        "puntos": 1,
        "corralon": False
    },
    "OBSTRUIR_PASO_EMERGENCIA": {
        "descripcion": "No ceder el paso a vehículos de emergencia",
        "articulo": "Art. 162",
        "multa": {"min": 1800.00, "max": 3100.00},
        "puntos": 3,
        "corralon": False
    },
    "MANEJO_TEMERARIO": {
        "descripcion": "Manejo negligente o temerario",
        "articulo": "Art. 101",
        "multa": {"min": 4000.00, "max": 6500.00},
        "puntos": 5,
        "corralon": True
    },
    "MENOR_SIN_SILLA": {
        "descripcion": "Menor de 5 años sin silla de retención",
        "articulo": "Art. 68",
        "multa": {"min": 1500.00, "max": 2600.00},
        "puntos": 3,
        "corralon": False
    },
    "INVADIR_CARRIL_BUS": {
        "descripcion": "Circular o invadir carril de transporte público",
        "articulo": "Art. 135",
        "multa": {"min": 2100.00, "max": 3800.00},
        "puntos": 2,
        "corralon": True
    },
    "RUIDO_EXCESIVO": {
        "descripcion": "Emisión de ruidos molestos o escape modificado",
        "articulo": "Art. 42",
        "multa": {"min": 550.00, "max": 1100.00},
        "puntos": 0,
        "corralon": False
    },
    "OBSTRUIR_PEATON": {
        "descripcion": "No ceder el paso o invadir zona peatonal",
        "articulo": "Art. 115",
        "multa": {"min": 1100.00, "max": 1900.00},
        "puntos": 3,
        "corralon": False
    },
    "OTRO": {
        "descripcion": "Otro",
        "articulo": "Art. 1 (General)",
        "multa": {"min": 100.00, "max": 10000.00},
        "puntos": 0,
        "corralon": False
    }
}

# Mapeo de Código Postal a Ciudad y Estado
MAPEO_CP = {
    "97000": ("Mérida", "Yucatán"),
    "97100": ("Mérida", "Yucatán"),
    "97130": ("Mérida", "Yucatán"),
    "97302": ("Progreso", "Yucatán"),
    "97370": ("Kanasín", "Yucatán"),
    # Puedes agregar más aquí...
}


TIPOS_INFRACCION = [datos["descripcion"] for datos in TABULADOR_INFRACCIONES.values()]