from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QTabWidget, 
QFormLayout, QDoubleSpinBox, QDateEdit, QTimeEdit, QMessageBox)
from PySide6.QtCore import Qt, QDate, QTime
import logic.catalogos as cat

#Importaciones backend
from models.infraccion import Infraccion
from logic.gestor_infracciones import GestorInfracciones
from logic.gestor_agentes import GestorAgentes
from logic.gestor_vehiculos import GestorVehiculos

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
        
        lbl_titulo = QLabel("Módulo de Infracciones de Tránsito")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(lbl_titulo)

        self.pestanas = QTabWidget()
        
        self.tab_registrar = QWidget()
        self.tab_gestionar = QWidget()
        
        self.construir_tab_registrar()
        self.construir_tab_gestionar()

        # --- APLICACIÓN DE ROLES (RBAC) ---
        rol = self.usuario_actual.rol
        
        if rol == cat.ROLES_USUARIO[0]: # Administrador
            self.pestanas.addTab(self.tab_registrar, "Registrar Infracción")
            self.pestanas.addTab(self.tab_gestionar, "Cobro y Cancelación")
            
        elif rol == cat.ROLES_USUARIO[2]: # Agente de Tránsito
            self.pestanas.addTab(self.tab_registrar, "Registrar Infracción")
            
        elif rol == cat.ROLES_USUARIO[3]: # Supervisor
            self.pestanas.addTab(self.tab_gestionar, "Consultar Infracción")

        layout_principal.addWidget(self.pestanas)

    # ==========================================
    # PESTAÑA 1: REGISTRAR INFRACCIÓN
    # ==========================================
    def construir_tab_registrar(self):
        layout = QVBoxLayout(self.tab_registrar)
        formulario = QFormLayout()
        
        self.input_vin = QLineEdit()
        self.input_vin.setPlaceholderText("Ingrese VIN o Placa del infractor")
        
        self.combo_agentes = QComboBox()
        self.combo_agentes.addItem("Seleccione al agente que levantó la multa...", None)
        
        exito, lista_agentes = GestorAgentes.obtener_agentes_para_combo()
        if exito:
            for id_agente, placa, nombre in lista_agentes:
                self.combo_agentes.addItem(f"{placa} - {nombre}", id_agente)
                
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDate(QDate.currentDate())
        
        self.input_hora = QTimeEdit()
        self.input_hora.setTime(QTime.currentTime())

        self.input_lugar = QLineEdit()
        
        self.input_motivo = QLineEdit()
        self.input_motivo.setReadOnly(True) # Evita que el usuario lo modifique
        self.input_motivo.setStyleSheet("background-color: #2c3e50; color: #bdc3c7; font-weight: bold;") # Estilo "Bloqueado" visualmente
        
        # === CAMBIO: COMBOBOX INTELIGENTE CON EL TABULADOR ===
        self.combo_tipo = QComboBox()
        for clave, datos in cat.TABULADOR_INFRACCIONES.items():
            self.combo_tipo.addItem(datos["descripcion"], clave)

        # === NUEVO: ETIQUETA DE RANGO ===
        self.lbl_rango_monto = QLabel("Rango permitido: $0.00 - $0.00")
        self.lbl_rango_monto.setStyleSheet("color: #e67e22; font-style: italic; font-weight: bold;")

        self.input_monto = QDoubleSpinBox()
        self.input_monto.setRange(1.0, 999999.99)
        self.input_monto.setPrefix("$ ")
        self.input_monto.setDecimals(2)

        self.combo_captura = QComboBox()
        self.combo_captura.addItems(cat.TIPOS_CAPTURA_INFRACCION)
        
        self.input_licencia = QLineEdit()
        self.input_licencia.setPlaceholderText("Opcional (Obligatorio en sitio)")

        # Agregamos todo al formulario
        formulario.addRow("VIN Infractor:", self.input_vin)
        formulario.addRow("Agente de Tránsito:", self.combo_agentes)
        formulario.addRow("Fecha del hecho:", self.input_fecha)
        formulario.addRow("Hora del hecho:", self.input_hora)
        formulario.addRow("Lugar:", self.input_lugar)
        formulario.addRow("Tipo de Infracción:", self.combo_tipo)
        formulario.addRow("", self.lbl_rango_monto) # La etiqueta va debajo del tipo de infracción
        formulario.addRow("Motivo:", self.input_motivo)
        formulario.addRow("Monto de la multa:", self.input_monto)
        formulario.addRow("Método de Captura:", self.combo_captura)
        formulario.addRow("Licencia Conductor:", self.input_licencia)

        layout.addLayout(formulario)

        self.btn_registrar = QPushButton("Emitir Infracción")
        self.btn_registrar.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold; padding: 10px;")
        self.btn_registrar.clicked.connect(self.procesar_registro)
        
        layout.addWidget(self.btn_registrar, alignment=Qt.AlignRight)

        # === CONECTAMOS EL EVENTO Y FORZAMOS LA CARGA INICIAL ===
        self.combo_tipo.currentIndexChanged.connect(self.actualizar_info_multa)
        self.actualizar_info_multa() # Llenar los datos de la primera opción al abrir

    # ==========================================
    # LÓGICA DINÁMICA DE LA INTERFAZ
    # ==========================================
    def actualizar_info_multa(self):
        """Autocompleta el motivo y muestra el rango de precios basado en el tabulador oficial."""
        clave_seleccionada = self.combo_tipo.currentData()
        
        if clave_seleccionada in cat.TABULADOR_INFRACCIONES:
            datos = cat.TABULADOR_INFRACCIONES[clave_seleccionada]
            
            # 1. Actualizar etiqueta de rango
            minimo = datos["multa"]["min"]
            maximo = datos["multa"]["max"]
            self.lbl_rango_monto.setText(f"Rango permitido: ${minimo:,.2f} - ${maximo:,.2f} MXN")
            
            # 2. Autocompletar motivo legal
            motivo_legal = f"{datos['articulo']} - {datos['descripcion']}"
            self.input_motivo.setText(motivo_legal)
            
            # 3. Poner el valor mínimo por defecto
            self.input_monto.setValue(minimo)

    # ==========================================
    # PESTAÑA 2: GESTIONAR ESTADO (COBROS)
    # ==========================================
    def construir_tab_gestionar(self):
        layout = QVBoxLayout(self.tab_gestionar)
        
        layout_busqueda = QHBoxLayout()
        self.input_buscar_folio = QLineEdit()
        self.input_buscar_folio.setPlaceholderText("Ej: INF-20260223-A1B2C3")
        btn_buscar = QPushButton("Buscar Folio")
        
        layout_busqueda.addWidget(QLabel("Folio de la Multa:"))
        layout_busqueda.addWidget(self.input_buscar_folio)
        layout_busqueda.addWidget(btn_buscar)
        
        layout.addLayout(layout_busqueda)

        formulario = QFormLayout()
        self.combo_nuevo_estado = QComboBox()
        self.combo_nuevo_estado.addItems(["Pagada", "Cancelada"]) 

        formulario.addRow("Cambiar estado a:", self.combo_nuevo_estado)
        layout.addLayout(formulario)

        self.btn_actualizar_estado = QPushButton("Aplicar Cambio de Estado")
        self.btn_actualizar_estado.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; padding: 10px;")
        self.btn_actualizar_estado.clicked.connect(self.procesar_cambio_estado)
        
        layout.addStretch() 
        layout.addWidget(self.btn_actualizar_estado, alignment=Qt.AlignRight)
        
    def aplicar_permisos(self):
        rol = self.usuario_actual.rol
        if rol == cat.ROLES_USUARIO[3]: 
            self.btn_actualizar_estado.setVisible(False)
            self.combo_nuevo_estado.setEnabled(False)
            
    # ==========================================
    # LÓGICA DE INTERFAZ Y BACKEND
    # ==========================================
    def procesar_registro(self):
        # 1. Obtenemos lo que haya escrito (puede ser VIN o Placa)
        criterio_vehiculo = self.input_vin.text().strip().upper()
        
        lugar = self.input_lugar.text().strip().upper()
        motivo = self.input_motivo.text().strip().upper()
        
        tipo_texto = self.combo_tipo.currentText() 
        clave_infraccion = self.combo_tipo.currentData() 
        
        tipo_captura = self.combo_captura.currentText()
        monto = self.input_monto.value()
        licencia = self.input_licencia.text().strip().upper()

        fecha = self.input_fecha.date().toString("yyyy-MM-dd")
        hora = self.input_hora.time().toString("HH:mm")
        id_agente = self.combo_agentes.currentData()

        # 2. Validación preventiva
        if not criterio_vehiculo or not lugar or not motivo:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor llene todos los campos obligatorios.")
            return

        # (Ya NO validamos len == 17 aquí porque la placa es más corta)
            
        if len(lugar) < 5: # El motivo ya no lo validamos así porque el sistema lo pone automáticamente
            QMessageBox.warning(self, "Detalles Insuficientes", "El 'Lugar' debe ser más descriptivo (mínimo 5 caracteres).")
            return
            
        if not id_agente:
            QMessageBox.warning(self, "Agente no seleccionado", "Por favor, seleccione al Agente de Tránsito que levantó la boleta.")
            return

        # ==========================================
        # 🚨 LA MAGIA: TRADUCIR PLACA A VIN 🚨
        # ==========================================
        exito_vehiculo, datos_vehiculo = GestorVehiculos.buscar_vehiculo_universal(criterio_vehiculo)
        
        if not exito_vehiculo:
            QMessageBox.warning(self, "Vehículo No Encontrado", "No existe ningún vehículo registrado con esa Placa o VIN.")
            return
            
        # Extraemos el VIN real de 17 caracteres que nos devolvió el buscador
        vin_real = datos_vehiculo["vin"] 
        # ==========================================

        # 🚨 CANDADO JURÍDICO 🚨
        if clave_infraccion in cat.TABULADOR_INFRACCIONES:
            datos_oficiales = cat.TABULADOR_INFRACCIONES[clave_infraccion]
            min_permitido = datos_oficiales["multa"]["min"]
            max_permitido = datos_oficiales["multa"]["max"]
            
            if monto < min_permitido or monto > max_permitido:
                QMessageBox.critical(self, "Monto Ilegal", 
                    f"El monto de ${monto:,.2f} está fuera de la ley.\n"
                    f"Para esta infracción el reglamento exige cobrar entre ${min_permitido:,.2f} y ${max_permitido:,.2f}."
                )
                return

        # 3. Empaquetamos en el Modelo usando el VIN_REAL
        nueva_infraccion = Infraccion(
            vin_infractor=vin_real, id_agente=id_agente, fecha=fecha, hora=hora,
            lugar=lugar, tipo_infraccion=tipo_texto, motivo=motivo,
            monto=monto, licencia_conductor=licencia
        )

        # 4. Enviamos al Gestor
        exito, msj = GestorInfracciones.registrar_infraccion(nueva_infraccion, tipo_captura)

        if exito:
            QMessageBox.information(self, "Éxito", msj)
            self.limpiar_formulario_registro()
        else:
            QMessageBox.critical(self, "Error al Registrar", msj)

    def procesar_cambio_estado(self):
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
        """Limpia el formulario y resetea los menús después de un registro exitoso."""
        self.input_vin.clear()
        self.input_lugar.clear()
        self.input_licencia.clear()
        
        self.combo_tipo.setCurrentIndex(0)
        self.combo_captura.setCurrentIndex(0)
        self.combo_agentes.setCurrentIndex(0)