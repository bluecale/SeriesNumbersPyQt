from PySide import QtGui
from PySide import QtCore
import sys, os
import fibonacci, padovan
import myColorPicker
import output

FIBONACCI_STRING = "Fibonacci"
PADOVAN_STRING = "Padovan"
SHELL_ICON = os.path.join(os.path.dirname(__file__), "shell.png")
SUM_ICON = os.path.join(os.path.dirname(__file__), "sum.png")
PLAY_ICON = os.path.join(os.path.dirname(__file__), "play.png")
STOP_ICON = os.path.join(os.path.dirname(__file__), "stop.png")
COLOR_ICON = os.path.join(os.path.dirname(__file__), "color.png")
FILE_FILTERS = "Text(.txt);;Jason(.json);;Exel(.csv)"

class Series_UI(QtGui.QWidget):

    def __init__(self):

        super(Series_UI, self).__init__()

        total_layout = QtGui.QVBoxLayout()

        top_layout = QtGui.QHBoxLayout()

        self.__series_picker = QtGui.QComboBox() 
        self.__series_picker.addItem(FIBONACCI_STRING)
        self.__series_picker.addItem(PADOVAN_STRING)

        options_layout = QtGui.QFormLayout()

        self.__recursion_spinner = QtGui.QDoubleSpinBox()
        self.__recursion_spinner.setRange(1, 1000)
        self.__recursion_spinner.setDecimals(0)
        options_layout.addRow("Recursions", self.__recursion_spinner)

        self.__offset_spinner = QtGui.QDoubleSpinBox()
        self.__offset_spinner.setRange(0, 100)
        self.__offset_spinner.setDecimals(0)
        options_layout.addRow("Offset", self.__offset_spinner)

        self.__multiply_spinner = QtGui.QDoubleSpinBox()
        self.__multiply_spinner.setRange(1, 100)
        options_layout.addRow("Multiply", self.__multiply_spinner)

        top_layout.addWidget(self.__series_picker)
        top_layout.addLayout(options_layout)

        run_layout = QtGui.QHBoxLayout()
        run_layout.addSpacing(50)

        self.__generate_button = QtGui.QPushButton(self)
        self.__generate_button.setIcon(QtGui.QIcon(PLAY_ICON))
        self.__generate_button.clicked.connect(self.start_generate_series)
        run_layout.addWidget(self.__generate_button)

        run_layout.addSpacing(10)

        self.__stop_button = QtGui.QPushButton(self)
        self.__stop_button.setIcon(QtGui.QIcon(STOP_ICON))
        self.__stop_button.setEnabled(False)
        run_layout.addWidget(self.__stop_button)

        run_layout.addSpacing(50)

        turtle_layout = QtGui.QHBoxLayout()
        turtle_layout.addSpacing(50)

        self.__turtle_runner = QtGui.QPushButton(self)
        self.__turtle_runner.clicked.connect(self.present_turtle)
        self.__turtle_runner.setEnabled(True)
        self.__turtle_runner.setIcon(QtGui.QIcon(SHELL_ICON))
        turtle_layout.addWidget(self.__turtle_runner)
        turtle_layout.addSpacing(10)

        self.__color_button = QtGui.QPushButton()
        self.__color_button.setIcon(QtGui.QIcon(COLOR_ICON))
        self.__color_button.clicked.connect(self.open_color_picker)
        self.__color_picker = myColorPicker.MyColorPickerDialog()
        turtle_layout.addWidget(self.__color_button)
        turtle_layout.addSpacing(50)

        self.__progress_bar = QtGui.QProgressBar()
        self.__progress_bar.setAlignment(QtCore.Qt.AlignHCenter)
        self.__progress_bar.setValue(0)

        self.__result_list = QtGui.QListWidget()

        self.__export_button = QtGui.QPushButton("Export")
        self.__export_button.clicked.connect(self.open_file_dialog)
        self.__export_button.setEnabled(False)

        total_layout.addLayout(top_layout)
        total_layout.addLayout(run_layout)
        total_layout.addWidget(self.__result_list)
        total_layout.addWidget(self.__progress_bar)
        total_layout.addLayout(turtle_layout)
        total_layout.addWidget(self.__export_button)

        self.setLayout(total_layout)
        self.setWindowTitle("Serious Numbers")
        self.setWindowIcon(QtGui.QIcon(SUM_ICON)) 

        self.__count = 0

    def start_generate_series(self):
        self.__result_list.clear()
        self.__count = 0
        series_name = self.__series_picker.itemText(self.__series_picker.currentIndex())
        recursions = int(self.__recursion_spinner.value())
        offset = int(self.__offset_spinner.value())
        multiply = int(self.__multiply_spinner.value())

        self.__get_thread = Generate_Thread(series_name, recursions, offset, multiply)
        self.connect(self.__get_thread, QtCore.SIGNAL("add_number(int)"), self.add_number)
        self.connect(self.__get_thread, QtCore.SIGNAL("finished()"), self.stop_thread)
        self.__get_thread.start()

        self.__progress_bar.setMaximum(recursions)
        self.__progress_bar.setValue(0)
        self.__stop_button.setEnabled(True)
        self.__generate_button.setEnabled(False)
        self.__turtle_runner.setEnabled(False)
        self.__export_button.setEnabled(False)
        self.__stop_button.clicked.connect(self.__get_thread.terminate)

    def add_number(self, num):
        self.__count += 1
        self.__result_list.addItem("{}:{}".format(self.__count, num))
        self.__progress_bar.setValue(self.__progress_bar.value() + 1)

    def present_turtle(self):
        seq = self.get_results()

        pen_color = self.__color_picker.pen_color
        pr = pen_color.toRgb().red()
        pg = pen_color.toRgb().green()
        pb = pen_color.toRgb().blue()

        background_color = self.__color_picker.background_color
        br = background_color.toRgb().red()
        bg = background_color.toRgb().green()
        bb = background_color.toRgb().blue()

        if self.__series_picker.currentText() == FIBONACCI_STRING:
            fibonacci.draw_fibonacci(seq, (pr, pg, pb), (br, bg, bb))
        elif series == PADOVAN_STRING:
            padovan.draw_padovan(seq)

    def open_color_picker(self):
        self.__color_picker.open()

    def open_file_dialog(self):    
        filename, filter = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Select output file', dir='.', filter= FILE_FILTERS  )   
        if filename:
            seq = self.get_results()
            output.generate_output(filename,seq)

    def get_results(self):
        seq = []
        for x in range(self.__result_list.count()):
            split_string = self.__result_list.item(x).text().split(":")
            seq.append(int(split_string[1]))
        return seq           

    def stop_thread(self):
        self.__generate_button.setEnabled(True)
        self.__stop_button.setEnabled(False)
        self.__turtle_runner.setEnabled(True)
        self.__progress_bar.setValue(0)
        self.__export_button.setEnabled(True)


class Generate_Thread(QtCore.QThread):

    def __init__(self, series_name, this_recursions, this_offset, this_multiply):

        super(Generate_Thread, self).__init__()

        self.__name = series_name
        self.__recursions = this_recursions
        self.__offset = this_offset
        self.__multiply = this_multiply

    def run(self):
        if self.__name == FIBONACCI_STRING:
            for x in fibonacci.fib(self.__recursions, self.__offset, self.__multiply):
                self.emit(QtCore.SIGNAL('add_number(int)'), x)
        if self.__name == PADOVAN_STRING:
            for x in padovan.pad(self.__recursions, self.__multiply):
                self.emit(QtCore.SIGNAL('add_number(int)'), x)

    def __del__(self):
        self.wait()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Series_UI()
    ex.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
