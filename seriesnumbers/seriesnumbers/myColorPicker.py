
from PySide import QtGui
from PySide import QtCore
import sys

class MyColorPickerDialog(QtGui.QDialog):

    def __init__(self):

        super(MyColorPickerDialog, self).__init__()

        self.background_color = QtGui.QColor(255,255,255)
        self.pen_color = QtGui.QColor(255,255,255)

        general_layout = QtGui.QVBoxLayout()

        self.__rainbow_gradient = ColorPicker()
        self.__color_gradient = ColorGradient(self.__rainbow_gradient)
        colors_layout = QtGui.QHBoxLayout()
        colors_layout.addWidget(self.__rainbow_gradient, stretch = 1)
        colors_layout.addWidget(self.__color_gradient, stretch = 5)

        options_layout = QtGui.QFormLayout()
        options_layout.setSpacing(0)
        self.background_button = QtGui.QPushButton()
        self.background_button.clicked.connect(self.update_background)
        self.pen_button = QtGui.QPushButton()
        self.pen_button.clicked.connect(self.update_pen)
        options_layout.addRow("Background", self.background_button)
        options_layout.addRow("Line", self.pen_button)

        apply_layout = QtGui.QHBoxLayout()
        apply_layout.addSpacing(150)
        self.apply_button = QtGui.QPushButton("Apply", self)
        self.apply_button.clicked.connect(self.close)
        apply_layout.addWidget(self.apply_button)
        apply_layout.addSpacing(150)

        general_layout.addLayout(colors_layout, stretch = 5)
        general_layout.addLayout(options_layout, stretch = 1)
        general_layout.addLayout(apply_layout, stretch = 1)

        self.setLayout(general_layout)
        self.setGeometry(60,70,500,400)

    def update_background(self):
        new_color = self.__color_gradient.selected_color
       	r = new_color.toRgb().red()
       	g = new_color.toRgb().green()
       	b = new_color.toRgb().blue()
       	new_style = "background-color:rgb({},{},{})".format(r,g,b)
       	self.background_color = QtGui.QColor(r, g, b)
       	self.background_button.setStyleSheet(new_style)

    def update_pen(self):
        new_color = self.__color_gradient.selected_color
       	r = new_color.toRgb().red()
       	g = new_color.toRgb().green()
       	b = new_color.toRgb().blue()
       	new_style = "background-color:rgb({},{},{})".format(r,g,b)
       	self.pen_color = QtGui.QColor(r, g, b)
       	self.pen_button.setStyleSheet(new_style)


class ColorGradient(QtGui.QWidget):

    def __init__(self,color_picker):
        super(ColorGradient,self).__init__()

        self.color_picker = color_picker
        self.color_picker.color_changed.connect(self.updateColor)
        self.gradient_image = None
        self.main_color = QtGui.QColor(255, 255, 255)
        self.__selector_y = 0.5
        self.__selector_x = 0.5
        self.selected_color = QtGui.QColor(0, 0, 0)
        self.getNewImage()
        self.updateColor(color_picker.color_selected)

        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self.getNewImage)

    def getNewImage(self):
        self.gradient_image = QtGui.QPixmap().grabWidget(self).toImage()

    def updateColor(self,color):
        self.main_color = color
        self.getNewImage()
        self.updatePixelColor()
        self.repaint()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawGradient(event,qp)
        qp.end()

    def drawGradient(self,event,qp):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        gradient = QtGui.QLinearGradient(QtCore.QPointF(width/2,height/9),QtCore.QPointF(width/2,8*height/9))
        gradient.setColorAt(0,QtGui.QColor(0,0,0))
        gradient.setColorAt(0.5,self.main_color)
        gradient.setColorAt(1,QtGui.QColor(255,255,255))
        gradient.InterpolationMode(QtGui.QGradient.ComponentInterpolation)

        qp.setBrush(gradient)
        qp.drawRect(width/10,height/9,8*width/10,7*height/9)

        qp.drawEllipse(self.__selector_x*9*width/10 - 10, self.__selector_y*8*height/9 - 10, 20, 20)

    def resizeEvent(self, event):
        self.__timer.start(500)

    def mouseReleaseEvent(self, event):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        cursor = QtGui.QCursor()
        new_pos = self.mapFromGlobal(cursor.pos())
        x = new_pos.x()
        y = new_pos.y()
        if x < \

                -9*width/10 and x > width/10 and y < 8*height/9 and y > height/9:
        	self.__selector_y = y/(8*height/9.0)
        	self.__selector_x = x/(9*width/10.0)
        self.updatePixelColor()
        self.repaint()

    def updatePixelColor(self):
        height = self.frameGeometry().height()
        width = self.frameGeometry().width()
        pixel_pos = QtCore.QPoint(self.__selector_x*9*width/10, self.__selector_y*8*height/9)
        self.selected_color = QtGui.QColor(self.gradient_image.pixel(pixel_pos))



class ColorPicker(QtGui.QWidget):

    color_changed = QtCore.Signal(QtGui.QColor)

    def __init__(self):
        super(ColorPicker,self).__init__()

        self.__selector_y = 0.1
        self.picker_image = None
        self.color_selected = QtGui.QColor(255,0,0)

        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self.getNewImage)

    def paintEvent(self,event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawColorPicker(event,qp)
        qp.end()

    def drawColorPicker(self,event,qp):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        gradient = QtGui.QLinearGradient(QtCore.QPointF(width/2,height/9), QtCore.QPointF(width/2,8*height/9))
        gradient.InterpolationMode(QtGui.QGradient.ComponentInterpolation)
        gradient.setColorAt(0,    QtGui.QColor(255, 0,   0))
        gradient.setColorAt(0.16, QtGui.QColor(255, 255, 0))
        gradient.setColorAt(0.32, QtGui.QColor(0,   255, 0))
        gradient.setColorAt(0.48, QtGui.QColor(0,   255, 255))
        gradient.setColorAt(0.64, QtGui.QColor(0,   0,   255))
        gradient.setColorAt(0.80, QtGui.QColor(255, 0,   255))
        gradient.setColorAt(1,    QtGui.QColor(255, 0,   0))

        qp.setBrush(gradient)
        qp.drawRect(width/3, height/9, width/3, 7*height/9)
        qp.drawEllipse(width/3,(self.__selector_y*8*height/9 - width/6), width/3, width/3)

    def mouseReleaseEvent(self, event):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        cursor = QtGui.QCursor()
        new_pos = self.mapFromGlobal(cursor.pos())
        x = new_pos.x()
        y = new_pos.y()
        if x < 2*width/3 and x > width/3 and y > height/9 and y < 8*height/9:
            self.__selector_y = (y)/(8*height/9.0)
        print self.__selector_y
        self.updatePixelColor()
        self.repaint()

    def resizeEvent(self,event):
        self.__timer.start(500)

    def updatePixelColor(self):
        height = self.frameGeometry().height()
        width = self.frameGeometry().width()
        pixel_pos = QtCore.QPoint(width/2, self.__selector_y*8*height/9)

        self.color_selected = QtGui.QColor(self.picker_image.pixel(pixel_pos))
        self.color_changed.emit(self.color_selected)

    def getNewImage(self):
        self.picker_image = QtGui.QPixmap().grabWidget(self).toImage()

    def RegisterSignal(self,obj):
        self.color_changed.connect(obj)


def main():
    app = QtGui.QApplication(sys.argv)
    dialog = MyColorPickerDialog()
    dialog.show()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
