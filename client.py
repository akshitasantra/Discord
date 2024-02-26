import socket
import threading
import tkinter
import tkinter.scrolledtext


class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        msg = tkinter.Tk()
        msg.withdraw()



        self.gui_done = False
        self.running = True

        # Starting Threads For Listening And Writing

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.start()


    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=5)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    # Sending Messages To Server
    def write(self):
        message = '{}: {}'.format(self.nickname, self.input_area.get('1.0', 'end'))
        self.sock.send(message.encode('ascii'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    # Listening to Server and Sending Nickname
    def receive(self):
        while True:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = self.sock.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('ascii'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except:
                # Close Connection When Error
                print("An error occurred!")
                self.sock.close()
                break

    def connect(self, root, ip, port):
        root.destroy()
        self.sock = sock.connect(ip, port)






client = Client()


