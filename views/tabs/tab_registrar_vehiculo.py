from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QFormLayout, 
QMessageBox, QSpinBox, QHBoxLayout)
from PySide6.QtCore import Qt

# Importaciones del backend (Mantenemos las rutas absolutas asumiendo que ejecutas desde el main)
import logic.catalogos as cat
from models.vehiculo import Vehiculo
from logic.gestor_vehiculos import GestorVehiculos
from logic.gestor_propietarios import GestorPropietarios

# [REFACTORIZACIÓN]: Cambiamos el nombre de la clase. 
# Ya no es "PanelVehiculos", ahora es un componente específico llamado "TabRegistrarVehiculo".
# Hereda directamente de QWidget, por lo que esta clase ES la pestaña en sí misma.
class TabRegistrarVehiculo(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.configurar_ui()

    def configurar_ui(self):
        """Construye el formulario garantizando la integridad de los datos mediante catálogos cerrados."""
        # [REFACTORIZACIÓN]: El layout ahora se aplica a 'self' (esta misma pestaña),
        # ya no a 'self.tab_registrar' porque esa variable ya no existe ni es necesaria.
        layout = QVBoxLayout(self)
        formulario = QFormLayout()
        
        # 1. Entradas de texto restringidas
        self.input_vin = QLineEdit()
        self.input_vin.setMaxLength(17) 
        self.input_vin.setPlaceholderText("Ej: 3G1SE516X3S205891")
        
        self.input_placa = QLineEdit()
        self.input_placa.setPlaceholderText("Ej: YYU-021-A")
        
        self.input_id_propietario = QLineEdit()
        self.input_id_propietario.setPlaceholderText("Ej. PRP-00001")
        self.input_id_propietario.textChanged.connect(self.verificar_limpieza_id)
        
        self.input_anio = QSpinBox()
        self.input_anio.setRange(1899, 2030)
        self.input_anio.setSpecialValueText(" ")
        self.input_anio.setValue(1899)
        self.input_anio.setButtonSymbols(QSpinBox.PlusMinus)
        
        # 2. Listas Desplegables (QComboBox) conectadas a catalogos.py
        self.combo_marca = QComboBox()
        self.combo_marca.addItems(cat.MARCAS_MODELOS_VEHICULO.keys())    
        self.combo_marca.setCurrentIndex(-1) 
        
        self.combo_modelo = QComboBox()
        self.combo_modelo.setCurrentIndex(-1) 
        
        self.combo_color = QComboBox()
        self.combo_color.addItems(cat.COLORES_VEHICULO)
        self.combo_color.setCurrentIndex(-1) 
        
        self.combo_clase = QComboBox()
        self.combo_clase.setCurrentIndex(-1) 
        
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(cat.ESTADOS_VEHICULO)
        self.combo_estado.setCurrentIndex(-1)
        
        self.combo_procedencia = QComboBox()
        self.combo_procedencia.addItems(cat.PROCEDENCIAS_VEHICULO)
        self.combo_procedencia.setCurrentIndex(-1) 
        
        # 3. CONEXIÓN DINÁMICA (Cascada Doble)
        self.combo_marca.currentTextChanged.connect(self.actualizar_modelos)
        self.combo_modelo.currentTextChanged.connect(self.actualizar_clases)
        
        # [REFACTORIZACIÓN]: Eliminé la línea duplicada de 'self.actualizar_modelos'.
        # Solo necesitamos forzarla una vez para arrancar con datos limpios.
        self.actualizar_modelos(self.combo_marca.currentText())

        # ==========================================
        # DISEÑO DEL BUSCADOR DE PROPIETARIO
        # ==========================================
        layout_id_busqueda = QHBoxLayout()
        
        self.input_id_propietario = QLineEdit()
        self.input_id_propietario.setPlaceholderText("Ej. PRP-00001")
        # Bloqueamos la edición manual para obligar a usar el buscador si prefieres 
        # o dejamos que el sistema limpie el formato PRP- después.
        
        self.btn_buscar_prop = QPushButton("🔍 Buscar por CURP")
        self.btn_buscar_prop.setStyleSheet("background-color: #34495e; color: white; padding: 5px;")
        self.btn_buscar_prop.clicked.connect(self.abrir_buscador_propietario)

        layout_id_busqueda.addWidget(self.input_id_propietario)
        layout_id_busqueda.addWidget(self.btn_buscar_prop)

        # Etiqueta de confirmación visual (Nombre del dueño)
        self.lbl_confirmacion_nombre = QLabel("Dueño: (No seleccionado)")
        self.lbl_confirmacion_nombre.setStyleSheet("color: #a6e3a1; font-style: italic; font-size: 11px;")

        
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
        formulario.addRow("ID Propietario:", layout_id_busqueda)
        formulario.addRow("", self.lbl_confirmacion_nombre) # Debajo del ID sale el nombre

        layout.addLayout(formulario)

        # Botón de Guardado
        self.btn_guardar = QPushButton("Guardar Vehículo")
        self.btn_guardar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px;")
        
        self.btn_guardar.clicked.connect(self.procesar_registro)
        layout.addWidget(self.btn_guardar, alignment=Qt.AlignRight)
        
    # ==========================================
    # MÉTODOS LÓGICOS
    # ==========================================

    def actualizar_modelos(self, marca_seleccionada):
        """Primera cascada: Llena los modelos basados en la marca."""
        self.combo_modelo.clear() 
        if marca_seleccionada in cat.MARCAS_MODELOS_VEHICULO:
            modelos_permitidos = list(cat.MARCAS_MODELOS_VEHICULO[marca_seleccionada].keys())
            self.combo_modelo.addItems(modelos_permitidos)
    
    def actualizar_clases(self, modelo_seleccionado):
        """Segunda cascada: Llena las clases y bloquea el campo si solo hay una opción."""
        self.combo_clase.clear()
        marca_actual = self.combo_marca.currentText()
        
        if marca_actual in cat.MARCAS_MODELOS_VEHICULO and modelo_seleccionado in cat.MARCAS_MODELOS_VEHICULO[marca_actual]:
            clases_permitidas = cat.MARCAS_MODELOS_VEHICULO[marca_actual][modelo_seleccionado]
            self.combo_clase.addItems(clases_permitidas)
            
            if len(clases_permitidas) == 1:
                self.combo_clase.setEnabled(False) 
            else:
                self.combo_clase.setEnabled(True) 
    
    def procesar_registro(self):
        """Extrae los datos de la interfaz, los empaqueta y los envía al backend."""
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

        if not vin or not placa or not id_propietario_str:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor, llene el VIN, Placa y el ID del Propietario.")
            return

        id_propietario_str = id_propietario_str.upper()
        
        if not id_propietario_str.startswith("PRP-") or not id_propietario_str[4:].isdigit():
            QMessageBox.warning(self, "Error de Formato", "El ID del propietario debe tener el formato de matrícula oficial (Ej. PRP-00003).")
            return
        id_propietario = int(id_propietario_str.replace("PRP-", ""))
        
        nuevo_vehiculo = Vehiculo(
            vin=vin, placa=placa, marca=marca, modelo=modelo, anio=anio, 
            color=color, clase=clase, estado_legal=estado, 
            procedencia=procedencia, id_propietario=id_propietario,
            id_usuario_registro=self.usuario_actual.id_usuario
        )

        exito, mensaje = GestorVehiculos.registrar_vehiculo(nuevo_vehiculo)

        if exito:
            QMessageBox.information(self, "Registro Exitoso", mensaje)
            self.limpiar_formulario() 
        else:
            QMessageBox.critical(self, "Error al Guardar", mensaje)

    def limpiar_formulario(self):
        """Limpia las cajas de texto después de un guardado exitoso."""
        self.input_vin.clear()
        self.input_placa.clear()
        self.input_id_propietario.clear()
        self.input_anio.setValue(2024) 
        self.combo_marca.setCurrentIndex(0)
        
    def abrir_buscador_propietario(self):
        """Abre un diálogo para buscar al dueño por su CURP."""
        from PySide6.QtWidgets import QInputDialog
        
        curp, ok = QInputDialog.getText(
            self, "Buscador de Propietarios", 
            "Ingrese la CURP del propietario para obtener su ID:"
        )

        if ok and curp.strip():
            # Usamos la lógica que ya tenemos en el gestor
            exito, resultado = GestorPropietarios.buscar_propietario_por_curp(curp.strip().upper())
            
            if exito:
                # El resultado ahora viene desglosado por los cambios que hicimos
                id_real = resultado["id_propietario"]
                nombre_completo = f"{resultado['nombres']} {resultado['apellido_paterno']}"
                
                # Auto-llenamos el campo con el formato de matrícula
                self.input_id_propietario.setText(f"PRP-{id_real:05d}")
                self.lbl_confirmacion_nombre.setText(f"Dueño: {nombre_completo}")
                
                QMessageBox.information(self, "Propietario Localizado", 
                                        f"Se vinculó a: {nombre_completo}")
            else:
                QMessageBox.warning(self, "No Encontrado", resultado)
                self.lbl_confirmacion_nombre.setText("Dueño: (No encontrado)")
                
    def verificar_limpieza_id(self, texto):
        # Si está vacío o si el texto no contiene "PRP-" (lo que indica que se está editando)
        if not texto.strip() or "PRP-" not in texto:
            self.lbl_confirmacion_nombre.setText("Dueño: (No seleccionado)")
            self.lbl_confirmacion_nombre.setStyleSheet("color: #a6adc8; font-style: italic; font-size: 11px;")