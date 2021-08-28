import socket
import time
import threading
from queue import Queue
import sys
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, 
	QPushButton)
from Gui.design import Ui_MainWindow


class Port(object):
	def __init__(self, number, ip):
		socket.setdefaulttimeout(0.25)
		self.print_lock = threading.Lock()

		self.status = None
		self.number = number
		self.Ip = ip

		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.con = self.s.connect((self.Ip, self.number))
			with self.print_lock:
				self.status = 'open'
			self.con.close()
		except:
			pass


class Threading(object):
	def __init__(self, func, flow):
		self.func = func
		for x in range(int(flow)):
			self.t = threading.Thread(target=self.func)
			self.t.daemon = True
			self.t.start()


class Scaner(QMainWindow,Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.start.clicked.connect(self.scanning)


	def scanning(self):
		self._q = Queue()
		self.startTime = time.time()

		self._IpAddr = self.IP.text()
		if self._IpAddr == '':
			self._IpAddr == '127.0.0.1'
		else:
			pass
		self.Ip = socket.gethostbyname(self._IpAddr)
		self.ports = []

		self._thread = Threading(self.threader, 1000)

		for _worker in range(1, 500):
			self._q.put(_worker)

		self._q.join()
		self.IPInput.setText('Time taken: {}'.format(time.time() - self.startTime))

	def threader(self):
		while True:
			_worker = self._q.get()
			self._p = Port(_worker, self.Ip)
			if self._p.status == None or self._p.number in self.ports:
				pass
			else:
				self.ports.append(self._p.number)
				self.response.addItem('{}:{}'.format(self._p.status, self._p.number))
			self._q.task_done()


if __name__ == '__main__':
	QApplication.setStyle("fusion")
	app = QApplication(sys.argv)
	scaner = Scaner()
	scaner.show()
	app.exec_()
