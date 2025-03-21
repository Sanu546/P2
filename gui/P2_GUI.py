from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QComboBox
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QSplitter, QStackedWidget, QSlider
from PyQt6.QtGui import QFont
import sys
from PyQt6.QtCore import Qt, QTimer
import cv2 as cv

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

class CameraView(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
            
        self.label = QLabel("Camera view")
        self.buttonOn = QPushButton("On")
        self.buttonOff = QPushButton("Off")

        self.buttonOn.clicked.connect(self.on)
        self.buttonOff.clicked.connect(self.off)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.buttonOn)
        layout.addWidget(self.buttonOff)
        self.setLayout(layout)
    
    def on(self):
        camera = cv.VideoCapture(0)
        frame = camera.read()
        cv.imshow('Camera View', frame)
        camera.release()
    
    def off(self):
        cv.destroyAllWindows

class TestMenu(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create label
        self.label = QLabel("Test Menu:")
        #Bold and underlined font
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedHeight(50)

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
    
    def Back(self):
        print("Back")

    def Reset(self):
        print("Reset")

class AutoMenu(QWidget):
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
        
    def setFunctionStart(self, function):
        self.buttonStart.clicked.connect(function)
    
    def setFunctionStop(self, function):
        self.buttonStop.clicked.connect(function)
    
    def setFunctionReset(self, function):
        self.buttonReset.clicked.connect(function)
    
    def start(self):
        print("Start")

    def stop(self):
        print("Stop")

    def reset(self):
        print("Reset")


class Calibrator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a label to display the pressed arrow key
        self.label = QLabel("Calibrating Buttons:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelLeft = QLabel("Rotate Left:")
        self.labelRight = QLabel(":Rotate Right")

        self.buttonUp = QPushButton("↑")
        self.buttonDown = QPushButton("↓")
        self.buttonLeft = QPushButton("←")
        self.buttonRight = QPushButton("→")
        self.buttonRotLeft = QPushButton("←")
        self.buttonRotRight = QPushButton("→")

        #connecting buttons to terminal print
        self.buttonUp.pressed.connect(self.up)
        self.buttonUp.released.connect(self.stopAction)
        self.buttonDown.pressed.connect(self.down)
        self.buttonDown.released.connect(self.stopAction)
        self.buttonLeft.pressed.connect(self.left)
        self.buttonLeft.released.connect(self.stopAction)
        self.buttonRight.pressed.connect(self.right)
        self.buttonRight.released.connect(self.stopAction)
        self.buttonRotLeft.pressed.connect(self.rotLeft)
        self.buttonRotLeft.released.connect(self.stopAction)
        self.buttonRotRight.pressed.connect(self.rotRight)
        self.buttonRotRight.released.connect(self.stopAction)

        self.dropdown = QComboBox()
        self.dropdown.addItems(["Hello","How are you","quite well","Thank you very much"])
        self.dropdown.currentIndexChanged.connect(self.base)

         # Main vertical layout
        vbox = QVBoxLayout()

        # Horizontal layout for rotator buttons
        rot = QHBoxLayout()
        rot.addWidget(self.labelLeft)
        rot.addWidget(self.buttonRotLeft)
        rot.addWidget(self.buttonRotRight)
        rot.addWidget(self.labelRight)

        # Horizontal layout for arrow buttons
        hbox = QHBoxLayout()
        hbox.addWidget(self.buttonLeft)
        hbox.addWidget(self.buttonDown)
        hbox.addWidget(self.buttonRight)

        # Add widgets and layouts to the main vertical layout in the desired order
        vbox.addWidget(self.dropdown) 
        vbox.addWidget(self.label)     
        vbox.addLayout(rot)             
        vbox.addWidget(self.buttonUp) 
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.timer = QTimer()
        self.timer.timeout.connect(self.performAction)

        self.currentAction = None

    def setFunctionUp(self,function):
        self.buttonUp.pressed.connect(function)
        self.currentAction = "up"
        self.timer.start(100)
    
    def setFunctionDown(self,function):
        self.buttonDown.pressed.connect(function)
        self.currentAction = "down"
        self.timer.start(100)
    
    def setFunctionLeft(self,function):
        self.buttonLeft.pressed.connect(function)
        self.currentAction = "left"
        self.timer.start(100)
    
    def setFunctionRight(self,function):
        self.buttonRight.pressed.connect(function)
        self.currentAction = "right"
        self.timer.start(100)        

    def setFunctionRotLeft(self,function):
        self.buttonRotLeft.pressed.connect(function)
        self.currentAction = "rotate left"
        self.timer.start(100)
    
    def setFunctionRotRight(self,function):
        self.buttonRotRight.pressed.connect(function)
        self.currentAction = "rotate right"
        self.timer.start(100)

    def setFunctionStopAction(self,function):
        self.buttonUp.released.connect(function)
        self.buttonDown.released.connect(function)
        self.buttonLeft.released.connect(function)
        self.buttonRight.released.connect(function)
        self.buttonRotLeft.released.connect(function)
        self.buttonRotRight.released.connect(function)
        self.currentAction = None
        self.timer.stop()

    def up(self):
        self.currentAction = "up"
        self.timer.start(100)

    def down(self):
        self.currentAction = "down"
        self.timer.start(100)
    
    def left(self):
        self.currentAction = "left"
        self.timer.start(100)

    def right(self):
        self.currentAction = "right"
        self.timer.start(100)

    def rotLeft(self):
        self.currentAction = "rotate left"
        self.timer.start(100)
    
    def rotRight(self):
        self.currentAction = "rotate right"
        self.timer.start(100)
    
    def stopAction(self):
        self.timer.stop()
        self.currentAction = None
    
    def performAction(self):
        if self.currentAction == "up":
            print("up")
            
        elif self.currentAction == "down":
            print("down")
            
        elif self.currentAction == "left":
            print("left")
        elif self.currentAction == "right":
            print("right")
           
        elif self.currentAction == "rotate left":
            print("rotate left")
        
        elif self.currentAction == "rotate right":
            print("rotate left")

    def base(self, index):
        print(index)

# This class lets us switch between the TestMenue and AutoMenue classes
class MenuStacker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create layout
        layout = QVBoxLayout()

        # Create a QStackedWidget
        self.StackedWidget = QStackedWidget()
        
        self.autoMenu = AutoMenu()
        self.testMenu = TestMenu()

        # Add the classes to the stacked widget
        self.StackedWidget.addWidget(self.autoMenu)
        self.StackedWidget.addWidget(self.testMenu)

        # Add the stacked widget to the layout
        layout.addWidget(self.StackedWidget)

        # Create buttons to switch between classes
        self.buttonWork = QPushButton('Work Mode', self)
        self.buttonTest = QPushButton('Test Mode', self)

        # Connect buttons to switch classes
        self.buttonWork.clicked.connect(self.switchWorkMode)
        self.buttonTest.clicked.connect(self.switchTestMode)

        # Add buttons to the layout
        layout.addWidget(self.buttonWork)
        layout.addWidget(self.buttonTest)
        self.setLayout(layout) 
    
    def switchWorkMode(self):
        # Switch to AutoMenue
        self.StackedWidget.setCurrentIndex(0)

    def switchTestMode(self):
        # Switch to TestMenue
        self.StackedWidget.setCurrentIndex(1)

class DropdownStacker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.StackedWidget = QStackedWidget()
        self.cellDisplay = CellDisplay()
        self.calibrator = Calibrator()
        self.CameraView = CameraView()

        self.StackedWidget.addWidget(self.cellDisplay)
        self.StackedWidget.addWidget(self.calibrator)
        self.StackedWidget.addWidget(self.CameraView)

        # dropdown menu
        self.dropdown = QComboBox()

        self.dropdown.addItems(["Cell Display","Calibrator","Camera View"])
        
        self.dropdown.currentIndexChanged.connect(self.switchMode)
        
        layout.addWidget(self.dropdown)
        layout.addWidget(self.StackedWidget)
        self.setLayout(layout)

    def switchMode(self, index):
        self.StackedWidget.setCurrentIndex(index)
    
# This class is the main window of the GUI
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
        self.controlMenu = MenuStacker()
        self.dropdownStacker = DropdownStacker()
        

        # Use QSplitter for resizable splits (Horizontal split)(Menue on the left, Cell on the right)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.controlMenu)
        splitter.addWidget(self.dropdownStacker)
        layout.addWidget(splitter)

        self.setLayout(layout)
        
    def runUI(self):
         self.show()
         self.app.exec() 

# Run the GUI
window = MainWindow()
window.runUI()