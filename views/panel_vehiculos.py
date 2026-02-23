from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QTabWidget, 
QFormLayout, QMessageBox, QSpinBox)
from PySide6.QtCore import Qt
import logic.catalogos as cat

class PanelVehiculos(QWidget):
    def __init__(self):
        super().__init__()
        self.configurar_ui()

    def configurar_ui(self):
        # Layout principal del panel
        layout_principal = QVBoxLayout(self)
        
        # Título del módulo
        lbl_titulo = QLabel("Módulo de Gestión de Vehículos")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(lbl_titulo)

        # ==========================================
        # CREACIÓN DE PESTAÑAS (QTabWidget)
        # ==========================================
        self.pestanas = QTabWidget()
        
        self.tab_registrar = QWidget()
        self.tab_modificar = QWidget()
        
        self.pestanas.addTab(self.tab_registrar, "Registrar Nuevo Vehículo")
        self.pestanas.addTab(self.tab_modificar, "Modificar Vehículo")
        
        layout_principal.addWidget(self.pestanas)

        # Construir el contenido de cada pestaña
        self.construir_tab_registrar()
        self.construir_tab_modificar()

    # ==========================================
    # PESTAÑA 1: REGISTRAR VEHÍCULO
    # ==========================================
    def construir_tab_registrar(self):
        layout = QVBoxLayout(self.tab_registrar)
        
        # QFormLayout es ideal para formularios: pone un Label a la izquierda y un Input a la derecha
        formulario = QFormLayout()
        
        self.input_vin = QLineEdit()
        self.input_placa = QLineEdit()
        self.input_marca = QLineEdit()
        self.input_modelo = QLineEdit()
        
        # QSpinBox es para números enteros (Ideal para el año)
        self.input_anio = QSpinBox()
        self.input_anio.setRange(1900, 2030)
        self.input_anio.setValue(2024)
        
        # QComboBox es una lista desplegable. Las llenamos con tus catálogos.
        self.combo_color = QComboBox()
        self.combo_color.addItems(cat.COLORES_VEHICULO)
        
        self.combo_clase = QComboBox()
        self.combo_clase.addItems(cat.CLASES_VEHICULO)
        
        self.combo_procedencia = QComboBox()
        self.combo_procedencia.addItems(["Nacional", "Extranjero"])
        
        self.input_id_propietario = QLineEdit()
        self.input_id_propietario.setPlaceholderText("ID numérico del propietario")

        # Agregamos las filas al formulario
        formulario.addRow("VIN (17 caracteres):", self.input_vin)
        formulario.addRow("Placa:", self.input_placa)
        formulario.addRow("Marca:", self.input_marca)
        formulario.addRow("Modelo:", self.input_modelo)
        formulario.addRow("Año:", self.input_anio)
        formulario.addRow("Color:", self.combo_color)
        formulario.addRow("Clase:", self.combo_clase)
        formulario.addRow("Procedencia:", self.combo_procedencia)
        formulario.addRow("ID Propietario:", self.input_id_propietario)

        layout.addLayout(formulario)

        # Botón de guardado
        self.btn_guardar = QPushButton("Guardar Vehículo")
        self.btn_guardar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px;")
        # self.btn_guardar.clicked.connect(self.logica_guardar) # Se conectará después
        
        layout.addWidget(self.btn_guardar, alignment=Qt.AlignRight)

    # ==========================================
    # PESTAÑA 2: MODIFICAR VEHÍCULO
    # ==========================================
    def construir_tab_modificar(self):
        layout = QVBoxLayout(self.tab_modificar)
        
        # Zona de búsqueda
        layout_busqueda = QHBoxLayout()
        self.input_buscar_vin = QLineEdit()
        self.input_buscar_vin.setPlaceholderText("Ingrese el VIN a buscar...")
        btn_buscar = QPushButton("Buscar")
        
        layout_busqueda.addWidget(QLabel("VIN del Vehículo:"))
        layout_busqueda.addWidget(self.input_buscar_vin)
        layout_busqueda.addWidget(btn_buscar)
        
        layout.addLayout(layout_busqueda)

        # Formulario de modificación (Solo los campos permitidos según tus reglas)
        formulario = QFormLayout()
        
        self.mod_placa = QLineEdit()
        self.mod_color = QComboBox()
        self.mod_color.addItems(cat.COLORES_VEHICULO)
        
        self.mod_estado = QComboBox()
        self.mod_estado.addItems(["Activo", "Inactivo", "Robado"]) # Debería venir de catálogos

        formulario.addRow("Nueva Placa:", self.mod_placa)
        formulario.addRow("Nuevo Color:", self.mod_color)
        formulario.addRow("Estado Legal:", self.mod_estado)
        
        layout.addLayout(formulario)

        # Botón de actualización
        self.btn_actualizar = QPushButton("Actualizar Datos")
        self.btn_actualizar.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold; padding: 10px;")
        
        layout.addStretch() # Empuja el botón hacia abajo
        layout.addWidget(self.btn_actualizar, alignment=Qt.AlignRight)