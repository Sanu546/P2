from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QComboBox
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSplitter, QStackedWidget
from PyQt6.QtGui import QFont, QImage, QPixmap
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
        layout = QVBoxLayout()

        self.camera = cv.VideoCapture(0)

        self.label = QLabel()
        
        layout.addWidget(self.label)
        self.setLayout(layout)
    
        self.timer = QTimer()
        self.timer.timeout.connect(self.runCamera)
        self.timer.start(30)

    def runCamera(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame = cv.flip(frame, 1)
            frame = cv.resize(frame,(300,300))
            

            h, w, ch = frame.shape
            bytesPerLine = ch * w
            qImg = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)

            self.label.setPixmap(QPixmap.fromImage(qImg))

    def closeEvent(self,event):
        self.camera.release()
        event.accept()
    
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
        self.buttonNext.setStyleSheet("background-color: gray")
        self.buttonBack.setStyleSheet("background-color: gray")
        self.buttonReset.setStyleSheet("background-color: blue")

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

class AutoMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Create label
        self.label = QLabel("Auto Menu:")
        #Bold and underlined font
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedHeight(50)


        # Create label, set size and align
        self.label = QLabel("Auto Menu:")
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedHeight(50)

        # Create buttons
        self.buttonStart = QPushButton("Auto Start")
        self.buttonStop = QPushButton("Auto Stop")
        self.buttonReset = QPushButton("Reset")
        
        #Disable the stop button
        self.buttonStop.setEnabled(False)

        # Set colors of the buttons
        self.buttonStart.setStyleSheet("background-color: white; color : black")
        self.buttonStop.setStyleSheet("background-color: black")
        self.buttonReset.setStyleSheet("background-color: blue")

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
        layout.addWidget(self.label)
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

class Calibrator(QWidget):
    
    rotateRightFunc = None
    rotateLeftFunc = None
    upFunc = None
    downFunc = None
    leftFunc = None
    rightFunc = None
    stopActionFunc = None
    upUpFunc = None
    downDownFunc = None
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a label to display the pressed arrow key
        self.startCal = QPushButton("Start Calibration")
        self.saveCal = QPushButton("Save Calibration")
        self.resetCal = QPushButton("Reset Calibration")
        self.stopCal = QPushButton("Stop Calibration")
        
        self.startCal.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.saveCal.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.resetCal.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.stopCal.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        self.startCal.setFixedHeight(30)
        self.saveCal.setFixedHeight(30)
        self.resetCal.setFixedHeight(30)
        self.stopCal.setFixedHeight(30)
        
        self.spacing = QLabel("")
        self.spacing.setFixedHeight(10)
        
        self.spacing2 = QLabel("")
        self.spacing2.setFixedHeight(10)
        
        self.xTitle = QLabel("X:")
        self.yTitle = QLabel("Y:")
        self.zTitle = QLabel("Z:")
        self.rotXTitle = QLabel("Rot X:")
        self.rotYTitle = QLabel("Rot Y:")
        self.rotZTitle = QLabel("Rot Z:")
        
        self.xTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.yTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rotXTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rotYTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rotZTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.xTitle.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.yTitle.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.zTitle.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.rotXTitle.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.rotYTitle.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.rotZTitle.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.xValue = QLineEdit()
        self.yValue = QLineEdit()
        self.zValue = QLineEdit()
        self.rotXValue = QLineEdit()
        self.rotYValue = QLineEdit()
        self.rotZValue = QLineEdit()
        
        self.xValue.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.yValue.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.zValue.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.rotXValue.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.rotYValue.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.rotZValue.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.xValue.setFixedHeight(30)
        self.yValue.setFixedHeight(30)
        self.zValue.setFixedHeight(30)
        self.rotXValue.setFixedHeight(30)
        self.rotYValue.setFixedHeight(30)
        self.rotZValue.setFixedHeight(30)
        
        self.xValue.setFixedWidth(100)
        self.yValue.setFixedWidth(100)
        self.zValue.setFixedWidth(100)
        self.rotXValue.setFixedWidth(100)   
        self.rotYValue.setFixedWidth(100)
        self.rotZValue.setFixedWidth(100)
        
        self.xValue.setReadOnly(True)
        self.yValue.setReadOnly(True)
        self.zValue.setReadOnly(True)
        self.rotXValue.setReadOnly(True)
        self.rotYValue.setReadOnly(True)
        self.rotZValue.setReadOnly(True)
        
        self.label = QLabel("Calibrating Buttons:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelLeft = QLabel("Rotate Left:")
        self.labelRight = QLabel(":Rotate Right")

        self.buttonUp = QPushButton("↑")
        self.buttonDown = QPushButton("↓")
        self.buttonLeft = QPushButton("←")
        self.buttonRight = QPushButton("→")
        self.buttonUpUp = QPushButton("↑")
        self.buttonDownDown = QPushButton("↓")
        
        self.buttonRotLeft = QPushButton("←")
        self.buttonRotRight = QPushButton("→")
        
        self.buttonDownDown.setFixedWidth(23)
        self.buttonUpUp.setFixedWidth(23)
        self.buttonUpUp.setFixedHeight(58)
        self.buttonDownDown.setFixedHeight(58)
        
        self.buttonUp.setEnabled(False)
        self.buttonDown.setEnabled(False)
        self.buttonLeft.setEnabled(False)
        self.buttonRight.setEnabled(False)
        self.buttonRotLeft.setEnabled(False)
        self.buttonRotRight.setEnabled(False)
        self.startCal.setEnabled(True)
        self.stopCal.setEnabled(False)
        self.saveCal.setEnabled(False)
        self.resetCal.setEnabled(False)
        self.buttonUpUp.setEnabled(False)
        self.buttonDownDown.setEnabled(False)
        
        self.startCal.clicked.connect(self.startCalibration)
        self.stopCal.clicked.connect(self.stopCalibration)
        self.resetCal.clicked.connect(self.resetCalibration)
        
        self.buttonUp.released.connect(self.adjustmentStop)
        self.buttonDown.released.connect(self.adjustmentStop)
        self.buttonLeft.released.connect(self.adjustmentStop)
        self.buttonRight.released.connect(self.adjustmentStop)
        self.buttonRotLeft.released.connect(self.adjustmentStop)
        self.buttonRotRight.released.connect(self.adjustmentStop)

        self.dropdown = QComboBox()
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
        
        xyTranslationBox = QVBoxLayout()
        
        xyTranslationBox.addWidget(self.buttonUp)
        xyTranslationBox.addLayout(hbox)
        
        translationBox = QHBoxLayout()
        translationBox.addWidget(self.buttonUpUp)
        translationBox.addLayout(xyTranslationBox)  
        translationBox.addWidget(self.buttonDownDown)
        
        
        startSaveBox = QHBoxLayout()
        startSaveBox.addWidget(self.startCal)
        startSaveBox.addWidget(self.saveCal)
        
        stopResetBox = QHBoxLayout()
        stopResetBox.addWidget(self.stopCal)
        stopResetBox.addWidget(self.resetCal)
        
        xTitleBox = QHBoxLayout()
        xTitleBox.addWidget(self.xTitle)
        xTitleBox.addWidget(self.rotXTitle)
        
        xValueBox = QHBoxLayout()
        xValueBox.addWidget(self.xValue)
        xValueBox.addWidget(self.rotXValue)
        
        yTitleBox = QHBoxLayout()
        yTitleBox.addWidget(self.yTitle)
        yTitleBox.addWidget(self.rotYTitle)
        
        yValueBox = QHBoxLayout()
        yValueBox.addWidget(self.yValue)
        yValueBox.addWidget(self.rotYValue)
        
        zTitleBox = QHBoxLayout()
        zTitleBox.addWidget(self.zTitle)
        zTitleBox.addWidget(self.rotZTitle)
        
        zValueBox = QHBoxLayout()
        zValueBox.addWidget(self.zValue)
        zValueBox.addWidget(self.rotZValue)
        
        cooradinateBoxL = QVBoxLayout()
        cooradinateBoxL.addWidget(self.xTitle)
        cooradinateBoxL.addWidget(self.xValue)
        cooradinateBoxL.addWidget(self.yTitle)
        cooradinateBoxL.addWidget(self.yValue)
        cooradinateBoxL.addWidget(self.zTitle)
        cooradinateBoxL.addWidget(self.zValue)
        
        cooradinateBoxR = QVBoxLayout()
        cooradinateBoxR.addWidget(self.rotXTitle)
        cooradinateBoxR.addWidget(self.rotXValue)
        cooradinateBoxR.addWidget(self.rotYTitle)
        cooradinateBoxR.addWidget(self.rotYValue)
        cooradinateBoxR.addWidget(self.rotZTitle)
        cooradinateBoxR.addWidget(self.rotZValue)
        
        cooradinateBoxL.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cooradinateBoxR.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        cooradinateBox = QHBoxLayout()
        cooradinateBox.addLayout(cooradinateBoxL)
        cooradinateBox.addLayout(cooradinateBoxR)
        
        cooradinateBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add widgets and layouts to the main vertical layout in the desired order
        vbox.addWidget(self.dropdown) 
        vbox.addWidget(self.spacing)
        vbox.addLayout(startSaveBox)
        vbox.addLayout(stopResetBox)
        vbox.addWidget(self.spacing2)
        vbox.addLayout(cooradinateBox)
        vbox.addLayout(rot)          
        vbox.addLayout(translationBox)
        
        self.setLayout(vbox)

        self.timer = QTimer()
        self.timer.timeout.connect(self.performAction)

        self.currentAction = None    
        
    def setStartCalibration(self, function):
        self.startCal.clicked.connect(function)
    
    def setSaveCalibration(self, function):
        self.saveCal.clicked.connect(function)
    
    def setResetCalibration(self, function):
        self.resetCal.clicked.connect(function)
    
    def setStopCalibration(self, function):
        self.stopCal.clicked.connect(function)
    
    def setFunctionUp(self,function):
        self.upFunc = function 
        self.currentAction = "up"
        self.timer.start(100)
    
    def setFunctionDown(self,function):
        self.downFunc = function
        self.currentAction = "down"
        self.timer.start(100)
    
    def setFunctionLeft(self,function):
        self.leftFunc = function
        self.currentAction = "left"
        self.timer.start(100)
    
    def setFunctionRight(self,function):
        self.rightFunc = function
        self.currentAction = "right"
        self.timer.start(100)        
        
    def setFunctionUpUp(self,function):
        self.upUpFunc = function 
        self.currentAction = "upup"
        self.timer.start(100)
    
    def setFunctionDownDown(self,function):
        self.downDownFunc = function
        self.currentAction = "downdown"
        self.timer.start(100)
        
    def setFunctionRotLeft(self,function):
        self.rotateLeftFunc = function
        self.currentAction = "rotate left"
        self.timer.start(100)
    
    def setFunctionRotRight(self,function):
        self.rotateRightFunc = function
        self.currentAction = "rotate right"
        self.timer.start(100)
    
    def setFunctionChangeBase(self,function):
        self.dropdown.currentIndexChanged.connect(function)
        
    def setCurrentPose(self, pose):
        self.rotXValue.setText(f"{pose[0]:.2f}")
        self.rotYValue.setText(f"{pose[1]:.2f}")
        self.rotZValue.setText(f"{pose[2]:.2f}")
        self.xValue.setText(f"{pose[3]*100:.2f}")
        self.yValue.setText(f"{pose[4]*100:.2f}")
        self.zValue.setText(f"{pose[5]*100:.2f}")
        
    def adjustmentStop(self):
        self.currentAction = None
        self.timer.stop()

    def startCalibration(self):
        print("Calibration started")
        self.buttonUp.setEnabled(True)
        self.buttonDown.setEnabled(True)
        self.buttonLeft.setEnabled(True)
        self.buttonRight.setEnabled(True)
        self.buttonRotLeft.setEnabled(True)
        self.buttonRotRight.setEnabled(True)
        self.buttonUpUp.setEnabled(True)
        self.buttonDownDown.setEnabled(True)
        self.startCal.setEnabled(False)
        self.stopCal.setEnabled(True)
        self.saveCal.setEnabled(True)
        self.resetCal.setEnabled(True)
        self.xValue.setReadOnly(False)
        self.yValue.setReadOnly(False)
        self.zValue.setReadOnly(False)
        self.rotXValue.setReadOnly(False)
        self.rotYValue.setReadOnly(False)
        self.rotZValue.setReadOnly(False)
    
    def stopCalibration(self):
        print("Calibration stopped")
        self.buttonUp.setEnabled(False)
        self.buttonDown.setEnabled(False)
        self.buttonLeft.setEnabled(False)
        self.buttonRight.setEnabled(False)
        self.buttonRotLeft.setEnabled(False)
        self.buttonRotRight.setEnabled(False)
        self.buttonUpUp.setEnabled(False)
        self.buttonDownDown.setEnabled(False)
        self.startCal.setEnabled(True)
        self.stopCal.setEnabled(False)
        self.saveCal.setEnabled(False)
        self.resetCal.setEnabled(False)
        self.xValue.setReadOnly(True)
        self.yValue.setReadOnly(True)
        self.zValue.setReadOnly(True)
        self.rotXValue.setReadOnly(True)
        self.rotYValue.setReadOnly(True)
        self.rotZValue.setReadOnly(True)    
    
    def resetCalibration(self):
        print("Calibration reset")
        self.buttonUp.setEnabled(False)
        self.buttonDown.setEnabled(False)
        self.buttonLeft.setEnabled(False)
        self.buttonRight.setEnabled(False)
        self.buttonRotLeft.setEnabled(False)
        self.buttonRotRight.setEnabled(False)
        self.buttonUpUp.setEnabled(False)   
        self.buttonDownDown.setEnabled(False)
        self.startCal.setEnabled(True)
        self.stopCal.setEnabled(False)
        self.saveCal.setEnabled(False)
        self.resetCal.setEnabled(False)
        self.xValue.setReadOnly(False)
        self.yValue.setReadOnly(False)
        self.zValue.setReadOnly(False)
        self.rotXValue.setReadOnly(False)
        self.rotYValue.setReadOnly(False)
        self.rotZValue.setReadOnly(False)
        
    
    def performAction(self):
        if self.currentAction == "up":
            if self.upFunc == None:
                print("Up not defined")
                return
            print("Up")
            self.upFunc()
        elif self.currentAction == "down":
            if self.downFunc == None:
                print("Down not defined")
                return
            print("Down")
            self.downFunc()
        elif self.currentAction == "left":
            if self.leftFunc == None:   
                print("Left not defined")
                return
            print("Left")
            self.leftFunc() 
        elif self.currentAction == "right":
            if self.rightFunc == None:
                print("Right not defined")
                return
            print("Right")
            self.rightFunc()
        elif self.currentAction == "rotate left":
            if self.rotateLeftFunc == None:
                print("Rotate Left not defined")
                return
            print("Rotate Left")
            self.rotateLeftFunc()
        elif self.currentAction == "rotate right":
            if self.rotateRightFunc == None:
                print("Rotate Right not defined")
                return
            print("Rotate Right")
            self.rotateRightFunc()  
        elif self.currentAction == "upup":
            if self.upUpFunc == None:
                print("Up Up not defined")
                return
            print("Up Up")
            self.upUpFunc()
        elif self.currentAction == "downdown":
            if self.downDownFunc == None:
                print("Down Down not defined")
                return
            print("Down Down")
            self.downDownFunc()
        else:
            print("No action")

    def base(self, index):
        print("Base changed to:", index)
        

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
        
        self.progressTitleLable = QLabel(f"Progress:")
        self.progressLable = QLabel(f"Step 0/0")
        self.currentTargetTitleLable = QLabel("Current Target:")
        self.currentTargetLable = QLabel("None")
        self.nextTargetTitleLable = QLabel("Next Target:")
        self.nextTargetLable = QLabel("None")

        
        self.progressLable.setFont(QFont("Arial", 12, QFont.Weight.Bold, True))
        self.progressTitleLable.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.progressLable.setStyleSheet("color: grey")
        
        self.currentTargetTitleLable.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.currentTargetLable.setFont(QFont("Arial", 12, QFont.Weight.Bold, True))
        self.currentTargetLable.setStyleSheet("color: grey")
        
        self.nextTargetTitleLable.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.nextTargetLable.setFont(QFont("Arial", 12, QFont.Weight.Bold, True))
        self.nextTargetLable.setStyleSheet("color: grey")
        
        self.spaceing = QLabel("")
        self.spaceing.setFixedHeight(100)

        # Create buttons to switch between classes
        self.buttonWork = QPushButton('Work Mode', self)
        self.buttonTest = QPushButton('Test Mode', self)

        # Connect buttons to switch classes
        self.buttonWork.clicked.connect(self.switchWorkMode)
        self.buttonTest.clicked.connect(self.switchTestMode)

        # Add buttons to the layout
        layout.addWidget(self.progressTitleLable)
        layout.addWidget(self.progressLable)
        layout.addWidget(self.currentTargetTitleLable)
        layout.addWidget(self.currentTargetLable)
        layout.addWidget(self.nextTargetTitleLable)
        layout.addWidget(self.nextTargetLable)
        layout.addWidget(self.spaceing)
        layout.addWidget(self.buttonWork)
        layout.addWidget(self.buttonTest)
        self.setLayout(layout) 
    
    def setProgress(self, currentStep, totalSteps):
        self.progressLable.setText(f"Step {currentStep}/{totalSteps}")
    
    def setCurrentTarget(self, target):
        self.currentTargetLable.setText(f"{target}")
    
    def getCurrentMode(self):
        currentIndex = self.StackedWidget.currentIndex()
        if currentIndex == 0:
            return "auto"
        else:
            return "test"
    
    def setNextTarget(self, target):
        self.nextTargetLable.setText(f"{target}")
    
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
#window = MainWindow()
#window.runUI() 

