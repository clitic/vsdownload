# Form implementation generated from reading ui file 'vsdownload/vsdownload.ui'
#
# Created by: PyQt6 UI code generator 6.0.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 550)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.base_vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.base_vertical_layout.setObjectName("base_vertical_layout")
        self.base_tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.base_tab_widget.setObjectName("base_tab_widget")
        self.save_page_base_stacked_widget = QtWidgets.QWidget()
        self.save_page_base_stacked_widget.setObjectName("save_page_base_stacked_widget")
        self.save_page_base_vertical_layout = QtWidgets.QVBoxLayout(self.save_page_base_stacked_widget)
        self.save_page_base_vertical_layout.setObjectName("save_page_base_vertical_layout")
        self.save_page_scroll_area = QtWidgets.QScrollArea(self.save_page_base_stacked_widget)
        self.save_page_scroll_area.setWidgetResizable(True)
        self.save_page_scroll_area.setObjectName("save_page_scroll_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 389, 460))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.save_page_basic_grid_layout = QtWidgets.QGridLayout()
        self.save_page_basic_grid_layout.setObjectName("save_page_basic_grid_layout")
        self.save_page_output_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.save_page_output_btn.setObjectName("save_page_output_btn")
        self.save_page_basic_grid_layout.addWidget(self.save_page_output_btn, 1, 2, 1, 1)
        self.save_page_input_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.save_page_input_btn.setObjectName("save_page_input_btn")
        self.save_page_basic_grid_layout.addWidget(self.save_page_input_btn, 0, 2, 1, 1)
        self.threadsSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.threadsSpinBox.setMinimum(1)
        self.threadsSpinBox.setMaximum(16)
        self.threadsSpinBox.setObjectName("threadsSpinBox")
        self.save_page_basic_grid_layout.addWidget(self.threadsSpinBox, 5, 1, 1, 1)
        self.outputLabel_save = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.outputLabel_save.setObjectName("outputLabel_save")
        self.save_page_basic_grid_layout.addWidget(self.outputLabel_save, 1, 0, 1, 1)
        self.inputLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.inputLabel.setObjectName("inputLabel")
        self.save_page_basic_grid_layout.addWidget(self.inputLabel, 0, 0, 1, 1)
        self.threadsLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.threadsLabel.setObjectName("threadsLabel")
        self.save_page_basic_grid_layout.addWidget(self.threadsLabel, 5, 0, 1, 1)
        self.inputLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.inputLineEdit.setObjectName("inputLineEdit")
        self.save_page_basic_grid_layout.addWidget(self.inputLineEdit, 0, 1, 1, 1)
        self.outputLineEdit_save = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.outputLineEdit_save.setObjectName("outputLineEdit_save")
        self.save_page_basic_grid_layout.addWidget(self.outputLineEdit_save, 1, 1, 1, 1)
        self.cleanupCheckBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cleanupCheckBox.setObjectName("cleanupCheckBox")
        self.save_page_basic_grid_layout.addWidget(self.cleanupCheckBox, 2, 1, 1, 1)
        self.cleanupLabel_save = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.cleanupLabel_save.setObjectName("cleanupLabel_save")
        self.save_page_basic_grid_layout.addWidget(self.cleanupLabel_save, 2, 0, 1, 1)
        self.chunk_sizeLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.chunk_sizeLabel.setObjectName("chunk_sizeLabel")
        self.save_page_basic_grid_layout.addWidget(self.chunk_sizeLabel, 6, 0, 1, 1)
        self.headersLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.headersLabel.setObjectName("headersLabel")
        self.save_page_basic_grid_layout.addWidget(self.headersLabel, 7, 0, 1, 1)
        self.key_ivLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.key_ivLabel.setObjectName("key_ivLabel")
        self.save_page_basic_grid_layout.addWidget(self.key_ivLabel, 8, 0, 1, 1)
        self.proxy_addressLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.proxy_addressLabel.setObjectName("proxy_addressLabel")
        self.save_page_basic_grid_layout.addWidget(self.proxy_addressLabel, 9, 0, 1, 1)
        self.chunk_sizeSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.chunk_sizeSpinBox.setMinimum(1024)
        self.chunk_sizeSpinBox.setMaximum(16384)
        self.chunk_sizeSpinBox.setSingleStep(1024)
        self.chunk_sizeSpinBox.setObjectName("chunk_sizeSpinBox")
        self.save_page_basic_grid_layout.addWidget(self.chunk_sizeSpinBox, 6, 1, 1, 1)
        self.headersLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.headersLineEdit.setObjectName("headersLineEdit")
        self.save_page_basic_grid_layout.addWidget(self.headersLineEdit, 7, 1, 1, 1)
        self.key_ivLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.key_ivLineEdit.setObjectName("key_ivLineEdit")
        self.save_page_basic_grid_layout.addWidget(self.key_ivLineEdit, 8, 1, 1, 1)
        self.ffmpeg_pathLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ffmpeg_pathLabel.setObjectName("ffmpeg_pathLabel")
        self.save_page_basic_grid_layout.addWidget(self.ffmpeg_pathLabel, 10, 0, 1, 1)
        self.tempdirLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.tempdirLabel.setObjectName("tempdirLabel")
        self.save_page_basic_grid_layout.addWidget(self.tempdirLabel, 11, 0, 1, 1)
        self.retry_countLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.retry_countLabel.setObjectName("retry_countLabel")
        self.save_page_basic_grid_layout.addWidget(self.retry_countLabel, 12, 0, 1, 1)
        self.timeoutLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.timeoutLabel.setObjectName("timeoutLabel")
        self.save_page_basic_grid_layout.addWidget(self.timeoutLabel, 13, 0, 1, 1)
        self.pre_selectLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.pre_selectLabel.setObjectName("pre_selectLabel")
        self.save_page_basic_grid_layout.addWidget(self.pre_selectLabel, 14, 0, 1, 1)
        self.proxy_addressLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.proxy_addressLineEdit.setObjectName("proxy_addressLineEdit")
        self.save_page_basic_grid_layout.addWidget(self.proxy_addressLineEdit, 9, 1, 1, 1)
        self.ffmpeg_pathLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.ffmpeg_pathLineEdit.setObjectName("ffmpeg_pathLineEdit")
        self.save_page_basic_grid_layout.addWidget(self.ffmpeg_pathLineEdit, 10, 1, 1, 1)
        self.tempdirLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.tempdirLineEdit.setObjectName("tempdirLineEdit")
        self.save_page_basic_grid_layout.addWidget(self.tempdirLineEdit, 11, 1, 1, 1)
        self.retry_countSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.retry_countSpinBox.setMinimum(1)
        self.retry_countSpinBox.setMaximum(100)
        self.retry_countSpinBox.setObjectName("retry_countSpinBox")
        self.save_page_basic_grid_layout.addWidget(self.retry_countSpinBox, 12, 1, 1, 1)
        self.timeoutSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.timeoutSpinBox.setObjectName("timeoutSpinBox")
        self.save_page_basic_grid_layout.addWidget(self.timeoutSpinBox, 13, 1, 1, 1)
        self.pre_selectSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.pre_selectSpinBox.setMinimum(-1)
        self.pre_selectSpinBox.setProperty("value", -1)
        self.pre_selectSpinBox.setObjectName("pre_selectSpinBox")
        self.save_page_basic_grid_layout.addWidget(self.pre_selectSpinBox, 14, 1, 1, 1)
        self.save_page_ffmpeg_path_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.save_page_ffmpeg_path_btn.setObjectName("save_page_ffmpeg_path_btn")
        self.save_page_basic_grid_layout.addWidget(self.save_page_ffmpeg_path_btn, 10, 2, 1, 1)
        self.save_page_tempdir_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.save_page_tempdir_btn.setObjectName("save_page_tempdir_btn")
        self.save_page_basic_grid_layout.addWidget(self.save_page_tempdir_btn, 11, 2, 1, 1)
        self.save_page_headers_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.save_page_headers_btn.setObjectName("save_page_headers_btn")
        self.save_page_basic_grid_layout.addWidget(self.save_page_headers_btn, 7, 2, 1, 1)
        self.verboseCheckBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.verboseCheckBox.setText("")
        self.verboseCheckBox.setObjectName("verboseCheckBox")
        self.save_page_basic_grid_layout.addWidget(self.verboseCheckBox, 3, 1, 1, 1)
        self.baseurlLineEdit_save = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.baseurlLineEdit_save.setObjectName("baseurlLineEdit_save")
        self.save_page_basic_grid_layout.addWidget(self.baseurlLineEdit_save, 4, 1, 1, 1)
        self.verboseLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.verboseLabel.setObjectName("verboseLabel")
        self.save_page_basic_grid_layout.addWidget(self.verboseLabel, 3, 0, 1, 1)
        self.baseurlLabel_save = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.baseurlLabel_save.setObjectName("baseurlLabel_save")
        self.save_page_basic_grid_layout.addWidget(self.baseurlLabel_save, 4, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.save_page_basic_grid_layout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.save_page_scroll_area.setWidget(self.scrollAreaWidgetContents)
        self.save_page_base_vertical_layout.addWidget(self.save_page_scroll_area)
        self.base_tab_widget.addTab(self.save_page_base_stacked_widget, "")
        self.base_stacked_widget_capture_page = QtWidgets.QWidget()
        self.base_stacked_widget_capture_page.setObjectName("base_stacked_widget_capture_page")
        self.capture_page_base_vertical_layout = QtWidgets.QVBoxLayout(self.base_stacked_widget_capture_page)
        self.capture_page_base_vertical_layout.setObjectName("capture_page_base_vertical_layout")
        self.capture_page_scroll_area = QtWidgets.QScrollArea(self.base_stacked_widget_capture_page)
        self.capture_page_scroll_area.setWidgetResizable(True)
        self.capture_page_scroll_area.setObjectName("capture_page_scroll_area")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 219, 166))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.capture_page_basic_grid_layout = QtWidgets.QGridLayout()
        self.capture_page_basic_grid_layout.setObjectName("capture_page_basic_grid_layout")
        self.outputLineEdit_capture = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.outputLineEdit_capture.setObjectName("outputLineEdit_capture")
        self.capture_page_basic_grid_layout.addWidget(self.outputLineEdit_capture, 2, 1, 1, 1)
        self.urlLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.urlLineEdit.setObjectName("urlLineEdit")
        self.capture_page_basic_grid_layout.addWidget(self.urlLineEdit, 0, 1, 1, 1)
        self.scan_extLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.scan_extLabel.setObjectName("scan_extLabel")
        self.capture_page_basic_grid_layout.addWidget(self.scan_extLabel, 3, 0, 1, 1)
        self.outputLabel_capture = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.outputLabel_capture.setObjectName("outputLabel_capture")
        self.capture_page_basic_grid_layout.addWidget(self.outputLabel_capture, 2, 0, 1, 1)
        self.driverLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.driverLabel.setObjectName("driverLabel")
        self.capture_page_basic_grid_layout.addWidget(self.driverLabel, 1, 0, 1, 1)
        self.driverLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.driverLineEdit.setObjectName("driverLineEdit")
        self.capture_page_basic_grid_layout.addWidget(self.driverLineEdit, 1, 1, 1, 1)
        self.scan_extLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.scan_extLineEdit.setObjectName("scan_extLineEdit")
        self.capture_page_basic_grid_layout.addWidget(self.scan_extLineEdit, 3, 1, 1, 1)
        self.urlLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.urlLabel.setObjectName("urlLabel")
        self.capture_page_basic_grid_layout.addWidget(self.urlLabel, 0, 0, 1, 1)
        self.baseurlCheckBox_capture = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
        self.baseurlCheckBox_capture.setObjectName("baseurlCheckBox_capture")
        self.capture_page_basic_grid_layout.addWidget(self.baseurlCheckBox_capture, 4, 1, 1, 1)
        self.baseurlLabel_capture = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.baseurlLabel_capture.setObjectName("baseurlLabel_capture")
        self.capture_page_basic_grid_layout.addWidget(self.baseurlLabel_capture, 4, 0, 1, 1)
        self.capture_page_driver_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.capture_page_driver_btn.setObjectName("capture_page_driver_btn")
        self.capture_page_basic_grid_layout.addWidget(self.capture_page_driver_btn, 1, 2, 1, 1)
        self.capture_page_output_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.capture_page_output_btn.setObjectName("capture_page_output_btn")
        self.capture_page_basic_grid_layout.addWidget(self.capture_page_output_btn, 2, 2, 1, 1)
        self.verticalLayout_5.addLayout(self.capture_page_basic_grid_layout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.capture_page_scroll_area.setWidget(self.scrollAreaWidgetContents_2)
        self.capture_page_base_vertical_layout.addWidget(self.capture_page_scroll_area)
        self.base_tab_widget.addTab(self.base_stacked_widget_capture_page, "")
        self.base_vertical_layout.addWidget(self.base_tab_widget)
        self.execute_command_text_browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.execute_command_text_browser.setMaximumSize(QtCore.QSize(16777215, 50))
        self.execute_command_text_browser.setObjectName("execute_command_text_browser")
        self.base_vertical_layout.addWidget(self.execute_command_text_browser)
        self.execute_btn = QtWidgets.QPushButton(self.centralwidget)
        self.execute_btn.setObjectName("execute_btn")
        self.base_vertical_layout.addWidget(self.execute_btn)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 24))
        self.menubar.setObjectName("menubar")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_report_a_bug = QtGui.QAction(MainWindow)
        self.action_report_a_bug.setObjectName("action_report_a_bug")
        self.action_about_vsdownload = QtGui.QAction(MainWindow)
        self.action_about_vsdownload.setObjectName("action_about_vsdownload")
        self.action_about_qt = QtGui.QAction(MainWindow)
        self.action_about_qt.setObjectName("action_about_qt")
        self.menu_help.addAction(self.action_report_a_bug)
        self.menu_help.addSeparator()
        self.menu_help.addAction(self.action_about_vsdownload)
        self.menu_help.addAction(self.action_about_qt)
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        self.base_tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "vsdownload"))
        self.save_page_output_btn.setText(_translate("MainWindow", "save"))
        self.save_page_input_btn.setText(_translate("MainWindow", "open"))
        self.outputLabel_save.setText(_translate("MainWindow", "output*"))
        self.inputLabel.setText(_translate("MainWindow", "input*"))
        self.threadsLabel.setText(_translate("MainWindow", "threads"))
        self.cleanupLabel_save.setText(_translate("MainWindow", "cleanup"))
        self.chunk_sizeLabel.setText(_translate("MainWindow", "chunk_size"))
        self.headersLabel.setText(_translate("MainWindow", "headers"))
        self.key_ivLabel.setText(_translate("MainWindow", "key_iv"))
        self.proxy_addressLabel.setText(_translate("MainWindow", "proxy_address"))
        self.ffmpeg_pathLabel.setText(_translate("MainWindow", "ffmpeg_path"))
        self.tempdirLabel.setText(_translate("MainWindow", "tempdir"))
        self.retry_countLabel.setText(_translate("MainWindow", "retry_count"))
        self.timeoutLabel.setText(_translate("MainWindow", "timeout"))
        self.pre_selectLabel.setText(_translate("MainWindow", "pre_select"))
        self.save_page_ffmpeg_path_btn.setText(_translate("MainWindow", "open"))
        self.save_page_tempdir_btn.setText(_translate("MainWindow", "open"))
        self.save_page_headers_btn.setText(_translate("MainWindow", "open"))
        self.verboseLabel.setText(_translate("MainWindow", "verbose"))
        self.baseurlLabel_save.setText(_translate("MainWindow", "baseurl"))
        self.base_tab_widget.setTabText(self.base_tab_widget.indexOf(self.save_page_base_stacked_widget), _translate("MainWindow", "save"))
        self.scan_extLabel.setText(_translate("MainWindow", "scan_ext"))
        self.outputLabel_capture.setText(_translate("MainWindow", "output*"))
        self.driverLabel.setText(_translate("MainWindow", "driver*"))
        self.urlLabel.setText(_translate("MainWindow", "url*"))
        self.baseurlLabel_capture.setText(_translate("MainWindow", "baseurl"))
        self.capture_page_driver_btn.setText(_translate("MainWindow", "open"))
        self.capture_page_output_btn.setText(_translate("MainWindow", "save"))
        self.base_tab_widget.setTabText(self.base_tab_widget.indexOf(self.base_stacked_widget_capture_page), _translate("MainWindow", "capture"))
        self.execute_btn.setText(_translate("MainWindow", "execute"))
        self.menu_help.setTitle(_translate("MainWindow", "help"))
        self.action_report_a_bug.setText(_translate("MainWindow", "report a bug"))
        self.action_about_vsdownload.setText(_translate("MainWindow", "about vsdownload"))
        self.action_about_qt.setText(_translate("MainWindow", "about qt"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
