from turtle import right
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QPropertyAnimation, QRect, Qt
import sys


#Class for box animation
class Box(QWidget):
    def __init__(self, colors):
        super().__init__()
     
        

# Button Widget Class
class ButtonWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buttons with Click Events")
        button_layout = QVBoxLayout()

        # Main layout (Horizontal: Buttons on the left, animation on the right)
        #main_layout = QHBoxLayout()

        # Left side: Vertical layout for buttons
        #button_layout = QVBoxLayout()

        self.button1 = QPushButton("Start Program")
        self.button2 = QPushButton("Stop After Cycle")
        self.button3 = QPushButton("Close App")
        self.button4 = QPushButton("Start Test Cycle")

        # Set colors of the buttons
        self.button1.setStyleSheet("background-color: green")
        self.button2.setStyleSheet("background-color: red")
        self.button3.setStyleSheet("background-color: orange")
        self.button4.setStyleSheet("background-color: blue")

        # Set the size of the buttons
        self.button1.setFixedHeight(50)
        self.button2.setFixedHeight(50)
        self.button3.setFixedHeight(50)
        self.button4.setFixedHeight(50)

        # Set the font size of the buttons
        self.button1.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.button2.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.button3.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.button4.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # Connect buttons to functions (slots)
        self.button1.clicked.connect(self.start)
        self.button2.clicked.connect(self.stop)
        self.button3.clicked.connect(self.close_app)
        self.button4.clicked.connect(self.start_test_cycle)

        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button4)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button3)
        button_layout.addStretch()


       

        self.setLayout(button_layout)

    def start(self):
        print("Start Program")

    def stop(self):
        print("Stop After Cycle")

    def close_app(self):
        self.close()  # Close the window

    def start_test_cycle(self):
        print("Test cycle started")

# Main Window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        

# Run the application
app = QApplication(sys.argv)
window = ButtonWidget()
window.setMinimumSize(500, 500)
window.show()
app.exec()
