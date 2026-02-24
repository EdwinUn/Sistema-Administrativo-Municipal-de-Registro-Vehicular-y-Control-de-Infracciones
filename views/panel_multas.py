from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QTabWidget, 
QFormLayout, QDoubleSpinBox, QDateEdit, QTimeEdit)
from PySide6.QtCore import Qt, QDate, QTime
import logic.catalogos as cat


class PanelMultas(QWidget):
    def __init__(self):
        super().__init__()
        self.configurar_ui()

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
        
        # Añadimos los lienzos al contenedor con sus respectivos títulos
        self.pestanas.addTab(self.tab_registrar, "Registrar Infracción")
        self.pestanas.addTab(self.tab_gestionar, "Cobro y Cancelación")
        
        layout_principal.addWidget(self.pestanas)

        # Llamamos a los métodos que construyen el interior de cada pestaña
        self.construir_tab_registrar()
        self.construir_tab_gestionar()

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
        
        self.input_id_agente = QLineEdit()
        self.input_id_agente.setPlaceholderText("ID interno del Agente")

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
        formulario.addRow("ID Agente Emisor:", self.input_id_agente)
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
        
        layout.addStretch() # Empuja el botón al fondo de la pestaña
        layout.addWidget(self.btn_actualizar_estado, alignment=Qt.AlignRight)