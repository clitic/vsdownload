import os
import sys
import subprocess
import webbrowser
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from .vsdownload_ui import Ui_MainWindow as vsdownload_ui_main_window
from . import utils


class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = vsdownload_ui_main_window()
        self.ui.setupUi(self)
        # connecting slots and signals
        self.save_callargs = utils.get_command_callargs("call_save")
        self.capture_callargs = utils.get_command_callargs("call_capture")
        self.make_ui_updates()
        self.make_connections()

    def update_placeholders_tooltips(self, option, ui_widget) -> None:
        exec(f"self.ui.{ui_widget}.setToolTip('{option.help}')")

        if "LineEdit" in ui_widget:
            if option.default == Ellipsis:
                exec(f"self.ui.{ui_widget}.setPlaceholderText('{option.help}')")
            elif option.default is not None:
                exec(f"self.ui.{ui_widget}.setPlaceholderText('{option.default}')")
            else:
                exec(f"self.ui.{ui_widget}.setPlaceholderText('{option.metavar}')")

        elif "SpinBox" in ui_widget and option.default is not None:
            exec(f"self.ui.{ui_widget}.setValue({option.default})")
        elif "CheckBox" in ui_widget:
            exec(f"self.ui.{ui_widget}.setChecked({option.default})")
    
    def make_ui_updates(self) -> None:
        self.setWindowTitle(f"vsdownload v{utils.get_version()}")
        self.ui.execute_command_text_browser.setPlaceholderText("updated command will be shown here")
        self.update_placeholders_tooltips(self.save_callargs["input"], "inputLineEdit")
        self.update_placeholders_tooltips(self.save_callargs["output"], "outputLineEdit_save")
        self.update_placeholders_tooltips(self.save_callargs["cleanup"], "cleanupCheckBox")
        self.update_placeholders_tooltips(self.save_callargs["max_quality"], "max_qualityCheckBox")
        self.update_placeholders_tooltips(self.save_callargs["verbose"], "verboseCheckBox")
        self.update_placeholders_tooltips(self.save_callargs["baseurl"], "baseurlLineEdit_save")
        self.update_placeholders_tooltips(self.save_callargs["threads"], "threadsSpinBox")
        self.update_placeholders_tooltips(self.save_callargs["chunk_size"], "chunk_sizeSpinBox")
        self.update_placeholders_tooltips(self.save_callargs["headers"], "headersLineEdit")
        self.update_placeholders_tooltips(self.save_callargs["decrypt"], "decryptCheckBox")
        self.update_placeholders_tooltips(self.save_callargs["key_iv"], "key_ivLineEdit")
        self.update_placeholders_tooltips(self.save_callargs["proxy_address"], "proxy_addressLineEdit")
        self.update_placeholders_tooltips(self.save_callargs["ffmpeg_path"], "ffmpeg_pathLineEdit")
        self.update_placeholders_tooltips(self.save_callargs["tempdir"], "tempdirLineEdit")
        self.update_placeholders_tooltips(self.save_callargs["retry_count"], "retry_countSpinBox")
        self.update_placeholders_tooltips(self.save_callargs["timeout"], "timeoutSpinBox")
        self.update_placeholders_tooltips(self.save_callargs["pre_select"], "pre_selectSpinBox")
        self.update_placeholders_tooltips(self.capture_callargs["url"], "urlLineEdit")
        self.update_placeholders_tooltips(self.capture_callargs["output"], "outputLineEdit_capture")
        self.update_placeholders_tooltips(self.capture_callargs["driver"], "driverLineEdit")
        self.update_placeholders_tooltips(self.capture_callargs["scan_ext"], "scan_extLineEdit")
        self.update_placeholders_tooltips(self.capture_callargs["baseurl"], "baseurlCheckBox_capture")

    def make_connections(self) -> None:
        # connecting menu bar items
        self.ui.action_report_a_bug.triggered.connect(lambda: webbrowser.open("https://github.com/360modder/vsdownload/issues", new=2))
        self.ui.action_about_vsdownload.triggered.connect(lambda: self.about_vsdownload())
        self.ui.action_about_qt.triggered.connect(lambda: QApplication.aboutQt())
        # connecting buttons
        self.ui.execute_btn.clicked.connect(self.launch_vsdownload)
        self.ui.save_page_input_btn.clicked.connect(
            lambda: self.ui.inputLineEdit.setText(QFileDialog.getOpenFileName(filter="Files (*.m3u8, *.json)")[0])
        )
        self.ui.save_page_output_btn.clicked.connect(
            lambda: self.ui.outputLineEdit_save.setText(QFileDialog.getSaveFileName(filter="Files (*.ts, *.*)")[0].rstrip(","))
        )
        self.ui.save_page_headers_btn.clicked.connect(
            lambda: self.ui.headersLineEdit.setText(QFileDialog.getOpenFileName(filter="Files (*.json)")[0])
        )
        self.ui.save_page_ffmpeg_path_btn.clicked.connect(
            lambda: self.ui.ffmpeg_pathLineEdit.setText(QFileDialog.getOpenFileName()[0])
        )
        self.ui.save_page_tempdir_btn.clicked.connect(
            lambda: self.ui.tempdirLineEdit.setText(os.path.join(QFileDialog.getExistingDirectory(), "temptsfiles").replace("\\", "/"))
        )
        self.ui.capture_page_driver_btn.clicked.connect(
            lambda: self.ui.driverLineEdit.setText(QFileDialog.getOpenFileName()[0])
        )
        self.ui.capture_page_output_btn.clicked.connect(
            lambda: self.ui.outputLineEdit_capture.setText(QFileDialog.getSaveFileName(filter="Files (*.json)")[0])
        )
        # connecting widget update and change states
        self.ui.inputLineEdit.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.outputLineEdit_save.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.cleanupCheckBox.stateChanged.connect(self.update_execute_command)
        self.ui.max_qualityCheckBox.stateChanged.connect(self.update_execute_command)
        self.ui.verboseCheckBox.stateChanged.connect(self.update_execute_command)
        self.ui.baseurlLineEdit_save.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.threadsSpinBox.valueChanged.connect(self.update_execute_command)
        self.ui.chunk_sizeSpinBox.valueChanged.connect(self.update_execute_command)
        self.ui.headersLineEdit.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.decryptCheckBox.stateChanged.connect(self.update_execute_command)
        self.ui.key_ivLineEdit.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.proxy_addressLineEdit.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.ffmpeg_pathLineEdit.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.tempdirLineEdit.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.retry_countSpinBox.valueChanged.connect(self.update_execute_command)
        self.ui.timeoutSpinBox.valueChanged.connect(self.update_execute_command)
        self.ui.pre_selectSpinBox.valueChanged.connect(self.update_execute_command)
        self.ui.urlLineEdit.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.driverLineEdit.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.outputLineEdit_capture.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.scan_extLineEdit.cursorPositionChanged.connect(self.update_execute_command)
        self.ui.baseurlCheckBox_capture.stateChanged.connect(self.update_execute_command)

    def update_execute_command(self) -> None:
        args = ["vsdownload"]
        sub_command = self.ui.base_tab_widget.tabText(self.ui.base_tab_widget.currentIndex())
        args.append(sub_command)

        if sub_command == "save":
            args.extend(self.generate_save_command_args())
        
        elif sub_command == "capture":
            args.extend(self.generate_capture_command_args())

        self.ui.execute_command_text_browser.setText(" ".join(args))
                
    def generate_save_command_args(self) -> list:
        args = []
        
        if self.ui.inputLineEdit.text() != "":
            args.append(f"\"{self.ui.inputLineEdit.text()}\"")

        if self.ui.outputLineEdit_save.text() != "":
            args.append("-o")
            args.append(f"\"{self.ui.outputLineEdit_save.text()}\"")

        if not self.ui.cleanupCheckBox.isChecked():
            args.append("--no-cleanup")

        if self.ui.max_qualityCheckBox.isChecked():
            args.append("-m")
                        
        if self.ui.verboseCheckBox.isChecked():
            args.append("-v")
            
        if self.ui.baseurlLineEdit_save.text() != "":
            args.append("-b")
            args.append(f"\"{self.ui.baseurlLineEdit_save.text()}\"")

        if self.ui.threadsSpinBox.value() != self.save_callargs["threads"].default:
            args.append("-t")
            args.append(str(self.ui.threadsSpinBox.value()))
        
        if self.ui.chunk_sizeSpinBox.value() != self.save_callargs["chunk_size"].default:
            args.append("--chunk-size")
            args.append(str(self.ui.chunk_sizeSpinBox.value()))

        if self.ui.headersLineEdit.text() != "":
            args.append("--headers")
            args.append(f"\"{self.ui.headersLineEdit.text()}\"")

        if not self.ui.verboseCheckBox.isChecked():
            args.append("--no-decrypt")
            
        if self.ui.key_ivLineEdit.text() != "":
            args.append("--key-iv")
            args.append(f"\"{self.ui.key_ivLineEdit.text()}\"")

        if self.ui.proxy_addressLineEdit.text() != "":
            args.append("--proxy-address")
            args.append(f"\"{self.ui.proxy_addressLineEdit.text()}\"")

        if self.ui.ffmpeg_pathLineEdit.text() != "":
            args.append("--ffmpeg-path")
            args.append(f"\"{self.ui.ffmpeg_pathLineEdit.text()}\"")

        if self.ui.tempdirLineEdit.text() != "":
            args.append("--tempdir")
            args.append(f"\"{self.ui.tempdirLineEdit.text()}\"")

        if self.ui.retry_countSpinBox.value() != self.save_callargs["retry_count"].default:
            args.append("--retry-count")
            args.append(str(self.ui.retry_countSpinBox.value()))

        if self.ui.timeoutSpinBox.value() != self.save_callargs["timeout"].default:
            args.append("--timeout")
            args.append(str(self.ui.timeoutSpinBox.value()))

        if self.ui.pre_selectSpinBox.value() != -1:
            args.append("--pre-select")
            args.append(str(self.ui.pre_selectSpinBox.value()))
        
        return args
    
    def generate_capture_command_args(self)  -> list:
        args = []

        if self.ui.urlLineEdit.text() != "":
            args.append(f"\"{self.ui.urlLineEdit.text()}\"")

        if self.ui.driverLineEdit.text() != "":
            args.append("--driver")
            args.append(f"\"{self.ui.driverLineEdit.text()}\"")

        if self.ui.outputLineEdit_capture.text() != "":
            args.append("-o")
            args.append(f"\"{self.ui.outputLineEdit_capture.text()}\"")

        if self.ui.scan_extLineEdit.text() != "":
            args.append("--scan-ext")
            args.append(self.ui.scan_extLineEdit.text())

        if self.ui.baseurlCheckBox_capture.isChecked():
            args.append("--baseurl")
        
        return args
                
    def check_save_command_args(self) -> bool:
        execute = False
        
        if self.ui.inputLineEdit.text() == "":
            self.argument_error("input", "no input supplied")

        elif self.ui.outputLineEdit_save.text() == "":
            self.argument_error("output", "no output file specified")

        else:
            execute = True
        
        return execute

    def check_capture_command_args(self) -> bool:
        execute = False
        
        if self.ui.urlLineEdit.text() == "":
            self.argument_error("url", "no url specified")

        elif self.ui.driverLineEdit.text() == "":
            self.argument_error("driver", "chromedriver path not specified")

        elif self.ui.outputLineEdit_capture.text() == "":
            self.argument_error("output", "no output json file specified")

        else:
            execute = True
        
        return execute
    
    def launch_vsdownload(self):
        execute = False
        sub_command = self.ui.base_tab_widget.tabText(self.ui.base_tab_widget.currentIndex())

        if sub_command == "save":
            execute = self.check_save_command_args()

        elif sub_command == "capture":
            execute = self.check_capture_command_args()

        if execute:
            if sys.platform.lower().startswith("win"):
                subprocess.run(self.ui.execute_command_text_browser.toPlainText(), creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                self.non_windows_platform_message()
                                
    def non_windows_platform_message(self) -> None:
        QApplication.clipboard().setText(self.ui.execute_command_text_browser.toPlainText())
        msg = QMessageBox()
        msg.setWindowTitle("vsdownload")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("copied to clipboard")
        msg.setInformativeText("cannot execute a subprocess on non windows platform")
        msg.exec()

    @staticmethod
    def argument_error(title, message) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("argument error")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.exec()

    @staticmethod
    def about_vsdownload():
        msg = QMessageBox()
        msg.setWindowTitle("about vsdownload")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(f"vsdownload v{utils.get_version()}")
        msg.setInformativeText("developed by 360modder")
        msg.setDetailedText("build with python & PyQt6")
        msg.exec()


def console_script():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    console_script() # python -m vsdownload.vsdownload_gui_wrapper vsdownload_gui_wrapper.py
