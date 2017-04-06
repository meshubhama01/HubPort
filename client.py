import socket
from Tkinter import *
import tkMessageBox
import os
import pickle

#connectivity setup initialises
port = [3500] 
ip = ['127.0.0.1']
s=[socket.socket()]

#change frame on calling
def raise_frame(frame):
	frame.tkraise()

#connect to a open socket
def connect(event,ip):
	#initial requirement for a socket
	s[0]=socket.socket()
	port[0] = int(event['port'].get())
	ip[0] = ip['ip'].get()

	try:
		s[0].connect((ip[0],port[0]))
		f2.tkraise()
		portNotify.config(text="Connected to " + ip[0] + ":" + str(port[0]))
		portNotify.config(width="500")
		host = s[0].recv(1024) #recieves the host name
		dir = s[0].recv(1024)
		dir = pickle.loads(dir)
		for item in dir[1]:
			textList.insert(END,item)
		#print( pickle.loads(dir))
		hostname.config(text="Host:- "+ str(host) )
		hostname.config(width="500")
		exploreFrom.config(text="Exploring files of "+ str(host))
		exploreFrom.config(width="500")
		return s
	except:
		tkMessageBox.showinfo("Status","There is a network error.This can be because the network you wanna join may to be open\nTry another network")
		disconnect()

def disconnect(): 
	#clos the socket
	print("disconnected")
	s[0].close()
	raise_frame(f1)#get back to the home page


#create text box to insert the file you want to download
def makeform():
   entries = {}
   ent = Entry(f2)
   ent.insert(0,"0")
   ent.pack()
   entries['handle'] = ent
   ent.place(x=180,y=130)
   return entries

#textbox to enter port
def make_portbox():
	entries = {}
	portEntry = Entry(f1)
	portEntry.pack()
	portEntry.insert(0,port[0])
	portEntry.place(x=180,y=180)
	entries['port'] = portEntry
	return entries

#textbox to enter ip address
def make_ipbox():
	entries = {}
	ipEntry = Entry(f1)
	ipEntry.pack()
	ipEntry.insert(0,ip[0])
	ipEntry.place(x=180,y=225)
	entries['ip'] = ipEntry
	return entries

#function to download any file
def download(event):
	file = str(event['handle'].get())
	filename = file
	#create a new socket to download as if we will send the same request again and again to the server
	#but there is not possible for server to respond them as they have less numer of response per socket
	s[0]=socket.socket()
	s[0].connect((ip[0],port[0]))
	host = s[0].recv(1024) #reecieves host name
	if filename !='q':
		s[0].send('www/'+filename) #send the required path of the file to the server
		data = s[0].recv(1024) 
		print(data)#recieves the status of the file weather it exsiss or not
		if data=='File Exists':
			print "hello"
			data = s[0].recv(1024) #if file exists get the size of the file
			try:
				filesize = long(data)
			except:
				print("some error occured plzz try again")
				exit(1)

			#create the same file in the download directory
			f = open('downloaded/'+filename,'wb')
			data = s[0].recv(1024) #recieve the 1024 byte of the requested file data
			totalrecv = len(data)
			f.write(data) 
			print("recieving data....")
			while totalrecv<filesize: #get all the bytes of the file  data
				data = s[0].recv(1024)
				totalrecv = totalrecv + len(data)
				f.write(data)
				print("recieving....")
			tkMessageBox.showinfo("Download","Download Succssesfully completed")
		else:
			tkMessageBox.showinfo("Download","File not exsists\nTry another file")




os.startfile("server.py") #on starting a client gui ur server allready starts

#set up root geometry
root = Tk()
root.geometry("500x500")
root.title("HubPort")

#define frames
f1 = Frame(root,bg="black",height="500",width="500")
f2 = Frame(root,bg="black",height="500",width="500")
f3 = Frame(root,bg="black",height="500",width="500")
#position frames
for frame in (f1,f2,f3):
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

hostname = Message(f2)
hostname.config(font=('times',20,'italic'),fg="white",bg="black")
hostname.pack()

disconnectButton = Button(f2,text="Disconnect",command=lambda:disconnect())
disconnectButton.pack()
disconnectButton.place(x=210,y=220)
ents = makeform()

downloadButton =Button(f2,text="Download",command=lambda e=ents:download(e))
downloadButton.pack()
downloadButton.place(x=180,y=158)

exploreButton = Button(f2,text="Explore Files",command=lambda:raise_frame(f3))
exploreButton.pack()
exploreButton.place(x=210,y=325)

exploreFrom = Message(f3)
exploreFrom.config(font=('times',24,'italic'),fg="white",bg="black")
exploreFrom.pack()

textList = Listbox(f3)
textList.pack()








root.mainloop()
