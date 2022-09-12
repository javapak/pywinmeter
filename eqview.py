from PySide6 import QtWidgets, QtGui, QtCore
from qt_material import apply_stylesheet, QtStyleTools

class EqualizerView(QtWidgets.QWidget, QtStyleTools): 
    def __init__(self):
        super(EqualizerView, self).__init__(parent=None)
        size = QtGui.QGuiApplication.primaryScreen().availableSize()
        w = size.width()
        h = size.height()
        self.setFixedSize(w/3, h/1.5)
        self.setWindowTitle("EQ Settings")
        self.setWindowOpacity(0.95)
        radius = 35.0
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), radius, radius)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        self.setWindowFlag(QtCore.Qt.Window.FramelessWindowHint)
        self.scroll_panel = QtWidgets.QWidget()
        self.scroll_panel_layout = QtWidgets.QVBoxLayout(self.scroll_panel)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_panel)
        self.mainlay = QtWidgets.QVBoxLayout(self)
        self.mainlay.addWidget(self.scroll_area)
        self.sliders = []

        apply_stylesheet(self, theme='dark_purple.xml')
        
    def init_slider(self):
        self.sliders.append(QtWidgets.QSlider(QtCore.Qt.Horizontal))

    def slider_layout(self, index, label):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.sliders[index])
        self.scroll_panel_layout.addLayout(layout)
    
    def connect(self, signal_func):

        for slider in self.sliders:
            slider.setMinimum(-100)
            slider.setMaximum(100)
            slider.setObjectName(str(self.sliders.index(slider))) # I know how strange this looks, get the index from the object itself, but I was getting errors thrown when attempting use enumerate, etc...
            slider.valueChanged.connect(lambda: signal_func(self.sliders.index(slider), self.sliders[self.sliders.index(slider)].value()))
    

    def snap_to_br(self):
        ag = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        sg = QtGui.QGuiApplication.primaryScreen().size()
        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)
        
                
    def slider_view(self, bandfreqs, signal_func): #for loop solution seems to involve memory being overwritten with that of the last slider..., seems pretty straight forward so i'll figure it out later. 
        back_button = QtWidgets.QPushButton(text = "BACK")
        back_button.clicked.connect(self.close)
        self.scroll_panel_layout.addWidget(back_button)
        for i, freq in enumerate(bandfreqs):
            self.init_slider()
            labeltext = freq.split(' ')
            labeltext = labeltext[0] + " Hz"
            label = QtWidgets.QLabel(text= labeltext)
            self.slider_layout(i, label)
            self.connect(signal_func)


            

