from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget
from PySide6.QtCore import Qt
from views.tabs.registrar_agente import TabRegistrarAgente
# (Asumiendo que crearás una TabModificarAgente similar a la de propietarios)
import logic.catalogos as cat

class PanelAgentes(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.configurar_ui()

    def configurar_ui(self):
        layout = QVBoxLayout(self)
        
        lbl_titulo = QLabel("Módulo de Oficiales y Agentes")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #cdd6f4;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        self.pestanas = QTabWidget()
        self.tab_registrar = TabRegistrarAgente(self.usuario_actual)
        
        rol = self.usuario_actual.rol
        # Solo Admin y Supervisor gestionan agentes
        if rol in [cat.ROLES_USUARIO[0], cat.ROLES_USUARIO[3]]:
            self.pestanas.addTab(self.tab_registrar, "Registrar Agente")
            # Aquí agregarías la pestaña de modificación
            
        layout.addWidget(self.pestanas)