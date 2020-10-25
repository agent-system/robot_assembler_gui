#!/usr/bin/env python

import sys

from robot_assembler_gui.assemble_editor import AssembleEditor
from rqt_gui.main import Main

plugin = 'robot_assembler_gui.assemble_editor.AssembleEditor'
main = Main(filename=plugin)
sys.exit(main.main(standalone=plugin))
