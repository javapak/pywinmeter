
from turtle import down, isdown
from PySide6 import QtWidgets, QtCore, QtGui
import ctypes
import subprocess
import winapps

from qt_material import apply_stylesheet
from qt_material import QtStyleTools

#class to create PySide6 main window instance
class View(QtWidgets.QWidget, QtStyleTools):
    icons = {}
    def __init__(self):
        super(View, self).__init__(parent=None)
        apply_stylesheet(self, theme='dark_purple.xml')
        size = QtGui.QGuiApplication.primaryScreen().availableSize()
        w = size.width()
        h = size.height()
        self.setWindowOpacity(0.95)
        self.setFixedSize(w/3, h/1.5)
        self.setWindowFlag(QtCore.Qt.Window.FramelessWindowHint)
        self.setContentsMargins(15,15,15,15)
        self.scroll_panel = QtWidgets.QWidget()
        self.scroll_panel_layout = QtWidgets.QVBoxLayout()
        self.scroll_panel.setLayout(self.scroll_panel_layout)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_bar = QtWidgets.QScrollBar()
        self.scroll_bar.setStyleSheet('dark_purple.xml')
        self.scroll_area.addScrollBarWidget(self.scroll_bar, QtCore.Qt.AlignRight)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_panel)
        
        radius = 35.0
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), radius, radius)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        self.endpoint_sessions_vbox_dict = {}
        self.setWindowTitle("Pywinmeter")
        # layout
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.deviceSettings = QtWidgets.QPushButton(text='Device settings')
        self.deviceSettings.clicked.connect(lambda: subprocess.run("control mmsys.cpl sounds"))
        self.mainLayout.addWidget(self.deviceSettings)
        self.mainLayout.addWidget(self.scroll_area)
    
    def snap_to_br(self):
        ag = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        sg = QtGui.QGuiApplication.primaryScreen().size()
        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)
    
 
    def endpoint_view(self, endpoint_name, id, volume, signal_func):
        layout = QtWidgets.QHBoxLayout()
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        label = QtWidgets.QLabel(text = "<b>" + endpoint_name + "</b>")
        layout.addWidget(label)
        slider.valueChanged.connect(lambda: signal_func(id, slider.value()))
        slider.setValue(volume)
        self.scroll_panel_layout.addLayout(layout)
        self.scroll_panel_layout.addWidget(slider)
        self.endpoint_sessions_vbox_dict[id] = QtWidgets.QVBoxLayout()
        self.scroll_panel_layout.addLayout(self.endpoint_sessions_vbox_dict[id])
    
    def on_session_create_show(self, key, endpoint_id, id, volume, signal_func, mute_func):
        frame = QtWidgets.QFrame()
        frame.setLayout(self.endpoint_sessions_vbox_dict[endpoint_id])
        layout = QtWidgets.QHBoxLayout()
        toolbutton = QtWidgets.QToolButton()
        toolbutton.setText(key + ': No icon found')
        if self.icons.get(key) != None:
            toolbutton.setText('')
            icon = QtGui.QImage(self.icons.get(key).rgbSwapped())
            pixmap = QtGui.QPixmap().fromImage(icon)
            q_icon = QtGui.QIcon(pixmap)
            toolbutton.setIcon(q_icon)
            toolbutton.setIconSize(QtCore.QSize(24,24))
        toolbutton.setObjectName(id)
        toolbutton.clicked.connect(lambda: mute_func(id, endpoint_id))
        toolbutton.setCheckable(True)
        layout.addWidget(toolbutton)
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setObjectName(id)
        slider.setValue(volume)
        slider.valueChanged.connect(lambda: signal_func(endpoint_id, id, slider.value()))
        layout.addWidget(slider)
        self.endpoint_sessions_vbox_dict[endpoint_id].addLayout(layout)
        frame.show()
        print('oi go fuck yourself i guess')
        
        self.update()




        

 
    def session_slider_view(self, key, endpoint_id, id, volume, signal_func, mute_func): #add slider widgets to main window.
        layout = QtWidgets.QHBoxLayout()
        toolbutton = QtWidgets.QToolButton()
        toolbutton.setText(key + ': No icon found')
        if self.icons.get(key) != None:
            toolbutton.setText('')
            icon = QtGui.QImage(self.icons.get(key).rgbSwapped())
            pixmap = QtGui.QPixmap().fromImage(icon)
            q_icon = QtGui.QIcon(pixmap)
            toolbutton.setIcon(q_icon)
            toolbutton.setIconSize(QtCore.QSize(24,24))
        toolbutton.setObjectName(id)
        toolbutton.clicked.connect(lambda: mute_func(id, endpoint_id))
        toolbutton.setCheckable(True)
        layout.addWidget(toolbutton)
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setObjectName(id)
        slider.setValue(volume)
        slider.valueChanged.connect(lambda: signal_func(endpoint_id, id, slider.value()))
        layout.addWidget(slider)
        self.endpoint_sessions_vbox_dict[endpoint_id].addLayout(layout)


            

        
    
    def if_equalizer_apo(self, show_func): 
        for item in winapps.list_installed():
            app_name = "Equalizer APO"
            if app_name in item.name:
                get_path = item.uninstall_string
                equalizer_apo = QtWidgets.QPushButton(text="Equalizer APO Parameters")
                equalizer_apo.clicked.connect(show_func)
                get_path = get_path.replace('Uninstall.exe', 'config\\config.txt')
                self.mainLayout.addWidget(equalizer_apo)
                return get_path
    




        



                
        

