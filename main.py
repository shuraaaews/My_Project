import json
import os
import sys

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication, QMainWindow

from MainWindow import Ui_TextEditor


class MainWindow(QMainWindow, Ui_TextEditor):
    def __init__(self, fileName=None, parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.setMinimumSize(600,400)
        self.showMaximized()
        self.setWindowIcon(QIcon("text_editor.png"))


        setting_ = open("setting.json", "r")
        json_file = json.loads(setting_.read())
        font_name = json_file["fonts"]["font-name"]
        font_size = int(json_file["fonts"]["font-size"])
        # StyleSheet = json_file["themes"]["logo-color"]
        theme_name = str(json_file["themes"]["style"])
        style_name = "Themes/" + theme_name + ".ini"

        style_file = open(style_name, "r")
        style_theme = str(style_file.read())
        style_file.close()
        theme_ = str(json_file["themes"]["theme"])
        setting_.close()

        self.setStyleSheet(style_theme)
        QApplication.setStyle(QStyleFactory.create(theme_))
        self.textEdit.setFont(QFont(font_name, font_size))
        self.highlighter = Highlighter(self.textEdit.document())

        if fileName is None:
            fileName = 'Welcome.txt'

        if not self.load(fileName):
            self.new_file()

        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("New File")
        self.newAction.triggered.connect(self.new_file)

        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Open File")
        self.openAction.triggered.connect(self.open_file)

        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.setStatusTip("Save File")
        self.saveAction.triggered.connect(self.save_file)

        self.saveAsAction.setShortcut("Ctrl+Alt+s")
        self.saveAsAction.setStatusTip("Save As")
        self.saveAsAction.triggered.connect(self.saveAs_file)

        self.printAction.setShortcut("Ctrl+P")
        self.printAction.setStatusTip("Print")
        self.printAction.triggered.connect(self.print_file)

        self.printPreview.setShortcut("Ctrl+Alt+P")
        self.printPreview.setStatusTip("Print Preview")
        self.printPreview.triggered.connect(self.print_Preview)

        # Edit
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.setStatusTip("Undo")
        self.undoAction.triggered.connect(self.textEdit.undo)

        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.setStatusTip("Redo")
        self.redoAction.triggered.connect(self.textEdit.redo)

        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.setStatusTip("Cut")
        self.cutAction.triggered.connect(self.textEdit.cut)

        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.setStatusTip("Copy")
        self.copyAction.triggered.connect(self.textEdit.copy)

        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.setStatusTip("Paste")
        self.pasteAction.triggered.connect(self.textEdit.paste)

        self.exitAction.setShortcut("Ctrl+E")
        self.exitAction.setStatusTip("Exit")
        self.exitAction.triggered.connect(self.exit_app)

        # BISSU action
        self.boldAction.setShortcut("Ctrl+B")
        self.boldAction.setStatusTip("Bold")
        self.boldAction.triggered.connect(self._bold)

        self.italicAction.setShortcut("Ctrl+I")
        self.italicAction.setStatusTip("Italic")
        self.italicAction.triggered.connect(self._italic)

        self.underlineAction.setShortcut("Ctrl+U")
        self.underlineAction.setStatusTip("Underline")
        self.underlineAction.triggered.connect(self._underline)

        self.strikeAction.setShortcut("Ctrl+Shift+S")
        self.strikeAction.setStatusTip("Strike Through.png")
        self.strikeAction.triggered.connect(self._strike)

        self.superScriptAction.setShortcut("Ctrl+Shift+U")
        self.superScriptAction.setStatusTip("Super Script")
        self.superScriptAction.triggered.connect(self._superScript)

        self.subscriptAction.setShortcut("Ctrl+Shift+L")
        self.subscriptAction.setStatusTip("Sub Script")
        self.subscriptAction.triggered.connect(self._subscript)

        self.alignLeft.triggered.connect(self._alignLeft)
        self.alignCenter.triggered.connect(self._alignCenter)
        self.alignRight.triggered.connect(self._alignRight)
        self.alignJustify.triggered.connect(self._alignJustify)

        # Format action
        self.fontAction.setShortcut("F3")
        self.fontAction.setStatusTip("Font")
        self.fontAction.triggered.connect(self.font_dialog)

        self.colorAction.setShortcut("Ctrl+Shift+O")
        self.colorAction.setStatusTip("Text Color")
        self.colorAction.triggered.connect(self.color_dialog)

        self.highlighterAction.setShortcut("Ctrl+H")
        self.highlighterAction.setStatusTip("Text Highlighter")
        self.highlighterAction.triggered.connect(self.texthighlighter)

        self.datetime.setShortcut("Ctrl+D")
        self.datetime.setStatusTip("Date and Time")
        self.datetime.triggered.connect(self.dateTime)

        self.aboutAction.setShortcut("Ctrl+M")
        self.aboutAction.setStatusTip("About Us")
        self.aboutAction.triggered.connect(self.about_dialog)

        self.pdfAction.setStatusTip("Export PDF")
        self.pdfAction.triggered.connect(self.exportPdf)

        self.findAction.setStatusTip("Find and words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(self.Find)

        self.show()



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
