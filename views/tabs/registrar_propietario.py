from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, 
                               QLineEdit, QPushButton, QComboBox, QMessageBox, 
                               QGroupBox, QScrollArea)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

# Importamos el backend real
from models.propietario import Propietario
from logic.gestor_propietarios import GestorPropietarios
import logic.catalogos as cat


class TabRegistrarPropietario(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.configurar_ui()

    def configurar_ui(self):
        # Usamos un ScrollArea por si la ventana se hace pequeña, el formulario largo no se corte
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        
        widget_contenedor = QWidget()
        layout_principal = QVBoxLayout(widget_contenedor)
        
        # --- NUEVO: Darle respiro al layout principal ---
        layout_principal.setSpacing(25) # Separación entre los cuadros (Personales, Dirección, Contacto)
        layout_principal.setContentsMargins(30, 35, 30, 20) # Márgenes contra los bordes de la ventana


        # ==========================================
        # BLOQUE 1: DATOS PERSONALES
        # ==========================================
        label_personales = QLabel("Datos Personales")
        label_personales.setStyleSheet("font-weight: bold; color: #89b4fa;")

        contenedor_personales = QWidget()
        # CAMBIO AQUÍ: Se usa #nombre_objeto para que el estilo sea EXCLUSIVO del contenedor
        contenedor_personales.setObjectName("bloquePersonales")
        contenedor_personales.setStyleSheet("#bloquePersonales { border: 1px solid white; border-radius: 4px; }")
        
        grid_personales = QGridLayout(contenedor_personales)
        grid_personales.setVerticalSpacing(15)
        grid_personales.setHorizontalSpacing(15)

        self.input_nombres = QLineEdit()
        self.input_nombres.setPlaceholderText("Nombre(s) *")

        self.input_ap_paterno = QLineEdit()
        self.input_ap_paterno.setPlaceholderText("Apellido Paterno *")

        self.input_ap_materno = QLineEdit()
        self.input_ap_materno.setPlaceholderText("Apellido Materno *")

        self.input_curp = QLineEdit()
        self.input_curp.setMaxLength(18)
        self.input_curp.setPlaceholderText("18 caracteres alfanuméricos *")

        grid_personales.addWidget(QLabel("Nombre(s): *"), 0, 0)
        grid_personales.addWidget(self.input_nombres, 0, 1, 1, 3)

        grid_personales.addWidget(QLabel("Ap. Paterno: *"), 1, 0)
        grid_personales.addWidget(self.input_ap_paterno, 1, 1)

        grid_personales.addWidget(QLabel("Ap. Materno:"), 1, 2)
        grid_personales.addWidget(self.input_ap_materno, 1, 3)

        grid_personales.addWidget(QLabel("CURP: *"), 2, 0)
        grid_personales.addWidget(self.input_curp, 2, 1, 1, 3)

        layout_principal.addWidget(label_personales)
        layout_principal.addWidget(contenedor_personales)

        # ==========================================
        # BLOQUE 2: DIRECCIÓN
        # ==========================================
        label_direccion = QLabel("Dirección de Residencia")
        label_direccion.setStyleSheet("font-weight: bold; color: #89b4fa;")

        contenedor_direccion = QWidget()
        # CAMBIO AQUÍ: Selector de ID exclusivo
        contenedor_direccion.setObjectName("bloqueDireccion")
        contenedor_direccion.setStyleSheet("#bloqueDireccion { border: 1px solid white; border-radius: 4px; }")
        
        grid_direccion = QGridLayout(contenedor_direccion)
        grid_direccion.setVerticalSpacing(15)
        grid_direccion.setHorizontalSpacing(15)

        self.input_calle = QLineEdit()
        self.input_calle.setPlaceholderText("Ej. Calle 60 *")

        self.input_num_ext = QLineEdit()
        self.input_num_ext.setPlaceholderText("Ej. 123 *")

        self.input_num_int = QLineEdit()
        self.input_num_int.setPlaceholderText("Ej. B (Opcional)")

        self.input_colonia = QLineEdit()
        self.input_colonia.setPlaceholderText("Ej. Centro *")

        self.input_cp = QLineEdit()
        self.input_cp.setMaxLength(5)
        self.input_cp.setPlaceholderText("Ej. 97000 *")
        validador_cp = QRegularExpressionValidator(QRegularExpression(r"^[0-9]{5}$"))
        self.input_cp.setValidator(validador_cp)
        self.input_cp.textChanged.connect(self.autocompletar_ubicacion)
        
        
        self.input_ciudad = QLineEdit()
        self.input_ciudad.setReadOnly(True) # Bloqueado
        self.input_ciudad.setPlaceholderText("Automático por CP *")
        self.input_ciudad.setStyleSheet("background-color: #181825; color: #a6adc8;") # Estilo visual de bloqueado

        self.input_estado_prov = QLineEdit()
        self.input_estado_prov.setReadOnly(True) # Bloqueado
        self.input_estado_prov.setPlaceholderText("Automático por CP *")
        self.input_estado_prov.setStyleSheet("background-color: #181825; color: #a6adc8;")
        grid_direccion.addWidget(QLabel("Calle: *"), 0, 0)
        grid_direccion.addWidget(self.input_calle, 0, 1, 1, 3)

        grid_direccion.addWidget(QLabel("No. Ext: *"), 1, 0)
        grid_direccion.addWidget(self.input_num_ext, 1, 1)

        grid_direccion.addWidget(QLabel("No. Int:"), 1, 2)
        grid_direccion.addWidget(self.input_num_int, 1, 3)

        grid_direccion.addWidget(QLabel("Colonia: *"), 2, 0)
        grid_direccion.addWidget(self.input_colonia, 2, 1)

        grid_direccion.addWidget(QLabel("C.P.: *"), 2, 2)
        grid_direccion.addWidget(self.input_cp, 2, 3)

        grid_direccion.addWidget(QLabel("Ciudad: *"), 3, 0)
        grid_direccion.addWidget(self.input_ciudad, 3, 1)

        grid_direccion.addWidget(QLabel("Estado: *"), 3, 2)
        grid_direccion.addWidget(self.input_estado_prov, 3, 3)

        layout_principal.addWidget(label_direccion)
        layout_principal.addWidget(contenedor_direccion)

        # ==========================================
        # BLOQUE 3: CONTACTO Y ADMINISTRATIVO
        # ==========================================
        label_contacto = QLabel("Datos de Contacto y Licencia")
        label_contacto.setStyleSheet("font-weight: bold; color: #89b4fa;")

        contenedor_contacto = QWidget()
        # CAMBIO AQUÍ: Selector de ID exclusivo
        contenedor_contacto.setObjectName("bloqueContacto")
        contenedor_contacto.setStyleSheet("#bloqueContacto { border: 1px solid white; border-radius: 4px; }")
        
        grid_contacto = QGridLayout(contenedor_contacto)
        grid_contacto.setVerticalSpacing(15)
        grid_contacto.setHorizontalSpacing(15)

        self.input_telefono = QLineEdit()
        self.input_telefono.setMaxLength(10)
        self.input_telefono.setPlaceholderText("10 dígitos numéricos *")
        validador_numeros = QRegularExpressionValidator(QRegularExpression(r"^[0-9]+$"))
        self.input_telefono.setValidator(validador_numeros)

        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("ejemplo@correo.com *")

        self.combo_licencia = QComboBox()
        self.combo_licencia.addItems(cat.ESTADOS_LICENCIA)
        self.combo_licencia.setMinimumHeight(30)

        grid_contacto.addWidget(QLabel("Teléfono: *"), 0, 0)
        grid_contacto.addWidget(self.input_telefono, 0, 1)

        grid_contacto.addWidget(QLabel("Correo: *"), 0, 2)
        grid_contacto.addWidget(self.input_correo, 0, 3)

        grid_contacto.addWidget(QLabel("Estado Licencia: *"), 1, 0)
        grid_contacto.addWidget(self.combo_licencia, 1, 1)

        layout_principal.addWidget(label_contacto)
        layout_principal.addWidget(contenedor_contacto)

        # ==========================================
        self.btn_guardar = QPushButton("Registrar Propietario")
        self.btn_guardar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 12px; margin-top: 10px;")
        self.btn_guardar.clicked.connect(self.procesar_registro)
        
        layout_principal.addStretch()
        layout_principal.addWidget(self.btn_guardar, alignment=Qt.AlignRight)

        # Ensamblamos todo en el layout principal de la pestaña
        scroll_area.setWidget(widget_contenedor)
        layout_final = QVBoxLayout(self)
        layout_final.setContentsMargins(0, 0, 0, 0)
        layout_final.addWidget(scroll_area)

    # ==========================================
    # LÓGICA DE INTERFAZ
    # ==========================================
    def procesar_registro(self):
        """Valida que los campos no estén vacíos y empaqueta el nuevo formato."""
        
        nombres = self.input_nombres.text().strip().upper()
        ap_paterno = self.input_ap_paterno.text().strip().upper()
        ap_materno = self.input_ap_materno.text().strip().upper()
        curp = self.input_curp.text().strip().upper()
        
        calle = self.input_calle.text().strip().upper()
        num_ext = self.input_num_ext.text().strip().upper()
        num_int = self.input_num_int.text().strip().upper()
        colonia = self.input_colonia.text().strip().upper()
        cp = self.input_cp.text().strip()
        ciudad = self.input_ciudad.text().strip().upper()
        estado_prov = self.input_estado_prov.text().strip().upper()
        
        telefono = self.input_telefono.text().strip()
        correo = self.input_correo.text().strip().lower() 
        licencia = self.combo_licencia.currentText()

        # 1. Validación de campos obligatorios
        if not all([nombres, ap_paterno, curp, calle, num_ext, colonia, cp, ciudad, estado_prov, telefono, correo]):
            QMessageBox.warning(self, "Campos Incompletos", "Por favor llene todos los campos marcados con asterisco (*).")
            return

        # 2. Validación de longitud de CURP
        if len(curp) != 18:
            QMessageBox.warning(self, "CURP Inválida", "La CURP debe tener exactamente 18 caracteres.")
            return

        # 3. Validación básica de correo
        if "@" not in correo or "." not in correo:
            QMessageBox.warning(self, "Correo Inválido", "Por favor ingrese un correo electrónico válido.")
            return

        # 4. Empaquetado en el nuevo modelo respetando el gafete de auditoría
        nuevo_propietario = Propietario(
            nombres=nombres,
            apellido_paterno=ap_paterno,
            apellido_materno=ap_materno,
            curp=curp,
            calle=calle,
            numero_exterior=num_ext,
            numero_interior=num_int,
            colonia=colonia,
            codigo_postal=cp,
            ciudad=ciudad,
            estado_provincia=estado_prov,
            telefono=telefono,
            correo_electronico=correo,
            estado_licencia=licencia,
            estado="Activo",
            id_usuario_registro=self.usuario_actual.id_usuario # Garantizamos el reporte de auditoría
        )
        
        # Llamamos al gestor
        exito, mensaje = GestorPropietarios.registrar_propietario(nuevo_propietario)
        
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error al Guardar", mensaje)

    def autocompletar_ubicacion(self, cp_texto):
        if cp_texto in cat.MAPEO_CP:
            ciudad, estado = cat.MAPEO_CP[cp_texto]
            self.input_ciudad.setText(ciudad)
            self.input_estado_prov.setText(estado)
    
    
    def limpiar_formulario(self):
        """Devuelve el formulario a su estado original."""
        self.input_nombres.clear()
        self.input_ap_paterno.clear()
        self.input_ap_materno.clear()
        self.input_curp.clear()
        
        self.input_calle.clear()
        self.input_num_ext.clear()
        self.input_num_int.clear()
        self.input_colonia.clear()
        self.input_cp.clear()
        self.input_ciudad.clear()
        self.input_estado_prov.setText("Yucatán") 
        
        self.input_telefono.clear()
        self.input_correo.clear()
        self.combo_licencia.setCurrentIndex(0)