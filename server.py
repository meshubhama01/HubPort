import socket
import threading
import os

def download(name,socket):
	fileName = socket.recv(1024)
	print("recieved")
	if os.path.isfile(fileName):
		#socket.send("EXISTS " + str(os.path.getsize(fileName)))
		#print(os.path.getsize(fileName))
		#response = socket.recv(1024)
		#if response[:2]== 'OK':
		print(fileName)
		print("file exists")
		socket.send("File Exists")
		socket.send(str(os.path.getsize(fileName)))
		with open(fileName,'rb') as f:
			bytes = f.read(1024)
			socket.send(bytes)
			while bytes!="":
				bytes = f.read(1024)
				socket.send(bytes)
				print("sending...")
	else:
		print("not exists")
		socket.send("File don't exists")

	socket.close()

def Main():
	host = '192.168.0.102'
	port = 3500
	s = socket.socket()
	s.bind((host,port))
	s.listen(5)
	print("server started")

	while True:
		c, addr = s.accept()
		print(addr)
		print("client connected")
		t = threading.Thread(target=download,args=("download",c))
		t.start()
	s.close()

if __name__ == '__main__':
	Main()
