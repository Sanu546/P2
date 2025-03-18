from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QSplitter, QStackedWidget, QSlider
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import sys

"""
The first 3 classes is what will be displayed on the GUI.
the classes TestMenue and AutoMenue is for the interactive buttons, that we will be using to control the robot cell.
The last 2 classes if for the layout of the GUI. 
The MenueStacker class is for the buttons that will switch between the TestMenue and AutoMenue. 
the CellDisplay class shows the detected battery cells.  
"""

#Class for detected battery cell visualization
class CellDisplay(QWidget):
    def __init__(self,):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the layout
        self.grid_layout = QGridLayout()
        self.input_layout = QVBoxLayout()

        # Create a 2x4 grid of boxes (buttons)
        self.boxes = []
        for row in range(4):
            for col in range(2):
                box = QPushButton('', self)
                box.setFixedSize(50, 50)  # Set a fixed size for the boxes
                self.grid_layout.addWidget(box, row, col)
                self.boxes.append(box)

        # Input field for the array
        self.input_label = QLabel('Enter 8 colors (comma-separated):')
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText('e.g., red,green,blue,...')
        self.update_button = QPushButton('Update Visualisation')
        self.update_button.clicked.connect(self.update_colors)

        # Add widgets to the input layout
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.input_field)
        self.input_layout.addWidget(self.update_button)

        # Combine the grid and input layouts
        layout = QVBoxLayout()
        layout.addLayout(self.grid_layout)
        layout.addLayout(self.input_layout)

        # Set the main layout
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('2x8 Color Grid')
        self.setGeometry(300, 300, 500, 200)

    def update_colors(self):
        """Update the colors of the boxes based on the input array."""
        input_text = self.input_field.text().strip()
        if not input_text:
            return

        # Split the input into a list of colors
        colors = input_text.split(',')
        if len(colors) != 8:
            self.input_field.setPlaceholderText('Please enter exactly 8 colors.')
            return

        # Update the colors of the boxes
        for i, box in enumerate(self.boxes):
            color = colors[i].strip()
            box.setStyleSheet(f'background-color: {color};')
        
class TestMenue(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create label
        self.label = QLabel("Test Menue")
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # Create buttons
        self.button69 = QPushButton("Next Procces Step")
        self.buttonBack = QPushButton("Back")
        self.buttonReset = QPushButton("Reset")
    
        # Set color of the buttons
        self.button69.setStyleSheet("background-color: green")
        self.buttonBack.setStyleSheet("background-color: red")
        self.buttonReset.setStyleSheet("background-color: orange")

        # Set the size of the buttons
        self.button69.setFixedHeight(50)
        self.buttonBack.setFixedHeight(50)
        self.buttonReset.setFixedHeight(50)


        # Set the font size of the buttons
        self.button69.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.buttonBack.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.buttonReset.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # Connect buttons to functions (slots)
        self.button69.clicked.connect(self.NextProccesStep)
        self.buttonBack.clicked.connect(self.Back)
        self.buttonReset.clicked.connect(self.Reset)

        # Add buttons to the layout
        layout.addWidget(self.label)
        layout.addWidget(self.button69)
        layout.addWidget(self.buttonBack)
        layout.addWidget(self.buttonReset)
        layout.addStretch()

        self.setLayout(layout)

    def NextProccesStep(self):
        print("Next Procces Step")
    
    def Back(self):
        print("Back")

    def Reset(self):
        print("Reset")

class AutoMenue(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        # Create buttons
        self.buttonStart = QPushButton("Auto Start")
        self.buttonStop = QPushButton("Auto Stop")
        self.buttonReset = QPushButton("Reset")

        # Set colors of the buttons
        self.buttonStart.setStyleSheet("background-color: green")
        self.buttonStop.setStyleSheet("background-color: red")
        self.buttonReset.setStyleSheet("background-color: orange")

        # Set the size of the buttons
        self.buttonStart.setFixedHeight(50)
        self.buttonStop.setFixedHeight(50)
        self.buttonReset.setFixedHeight(50)

        # Set the font size of the buttons
        self.buttonStart.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.buttonStop.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.buttonReset.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # Connect buttons to functions (slots)
        self.buttonStart.clicked.connect(self.start)
        self.buttonStop.clicked.connect(self.stop)
        self.buttonReset.clicked.connect(self.reset)

        # Add buttons to the layout
        layout.addWidget(self.buttonStart)
        layout.addWidget(self.buttonStop)
        layout.addWidget(self.buttonReset)
        layout.addStretch()

        self.setLayout(layout)

    def start(self):
        print("Start")

    def stop(self):
        print("Stop")

    def reset(self):
        print("Reset")

class CalibratingMenue(QWidget):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.initUI()
    
    def initUI(self):
        
        # Create sliders
        self.x_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.x_slider.setRange(-500, 500)
        self.x_slider.setValue(self.x)
        self.x_slider.valueChanged.connect(self.update_x)

        self.y_slider = QSlider(Qt.Orientation.Vertical, self)
        self.y_slider.setRange(-500, 500)
        self.y_slider.setValue(self.y)
        self.y_slider.valueChanged.connect(self.update_y)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("y Direction"))
        layout.addWidget(self.y_slider)
        layout.addWidget(QLabel("x Direction"))
        layout.addWidget(self.x_slider)
        self.setLayout(layout)
    
    def update_x(self, value):
        self.x = value
        print(f"x: {self.x}")

    def update_y(self, value):
        self.y = value
        print(f"y: {self.y}")


#This class lets us switch between the TestMenue and AutoMenue classes
class MenueStacker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create layout
        layout = QVBoxLayout()

        # Create a QStackedWidget
        self.StackedWidget = QStackedWidget()

        # Add the classes to the stacked widget
        self.StackedWidget.addWidget(AutoMenue())
        self.StackedWidget.addWidget(TestMenue())
        self.StackedWidget.addWidget(CalibratingMenue())

        # Add the stacked widget to the layout
        layout.addWidget(self.StackedWidget)

        # Create buttons to switch between classes
        self.buttonWork = QPushButton('Work Mode', self)
        self.buttonTest = QPushButton('Test Mode', self)
        self.buttonCalibrate = QPushButton('Calibrate', self)

        # Connect buttons to switch classes
        self.buttonWork.clicked.connect(self.switch_WorkMode)
        self.buttonTest.clicked.connect(self.switch_TestMode)
        self.buttonCalibrate.clicked.connect(self.switch_CalibratingMenue)

        # Create layout and add buttons
        
        layout.addWidget(self.buttonWork)
        layout.addWidget(self.buttonTest)
        layout.addWidget(self.buttonCalibrate)
        self.setLayout(layout) 
    
    def switch_WorkMode(self):
        # Switch to AutoMenue
        self.StackedWidget.setCurrentIndex(0)

    def switch_TestMode(self):
        # Switch to TestMenue
        self.StackedWidget.setCurrentIndex(1)

    def switch_CalibratingMenue(self):
        # Switch to CalibratingMenue
        self.StackedWidget.setCurrentIndex(2)

#This class is the main window of the GUI
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set layout
        layout = QVBoxLayout()

        # Create instance of classes
        self.ClassMenue = MenueStacker()
        self.ClassCell = CellDisplay()

        # Use QSplitter for resizable splits (Horizontal split)(Menue on the left, Cell on the right)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.ClassMenue)
        splitter.addWidget(self.ClassCell)
        layout.addWidget(splitter)

        self.setLayout(layout)
    
    
# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.setMinimumSize(500, 500)
window.setWindowTitle('P2 GUI')
window.show()
app.exec()