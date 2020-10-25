import os
import argparse
import threading

from qt_gui.plugin import Plugin

from .edit_widget import RAEditWidget

class AssembleEditor(Plugin):

    """

    """

    def __init__(self, context):
        """

        """
        super(AssembleEditor, self).__init__(context)
        self.setObjectName('AssembleEditor')

        self._widget = RAEditWidget(context)

        if context.serial_number() > 1:
            self._widget.setWindowTitle(
                self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)
