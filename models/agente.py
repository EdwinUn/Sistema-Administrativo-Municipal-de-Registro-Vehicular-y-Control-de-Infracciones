class Agente:
    """
    Representa a un funcionario municipal autorizado para emitir infracciones. 
    """
    def __init__(self, numero_placa, nombre_completo, cargo, estado="Activo", id_agente=None):
        self.id_agente = id_agente # Generado por la base de datos 
        self.numero_placa = numero_placa # Identificador oficial único 
        self.nombre_completo = nombre_completo
        self.cargo = cargo
        self.estado = estado # Activo / Inactivo

    def __repr__(self):
        return f"<Agente {self.numero_placa}: {self.nombre_completo} - {self.estado}>"