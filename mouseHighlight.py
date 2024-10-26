#!/usr/bin/env python3
# I was looking at a certain provissioning tool, and keeping track of all the lines was hard,
# highlighting isnt an option, and theres a lot of stuff on the sceen. 
# this script is to help me keep track of the line I'm on. 

# pip install PyQt5


import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class HighlightLineOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool |
            QtCore.Qt.WindowTransparentForInput
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Set the overlay window to full screen
        self.screen_width = QtWidgets.QApplication.primaryScreen().size().width()
        self.screen_height = QtWidgets.QApplication.primaryScreen().size().height()
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        # Create the highlight bar with semi-transparent color
        self.bar_height = 15  # Adjust bar thickness here
        self.bar_color = QtGui.QColor(255, 255, 0, 50)  # Yellow bar with transparency (150)
        self.bar_y_position = 100  # Initial Y position
        self.showFullScreen()

        # Set up a timer to update the bar position based on mouse Y coordinate
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_bar_position)
        self.timer.start(20)  # Refresh rate

    def paintEvent(self, event):
        # Draw the highlight bar
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(self.bar_color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(0, self.bar_y_position, self.screen_width, self.bar_height)

    def update_bar_position(self):
        # Get the current mouse position
        cursor_pos = QtGui.QCursor.pos()
        # Update the bar's Y position to follow the mouse's Y coordinate
        self.bar_y_position = cursor_pos.y()
        self.update()  # Redraw the bar at the new position

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    overlay = HighlightLineOverlay()
    overlay.show()
    sys.exit(app.exec_())

