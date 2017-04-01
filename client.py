import socket
from Tkinter import *
import tkMessageBox



def makeform(root):
   entries = {}
   ent = Entry(root)
   ent.insert(0,"0")
   ent.pack(side=RIGHT, expand=YES, fill=X)
   entries['handle'] = ent
   ent.place(x=10,y=30)
   return entries


def download(event):
	file = str(event['handle'].get())
	print("downloading files")
	host = '127.0.0.1'
	port = 3500

	s=socket.socket()
	try:
		s.connect((host,port))
	except:
		text.delete(1.0,END)
		text.insert(INSERT,"Connectivity problem")
	#print("downloading files")

	filename = file
	if filename !='q':
		#print("downloading files")
		s.send(filename)
		#print("downloading files")
		data = s.recv(1024)
		#print("downloading files")
		if data=='File Exists':
			print "hello"
			data = s.recv(1024)
			try:
				filesize = long(data)
			except:
				print("some error occured plzz try again")
				exit(1)
			#print(filesize)
			#message = raw_input("press y/n")
			#if message=='y':
			#s.send('OK')
			f = open('new_'+filename,'wb')
			data = s.recv(1024)
			totalrecv = len(data)
			#print(len(data))
			#print(totalrecv)
			f.write(data)
			text.delete(1.0,END)
			text.insert(INSERT, "Recieving " + filename + "....\n")
			print("recieving....")
			while totalrecv<filesize:
				data = s.recv(1024)
				totalrecv = totalrecv + len(data)
				f.write(data)
				print("recieving....")
				text.insert(INSERT, "Recieving " + filename + "....\n")
				#print "{0:.2f}".format((totalrecv/float(filesize))*100)+\
						#"% Done"
				
			print("download complete")
			tkMessageBox.showinfo("Status","Download Succssesfully completed")
		else:
			print("file dont exists with name "+filename)
			text.delete(1.0,END)
			text.insert(INSERT,"Sorry there is not any file with name " + filename + "\n")
			text.insert(INSERT,"Please try other files")
	s.close()




root = Tk()

root.geometry("500x500")

frame = Frame(root,bg="black",height="100",width="500")
frame.pack(side=TOP)
frame.place(x=0,y=0)

ents=makeform(root)
button = Button(frame,text="Explore",command=(lambda e=ents:download(e)))
button.pack();
button.place(x=10,y=60)

text = Text(root,width="60")
text.insert(INSERT, "Welcome to hub port")

text.pack()
text.place(x=10,y=110)

root.mainloop()
