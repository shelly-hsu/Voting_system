import socket
from tkinter import *
import tkinter.font as tkFont
from functools import partial
import pickle 
import threading


client_num = 0
host = '127.0.0.1'
port = 1233

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Waiting for connection')



try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print("error")
Response = ClientSocket.recv(1024)
print(Response.decode())


class client_window():

    def __init__(self):
        self.t1 = threading.Thread(target=self.server_handler)
        self.t1.start()
        self.main_window()
        

    def main_window(self):
        self.window = Tk()
        self.window.title("voting system")
        self.window.geometry("600x600")
        fontStyle = tkFont.Font(size=40)        
        labelTitle = Label(self.window, text="投票系統", font=fontStyle).place(x=180,y=60)
        self.button0 = Button(self.window, text="候選人1",command=partial(self.buttons_handler,0))       
        self.button0.place(x= 110, y=300)
        self.label0 = Label(self.window, text="0",font=fontStyle)
        self.label0.place(x=115,y=200)
        self.button1 = Button(self.window, text="候選人2",command=partial(self.buttons_handler,1))
        self.button1.place(x= 190, y=300)
        self.label1 = Label(self.window, text="0", font=fontStyle)
        self.label1.place(x=195,y=200)
        self.button2 = Button(self.window, text="候選人3",command=partial(self.buttons_handler,2))
        self.button2.place(x= 270, y=300)
        self.label2 = Label(self.window, text="0", font=fontStyle)
        self.label2.place(x=275,y=200)
        self.button3 = Button(self.window, text="候選人4",command=partial(self.buttons_handler,3))
        self.button3.place(x= 350, y=300)
        self.label3 = Label(self.window, text="0", font=fontStyle)
        self.label3.place(x=355,y=200)
        self.button4 = Button(self.window, text="候選人5",command=partial(self.buttons_handler,4))
        self.button4.place(x= 430, y=300)
        self.label4 = Label(self.window, text="0", font=fontStyle)
        self.label4.place(x=435,y=200)
        self.ExitButton = Button(self.window, text="Exit",command=partial(self.buttons_handler,5))
        self.ExitButton.place(x=270,y=400) 
        self.label_list = [self.label0,self.label1,self.label2,self.label3,self.label4]
        self.window.mainloop()
     
    def label_handler(self,votes):
        self.label0.config(text=votes[0])
        self.label1.config(text=votes[1])
        self.label2.config(text=votes[2])
        self.label3.config(text=votes[3])
        self.label4.config(text=votes[4])   

    def server_handler(self):
        while True:
            print("server_handler")
            recvd_data_votes = ClientSocket.recv(1024)
        
            if recvd_data_votes:
                Response_votes = pickle.loads(recvd_data_votes)
                self.label_handler(Response_votes)
                print(Response_votes)

            recvd_data_client_num = ClientSocket.recv(1024)
            if recvd_data_client_num:
                client_num = int(recvd_data_client_num.decode())
                print(client_num)
                if client_num == 0:
                    print("wait")
                    self.show_result(Response_votes)
                    break
    
    def buttons_handler(self,num):
        ClientSocket.send(str(num).encode())
        if num == 5:
           self.switch()

    def switch(self):
        self.button0["state"] = "disabled"
        self.button1["state"] = "disabled"
        self.button2["state"] = "disabled"
        self.button3["state"] = "disabled"
        self.button4["state"] = "disabled"
        self.ExitButton["state"] = "disabled"
        fontStyle = tkFont.Font(size=20) 
        self.result_label = Label(self.window,text="waiting for the result...",font=fontStyle)
        self.result_label.place(x=170,y=450)

    def show_result(self,Votes):
         max_value = max(Votes)
         winner_idx = Votes.index(max_value)
         self.label_list[winner_idx].config(fg="red")
         num = str(winner_idx+1)
         self.result_label.config(text="恭喜候選人"+ num +"當選 ! ! !", fg = "red")
         
c = client_window()

ClientSocket.close()