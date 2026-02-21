import re
from datetime import datetime

class Validador:
    """
    Centraliza todas las validaciones de formato y reglas de negocio.
    Retorna True si es válido, o (False, "Mensaje de error") si falla.
    """

    @staticmethod
    def validar_vin(vin):
        # Debe tener longitud válida (17 caracteres) 
        if not vin or len(str(vin).strip()) != 17:
            return False, "El VIN debe tener exactamente 17 caracteres."
        return True, ""

    @staticmethod
    def validar_curp(curp):
        # Debe cumplir con formato oficial (18 caracteres alfanuméricos) [cite: 337]
        patron = r'^[A-Z0-9]{18}$'
        if not re.match(patron, str(curp).strip().upper()):
            return False, "La CURP debe tener 18 caracteres alfanuméricos."
        return True, ""

    @staticmethod
    def validar_anio_vehiculo(anio):
        # Debe ser numérico, no mayor al año actual, y no menor a 1900 [cite: 357, 358, 359]
        try:
            anio_int = int(anio)
            anio_actual = datetime.now().year
            if anio_int < 1900 or anio_int > anio_actual:
                return False, f"El año debe estar entre 1900 y {anio_actual}."
            return True, ""
        except ValueError:
            return False, "El año debe ser un valor numérico."

    @staticmethod
    def validar_correo(correo):
        # Debe cumplir formato estándar [cite: 349]
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, str(correo).strip()):
            return False, "El formato del correo electrónico no es válido."
        return True, ""

    @staticmethod
    def validar_telefono(telefono):
        # Debe contener únicamente dígitos [cite: 351]
        # Asumimos longitud estándar nacional de 10 dígitos [cite: 352]
        if not str(telefono).isdigit() or len(str(telefono).strip()) != 10:
            return False, "El teléfono debe contener exactamente 10 dígitos numéricos."
        return True, ""

    @staticmethod
    def validar_monto(monto):
        # Debe ser numérico y mayor a cero.
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                return False, "El monto de la infracción debe ser mayor a cero."
            return True, ""
        except ValueError:
            return False, "El monto debe ser un valor numérico."