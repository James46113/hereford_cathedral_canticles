from canticles import load_canticles
import sys
from PySide6 import QtCore, QtWidgets
from datetime import datetime

def update_table():
    try:
        canticles = load_canticles()
        table.clearContents()

        table.setRowCount(len(canticles))
        first_row_height = table.rowHeight(0) if len(canticles) > 0 else 59
        header_height = table.horizontalHeader().height()


        screen = QtWidgets.QApplication.primaryScreen()
        screen_height = screen.availableGeometry().height()
        time_height = 80#time.sizeHint().height()
        available_rows = (screen_height-16-24-header_height-time_height) // first_row_height
        table.setRowCount(available_rows)
        table.setFixedHeight((first_row_height)*(available_rows)+(header_height+12))

        canticles = canticles[:available_rows]

        for row, canticle in enumerate(canticles):
            date_item = QtWidgets.QTableWidgetItem(canticle.date.strftime("%a %-d"))
            canticle_item = QtWidgets.QTableWidgetItem(canticle.canticles)
            composer_item = QtWidgets.QTableWidgetItem(canticle.composer)
            service_item = QtWidgets.QTableWidgetItem(canticle.type)

            service_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

            
            table.setItem(row, 0, date_item)
            table.setItem(row, 1, canticle_item)
            table.setItem(row, 2, composer_item)
            table.setItem(row, 3, service_item)

        for i in range(len(canticles), available_rows):
            for col in range(4):
                table.setItem(i, col, QtWidgets.QTableWidgetItem(""))

    except Exception as e:
        print(f"Error updating table: {e}")


# Create a Qt application
app = QtWidgets.QApplication(sys.argv)

# Create a Qt window
main_window = QtWidgets.QWidget()
main_window.setWindowTitle("Canticles Schedule")
QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.BlankCursor)

# Create main layout
layout = QtWidgets.QVBoxLayout()
layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

day = QtWidgets.QLabel()
day.setText("Canticle Departures")
day.setStyleSheet("""
    color: #fff;
    font-weight: bold;
    letter-spacing: 3px;
    font-size: 28px;
""")
# layout.addWidget(title)

# Create table widget
table = QtWidgets.QTableWidget()
table.setColumnCount(4)
table.setHorizontalHeaderLabels(["Date", "Canticles", "Composer", "Service"])

# Style the table for LED dot lights look
table.setStyleSheet("""
    QTableWidget {
        background-color: #1a1a1a;
        color: #ffe600;
        font-family: 'Dot Matrix', 'DS-Digital', 'Courier New', monospace;
        font-size: 32px;
        gridline-color: #1a1a1a;
        selection-background-color: #1a1a1a;
        border: none;
        letter-spacing: 2px;
        margin-top: 16px;
    }
    QHeaderView::section {
        background-color: #000;
        color: #fff;
        padding: 12px;
        padding-left: auto;
        border: none;
        font-weight: bold;
        font-size: 26px;
        letter-spacing: 3px;
        text-align: left;
    }
    QTableWidget::item {
        padding: 0 10 0 10;
        border-bottom: 5px solid #000;
        margin: 0;
        padding-left: auto;
    }
""")



    # QHeaderView::section {
        # background-color: #1a1a1a;
        # color: #ffe600;
        # font-family: 'Dot Matrix';
        # padding: 12px;
        # padding-left: auto;
        # border: none;
        # font-weight: bold;
        # font-size: 36px;
        # border-bottom: 5px solid #000;
        # letter-spacing: 3px;
        # text-align: left;
    # }

# Left align header labels programmatically
header = table.horizontalHeader()
header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
table.horizontalHeaderItem(3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter) # type: ignore

# Hide vertical headers (row numbers)
table.verticalHeader().setVisible(False)
table.setCornerButtonEnabled(False)

table.setShowGrid(False)

# Hide scroll bars
table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

# Make table fill the window
table.horizontalHeader().setStretchLastSection(True)
table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
# table.verticalHeader().setDefaultSectionSize(59)  # Fixed height of 60 pixels per row

table.setWordWrap(False)

# Set black background
palette = main_window.palette()
palette.setColor(main_window.backgroundRole(), QtCore.Qt.GlobalColor.black)
main_window.setPalette(palette)
main_window.setAutoFillBackground(True)

timer = QtCore.QTimer()
timer.timeout.connect(update_table)
timer.start(60000)

# Add table to layout
layout.addWidget(table)

bottom_label_style_sheet = """
    color: #fff;
    letter-spacing: 3px;
    padding: 0px;
    margin: 0px;
    padding-left: auto;
    background-color: #1a1a1a;
    color: #ffe600;
    font-family: 'Dot Matrix', 'DS-Digital', 'Courier New', monospace;
    font-size: 52px;
"""

time = QtWidgets.QLabel()
time.setText(datetime.now().strftime("%H:%M:%S"))
time.setStyleSheet(bottom_label_style_sheet + "font-size: 80px;")
time.setContentsMargins(0, 0, 0, 0)
# time.setMaximumHeight(80)

day = QtWidgets.QLabel()
day.setStyleSheet(bottom_label_style_sheet)
day.setContentsMargins(0, 0, 0, 0)

date = QtWidgets.QLabel()
date.setStyleSheet(bottom_label_style_sheet)
date.setContentsMargins(0, 0, 0, 0)

# Create a horizontal layout to left-align the title and right-align the time label
time_layout = QtWidgets.QHBoxLayout()
time_layout.setSpacing(0)


# Add a QWidget with #1a1a1a background to fill the space between title and time
spacer_left = QtWidgets.QWidget()
spacer_left.setStyleSheet("background-color: #1a1a1a;")
spacer_right = QtWidgets.QWidget()
spacer_right.setStyleSheet("background-color: #1a1a1a;")

time_layout.addWidget(day, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
time_layout.addWidget(spacer_left, stretch=1)
time_layout.addWidget(time, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
time_layout.addWidget(spacer_right, stretch=1)
time_layout.addWidget(date, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

layout.addLayout(time_layout)

def update_time():
    time.setText(datetime.now().strftime("%H:%M:%S"))
    day.setText(datetime.now().strftime("%A"))
    date.setText(datetime.now().strftime("%-d %b"))



timer = QtCore.QTimer()
timer.timeout.connect(update_time)
timer.start(500)

# Load and populate data
update_table()

main_window.setLayout(layout)

# Show the window
main_window.showFullScreen()

# Enter the Qt main loop and exit when done
sys.exit(app.exec())