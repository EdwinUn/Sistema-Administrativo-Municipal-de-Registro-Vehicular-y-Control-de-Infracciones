from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, 
                               QLineEdit, QPushButton, QComboBox, QMessageBox, 
                               QGroupBox, QScrollArea)
from PySide6.QtCore import Qt
from models.agente import Agente
from logic.gestor_agentes import GestorAgentes
import logic.catalogos as cat

class TabRegistrarAgente(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.configurar_ui()

    def configurar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setSpacing(25)
        layout_principal.setContentsMargins(30, 20, 30, 20)

        label_titulo = QLabel("Alta de Oficiales de Tránsito")
        label_titulo.setStyleSheet("font-weight: bold; color: #89b4fa; font-size: 16px;")
        
        contenedor = QWidget()
        contenedor.setObjectName("bloqueAgente")
        contenedor.setStyleSheet("#bloqueAgente { border: 1px solid white; border-radius: 4px; }")
        
        grid = QGridLayout(contenedor)
        grid.setSpacing(15)

        self.input_nombre = QLineEdit(); self.input_nombre.setPlaceholderText("Nombre completo del oficial *")
        self.input_placa = QLineEdit(); self.input_placa.setPlaceholderText("Ej. AG-105 *")
        self.input_cargo = QLineEdit(); self.input_cargo.setPlaceholderText("Ej. Patrullero / Vialidad *")

        grid.addWidget(QLabel("Nombre Completo: *"), 0, 0)
        grid.addWidget(self.input_nombre, 0, 1, 1, 3)
        grid.addWidget(QLabel("No. Placa: *"), 1, 0)
        grid.addWidget(self.input_placa, 1, 1)
        grid.addWidget(QLabel("Cargo: *"), 1, 2)
        grid.addWidget(self.input_cargo, 1, 3)

        self.btn_guardar = QPushButton("Registrar Oficial")
        self.btn_guardar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px;")
        self.btn_guardar.clicked.connect(self.procesar_registro)

        layout_principal.addWidget(label_titulo)
        layout_principal.addWidget(contenedor)
        layout_principal.addStretch()
        layout_principal.addWidget(self.btn_guardar, alignment=Qt.AlignRight)

    def procesar_registro(self):
        nombre = self.input_nombre.text().strip().upper()
        placa = self.input_placa.text().strip().upper()
        cargo = self.input_cargo.text().strip().upper()

        if not all([nombre, placa, cargo]):
            QMessageBox.warning(self, "Campos Vacíos", "Todos los campos son obligatorios.")
            return

        nuevo_agente = Agente(
            numero_placa=placa, nombre_completo=nombre, cargo=cargo,
            id_usuario_registro=self.usuario_actual.id_usuario
        )
        
        exito, msj = GestorAgentes.registrar_agente(nuevo_agente)
        if exito:
            QMessageBox.information(self, "Éxito", msj)
            self.input_nombre.clear(); self.input_placa.clear(); self.input_cargo.clear()
        else:
            QMessageBox.critical(self, "Error", msj)