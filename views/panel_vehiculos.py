from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QTabWidget, 
QFormLayout, QMessageBox, QSpinBox)
from PySide6.QtCore import Qt

#Conexiones con el backend (logic)
import logic.catalogos as cat
from models.vehiculo import Vehiculo
from logic.gestor_vehiculos import GestorVehiculos

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
        """Construye el formulario garantizando la integridad de los datos mediante catálogos cerrados."""
        layout = QVBoxLayout(self.tab_registrar)
        formulario = QFormLayout()
        
        # 1. Entradas de texto restringidas
        self.input_vin = QLineEdit()
        self.input_vin.setMaxLength(17) # Frontend Defensivo: Evita que escriban de más
        self.input_vin.setPlaceholderText("Ej: 3G1SE516X3S205891")
        self.input_placa = QLineEdit()
        self.input_placa.setPlaceholderText("Ej: YYU-021-A")
        self.input_id_propietario = QLineEdit()
        self.input_id_propietario.setPlaceholderText("ID numérico del propietario")
        
        self.input_anio = QSpinBox()
        self.input_anio.setRange(1900, 2030)
        self.input_anio.setValue(2024)
        self.input_anio.setButtonSymbols(QSpinBox.PlusMinus)
        
        # 2. Listas Desplegables (QComboBox) conectadas a catalogos.py
        self.combo_marca = QComboBox()
        self.combo_marca.addItems(cat.MARCAS_MODELOS_VEHICULO.keys())
        
        self.combo_modelo = QComboBox()
        
        self.combo_color = QComboBox()
        self.combo_color.addItems(cat.COLORES_VEHICULO)
        
        self.combo_clase = QComboBox()
        # Nota: Ya NO llenamos la clase aquí con cat.CLASES_VEHICULO. 
        # La clase se llenará sola dependiendo del modelo.
        
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(cat.ESTADOS_VEHICULO)

        self.combo_procedencia = QComboBox()
        self.combo_procedencia.addItems(cat.PROCEDENCIAS_VEHICULO)

        # 3. CONEXIÓN DINÁMICA (Cascada Doble)
        # Primera cascada: Al cambiar Marca -> Actualiza Modelos
        self.combo_marca.currentTextChanged.connect(self.actualizar_modelos)
        
        # Segunda cascada: Al cambiar Modelo -> Actualiza Clases
        self.combo_modelo.currentTextChanged.connect(self.actualizar_clases)
        
        # Forzamos la primera actualización para arrancar con datos
        self.actualizar_modelos(self.combo_marca.currentText())

        # Forzamos una primera actualización manual para que el modelo no empiece vacío al abrir el programa
        self.actualizar_modelos(self.combo_marca.currentText())

        # 4. Ensamblaje del Formulario
        formulario.addRow("VIN (17 caracteres):", self.input_vin)
        formulario.addRow("Placa:", self.input_placa)
        formulario.addRow("Marca:", self.combo_marca)
        formulario.addRow("Modelo:", self.combo_modelo)
        formulario.addRow("Año:", self.input_anio)
        formulario.addRow("Color:", self.combo_color)
        formulario.addRow("Clase:", self.combo_clase)
        formulario.addRow("Estado Legal:", self.combo_estado)
        formulario.addRow("Procedencia:", self.combo_procedencia)
        formulario.addRow("ID Propietario:", self.input_id_propietario)

        layout.addLayout(formulario)

        # Botón de Guardado
        self.btn_guardar = QPushButton("Guardar Vehículo")
        self.btn_guardar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px;")
        layout.addWidget(self.btn_guardar, alignment=Qt.AlignRight)

        # Conexion con el backend
        self.btn_guardar.clicked.connect(self.procesar_registro)
        layout.addWidget(self.btn_guardar, alignment=Qt.AlignRight)
        
        
    # ==========================================
    # MÉTODOS AUXILIARES PARA LA INTERFAZ
    # ==========================================
    def actualizar_modelos(self, marca_seleccionada):
        """Primera cascada: Llena los modelos basados en la marca."""
        self.combo_modelo.clear() 
        
        if marca_seleccionada in cat.MARCAS_MODELOS_VEHICULO:
            # Ahora extraemos solo las llaves (los nombres de los modelos)
            modelos_permitidos = list(cat.MARCAS_MODELOS_VEHICULO[marca_seleccionada].keys())
            self.combo_modelo.addItems(modelos_permitidos)
    
    def actualizar_clases(self, modelo_seleccionado):
        """Segunda cascada: Llena las clases y bloquea el campo si solo hay una opción."""
        self.combo_clase.clear()
        
        marca_actual = self.combo_marca.currentText()
        
        # Verificamos que la marca y el modelo existan en el catálogo
        if marca_actual in cat.MARCAS_MODELOS_VEHICULO and modelo_seleccionado in cat.MARCAS_MODELOS_VEHICULO[marca_actual]:
            
            # Traemos la lista de clases permitidas (ej. ["Sedán", "Hatchback"] o solo ["Sedán"])
            clases_permitidas = cat.MARCAS_MODELOS_VEHICULO[marca_actual][modelo_seleccionado]
            self.combo_clase.addItems(clases_permitidas)
            
            # Frontend Defensivo: Si solo hay una clase, bloqueamos el menú para evitar errores
            if len(clases_permitidas) == 1:
                self.combo_clase.setEnabled(False) # Se pone gris y no se puede cambiar
            else:
                self.combo_clase.setEnabled(True)  # Se habilita para que el operador elija
    
    def procesar_registro(self):
        """Extraemos los datos de la interfaz, los empaqueta y los enviamos al backend."""
        
        # 1. Extraer datos (Usamos .strip() para quitar espacios accidentales)
        # Convertimos VIN y Placa a mayúsculas automáticamente como medida defensiva
        vin = self.input_vin.text().strip().upper()
        placa = self.input_placa.text().strip().upper()
        marca = self.combo_marca.currentText()
        modelo = self.combo_modelo.currentText()
        anio = self.input_anio.value()
        color = self.combo_color.currentText()
        clase = self.combo_clase.currentText()
        estado = self.combo_estado.currentText()
        procedencia = self.combo_procedencia.currentText()
        
        id_propietario_str = self.input_id_propietario.text().strip()

        # Validación visual rápida: Que no intenten guardar con campos vacíos críticos
        if not vin or not placa or not id_propietario_str:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor, llene el VIN, Placa y el ID del Propietario.")
            return

        # Convertir el ID a entero (Si el usuario escribió letras, lo atrapamos aquí)
        try:
            id_propietario = int(id_propietario_str)
        except ValueError:
            QMessageBox.warning(self, "Error de Formato", "El ID del propietario debe ser un número entero válido.")
            return

        # 2. Empaquetar en el Modelo
        nuevo_vehiculo = Vehiculo(
            vin=vin, 
            placa=placa, 
            marca=marca, 
            modelo=modelo, 
            anio=anio, 
            color=color, 
            clase=clase, 
            estado_legal=estado, 
            procedencia=procedencia, 
            id_propietario=id_propietario
        )

        # 3. Enviar al Backend
        # Aquí cruzamos los dedos. El Gestor validará todo e insertará en SQLite
        exito, mensaje = GestorVehiculos.registrar_vehiculo(nuevo_vehiculo)

        # 4. Dar Retroalimentación al Operador
        if exito:
            QMessageBox.information(self, "Registro Exitoso", mensaje)
            self.limpiar_formulario() # Limpiamos la pantalla para el siguiente auto
        else:
            # Si falló (ej. VIN repetido, modelo inválido), mostramos el mensaje exacto de tu validador
            QMessageBox.critical(self, "Error al Guardar", mensaje)

    def limpiar_formulario(self):
        """Limpia las cajas de texto después de un guardado exitoso."""
        self.input_vin.clear()
        self.input_placa.clear()
        self.input_id_propietario.clear()
        self.input_anio.setValue(2024) # Regresamos al valor por defecto
        self.combo_marca.setCurrentIndex(0) # Regresamos a la primera marca
    

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
        self.mod_placa.setPlaceholderText("Ej: YYU-021-A")
        self.mod_color = QComboBox()
        self.mod_color.addItems(cat.COLORES_VEHICULO)
        
        self.mod_estado = QComboBox()
        self.mod_estado.addItems(cat.ESTADOS_VEHICULO) # Debería venir de catálogos

        formulario.addRow("Nueva Placa:", self.mod_placa)
        formulario.addRow("Nuevo Color:", self.mod_color)
        formulario.addRow("Estado Legal:", self.mod_estado)
        
        layout.addLayout(formulario)

        # Botón de actualización
        self.btn_actualizar = QPushButton("Actualizar Datos")
        self.btn_actualizar.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold; padding: 10px;")
        
        layout.addStretch() # Empuja el botón hacia abajo
        layout.addWidget(self.btn_actualizar, alignment=Qt.AlignRight)