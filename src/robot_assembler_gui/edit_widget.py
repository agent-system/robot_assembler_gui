import os
import time
import threading

import rospy
import rospkg

from std_msgs.msg import String
from std_srvs.srv import Empty
from std_srvs.srv import SetBool
from jsk_rviz_plugins.srv import EusCommand

from python_qt_binding import loadUi
from python_qt_binding.QtCore import qDebug, Qt, qWarning, Signal
from python_qt_binding.QtGui import QIcon
from python_qt_binding.QtWidgets import QFileDialog, QGraphicsView, QWidget, QMessageBox

from python_qt_binding.QtCore import QTimer

class RAEditGraphicsView(QGraphicsView):

    def __init__(self, parent=None):
        super(RAEditGraphicsView, self).__init__()


class RAEditWidget(QWidget):

    """
    """

    def __init__(self, context):
        """
        :param context: plugin context hook to enable adding widgets as a ROS_GUI pane, ''PluginContext''
        """
        super(RAEditWidget, self).__init__()
        rp = rospkg.RosPack()
        ui_file = os.path.join(rp.get_path('robot_assembler_gui'), 'resources', 'edit.ui')
        loadUi(ui_file, self, {'RAEditGraphicsView': RAEditGraphicsView})

        self.send_button.clicked[bool].connect(self._handle_send_clicked)

        self.modeButtonA.clicked[bool].connect(self._handle_modeA_clicked)
        self.modeButtonB.clicked[bool].connect(self._handle_modeB_clicked)
        self.modeButtonC.clicked[bool].connect(self._handle_modeC_clicked)

        self.rbutton0.clicked[bool].connect(self._r0_clicked)
        self.rbutton1.clicked[bool].connect(self._r1_clicked)
        self.rbutton2.clicked[bool].connect(self._r2_clicked)

        self._counter = 0
        self._mode = None
        ## click rbutton0 ...
        ## wait service ...
        self.rbutton0.click()

        self._text_lock = threading.Lock()
        self._update_text_timer = QTimer(self)
        self._update_text_timer.timeout.connect(self.updateText)
        self._update_text_timer.start(20)

        self._information_text_data = None
        rospy.Subscriber("robot_assembler/print_information", String, self._callback_information)

    def updateText(self):
        if self._information_text_data == None:
            return
        self._text_lock.acquire()
        for txt in self._information_text_data:
            if txt == ':clear':
                self.information_text.clear()
            else:
                self.information_text.append(txt)
        self._information_text_data = None
        self._text_lock.release()

    def _callback_information(self, msg):
        self._text_lock.acquire()
        msg_data = msg.data.split('\n')
        if self._information_text_data == None or msg_data[0] == ':clear':
            self._information_text_data = msg_data
        else:
            self._information_text_data = self._information_text_data + msg_data
        print (self._information_text_data)
        self._text_lock.release()

    def _handle_send_clicked(self, checked):
        print('_handle_send_clicked: %s'%(checked))
        self._counter = self._counter + 1

        srv = rospy.ServiceProxy('robot_assembler/command/service_command', EusCommand)
        #com = EusCommand()
        #com.command = self.command_text.toPlainText()
        try:
            srv(self.command_text.toPlainText())
        except rospy.ServiceException, e:
            self.showError('Failed to call')

    def _handle_modeA_clicked(self, checked):
        print('_mode_view_clicked: %s'%(checked))
        self.buttonCallbackImpl('robot_assembler/command/view_mode_view')

    def _handle_modeB_clicked(self, checked):
        print('_mode_model_clicked: %s'%(checked))
        self.buttonCallbackImpl('robot_assembler/command/view_mode_model')

    def _handle_modeC_clicked(self, checked):
        print('_mode_design_clicked: %s'%(checked))
        self.buttonCallbackImpl('robot_assembler/command/view_mode_design')

    def _r0_clicked(self, checked):
        ## fixed-point
        print('gui : fixed point clicked')
        self.command_name.setText('command(fixed point):')
        self.buttonCallbackImpl('robot_assembler/command/select_fixedpoint')
        self._mode = 'fixed-point'

    def _r1_clicked(self, checked):
        ## actuator
        print('gui : actuator clicked')
        self.command_name.setText('command(actuator):')
        self.buttonCallbackImpl('robot_assembler/command/select_actuator')
        self._mode = 'actuator'

    def _r2_clicked(self, checked):
        ## parts / not implemented
        print('gui : parts clicked')
        self.command_name.setText('command(parts):')
        self.buttonCallbackImpl('robot_assembler/command/select_parts')
        self._mode = 'parts'

    def buttonCallbackImpl(self, service_name, checked = None):
        if checked == None:
            srv = rospy.ServiceProxy(service_name, Empty)
            try:
                srv()
            except rospy.ServiceException, e:
                self.showError("Failed to call %s" % service_name)
        else:
            srv = rospy.ServiceProxy(service_name, SetBool)
            try:
                srv()
            except rospy.ServiceException, e:
                self.showError("Failed to call %s" % service_name)

    def showError(self, message):
        QMessageBox.about(self, "ERROR", message)
