from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from logic.auth import Auth

# Importamos la ventana principal para poder abrirla después del login
from views.principal import VentanaPrincipal

class VentanaLogin(QWidget):
    def __init__(self): # <--- NOTA: Aquí está vacío, no pide usuario. Esto arregla tu error.
        super().__init__()
        self.setWindowTitle("Sistema de Registro Vehicular - Login")
        self.resize(350, 450)
        
        self.configurar_ui()

    def configurar_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        titulo = QLabel("Iniciar Sesión")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")
        titulo.setAlignment(Qt.AlignCenter)

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Nombre de usuario")
        self.input_usuario.setMinimumHeight(35)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")
        self.input_password.setEchoMode(QLineEdit.Password) 
        self.input_password.setMinimumHeight(35)

        btn_ingresar = QPushButton("Ingresar")
        btn_ingresar.setMinimumHeight(40)
        btn_ingresar.setStyleSheet("background-color: #0055ff; color: white; font-weight: bold;")
        btn_ingresar.clicked.connect(self.verificar_credenciales)

        self.label_error = QLabel("")
        self.label_error.setStyleSheet("color: red; font-size: 12px;")
        self.label_error.setAlignment(Qt.AlignCenter)
        self.label_error.hide()

        layout.addWidget(titulo)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_error)
        layout.addWidget(btn_ingresar)

        self.setLayout(layout)

    def verificar_credenciales(self):
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text().strip()

        self.label_error.hide()

        # Llamada a la capa lógica para conectar con SQLite
        es_valido, usuario_obj, msj = Auth.autenticar_usuario(usuario, password)

        if es_valido:
            self.abrir_pantalla_principal(usuario_obj)
        else:
            self.label_error.setText(msj)
            self.label_error.show()

    def abrir_pantalla_principal(self, usuario_obj):
        """
        Cierra el login y levanta el menú principal inyectando el usuario.
        """
        # Aquí le pasamos el objeto a la VentanaPrincipal
        self.ventana_principal = VentanaPrincipal(usuario_obj)
        self.ventana_principal.show()
        
        # Cerramos la ventanita de login
        self.close()