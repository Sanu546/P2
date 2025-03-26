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
        #self.input_layout = QVBoxLayout()

        # Create a 2x4 grid of boxes (buttons)
        self.boxes = []
        for row in range(4):
            for col in range(2):
                box = QPushButton('', self)
                box.setFixedSize(50, 50)  # Set a fixed size for the boxes
                self.grid_layout.addWidget(box, row, col)
                self.boxes.append(box)

        # Input field for the array
        #self.input_label = QLabel('Enter 8 colors (comma-separated):')
        #self.input_field = QLineEdit(self)
        #self.input_field.setPlaceholderText('e.g., red,green,blue,...')
        #self.update_button = QPushButton('Update Visualisation')
        #self.update_button.clicked.connect(self.update_colors)
        
        # Add widgets to the input layout
        #self.input_layout.addWidget(self.input_label)
        #self.input_layout.addWidget(self.input_field)
        #self.input_layout.addWidget(self.update_button)
        
        # Combine the grid and input layouts
        layout = QVBoxLayout()
        layout.addLayout(self.grid_layout)
        #layout.addLayout(self.input_layout)

        # Set the main layout
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('2x8 Color Grid')
        self.setGeometry(300, 300, 500, 200)

    def update_colors(self, colors):
        """Update the colors of the boxes based on the input array."""
        #input_text = self.input_field.text().strip()
        #if not input_text:
            #return

        # Split the input into a list of colors
        #colors = input_text.split(',')
        # if len(colors) != 8:
        #     self.input_field.setPlaceholderText('Please enter exactly 8 colors.')
        #     return

        # Update the colors of the boxes
        
        
        for i, box in enumerate(self.boxes):
            x = 0 if i % 2 == 0 else 1
            y = i // 2
            color = colors[y][x].strip()
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
        self.buttonNext = QPushButton("Next Procces Step")
        self.buttonBack = QPushButton("Back")
        self.buttonReset = QPushButton("Reset")
    
        # Set color of the buttons
        self.buttonNext.setStyleSheet("background-color: green")
        self.buttonBack.setStyleSheet("background-color: red")
        self.buttonReset.setStyleSheet("background-color: orange")

        # Set the size of the buttons
        self.buttonNext.setFixedHeight(50)
        self.buttonBack.setFixedHeight(50)
        self.buttonReset.setFixedHeight(50)
        
        #Disable the back button
        self.buttonBack.setEnabled(False)

        # Set the font size of the buttons
        self.buttonNext.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.buttonBack.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.buttonReset.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # Connect buttons to functions (slots)
        self.buttonNext.clicked.connect(self.NextProccesStep)
        self.buttonBack.clicked.connect(self.Back)
        self.buttonReset.clicked.connect(self.Reset)

        # Add buttons to the layout
        layout.addWidget(self.label)
        layout.addWidget(self.buttonNext)
        layout.addWidget(self.buttonBack)
        layout.addWidget(self.buttonReset)
        layout.addStretch()

        self.setLayout(layout)
    #set function to button
    def setFunctionNext(self, function):
        self.buttonNext.clicked.connect(function)
    
    def setFunctionBack(self, function):
        self.buttonBack.clicked.connect(function)
    
    def setFunctionReset(self, function):
        self.buttonReset.clicked.connect(function)
    
    def NextProccesStep(self):
        print("Next Procces Step")
        self.buttonBack.setEnabled(True)
    
    def Back(self):
        self.buttonNext.setEnabled(True)
        print("Back")

    def Reset(self):
        print("Reset")
        self.buttonBack.setEnabled(False)
        self.buttonNext.setEnabled(True)

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
        
        #Disable the stop button
        self.buttonStop.setEnabled(False)

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
        
    def setFunctionStart(self, function):
        self.buttonStart.clicked.connect(function)
    
    def setFunctionStop(self, function):
        self.buttonStop.clicked.connect(function)
    
    def setFunctionReset(self, function):
        self.buttonReset.clicked.connect(function)
    
    def start(self):
        print("Start")
        self.buttonStop.setEnabled(True)
        self.buttonStart.setEnabled(False)

    def stop(self):
        print("Stop")
        self.buttonStop.setEnabled(False)
        self.buttonStart.setEnabled(True)

    def reset(self):
        print("Reset")
        self.buttonStop.setEnabled(False)
        self.buttonStart.setEnabled(True)

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
        
    def setChangeFunctionX(self, function):
        self.x_slider.valueChanged.connect(function)
    
    def setChangeFunctionY(self, function):
        self.y_slider.valueChanged.connect(function)
    
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
        
        self.autoMenu = AutoMenue()
        self.testMenu = TestMenue()
        self.calibratingMenu = CalibratingMenue()

        # Add the classes to the stacked widget
        self.StackedWidget.addWidget(self.autoMenu)
        self.StackedWidget.addWidget(self.testMenu)
        self.StackedWidget.addWidget(self.calibratingMenu)

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
    app = QApplication(sys.argv)
    def __init__(self, minSize = (500, 500), title = 'P2 GUI'):
        super().__init__()
        self.initUI()
        self.setMinimumSize(minSize[0], minSize[1])
        self.setWindowTitle(title)
       

    def initUI(self):
        # Set layout
        layout = QVBoxLayout()

        # Create instance of classes
        self.controlMenu = MenueStacker()
        self.cellDisplay = CellDisplay()

        # Use QSplitter for resizable splits (Horizontal split)(Menue on the left, Cell on the right)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.controlMenu)
        splitter.addWidget(self.cellDisplay)
        layout.addWidget(splitter)

        self.setLayout(layout)
        
    def runUI(self):
         self.show()
         self.app.exec() 
        
