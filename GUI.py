import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

# def window():
#     app = QApplication(sys.argv)
#     win = QMainWindow()

#     win.setGeometry(200,200, 300, 300)
#     win.setWindowTitle("StegoShark 2000")

#     win.show()
#     sys.exit(app.exec())

# window()
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('PyQt5 App')
window.setGeometry(100, 100, 280, 80)
window.move(60, 15)
helloMsg = QLabel('<h1>Hello World!</h1>', parent=window)
helloMsg.move(60, 15)
window.show()
sys.exit(app.exec_())