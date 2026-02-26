from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QTabWidget, 
QFormLayout, QTableWidget, QTableWidgetItem, 
QHeaderView, QMessageBox)
from PySide6.QtCore import Qt
import logic.catalogos as cat

# Importamos el backend
from logic.auth import Auth
from models.usuario import Usuario
from logic.gestor_usuarios import GestorUsuarios

class PanelUsuarios(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.configurar_ui()
        self.aplicar_permisos()
        self.cargar_lista_usuarios() # Llenar la tabla al abrir

    def configurar_ui(self):
        layout_principal = QVBoxLayout(self)

        lbl_titulo = QLabel("Gestión de Usuarios y Accesos")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(lbl_titulo)

        self.pestanas = QTabWidget()
        self.tab_registrar = QWidget()
        self.tab_gestionar = QWidget()
        
        self.pestanas.addTab(self.tab_registrar, "Nuevo Usuario")
        self.pestanas.addTab(self.tab_gestionar, "Control de Accesos")
        
        layout_principal.addWidget(self.pestanas)

        self.construir_tab_registrar()
        self.construir_tab_gestionar()

    def construir_tab_registrar(self):
        layout = QVBoxLayout(self.tab_registrar)
        formulario = QFormLayout()

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: operador_juan")
        
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Mínimo 6 caracteres")
        self.input_password.setEchoMode(QLineEdit.Password) # Oculta los caracteres

        self.combo_rol = QComboBox()
        self.combo_rol.addItems(cat.ROLES_USUARIO)

        formulario.addRow("Nombre de Usuario:", self.input_nombre)
        formulario.addRow("Contraseña:", self.input_password)
        formulario.addRow("Rol en el sistema:", self.combo_rol)

        layout.addLayout(formulario)

        self.btn_registrar = QPushButton("Crear Cuenta")
        self.btn_registrar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px;")
        self.btn_registrar.clicked.connect(self.procesar_registro)
        layout.addWidget(self.btn_registrar, alignment=Qt.AlignRight)

    def construir_tab_gestionar(self):
        layout = QVBoxLayout(self.tab_gestionar)

        # Tabla de usuarios
        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(4)
        self.tabla_usuarios.setHorizontalHeaderLabels(["ID", "Usuario", "Rol", "Estado"])
        self.tabla_usuarios.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_usuarios.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_usuarios.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Estilo oscuro para consistencia
        self.tabla_usuarios.setStyleSheet("""
            QTableWidget { background-color: #2b2b2b; alternate-background-color: #353535; color: #ffffff; }
            QHeaderView::section { background-color: #1e1e1e; color: #ffffff; font-weight: bold; }
        """)
        self.tabla_usuarios.itemSelectionChanged.connect(self.seleccionar_usuario_tabla)
        layout.addWidget(self.tabla_usuarios)

        # Controles de edición
        layout_edicion = QHBoxLayout()
        
        self.lbl_id_edit = QLabel("ID seleccionado: -")
        layout_edicion.addWidget(self.lbl_id_edit)

        layout_edicion.addWidget(QLabel("Nuevo Rol:"))
        self.combo_edit_rol = QComboBox()
        self.combo_edit_rol.addItems(cat.ROLES_USUARIO)
        layout_edicion.addWidget(self.combo_edit_rol)

        layout_edicion.addWidget(QLabel("Estado:"))
        self.combo_edit_estado = QComboBox()
        self.combo_edit_estado.addItems(["Activo", "Inactivo"])
        layout_edicion.addWidget(self.combo_edit_estado)

        self.btn_actualizar = QPushButton("Aplicar Cambios")
        self.btn_actualizar.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; padding: 8px;")
        self.btn_actualizar.clicked.connect(self.procesar_actualizacion)
        self.btn_actualizar.setEnabled(False) # Se activa al seleccionar a alguien
        layout_edicion.addWidget(self.btn_actualizar)

        layout.addLayout(layout_edicion)

    def aplicar_permisos(self):
        """Si por algún motivo alguien que no es Admin llega aquí, bloqueamos todo."""
        if self.usuario_actual.rol != "Administrador":
            self.pestanas.setEnabled(False)
            

    # ==========================================
    # LÓGICA DE INTERFAZ Y BACKEND
    # ==========================================
    def procesar_registro(self):
        nombre = self.input_nombre.text().strip()
        password = self.input_password.text().strip()
        rol = self.combo_rol.currentText()

        nuevo_usuario = Usuario(nombre_usuario=nombre, password=password, rol=rol)
        exito, msj = Auth.registrar_usuario(nuevo_usuario)

        if exito:
            QMessageBox.information(self, "Éxito", msj)
            self.input_nombre.clear()
            self.input_password.clear()
            self.cargar_lista_usuarios() # Refresca la tabla automáticamente
        else:
            QMessageBox.critical(self, "Error", msj)

    def cargar_lista_usuarios(self):
        self.tabla_usuarios.setRowCount(0)
        exito, datos = GestorUsuarios.obtener_todos_los_usuarios()
        
        if exito and datos:
            self.tabla_usuarios.setRowCount(len(datos))
            for fila_idx, usuario in enumerate(datos):
                for col_idx, valor in enumerate(usuario):
                    item = QTableWidgetItem(str(valor))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tabla_usuarios.setItem(fila_idx, col_idx, item)

    def seleccionar_usuario_tabla(self):
        filas_seleccionadas = self.tabla_usuarios.selectedItems()
        if filas_seleccionadas:
            fila = filas_seleccionadas[0].row()
            id_usuario = self.tabla_usuarios.item(fila, 0).text()
            rol_actual = self.tabla_usuarios.item(fila, 2).text()
            estado_actual = self.tabla_usuarios.item(fila, 3).text()

            self.lbl_id_edit.setText(f"ID seleccionado: {id_usuario}")
            self.combo_edit_rol.setCurrentText(rol_actual)
            self.combo_edit_estado.setCurrentText(estado_actual)
            self.btn_actualizar.setEnabled(True)

    def procesar_actualizacion(self):
        texto_id = self.lbl_id_edit.text().replace("ID seleccionado: ", "")
        if texto_id == "-":
            return

        id_usuario = int(texto_id)
        nuevo_rol = self.combo_edit_rol.currentText()
        nuevo_estado = self.combo_edit_estado.currentText()

        exito, msj = GestorUsuarios.actualizar_usuario(id_usuario, nuevo_rol, nuevo_estado)

        if exito:
            QMessageBox.information(self, "Actualizado", msj)
            self.cargar_lista_usuarios()
            self.btn_actualizar.setEnabled(False)
            self.lbl_id_edit.setText("ID seleccionado: -")
        else:
            QMessageBox.critical(self, "Error", msj)