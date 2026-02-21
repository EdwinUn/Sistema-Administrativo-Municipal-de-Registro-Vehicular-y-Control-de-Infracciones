from models.propietario import Propietario
from models.vehiculo import Vehiculo
from logic.gestor_propietarios import GestorPropietarios
from logic.gestor_vehiculos import GestorVehiculos

def probar_sistema():
    print("--- INICIANDO PRUEBA MAESTRA ---")

    # Datos de prueba
    prop = Propietario("Armando Muñoz", "MURA050101HYCMXRA1", "Mérida", "9991234567", "a@mail.com", "Vigente")
    
    # 1. Intentar registrar Propietario
    exito_p, msj_p = GestorPropietarios.registrar_propietario(prop)
    print(f"Registro Propietario: {'✅' if exito_p else '❌'} | Mensaje: {msj_p}")

    if exito_p:
        # 2. Intentar registrar Vehículo (solo si el dueño se creó)
        auto = Vehiculo("1HGCM82633A004352", "YUC100A", "Honda", "Civic", 2018, "Negro", "Sedán", "Nacional", 1)
        exito_v, msj_v = GestorVehiculos.registrar_vehiculo(auto)
        print(f"Registro Vehículo:    {'✅' if exito_v else '❌'} | Mensaje: {msj_v}")

if __name__ == "__main__":
    probar_sistema()