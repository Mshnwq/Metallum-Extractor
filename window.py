from PyQt5.QtCore import QMetaObject, QPoint, Qt, pyqtSignal
from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QGroupBox,
                             QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                             QMainWindow, QMenu, QPushButton, QStatusBar,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)


class Ui_MainWindow(QMainWindow):
    ##### Event Signal to be handled in Main #####
    extract_event_signal = pyqtSignal()
    folder_event_signal = pyqtSignal()
    excel_event_signal = pyqtSignal()
    youtube_event_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.full_length_bool = True
        self.single_bool = True
        self.collab_bool = True
        self.split_bool = True
        self.comp_bool = True
        self.live_bool = True
        self.demo_bool = True
        self.vid_bool = True
        self.box_bool = True
        self.ep_bool = True

    def setup_ui(self, MainWindow):
        # Initialize window
        MainWindow.setGeometry(100, 100, 800, 600)
        MainWindow.setMinimumSize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        
        # Initialize layout
        self.layout = QVBoxLayout(self.centralwidget) # type: ignore

        # Add search bar and button
        self.search_group = QGroupBox(self.centralwidget) 
        self.search_label = QLabel('URL:')
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Enter URL...')
        self.extract_button = QPushButton('Extract')
        self.extract_button.clicked.connect(
                                lambda: self._emit(
                                'extract_event_signal'))
        # Add checkbox to last column
        self.album_img_checkbox = QCheckBox("with album images")
        self.album_img_checkbox.setToolTip(\
            "Check if desire to extract album images also")
        search_layout = QHBoxLayout(self.search_group)
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.album_img_checkbox)
        search_layout.addWidget(self.extract_button)

        self.layout.addWidget(self.search_group)

        # Add table widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Name', 'Type', 'Year', 'Selected'])
        self.table.setSortingEnabled(True)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu) # type: ignore
        self.table.customContextMenuRequested.connect(self.customContextMenuRequested)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.table)

        # Add action group and button
        self.action_group = QGroupBox(self.centralwidget) 
        self.folder_button = QPushButton('Folder')
        self.excel_button = QPushButton('Excel')
        self.youtube_button = QPushButton('Youtube')
        self.folder_button.clicked.connect(
                                lambda: self._emit(
                                'folder_event_signal'))
        self.excel_button.clicked.connect(
                                lambda: self._emit(
                                'excel_event_signal'))
        self.youtube_button.clicked.connect(
                                lambda: self._emit(
                                'youtube_event_signal'))
        action_layout = QHBoxLayout(self.action_group)
        action_layout.addWidget(self.folder_button)
        action_layout.addWidget(self.excel_button)
        action_layout.addWidget(self.youtube_button)

        self.layout.addWidget(self.action_group)

        # Create status bar
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget) 
        QMetaObject.connectSlotsByName(MainWindow)

    def customContextMenuRequested(self, point: QPoint):
        # Create context menu and actions
        menu = QMenu(self.table)

        # Create a QAction with a checkbox widget for the Full Length filter
        full_length_action = QAction("Full Length", menu)
        full_length_action.setCheckable(True)
        full_length_action.setChecked(self.full_length_bool)
        full_length_action.toggled.connect(lambda: self.toggle_filter('full_length'))
        full_length_action.setStatusTip("Filter by Full Length")
        full_length_action.setToolTip("Filter by Full Length")

        # Create a QAction with a checkbox widget for the EP filter
        ep_action = QAction("EP", menu)
        ep_action.setCheckable(True)
        ep_action.setChecked(self.ep_bool)
        ep_action.toggled.connect(lambda: self.toggle_filter('ep'))
        ep_action.setStatusTip("Filter by EP")
        ep_action.setToolTip("Filter by EP")

        # Create a QAction with a checkbox widget for the Demo filter
        demo_action = QAction("Demo", menu)
        demo_action.setCheckable(True)
        demo_action.setChecked(self.demo_bool)
        demo_action.toggled.connect(lambda: self.toggle_filter('demo'))
        demo_action.setStatusTip("Filter by Demo")
        demo_action.setToolTip("Filter by Demo")

        # Create a QAction with a checkbox widget for the Split filter
        split_action = QAction("Split", menu)
        split_action.setCheckable(True)
        split_action.setChecked(self.split_bool)
        split_action.toggled.connect(lambda: self.toggle_filter('split'))
        split_action.setStatusTip("Filter by Split")
        split_action.setToolTip("Filter by Split")
        
        # Create a QAction with a checkbox widget for the Collab filter
        collab_action = QAction("Collab", menu)
        collab_action.setCheckable(True)
        collab_action.setChecked(self.collab_bool)
        collab_action.toggled.connect(lambda: self.toggle_filter('collab'))
        collab_action.setStatusTip("Filter by Collab")
        collab_action.setToolTip("Filter by Collab")
        
        # Create a QAction with a checkbox widget for the Live filter
        live_action = QAction("Live", menu)
        live_action.setCheckable(True)
        live_action.setChecked(self.live_bool)
        live_action.toggled.connect(lambda: self.toggle_filter('live'))
        live_action.setStatusTip("Filter by Live")
        live_action.setToolTip("Filter by Live")
        
        # Create a QAction with a checkbox widget for the Single filter
        single_action = QAction("Single", menu)
        single_action.setCheckable(True)
        single_action.setChecked(self.single_bool)
        single_action.toggled.connect(lambda: self.toggle_filter('single'))
        single_action.setStatusTip("Filter by Single")
        single_action.setToolTip("Filter by Single")
        
        # Create a QAction with a checkbox widget for the Comp filter
        comp_action = QAction("Comp", menu)
        comp_action.setCheckable(True)
        comp_action.setChecked(self.comp_bool)
        comp_action.toggled.connect(lambda: self.toggle_filter('comp'))
        comp_action.setStatusTip("Filter by Comp")
        comp_action.setToolTip("Filter by Comp")

        # Create a QAction with a checkbox widget for the Video filter
        video_action = QAction("Video", menu)
        video_action.setCheckable(True)
        video_action.setChecked(self.vid_bool)
        video_action.toggled.connect(lambda: self.toggle_filter('vid'))
        video_action.setStatusTip("Filter by Video")
        video_action.setToolTip("Filter by Video")

        # Create a QAction with a checkbox widget for the Boxed filter
        boxed_action = QAction("Boxed", menu)
        boxed_action.setCheckable(True)
        boxed_action.setChecked(self.box_bool)
        boxed_action.toggled.connect(lambda: self.toggle_filter('box'))
        boxed_action.setStatusTip("Filter by Boxed")
        boxed_action.setToolTip("Filter by Boxed")

        # Add checkboxes to menu
        menu.addAction(full_length_action)
        menu.addAction(demo_action)
        menu.addAction(ep_action)
        menu.addAction(split_action)
        menu.addAction(collab_action)
        menu.addAction(single_action)
        menu.addAction(comp_action)
        menu.addAction(live_action)
        menu.addAction(video_action)
        menu.addAction(boxed_action)

        menu.exec_(self.table.viewport().mapToGlobal(point))

    def filter_table(self, to_filter):
        # boss
        for row_index in range(self.table.rowCount()):
            type_text = self.table.item(row_index, 1).text().lower().replace('-','_')
            if self.compare_first_letters(to_filter, type_text):
                eval(f"self.table.setRowHidden(row_index, not self.{to_filter}_bool)")

    def compare_first_letters(self, s1, s2):
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                return False
        return True

    def toggle_filter(self, filter_str: str):
        # boss
        eval("exec('self.{0} = not self.{0}')".format(filter_str + "_bool"))
        self.filter_table(filter_str)

    def _emit(self, to_emit: str):
        print(f"Event Triggered: {to_emit}")
        eval(f"self.{to_emit}.emit()")

    def get_table_selected(self):
        selected = []
        for row_index in range(self.table.rowCount()):
            if self.table.isRowHidden(row_index):
                continue
            checkbox_widget = self.table.cellWidget(row_index, 3).layout().itemAt(0).widget()
            if checkbox_widget.isChecked():
                selected.append([self.table.item(row_index, column_index).text() for column_index in range(3)])
        return selected

    def update_table(self, data: list[str]):

        # Clear table
        self.table.setRowCount(0)

        # Filter and add rows to table
        for row_data in data:
            row_index = self.table.rowCount()
            self.table.insertRow(row_index)
            for column_index, column_data in enumerate(row_data):
                item = QTableWidgetItem(str(column_data))
                self.table.setItem(row_index, column_index, item)

                # Add checkbox to last column
                checkbox_container = QWidget()
                checkbox_layout = QHBoxLayout()
                checkbox_layout.setAlignment(Qt.AlignCenter) # type: ignore
                checkbox_layout.setContentsMargins(0,0,0,0)
                checkbox_widget = QCheckBox()
                checkbox_layout.addWidget(checkbox_widget)
                checkbox_container.setLayout(checkbox_layout)
                self.table.setCellWidget(row_index, 3, checkbox_container)
        ...


if __name__ == '__main__':
    app = QApplication([])
    main = QMainWindow()
    main.ui = Ui_MainWindow()
    main.ui.setup_ui(main)
    main.show()
    app.exec_()
    ...
