from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QTabWidget, 
QFormLayout, QDoubleSpinBox, QDateEdit, QTimeEdit, QMessageBox)
from PySide6.QtCore import Qt, QDate, QTime
import logic.catalogos as cat
#Importaciones backend
from models.infraccion import Infraccion
from logic.gestor_infracciones import GestorInfracciones
from logic.gestor_agentes import GestorAgentes
class PanelMultas(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.configurar_ui()
        self.aplicar_permisos()

    def configurar_ui(self):
        """
        Configura la estructura principal del panel, dividiéndolo en pestañas
        para separar el registro de nuevas multas y el cobro/cancelación de las existentes.
        """
        layout_principal = QVBoxLayout(self)
        
        # Título principal del módulo
        lbl_titulo = QLabel("Módulo de Infracciones de Tránsito")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(lbl_titulo)

        # Contenedor de pestañas (QTabWidget)
        self.pestanas = QTabWidget()
        
        # Creamos los dos "lienzos" en blanco para cada pestaña
        self.tab_registrar = QWidget()
        self.tab_gestionar = QWidget()
        
        # Llamamos a los métodos que construyen el interior de cada pestaña
        self.construir_tab_registrar()
        self.construir_tab_gestionar()

        # --- APLICACIÓN DE ROLES (RBAC) ---
        rol = self.usuario_actual.rol
        
        if rol == cat.ROLES_USUARIO[0]: # Administrador
            self.pestanas.addTab(self.tab_registrar, "Registrar Infracción")
            self.pestanas.addTab(self.tab_gestionar, "Cobro y Cancelación")
            
        elif rol == cat.ROLES_USUARIO[2]: # Agente de Tránsito
            # Solo ve la pestaña de registro
            self.pestanas.addTab(self.tab_registrar, "Registrar Infracción")
            
        elif rol == cat.ROLES_USUARIO[3]: # Supervisor
            # Solo ve la pestaña de gestión, pero en modo "Consulta"
            self.pestanas.addTab(self.tab_gestionar, "Consultar Infracción")

        layout_principal.addWidget(self.pestanas)

    # ==========================================
    # PESTAÑA 1: REGISTRAR INFRACCIÓN
    # ==========================================
    def construir_tab_registrar(self):
        """
        Construye el formulario para emitir una nueva multa. 
        Utiliza widgets restrictivos (fechas, números) para garantizar datos limpios.
        """
        layout = QVBoxLayout(self.tab_registrar)
        formulario = QFormLayout()
        
        # 1. Datos de Identificación
        self.input_vin = QLineEdit()
        self.input_vin.setPlaceholderText("VIN del vehículo infractor")
        
        self.combo_agentes = QComboBox()
        self.combo_agentes.addItem("Seleccione al agente que levantó la multa...", None)
        
        # Llamamos al backend para llenar el menú
        exito, lista_agentes = GestorAgentes.obtener_agentes_para_combo()
        if exito:
            for id_agente, placa, nombre in lista_agentes:
                # El usuario lee "AG-101 - Ricardo", pero el sistema guarda el ID (1)
                self.combo_agentes.addItem(f"{placa} - {nombre}", id_agente)
                
        formulario.addRow("Agente de Tránsito:", self.combo_agentes)
        # 2. Datos de Tiempo (QDateEdit y QTimeEdit)
        # Estos widgets muestran un calendario y un reloj respectivamente.
        # Evitan que el usuario escriba formatos erróneos como "12-enero-2026".
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True) # Muestra un calendario al hacer clic
        self.input_fecha.setDate(QDate.currentDate()) # Selecciona hoy por defecto
        
        self.input_hora = QTimeEdit()
        self.input_hora.setTime(QTime.currentTime()) # Selecciona la hora actual por defecto

        # 3. Datos del Hecho
        self.input_lugar = QLineEdit()
        self.input_motivo = QLineEdit()
        self.input_motivo.setPlaceholderText("Artículos violados o descripción")

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(cat.TIPOS_INFRACCION)

        # 4. Datos Económicos (QDoubleSpinBox)
        # Restringe la entrada exclusivamente a números con decimales.
        self.input_monto = QDoubleSpinBox()
        self.input_monto.setRange(1.0, 999999.99) # Rango permitido
        self.input_monto.setPrefix("$ ") # Pone el símbolo de moneda visualmente
        self.input_monto.setDecimals(2)

        # 5. Datos de Captura y Conductor
        self.combo_captura = QComboBox()
        self.combo_captura.addItems(cat.TIPOS_CAPTURA_INFRACCION)
        
        self.input_licencia = QLineEdit()
        self.input_licencia.setPlaceholderText("Opcional (Obligatorio en sitio)")

        # Agregamos todas las filas al formulario alineado
        formulario.addRow("VIN Infractor:", self.input_vin)
        formulario.addRow("Agente de Tránsito:", self.combo_agentes)
        formulario.addRow("Fecha del hecho:", self.input_fecha)
        formulario.addRow("Hora del hecho:", self.input_hora)
        formulario.addRow("Lugar:", self.input_lugar)
        formulario.addRow("Tipo de Infracción:", self.combo_tipo)
        formulario.addRow("Motivo:", self.input_motivo)
        formulario.addRow("Monto de la multa:", self.input_monto)
        formulario.addRow("Método de Captura:", self.combo_captura)
        formulario.addRow("Licencia Conductor:", self.input_licencia)

        layout.addLayout(formulario)

        # Botón para procesar el registro
        self.btn_registrar = QPushButton("Emitir Infracción")
        self.btn_registrar.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold; padding: 10px;")
        #Conexion con backend
        self.btn_registrar.clicked.connect(self.procesar_registro)
        
        layout.addWidget(self.btn_registrar, alignment=Qt.AlignRight)

    # ==========================================
    # PESTAÑA 2: GESTIONAR ESTADO (COBROS)
    # ==========================================
    def construir_tab_gestionar(self):
        """
        Construye la interfaz para buscar una infracción por su folio único
        y cambiar su estado administrativo (ej. de Pendiente a Pagada).
        """
        layout = QVBoxLayout(self.tab_gestionar)
        
        # 1. Zona superior: Búsqueda
        layout_busqueda = QHBoxLayout()
        self.input_buscar_folio = QLineEdit()
        self.input_buscar_folio.setPlaceholderText("Ej: INF-20260223-A1B2C3")
        btn_buscar = QPushButton("Buscar Folio")
        
        layout_busqueda.addWidget(QLabel("Folio de la Multa:"))
        layout_busqueda.addWidget(self.input_buscar_folio)
        layout_busqueda.addWidget(btn_buscar)
        
        layout.addLayout(layout_busqueda)

        # 2. Zona central: Formulario de actualización
        formulario = QFormLayout()
        
        # Desplegable para seleccionar el nuevo estado.
        # Se omitió "Pendiente" porque las reglas prohíben regresar una multa a ese estado.
        self.combo_nuevo_estado = QComboBox()
        self.combo_nuevo_estado.addItems(["Pagada", "Cancelada"]) 

        formulario.addRow("Cambiar estado a:", self.combo_nuevo_estado)
        layout.addLayout(formulario)

        # 3. Zona inferior: Botón de acción
        self.btn_actualizar_estado = QPushButton("Aplicar Cambio de Estado")
        self.btn_actualizar_estado.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; padding: 10px;")
        #Conexion con backend
        self.btn_actualizar_estado.clicked.connect(self.procesar_cambio_estado)
        
        layout.addStretch() # Empuja el botón al fondo de la pestaña
        layout.addWidget(self.btn_actualizar_estado, alignment=Qt.AlignRight)
        
    # ==========================================
    # SEGURIDAD Y PERMISOS (RBAC)
    # ==========================================
    def aplicar_permisos(self):
        """Bloquea elementos visuales según el rol del usuario."""
        rol = self.usuario_actual.rol
        
        if rol == cat.ROLES_USUARIO[3]: # Supervisor
            # El supervisor solo audita, no puede cobrar ni cancelar 
            self.btn_actualizar_estado.setVisible(False)
            self.combo_nuevo_estado.setEnabled(False)
            
    # ==========================================
    # LÓGICA DE INTERFAZ Y BACKEND
    # ==========================================
    def procesar_registro(self):
        """Extrae los datos, los empaqueta y los envía al Gestor para guardar en SQLite."""
        vin = self.input_vin.text().strip().upper()
        lugar = self.input_lugar.text().strip().upper()
        motivo = self.input_motivo.text().strip().upper()
        tipo_infraccion = self.combo_tipo.currentText()
        tipo_captura = self.combo_captura.currentText()
        monto = self.input_monto.value()
        licencia = self.input_licencia.text().strip().upper()

        # Extraemos la fecha y hora de los widgets especiales en el formato que pide el validador
        fecha = self.input_fecha.date().toString("yyyy-MM-dd")
        hora = self.input_hora.time().toString("HH:mm")

        # === CAMBIO CLAVE: Extraemos el ID numérico oculto del agente ===
        id_agente = self.combo_agentes.currentData()

        # 1. Validación preventiva en frontend (campos de texto)
        if not vin or not lugar or not motivo:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor llene todos los campos obligatorios.")
            return
            
        # 2. Validación para asegurar que seleccionaron un agente válido
        if not id_agente:
            QMessageBox.warning(self, "Agente no seleccionado", "Por favor, seleccione al Agente de Tránsito que levantó la boleta.")
            return

        # (Ya no necesitamos el try/except de ValueError porque currentData() ya nos da el número limpio)

        # 3. Empaquetamos en el Modelo
        nueva_infraccion = Infraccion(
            vin_infractor=vin, id_agente=id_agente, fecha=fecha, hora=hora,
            lugar=lugar, tipo_infraccion=tipo_infraccion, motivo=motivo,
            monto=monto, licencia_conductor=licencia
        )

        # 4. Enviamos al Gestor
        exito, msj = GestorInfracciones.registrar_infraccion(nueva_infraccion, tipo_captura)

        # 5. Retroalimentación visual
        if exito:
            QMessageBox.information(self, "Éxito", msj)
            self.limpiar_formulario_registro()
            # Opcional: regresar el combo de agentes a su estado original (índice 0)
            self.combo_agentes.setCurrentIndex(0) 
        else:
            QMessageBox.critical(self, "Error al Registrar", msj)

    def procesar_cambio_estado(self):
        """Envía la orden de cobro o cancelación al Gestor."""
        folio = self.input_buscar_folio.text().strip().upper()
        nuevo_estado = self.combo_nuevo_estado.currentText()
        
        if not folio:
            QMessageBox.warning(self, "Falta Folio", "Por favor ingrese el folio de la infracción.")
            return
            
        exito, msj = GestorInfracciones.cambiar_estado_infraccion(folio, nuevo_estado)
        
        if exito:
            QMessageBox.information(self, "Actualización Exitosa", msj)
            self.input_buscar_folio.clear()
        else:
            QMessageBox.critical(self, "Error", msj)
            
    def limpiar_formulario_registro(self):
        """Limpia el formulario después de un registro exitoso."""
        self.input_vin.clear()
        self.input_id_agente.clear()
        self.input_lugar.clear()
        self.input_motivo.clear()
        self.input_licencia.clear()
        
        self.input_monto.setValue(1.0)
        self.combo_tipo.setCurrentIndex(0)
        self.combo_captura.setCurrentIndex(0)