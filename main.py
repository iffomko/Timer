from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys


class MainWindow(QMainWindow):
    def choice_time_display(self):
        layout = QGridLayout()

        time_header = QLabel()

        time_header_font = time_header.font()
        time_header_font.setPixelSize(22)
        time_header_font.setFamily('Montserrat sans-serif')
        time_header.setFont(time_header_font)

        time_header.setText('Выбери время:')
        time_header.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(time_header, 0, 0)

        time_padding = QWidget()
        time_padding.setFixedSize(QSize(10, 100))

        layout.addWidget(time_padding)

        self.time = QTimeEdit()
        self.time.setDisplayFormat('hh:mm:ss')
        self.time.setFixedSize(QSize(int(self.WINDOW_WIDTH / 2), 35))
        self.time.setAlignment(Qt.AlignmentFlag(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter))

        layout.addWidget(self.time, 1, 0)
        layout.setAlignment(Qt.AlignmentFlag(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter))

        self.start_button = QPushButton()
        self.start_button.setText("Начать")
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.on_start_button)

        padding_top_button = QWidget()
        padding_top_button.setFixedSize(50, 50)

        layout.addWidget(padding_top_button, 2, 0)
        layout.addWidget(self.start_button, 3, 0)

        return layout

    def timer_display(self):
        layout = QGridLayout()

        self.pause_button = QPushButton()
        self.stop_button = QPushButton()

        self.pause_button.setText("Пауза")
        self.pause_button.setCheckable(True)
        self.pause_button.clicked.connect(self.on_pause_button)

        self.pause_button.setFixedSize(QSize(int(self.WINDOW_WIDTH / 2) - 10, 25))

        self.stop_button.setText("Стоп")
        self.stop_button.setFixedSize(QSize(int(self.WINDOW_WIDTH / 2) - 10, 25))

        self.stop_button.setCheckable(True)
        self.stop_button.clicked.connect(self.on_stop_button)

        self.time.setFixedSize(self.WINDOW_WIDTH - 15, 35)

        layout.addWidget(self.time, 0, 0)
        layout.addWidget(self.pause_button, 2, 0)
        layout.addWidget(self.stop_button, 2, 1)

        layout.setAlignment(Qt.AlignmentFlag(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop))

        return layout

    def timer_event(self):
        self.time.setReadOnly(False)
        self.time.setTime(self.time.time().addSecs(-1))
        self.time.setReadOnly(True)

        if self.time.text() == '00:00:00':
            self.timer.stop()

    def on_start_button(self):
        self.time.setReadOnly(True)

        if self.time.text() != '00:00:00':
            self.timer = QTimer()
            self.timer.timeout.connect(self.timer_event)
            self.timer.start(1000)

        widget = QWidget()
        widget.setLayout(self.timer_display())

        self.setCentralWidget(widget)
        self.start_button.setCheckable(False)
        self.setFixedSize(QSize(self.WINDOW_WIDTH, int(self.WINDOW_HEIGHT * 0.35)))

    def on_stop_button(self):
        if self.timer is not None:
            self.timer.stop()
            self.timer = None

        widget = QWidget()
        widget.setLayout(self.choice_time_display())

        self.setCentralWidget(widget)
        self.stop_button.setCheckable(False)
        self.setFixedSize(QSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    def toggle_pause(self):
        if self.pause:
            self.pause = False
            return

        self.pause = True

    def on_pause_button(self):
        self.toggle_pause()

        if self.pause:
            self.timer.stop()
            self.pause_button.setText('Возобновить')
            self.pause_button.setCheckable(False)
            return

        self.timer.start(1000)
        self.pause_button.setText('Пауза')
        self.pause_button.setCheckable(False)

    def __init__(self):
        super().__init__()

        self.pause = False
        self.timer = None
        self.time = None
        self.WINDOW_WIDTH = 350
        self.WINDOW_HEIGHT = 300
        self.stop_button = None
        self.pause_button = None
        self.start_button = None

        self.setWindowTitle('Таймер')
        self.setFixedSize(QSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        layout = self.choice_time_display()

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


def app(argv: list):
    application = QApplication(argv)

    window = MainWindow()
    window.show()

    application.exec()


if __name__ == '__main__':
    app(sys.argv)
