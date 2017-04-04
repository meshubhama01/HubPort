import socket
from Tkinter import *
import tkMessageBox
import os

port = [3500]
ip = ['127.0.0.1']
s=[socket.socket()]


def makeform(root):
   entries = {}
   ent = Entry(root)
   ent.insert(0,"0")
   ent.pack(side=RIGHT, expand=YES, fill=X)
   entries['handle'] = ent
   ent.place(x=10,y=30)
   return entries

def raise_frame(frame):
	frame.tkraise()

def connect(event,ip):
	s[0]=socket.socket()
	port[0] = int(event['port'].get())
	ip[0] = ip['ip'].get()
	print(ip[0])
	#try:
	print(port[0])
	s[0].connect((ip[0],port[0]))
	print("connected")
	f2.tkraise()
	portNotify.config(text="Connected to " + ip[0] + ":" + str(port[0]))
	portNotify.config(width="500")
	return s
	#except:
		#print("network error")

def disconnect():
	print("disconnected")
	s[0].close()

	raise_frame(f1)


def makeform():
   entries = {}
   ent = Entry(f2)
   ent.insert(0,"0")
   ent.pack()
   entries['handle'] = ent
   ent.place(x=180,y=130)
   return entries




def make_portbox():
	entries = {}
	portEntry = Entry(f1)
	portEntry.pack()
	portEntry.insert(0,port[0])
	portEntry.place(x=180,y=180)
	entries['port'] = portEntry
	return entries

def make_ipbox():
	entries = {}
	ipEntry = Entry(f1)
	ipEntry.pack()
	ipEntry.insert(0,ip[0])
	ipEntry.place(x=180,y=225)
	entries['ip'] = ipEntry
	return entries


def download(event):
	print(port[0])
	file = str(event['handle'].get())
	print("downloading files")
	

	
	#try:
	
	#except:
		#text.delete(1.0,END)
		#text.insert(INSERT,"Connectivity problem")
	#print("downloading files")
	

	filename = file
	if filename !='q':
		#print("downloading files")
		s[0]=socket.socket()
		#print(port[0])
		s[0].connect(('192.168.0.102',port[0]))
		s[0].send('www/'+filename)
		#print("downloading files")
		data = s[0].recv(1024)
		#print("downloading files")
		if data=='File Exists':
			print "hello"
			data = s[0].recv(1024)
			try:
				filesize = long(data)
			except:
				print("some error occured plzz try again")
				exit(1)
			#print(filesize)
			#message = raw_input("press y/n")
			#if message=='y':
			#s.send('OK')
			f = open('downloaded/'+filename,'wb')
			data = s[0].recv(1024)
			totalrecv = len(data)
			#print(len(data))
			#print(totalrecv)
			f.write(data)
			#text.delete(1.0,END)
			#text.insert(INSERT, "Recieving " + filename + "....\n")
			print("recieving....")
			while totalrecv<filesize:
				data = s[0].recv(1024)
				totalrecv = totalrecv + len(data)
				f.write(data)
				print("recieving....")
				#text.insert(INSERT, "Recieving " + filename + "....\n")
				#print "{0:.2f}".format((totalrecv/float(filesize))*100)+\
						#"% Done"
				
			print("download complete")
			#tkMessageBox.showinfo("Status","Download Succssesfully completed")
		else:
			print("file dont exists with name "+filename)
			#text.delete(1.0,END)
			#text.insert(INSERT,"Sorry there is not any file with name " + filename + "\n")
			#text.insert(INSERT,"Please try other files")
	#s[0]=socket.socket()
	#print(port[0])
	#s[0].connect(('127.0.0.1',port[0]))
	#print("connection closed")
	#s.close()




os.startfile("server.py")

root = Tk()
root.geometry("500x500")
root.title("HubPort")
f1 = Frame(root,bg="black",height="500",width="500")
f2 = Frame(root,bg="black",height="500",width="500")
f3 = Frame(root)
f4 = Frame(root)

for frame in (f1,f2,f3,f4):
	frame.grid(row=0, column=0, sticky='news')

title = Message(f1,text="WELCOME TO HUBPORT")
title.config(font=('times', 24, 'italic'),width="500",bg="black",fg="white")
ent = make_portbox()
ip = make_ipbox()

print(ent['port'].get())
portButton = Button(f1,text="Connect",command=lambda e=ent,i=ip:connect(e,i))
portButton.pack()
portButton.place(x=210,y=260)
title.pack()
title.place(x=40,y=10)

raise_frame(f1)



portNotify = Message(f2)
portNotify.config(font=('times',24,'italic'),fg="white",bg="black")
portNotify.pack()

disconnectButton = Button(f2,text="Disconnect",command=lambda:disconnect())
disconnectButton.pack()
disconnectButton.place(x=210,y=220)
ents = makeform()

downloadButton =Button(f2,text="Download",command=lambda e=ents:download(e))
downloadButton.pack()
downloadButton.place(x=180,y=158)




root.mainloop()
