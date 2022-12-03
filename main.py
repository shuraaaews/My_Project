
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtPrintSupport
from MainWindowUi import Ui_MainWindow
from PyQt5.QtWidgets import QDockWidget, QListWidget

from PyQt5.QtCore import QDate, QFile, Qt, QTextStream
from PyQt5.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,
        QTextCursor, QTextTableFormat)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QDockWidget,
        QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit)


#import resources 


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        '''
        self.createDockWindows()        
        # BLUR EXPERIMENT
        # self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        # hWnd = self.winId()
        # blur(hWnd)
        # self.setWindowOpacity(0.98)

    def createDockWindows(self):
        dock = QDockWidget("Customers", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.customerList = QListWidget(dock)
        self.customerList.addItems((
            "John Doe, Harmony Enterprises, 12 Lakeside, Ambleton",
            "Jane Doe, Memorabilia, 23 Watersedge, Beaton",
            "Tammy Shea, Tiblanka, 38 Sea Views, Carlton",
            "Tim Sheen, Caraba Gifts, 48 Ocean Way, Deal",
            "Sol Harvey, Chicos Coffee, 53 New Springs, Eccleston",
            "Sally Hobart, Tiroli Tea, 67 Long River, Fedula"))
        dock.setWidget(self.customerList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
 #       self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Paragraphs", self)
        self.paragraphsList = QListWidget(dock)
        self.paragraphsList.addItems((
            "Thank you for your payment which we have received today.",
            "Your order has been dispatched and should be with you within "
                "28 days.",
            "We have dispatched those items that were in stock. The rest of "
                "your order will be dispatched once all the remaining items "
                "have arrived at our warehouse. No additional shipping "
                "charges will be made.",
            "You made a small overpayment (less than $5) which we will keep "
                "on account for you, or return at your request.",
            "You made a small underpayment (less than $1), but we have sent "
                "your order anyway. We'll add this underpayment to your next "
                "bill.",
            "Unfortunately you did not send enough money. Please remit an "
                "additional $. Your order will be dispatched as soon as the "
                "complete amount has been received.",
            "You made an overpayment (more than $5). Do you wish to buy more "
                "items, or should we return the excess to you?"))
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
  #      self.viewMenu.addAction(dock.toggleViewAction())

     #   self.customerList.currentTextChanged.connect(self.insertCustomer)
#        self.paragraphsList.currentTextChanged.connect(self.addParagraph)




        '''

        '''
        self.filename = ""
        self.changesSaved = False
        self.current_editor = self.create_editor()
        self.current_editor.setFocus()
        self.text_editors = []

        # self.setContentsMargins(qtc.QMargins())

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready") 

        self.tabs = qtw.QTabWidget(self)
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True) # let's you double click tab bar to create new tabs
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.tabCloseRequested.connect(self.remove_editor)
        self.tabs.currentChanged.connect(self.change_text_editor)
        self.tabs.tabBar().setMovable(True)
 #       self.setStyleSheet(self.myStyleSheet())
        self.setCentralWidget(self.tabs)

        self.new_tab()
        self.closeTab()
 #       self._createActions()
 #       self._createMenuBar()
 #       self._connectActions()
 #       self._createToolBars()
    
    

        '''

    def create_editor(self):
        current_editor = qtw.QTextEdit()
        # Set the tab stop width to around 33 pixels which is
        # about 8 spaces
        current_editor.setTabStopWidth(33)
        return current_editor

    def change_text_editor(self, index):
        if index < len(self.text_editors):
            self.current_editor = self.text_editors[index]

    def remove_editor(self, index):
        if self.tabs.count() < 2:
            return
        
        self.tabs.removeTab(index)
        if index < len(self.text_editors):
            del self.text_editors[index]

    def closeTab(self):
        close_tab = qtw.QShortcut(qtg.QKeySequence("Ctrl+W"), self)
        close_tab.activated.connect(lambda:self.remove_editor(self.tabs.currentIndex()))
    
    def tab_open_doubleclick(self, index):
        if index == -1:
            self.new_tab()

    def new_tab(self, checked = False, title = "Untitled.txt"):
        self.current_editor = self.create_editor() # create a QTextEdit
        self.text_editors.append(self.current_editor) # add current editor id to the array list 
        self.tabs.addTab(self.current_editor, title)
        self.tabs.setCurrentWidget(self.current_editor) # set the currently tab selected as current widget

    def open_document(self):
        options = qtw.QFileDialog.Options()
        # Get filename and show only .notes files
        #PYQT5 Returns a tuple in PyQt5, we only need the following filenames
        self.filename, _ = qtw.QFileDialog.getOpenFileName(
            self, 'Open File',".",
            "(*.notes);;Text Files (*.txt);;Python Files (*.py)",
            options=options
        )
        if self.filename:
            with open(self.filename,"rt") as file:
                content = file.read()
                self.current_editor = self.create_editor() 
                currentIndex = self.tabs.addTab(self.current_editor, str(self.filename))   # use that widget as the new tab
                self.current_editor.setText(content) # set the contents of the file as the text
                self.tabs.setCurrentIndex(currentIndex) # make current opened tab be on focus

    def save_document (self):
        if not self.current_editor.document().isModified():
            self.statusBar().showMessage("There are no texts to be saved!")
        else:
            # Only open dialog if there is no filename yet
            #PYQT5 Returns a tuple in PyQt5, we only need the filename
            options = qtw.QFileDialog.Options()
            file_filter = 'Notes_ file (*.notes);; Text file (*.txt);; Python file (*.py)'
            if not self.filename:
                self.filename = qtw.QFileDialog.getSaveFileName(self,caption='Save File',directory=".",filter=file_filter,initialFilter='Notes Files (*.notes)')[0] # zero index is required, otherwise it would throw an error if no selection was made
            
            if self.filename:

                # We just store the contents of the text file along with the
                # format in html, which Qt does in a very nice way for us
                with open(self.filename,"wt") as file:
                    file.write(self.current_editor.toHtml())
                    print(self.tabs.currentIndex())
                    print(str(self.filename))
                    self.tabs.setTabText(self.tabs.currentIndex(), str(self.filename)) # renames the current tabs with the filename
                    self.statusBar().showMessage(f"Saved to {self.filename}")
                    
                self.changesSaved = True

    def insert_image(self):
        # Get image file name
        #PYQT5 Returns a tuple in PyQt5
        filename = qtw.QFileDialog.getOpenFileName(self, 'Insert image',".","Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

        if filename:
            # Create image object
            image = qtg.QImage(filename)
            # Error if unloadable
            
            if image.isNull():
                popup = qtw.QMessageBox(qtw.QMessageBox.Critical,
                                          "Image load error",
                                          "Could not load image file!",
                                          qtw.QMessageBox.Ok,
                                          self)
                popup.show()
            else:
                cursor = self.current_editor.textCursor()
                cursor.insertImage(image,filename)

    def indent(self):

        # Grab the cursor
        cursor = self.current_editor.textCursor()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()
            # Move to the selection's end
            cursor.setPosition(cursor.anchor())
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
            direction = qtg.QTextCursor.Up if diff > 0 else qtg.QTextCursor.Down
            # Iterate over lines (diff absolute value)
            
            for n in range(abs(diff) + 1):
                # Move to start of each line
                cursor.movePosition(qtg.QTextCursor.StartOfLine)
                # Insert tabbing
                cursor.insertText("\t")
                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:
            cursor.insertText("\t")

    def handleDedent(self,cursor):

        cursor.movePosition(qtg.QTextCursor.StartOfLine)
        # Grab the current line
        line = cursor.block().text()
        # If the line starts with a tab character, delete it
        if line.startswith("\t"):
            # Delete next character
            cursor.deleteChar()
        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:
                if char != " ":
                    break
                cursor.deleteChar()

    def unindent(self):

        cursor = self.current_editor.textCursor()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()
            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
            direction = qtg.QTextCursor.Up if diff > 0 else qtg.QTextCursor.Down
            # Iterate over lines
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)
                # Move up
                cursor.movePosition(direction)
        else:
            self.handleDedent(cursor)

    def preview(self):

        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.current_editor.print_(p))
        preview.exec_()

    def print_handler(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == qtw.QDialog.Accepted:
            self.current_editor.document().print_(dialog.printer())

    def font_dialog(self):
        font, ok =qtw.QFontDialog.getFont()
        if ok:
            self.current_editor.setFont(font)

    # toolbar update display color depending on color selected
    def textColor(self):
        col = qtw.QColorDialog.getColor(self.current_editor.textColor(), self)
        if not col.isValid():
            return
        fmt = qtg.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)
    
    def colorChanged(self, color):
        pix = qtg.QPixmap(16, 16)
        pix.fill(color)
        self.text_color_action.setIcon(qtg.QIcon(pix))

    def textSize(self, pointSize):
        pointSize = int(self.comboSize.currentText())
        if pointSize > 0:
            fmt = qtg.QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)
            
    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.current_editor.textCursor()
        if not cursor.hasSelection(): 
            cursor.select(qtg.QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.current_editor.mergeCurrentCharFormat(format)

    @qtc.pyqtSlot(str)
    def text_family(self, f):
        fmt = qtg.QTextCharFormat()
        fmt.setFontFamilies({f})
        self.mergeFormatOnWordOrSelection(fmt)
    
    def bold_text(self): 
        fmt = qtg.QTextCharFormat()
        weight = qtg.QFont.DemiBold if self.bold_text_action.isChecked() else qtg.QFont.Normal
        fmt.setFontWeight(weight)
        self.mergeFormatOnWordOrSelection(fmt)
    
    def italic_text(self):
        fmt = qtg.QTextCharFormat()
        fmt.setFontItalic(self.italic_text_action.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def underlined_text(self):
        fmt = qtg.QTextCharFormat()
        fmt.setFontUnderline(self.underline_text_action.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def strike_out_text(self):

        # Grab the text's format
        fmt = qtg.QTextCharFormat()
        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(self.strike_out_text_action.isChecked())
        # And set the next char format
        self.mergeFormatOnWordOrSelection(fmt)

    def superScript(self):

        # Grab the current format
        fmt = self.current_editor.currentCharFormat()
        # And get the vertical alignment property
        align = fmt.verticalAlignment()
        # Toggle the state
        if align == qtg.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(qtg.QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(qtg.QTextCharFormat.AlignNormal)
        # Set the new format
        self.current_editor.setCurrentCharFormat(fmt)

    def subScript(self):
        # Grab the current format
        fmt = self.current_editor.currentCharFormat()
        # And get the vertical alignment property
        align = fmt.verticalAlignment()
        # Toggle the state
        if align == qtg.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(qtg.QTextCharFormat.AlignSubScript)
        else:
            fmt.setVerticalAlignment(qtg.QTextCharFormat.AlignNormal)
        # Set the new format
        self.current_editor.setCurrentCharFormat(fmt)

    def bulletList(self):

        cursor = self.current_editor.textCursor()
        # Insert bulleted list
        cursor.insertList(qtg.QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.current_editor.textCursor()
        # Insert list with numbers
        cursor.insertList(qtg.QTextListFormat.ListDecimal)
    

   

    def export_as_odt(self):
            if not self.current_editor.document().isModified():
                self.statusBar().showMessage("There are no texts to export!")
                # Append extension if not there yet
            else:
                filename, _ = qtw.QFileDialog.getSaveFileName(self, "Export as OpenOffice Document", self.strippedName(self.filename).replace(".html",""),
                    "OpenOffice document (*.odt)")
                if not filename:
                    return False
                lfn = filename.lower()
                if not lfn.endswith(('.odt')):
                    filename += '.odt'
                return self.file_export_odt(filename)
    
    def file_export_odt(self, filename): 
        writer = qtg.QTextDocumentWriter(filename)
        success = writer.write(self.current_editor.document())
        if success:
            self.statusBar().showMessage("saved file '" + filename + "'")
            self.tabs.setTabText(self.tabs.currentIndex(), str(filename)) # renames the current tabs with the filename
            self.changesSaved = True
            self.statusBar().showMessage(f"Exported {filename}")
        return success

    def strippedName(self, fullFileName): 
        return qtc.QFileInfo(fullFileName).fileName()

    def export_as_pdf(self): 
        if not self.current_editor.document().isModified():
            self.statusBar().showMessage("There are no texts to export!")
        else:
            file_dialog = qtw.QFileDialog(self, "Export PDF")
            file_dialog.setAcceptMode(qtw.QFileDialog.AcceptSave)
            file_dialog.setMimeTypeFilters(["application/pdf"])
            file_dialog.setDefaultSuffix("pdf")
            if file_dialog.exec() != qtw.QDialog.Accepted:
                return
            pdf_file_name = file_dialog.selectedFiles()[0]
            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
            printer.setOutputFileName(pdf_file_name)
            self.current_editor.document().print_(printer)
            native_fn = qtc.QDir.toNativeSeparators(pdf_file_name)
            self.changesSaved = True
            self.statusBar().showMessage(f'Exported "{native_fn}"')
            self.tabs.setTabText(self.tabs.currentIndex(), str(native_fn)) # renames the current tabs with the filename

    def select_all_document(self): 
        self.current_editor.selectAll()

    def cut_document(self): 
        self.current_editor.cut()

    def copy_document(self): 
        self.current_editor.copy()

    def paste_document(self): 
        self.current_editor.paste()
    
    def undo_document(self): 
        self.current_editor.undo()

    def redo_document(self): 
        self.current_editor.redo()
    
    def color_dialog(self):
        color = qtw.QColorDialog.getColor(self.current_editor.textColor(), self)
        if not color.isValid():
            return
        self.current_editor.setTextColor(color)

    def align_left(self):
        self.current_editor.setAlignment(qtc.Qt.AlignLeft)
        self.current_editor.setFocus()
    
    def align_right(self):
        self.current_editor.setAlignment(qtc.Qt.AlignRight)
        self.current_editor.setFocus()

    def align_center(self):
        self.current_editor.setAlignment(qtc.Qt.AlignHCenter)
        self.current_editor.setFocus()

    def align_justify(self):
        self.current_editor.setAlignment(qtc.Qt.AlignLeft)
        self.current_editor.setFocus()
    
    def fullscreen(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else :
            self.showMaximized()
    
    # def increment_font_size(self):
    #     self.counterFontSize +=1
    #     font = self.current_editor.font()                         
    #     font.setPointSize(int(self.counterFontSize))       
    #     self.current_editor.setFont(font)                         

    # def decrement_font_size(self):
    #     self.counterFontSize -=1
    #     font = self.current_editor.font()                         
    #     font.setPointSize(int(self.counterFontSize))       
    #     self.current_editor.setFont(font)                          

    # def set_default_font_size(self):
    #     self.current_editor.selectAll
    #     font = self.current_editor.font()                         
    #     font.setPointSize(int(self.defaultFontSize))  
    #     self.current_editor.setFont(font)                          
    #     self.counterFontSize = self.defaultFontSize
    #     self.comboSize.setCurrentText(str(self.counterFontSize))

    def toggle_menu(self, state):
            if state:
                self.statusbar.show()
            else:
                self.statusbar.hide()

    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

    def maybe_save(self):
        if not self.current_editor.document().isModified():
            return True
        if  self.changesSaved == True:
            qtw.QApplication.quit() 
        else:    
            reply = qtw.QMessageBox.warning(self, qtc.QCoreApplication.applicationName(),
                                    "The document has been modified.\n"
                                    "Do you want to save your changes?",
                                    qtw.QMessageBox.Save | qtw.QMessageBox.Discard
                                    | qtw.QMessageBox.Cancel)
            if reply == qtw.QMessageBox.Save:
                return self.save_document()
            if reply == qtw.QMessageBox.Cancel:
                return False
            return True
    
    '''
    
    def myStyleSheet(self): # css guide: https://doc.qt.io/qt-6/stylesheet-reference.html
        return """
            QMainWindow{ background: #1c2028; border-style: none;}
            QStatusBar { color: #BFBDB6; background: #1c2028; }
            QMenuBar::item:pressed {  color: #BFBDB6; background: #1c2028; }
            QMenuBar::item { color: #BFBDB6; background: #1c2028; }
         
            QTextEdit QMenu::item {color: #ffb454; font-weight: normal}
            QTextEdit
            {
                border: none;
                font: "Consolas";
                color: #BFBDB6;
                background: #161a21;
                selection-background-color: #ffb454;
                selection-color: #000000;
            }

            QMenuBar
            {
                color: #BFBDB6;
                background: #1c2028;
                border: none;
                border-style: none;
            }

            QMenuBar::item:selected 
            { 
                color: #BFBDB6;
                background: #1c2028; 
            } 

            QToolBar
            {
                background: #1c2028;
                border: none;
                border-style: none;
            }
            
            QTabBar::tab { border: none; }
            QTabBar::tab:!selected:hover { background: #1c2028; }
            QTabBar::tab:top:!selected { background: #1c2028; }
            
            QTabBar::close-button { image: url(:/images/close_default.png); margin: 2px}
            QTabBar::close-button:hover { image: url(:/images/close_active.png);  margin: 2px}
            
            QTabBar::tab:selected {
                color: #e1af4b;
                background: #161a21;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:!selected {
                background: silver;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:top, QTabBar::tab:bottom {
                min-width: 8ex;
                margin-right: -1px;
                padding: 5px 10px 5px 10px;
            }
            
        """

        '''
if __name__ == "__main__":
    app = qtw.QApplication(sys.argv) 
    app.setStyle(qtw.QStyleFactory.create("Fusion")) # Oxygen, Windows, Fusion etc.
    # Now use a palette to switch to dark colors:
    '''
    palette = qtg.QPalette()
    palette.setColor(qtg.QPalette.Window, qtg.QColor("#161a21"))
    palette.setColor(qtg.QPalette.WindowText, qtg.QColor("#BFBDB6"))
    palette.setColor(qtg.QPalette.AlternateBase, qtg.QColor("#161a21"))
    palette.setColor(qtg.QPalette.ToolTipBase, qtc.Qt.black)
    palette.setColor(qtg.QPalette.ToolTipText, qtg.QColor("#BFBDB6"))
    palette.setColor(qtg.QPalette.Text, qtg.QColor("#BFBDB6"))
    palette.setColor(qtg.QPalette.Button, qtg.QColor("#161a21")) # button color
    palette.setColor(qtg.QPalette.Base, qtg.QColor("#161a21")) # textedit
    palette.setColor(qtg.QPalette.ButtonText, qtg.QColor("#BFBDB6"))
    palette.setColor(qtg.QPalette.BrightText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Link, qtg.QColor("#0086b6"))
    palette.setColor(qtg.QPalette.Highlight, qtg.QColor("#0086b6"))
    palette.setColor(qtg.QPalette.HighlightedText, qtc.Qt.black)
    app.setPalette(palette)
    '''
    main = MainWindow()
    main.resize(710,590)
    main.setMinimumSize(700,550)
    main.setWindowTitle(" ") 
    QPixmap = qtg.QPixmap( 32, 32 )
    QPixmap.fill( qtc.Qt.transparent ) 
    main.setWindowIcon(qtg.QIcon(QPixmap))
    # main.setWindowIcon(qtg.QIcon(":/images/notepad.png"))
    main.show()
    sys.exit(app.exec_())
