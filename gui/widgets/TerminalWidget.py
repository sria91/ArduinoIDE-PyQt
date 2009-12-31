# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui


from gui.icons import Ico 
from gui.icons import Icon 

"""
The general idea is that this handles the shell commands and to Card
* uses QProcess
* set icon and label on return of errror or higlighing
* TODO error higllighting
* TODO needs tewekaing BIG time for bi-directional hackeers

Currently reads and presents error + stand and sets icons/message aaccordingly
* its called terminal cos it leads to frustration ;-)
"""

class TerminalWidget(QtGui.QWidget):

	
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main
		
		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		self.setLayout(layout)

		hbox = QtGui.QHBoxLayout()
		hbox.setContentsMargins(0, 0, 0, 0)
		hbox.setSpacing(0)
		layout.addLayout(hbox)

		## This is the box with the buttons u set the size u wanna view
		sizeButtonsBox = QtGui.QHBoxLayout()
		layout.addLayout(sizeButtonsBox)
		sizeButtonsBox.addStretch(100) # stuff the widgets to the right
		
		self.viewSizeButtonGroup = QtGui.QButtonGroup(self)
		#self.connect(self.viewSizeButtonGroup, QtCore.SIGNAL("button"), self.on_view_size_clicked)
		for ico, caption in [[Ico.Small, 'Small'],[Ico.Medium, 'Medium'],[Ico.Large, 'Larger']]:
			butt = QtGui.QPushButton()
			sizeButtonsBox.addWidget(butt)
			butt.setText(caption)
			butt.setIcon(Icon(ico))
			butt.setCheckable(True)
			butt.setChecked(caption == 'Small') # TODO setting


		self.textWidget = QtGui.QPlainTextEdit()
		layout.addWidget(self.textWidget)
		self.textWidget.setDocumentTitle("Foo")
		self.textWidget.setStyleSheet("color: white; background-color: black;")


		hbox = QtGui.QHBoxLayout()
		layout.addLayout(hbox)

		self.actionIcon = QtGui.QPushButton()
		self.actionIcon.setFlat(True)
		self.actionIcon.setIcon(Icon(Ico.Black))
		hbox.addWidget(self.actionIcon, 1)

		#elf.statusBar.showMessage("ssssssssssssssss-")
		#self.statusLabel = QtGui.QLabel("Terminal Output")
		#hbox.addWidget(self.statusLabel, 20)

		
		#self.progress = QtGui.QProgressBar()
		#self.progress.setRange(0, 3)
		#self.progress.setFixedHeight(15)
		#self.progress.hide()
		#hbox.addWidget(self.progress)

	

	def set_text(self, txt, is_error):
		if is_error:
			self.headerLabel.setText("Error")
		else:
			self.headerLabel.setText("result")
		self.textWidget.setPlainText(txt)

	def set_error(self, title, shell):
		self.actionIcon.setIcon(Icon(Ico.CompileError))
		self.statusLabel.setText(title)
		self.textWidget.setPlainText(QtCore.QString(shell))

	def compile(self, file_path):

		self.current_file_path = file_path
		self.progress.show()

		arduino_path = settings.arduino_path()
		if not arduino_path:
			self.set_error("Arduino root path not found", "..nothing to do ..")
			return
		## Set Envoironment
		env = QtCore.QStringList()
		env << QtCore.QString("ARDUINO_DIR=").append()
		env << QtCore.QString("ARDUINO_BOARD=").append("atmega328")
		env << QtCore.QString("ARDUINO_sPORT=").append("s/ssdev/ttyUSB0")
		self.process.setEnvironment(env)

		print "----------------------------------------"

		## Set working dir
		sketch_dir = QtCore.QFileInfo(self.current_file_path).absolutePath()
		
		self.process.setWorkingDirectory(sketch_dir)

		command = QtCore.QString("sh ")
		## Create command sh arduinp_make.sh 
		#command.append("pwd  ") #.append(QtCore.QFileInfo(self.current_file_path).dir().path())
		#args = QtCore.QStringList()
		command.append(self.main.settings.app_path()).append("/etc/arduino_make.sh compile ")
		#command.append(QtCore.QFileInfo(self.current_file_path).dir().path())
		print "command=", command
		self.process.start(command)
		if self.process.waitForStarted(): 
			self.process.waitForFinished()
			result =  self.process.readAllStandardOutput()
			#print type(result), result
			error = self.process.readAllStandardError()
			#print type(error), error
			if error:
				print "is error"
				self.actionIcon.setIcon(Icon(Ico.CompileError))
				self.statusLabel.setText("Error")
				self.textWidget.setPlainText(QtCore.QString(error))
			else:
				print "is ok"
				self.statusLabel.setText("OK")
				self.actionIcon.setIcon(Icon(Ico.CompileOk))
				self.textWidget.setPlainText(QtCore.QString(result))



		self.progress.hide()
		return
		command = QtCore.QString()
		## Create command sh arduinp_make.sh 
		command.append("pwd") # sh ").append(self.main.settings.app_path()).append("/etc/arduino_make.sh compile")
		#args = QtCore.QStringList()
		#command.append(self.main.settings.app_path()).append("/etc/arduino_make.sh compile ")
		#command.append(QtCore.QFileInfo(self.current_file_path).dir().path())
		print "command=", command
		process = QtCore.QProcess(self)
		process.start(command)
		if process.waitForStarted(): 
			process.waitForFinished();
			result =  process.readAllStandardOutput()
			#print type(result), result
			error = process.readAllStandardError()
			#print type(error), error
			if error:
			
				self.textWidget.setPlainText(QtCore.QString(error))
			else:
				self.textWidget.setPlainText(QtCore.QString(result))
