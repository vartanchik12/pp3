import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *

from createann import create_annotation
from csvann import create_dataset2, create_annotation2
from newdataset import create_dataset3, create_annotation3
from iterator import Iterator


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initIterators()
        self.createAct()
        self.createMenuBar()
        self.createToolBar()
        self.dataset2_path = ''
        self.dataset3_path = ''
        self.annotation1_path = ''
        self.annotation2_path = ''
        self.annotation3_path = ''

    def initUI(self):
        self.center()
        self.setWindowTitle('Roses and tulips')
        self.setWindowIcon(QIcon('img/main.png'))
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        rose_btn = QPushButton('Next rose', self)
        tulip_btn = QPushButton('Next tulip', self)

        pixmap = QPixmap('img/rosmain.jpg')
        self.lbl = QLabel(self)
        self.lbl.setPixmap(pixmap)
        self.lbl.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()
        hbox.addSpacing(1)
        hbox.addWidget(rose_btn)
        hbox.addWidget(tulip_btn)

        vbox = QVBoxLayout()
        vbox.addSpacing(1)
        vbox.addWidget(self.lbl)
        vbox.addLayout(hbox)

        self.centralWidget.setLayout(vbox)

        rose_btn.clicked.connect(self.nextRose)
        tulip_btn.clicked.connect(self.nextTulip)

        self.folderpath = ' '

        self.showMaximized()

    def initIterators(self):
        self.roses = Iterator('rose', 'dataset')
        self.tulips = Iterator('tulip', 'dataset')

    def nextRose(self):
        """
            данная функция получает следующее изображения и размещает на главном окне
            parameters

            self
            returns

            none
        """
        lbl_size = self.lbl.size()
        next_image = next(self.roses)
        if next_image != None:
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        else:
            self.initIterators()
            self.nextRose()

    def nextTulip(self):
        lbl_size = self.lbl.size()
        next_image = next(self.tulips)
        if next_image != None:
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        else:
            self.initIterators()
            self.nextTulip()


    def center(self):
        widget_rect = self.frameGeometry()
        pc_rect = QDesktopWidget().availableGeometry().center()
        widget_rect.moveCenter(pc_rect)
        self.move(widget_rect.center())

    def createMenuBar(self):
        menuBar = self.menuBar()

        self.fileMenu = menuBar.addMenu('&File')
        self.fileMenu.addAction(self.exitAction)
        self.fileMenu.addAction(self.changeAction)

        self.annotMenu = menuBar.addMenu('&Annotation')
        self.annotMenu.addAction(self.createAnnotAction)

        self.dataMenu = menuBar.addMenu('&Dataset')
        self.dataMenu.addAction(self.createData2Action)

    def createToolBar(self):
        fileToolBar = self.addToolBar('File')
        fileToolBar.addAction(self.exitAction)

        annotToolBar = self.addToolBar('Annotation')
        annotToolBar.addAction(self.createAnnotAction)

    def createAct(self):
        self.exitAction = QAction(QIcon('img/exit.png'), '&Exit')
        self.exitAction.triggered.connect(qApp.quit)

        self.changeAction = QAction(QIcon('img/change.png'), '&Change dataset')
        self.changeAction.triggered.connect(self.changeDataset)

        self.createAnnotAction = QAction(
            QIcon('img/csv.png'), '&Create annotation for current dataset')
        self.createAnnotAction.triggered.connect(self.createAnnotation)

        self.createData2Action = QAction(
            QIcon('img/new_dataset.png'), '&Create dataset2')
        self.createData2Action.triggered.connect(self.createDataset2)

        self.createData3Action = QAction(
            QIcon('img/new_dataset.png'), '&Create dataset3')
        self.createData3Action.triggered.connect(self.createDataset3)

    def createAnnotation(self):
        if 'dataset2' in str(self.folderpath):
            self.annotation2_path = QFileDialog.getExistingDirectory(
                self, 'Select folder annotation of 2 dataset')
            create_annotation2(self.dataset2_path, self.annotation2_path)
            QMessageBox.information(self, 'Файл аннотации успешно создан', f'Файл аннотации для 2 датасета успешно создан в папке {self.annotation2_path}')

        elif 'dataset3' in str(self.folderpath):
            self.annotation3_path = QFileDialog.getExistingDirectory(
                self, 'Select folder annotation of 3 dataset')
            create_annotation3(self.dataset2_path, self.dataset3_path, self.annotation3_path)
            QMessageBox.information(self, 'Файл аннотации успешно создан',
                                    f'Файл аннотации для 3 датасета успешно создан в папке {self.annotation3_path}')

        elif 'dataset' in str(self.folderpath):
            self.annotation1_path = QFileDialog.getExistingDirectory(self, 'Select folder annotation of 1 dataset')
            create_annotation(self.annotation1_path)
            QMessageBox.information(self, 'Файл аннотации успешно создан',
                                    f'Файл аннотации для 1 датасета успешно создан в папке {self.annotation1_path}')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберите папку с исходным датасетом')
    def createDataset2(self):
        self.dataset2_path = QFileDialog.getExistingDirectory(
            self, 'Select folder for second dataset')
        create_dataset2(self.dataset2_path)
        QMessageBox.information(self, 'Датасет создан', f'Датасет 2 успешно создан в папке {self.dataset2_path}')
        self.dataMenu.addAction(self.createData3Action)

    def createDataset3(self):
        self.dataset3_path = QFileDialog.getExistingDirectory(
        self, 'Select folder for third dataset')
        create_dataset3(self.dataset2_path, self.dataset3_path)
        QMessageBox.information(self, 'Датасет создан', f'Датасет 3 успешно создан в папке {self.dataset3_path}')


    def changeDataset(self):
        reply = QMessageBox.question(self, 'Warning', f'Are you sure you want to change current dataset?\nCurrent dataset: {str(self.folderpath)}',
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.folderpath = QFileDialog.getExistingDirectory(
                self, 'Select Folder')
            QMessageBox.information(self, 'Изменение папки текущего датасета',
                                    f'Текущий датасет изменен на датасет с расположением {self.folderpath}')

        else:
            pass

    def closeEvent(self, event: QEvent):
        reply = QMessageBox.question(self, 'Warning', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
