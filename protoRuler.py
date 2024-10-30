#!/usrbin/env python3
# pip install PyQt5
"""
If you have ever seen someone use a ruler on a screen, to try and get measurements,
This proto-program is for them. Its a work in progress. 
"""
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
"""
ToDo:
A means to tilt the bar, would be handy. (This may introduce skew)

An easier way to change / show units on the fly would be nice.
An easier way to change bar, and text colours on the fly would be cool.
A way to shift the measurements to an arbitrary starting point would be nice. 
auto contrasing aginst whatever is in the background would be cool.
"""

class HighlightLineOverlay(QtWidgets.QWidget):
    def __init__(self, unit="inches", screen_width_inches=48):
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

        # Define screen DPI based on actual screen width in inches
        self.screen_width_inches = screen_width_inches
        self.dpi = self.screen_width / self.screen_width_inches
        self.unit = unit  # Choose "inches", "cm", or "mm"
        self.pixels_per_unit = self.get_pixels_per_unit()

        # Create the highlight bar with semi-transparent color
        self.bar_height = 5  # Adjust bar thickness here
        self.bar_color = QtGui.QColor(255, 255, 0, 150)  # Yellow bar with transparency
        self.bar_y_position = 100  # Initial Y position
        self.showFullScreen()

        # Set up a timer to update the bar position based on mouse Y coordinate
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_bar_position)
        self.timer.start(20)  # Adjust the refresh rate as needed

    def get_pixels_per_unit(self):
        # Define conversion based on actual screen DPI
        if self.unit == "inches":
            return self.dpi  # Pixels per inch
        elif self.unit == "cm":
            return self.dpi / 2.54  # Pixels per centimeter
        elif self.unit == "mm":
            return self.dpi / 25.4  # Pixels per millimeter
        else:
            return self.dpi  # Default to pixels per inch

    def paintEvent(self, event):
        # Draw the highlight bar and ruler
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Draw the highlight bar
        painter.setBrush(self.bar_color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(0, self.bar_y_position, self.screen_width, self.bar_height)
        
        # Draw the ruler above the highlight bar
        self.draw_ruler(painter)

    def draw_ruler(self, painter):
        # Set ruler properties
        ruler_height = 20
        tick_length = 10
        label_offset = 5
        painter.setPen(QtGui.QColor(255, 255, 255, 150))  # White semi-transparent ticks and labels

        # Calculate positions for ticks and labels
        num_ticks = int(self.screen_width / self.pixels_per_unit)
        for i in range(num_ticks + 1):
            x = int(i * self.pixels_per_unit)
            # Draw major tick
            painter.drawLine(x, self.bar_y_position - ruler_height, x, self.bar_y_position - ruler_height + tick_length)

            # Draw label for each major tick
            painter.drawText(x + label_offset, self.bar_y_position - ruler_height + 15, f"{i} {self.unit}")

    def update_bar_position(self):
        # Get the current mouse position
        cursor_pos = QtGui.QCursor.pos()
        # Update the bar's Y position to follow the mouse's Y coordinate
        self.bar_y_position = cursor_pos.y()
        self.update()  # Redraw the bar and ruler at the new position

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    overlay = HighlightLineOverlay(unit="\"", screen_width_inches=48)  # Set your screen width in inches
    overlay.show()
    sys.exit(app.exec_())

