from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QPushButton, QFileDialog, QColorDialog, QLabel
from PyQt5.QtCore import Qt
import moderngl
from mandelbrot import MandelbrotRenderer
import settings


class MandelbrotWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zoom = settings.ZOOM
        self.center = [settings.X_CENTER, settings.Y_CENTER]
        self.max_iter = settings.MAX_ITER
        self.color1 = (1.0, 0.0, 1.0)  # Default color (purple)
        self.color2 = (0.0, 1.0, 1.0)  # Default color (cyan)
        self.color3 = (1.0, 0.0, 0.0)  # Default color (red)
        self.color4 = (0.0, 1.0, 0.0)  # Default color (green)
        self.color5 = (1.0, 1.0, 0.0)  # Default color (yellow)
        self.last_mouse_pos = None

    def initializeGL(self):
        self.ctx = moderngl.create_context()
        self.renderer = MandelbrotRenderer(self.ctx, self.width(), self.height())

    def paintGL(self):
        self.renderer.render(self.zoom, self.center, self.max_iter, self.color1, self.color2, self.color3, self.color4, self.color5)
        self.ctx.finish()

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.zoom *= 0.9 if delta > 0 else 1.1
        self.update()

    def mousePressEvent(self, event):
        self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_mouse_pos:
            dx = (event.x() - self.last_mouse_pos.x()) / self.width() * self.zoom
            dy = (event.y() - self.last_mouse_pos.y()) / self.height() * self.zoom
            self.center[0] -= dx
            self.center[1] += dy
            self.last_mouse_pos = event.pos()
            self.update()


class MandelbrotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fractal de Mandelbrot Interactivo")
        self.setGeometry(100, 100, settings.WIDTH, settings.HEIGHT)

        self.color1 = (1.0, 0.0, 1.0)  # Default color (purple)
        self.color2 = (0.0, 1.0, 1.0)  # Default color (cyan)
        self.color3 = (1.0, 0.0, 0.0)  # Default color (red)
        self.color4 = (0.0, 1.0, 0.0)  # Default color (green)
        self.color5 = (1.0, 1.0, 0.0)  # Default color (yellow)

        # Configura el modo oscuro
        self.set_dark_mode()

        self.widget = MandelbrotWidget(self)
        self.layout = QVBoxLayout()

        # Slider de iteraciones
        self.iter_slider = QSlider(Qt.Horizontal)
        self.iter_slider.setRange(50, 55000)
        self.iter_slider.setValue(settings.MAX_ITER)
        self.iter_slider.valueChanged.connect(self.update_iterations)

        # Etiqueta para mostrar el valor de las iteraciones
        self.iter_label = QLabel(f"Iteraciones: {settings.MAX_ITER}")
        
        # Layout horizontal para slider y etiqueta
        self.iter_layout = QHBoxLayout()
        self.iter_layout.addWidget(self.iter_label)
        self.iter_layout.addWidget(self.iter_slider)

        # Hacemos una fila horizontal para los botones de colores
        self.color_layout = QHBoxLayout()

        # Botones para los colores, con colores que cambian según la selección
        self.color_button1 = QPushButton("Color 1 (Iteración < 20%)")
        self.color_button1.clicked.connect(self.select_color1)
        self.color_button1.setStyleSheet(f"background-color: rgb({int(self.color1[0] * 255)}, {int(self.color1[1] * 255)}, {int(self.color1[2] * 255)})")

        self.color_button2 = QPushButton("Color 2 (Iteración < 40%)")
        self.color_button2.clicked.connect(self.select_color2)
        self.color_button2.setStyleSheet(f"background-color: rgb({int(self.color2[0] * 255)}, {int(self.color2[1] * 255)}, {int(self.color2[2] * 255)})")

        self.color_button3 = QPushButton("Color 3 (Iteración < 60%)")
        self.color_button3.clicked.connect(self.select_color3)
        self.color_button3.setStyleSheet(f"background-color: rgb({int(self.color3[0] * 255)}, {int(self.color3[1] * 255)}, {int(self.color3[2] * 255)})")

        self.color_button4 = QPushButton("Color 4 (Iteración < 80%)")
        self.color_button4.clicked.connect(self.select_color4)
        self.color_button4.setStyleSheet(f"background-color: rgb({int(self.color4[0] * 255)}, {int(self.color4[1] * 255)}, {int(self.color4[2] * 255)})")

        self.color_button5 = QPushButton("Color 5 (Iteración >= 80%)")
        self.color_button5.clicked.connect(self.select_color5)
        self.color_button5.setStyleSheet(f"background-color: rgb({int(self.color5[0] * 255)}, {int(self.color5[1] * 255)}, {int(self.color5[2] * 255)})")

        # Añadimos los botones a la fila
        self.color_layout.addWidget(self.color_button1)
        self.color_layout.addWidget(self.color_button2)
        self.color_layout.addWidget(self.color_button3)
        self.color_layout.addWidget(self.color_button4)
        self.color_layout.addWidget(self.color_button5)

        self.save_button = QPushButton("Guardar Imagen")
        self.save_button.clicked.connect(self.save_image)

        container = QWidget()
        self.layout.addWidget(self.widget)
        self.layout.addLayout(self.iter_layout)  # Añadimos el layout con el slider y la etiqueta
        self.layout.addLayout(self.color_layout)  # Añadimos la fila horizontal de botones
        self.layout.addWidget(self.save_button)
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def set_dark_mode(self):
        # Establece la paleta oscura
        dark_palette = self.palette()
        dark_palette.setColor(self.backgroundRole(), Qt.black)
        dark_palette.setColor(self.foregroundRole(), Qt.white)
        self.setPalette(dark_palette)

        # Estilos CSS para los botones y widgets
        self.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #333;
                border: 1px solid #555;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QLabel {
                color: white;
            }
            QSlider {
                background-color: #555;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999;
                background: #444;
                height: 8px;
            }
            QSlider::handle:horizontal {
                background: #888;
                border: 1px solid #555;
                width: 12px;
                height: 20px;
                margin: -5px 0;
            }
        """)

    def update_iterations(self, value):
        self.widget.max_iter = value
        self.iter_label.setText(f"Iteraciones: {value}")
        self.widget.update()

    def update_color(self, index):
        self.widget.color_scheme = list(settings.COLOR_SCHEMES.values())[index]
        self.widget.update()

    def select_color1(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color1 = (color.redF(), color.greenF(), color.blueF())
            self.color_button1.setStyleSheet(f"background-color: rgb({int(self.color1[0] * 255)}, {int(self.color1[1] * 255)}, {int(self.color1[2] * 255)})")
            self.widget.color1 = self.color1
            self.widget.update()

    def select_color2(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color2 = (color.redF(), color.greenF(), color.blueF())
            self.color_button2.setStyleSheet(f"background-color: rgb({int(self.color2[0] * 255)}, {int(self.color2[1] * 255)}, {int(self.color2[2] * 255)})")
            self.widget.color2 = self.color2
            self.widget.update()

    def select_color3(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color3 = (color.redF(), color.greenF(), color.blueF())
            self.color_button3.setStyleSheet(f"background-color: rgb({int(self.color3[0] * 255)}, {int(self.color3[1] * 255)}, {int(self.color3[2] * 255)})")
            self.widget.color3 = self.color3
            self.widget.update()

    def select_color4(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color4 = (color.redF(), color.greenF(), color.blueF())
            self.color_button4.setStyleSheet(f"background-color: rgb({int(self.color4[0] * 255)}, {int(self.color4[1] * 255)}, {int(self.color4[2] * 255)})")
            self.widget.color4 = self.color4
            self.widget.update()

    def select_color5(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color5 = (color.redF(), color.greenF(), color.blueF())
            self.color_button5.setStyleSheet(f"background-color: rgb({int(self.color5[0] * 255)}, {int(self.color5[1] * 255)}, {int(self.color5[2] * 255)})")
            self.widget.color5 = self.color5
            self.widget.update()

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Imagen", "", "PNG (*.png)")
        if file_path:
            self.widget.grabFramebuffer().save(file_path)



