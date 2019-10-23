import tkinter as tk
from tkinter import font
from src.interface import interpreter

WIDTH = 800
HEIGHT = 600
class GUI ():

    def __init__ (self):
        self.GUI_interpreter = interpreter.interpreter()

    def try_login (self, username, password):
        try:
            self.GUI_interpreter.login(username, password)
        except:
            self.login_msg['text'] = 'Wrong username or password.'
        else:
            self.user_type = username
            self.user_login.destroy()
            return

    def execute_command (self, command_str):
        try:
            self.response = self.GUI_interpreter.execute(command_str)
        except:
            command_response = 'Invalid command.'
        else:
            command_response = self.response

        self.scrollbar = tk.Scrollbar(self.command_frame)
        self.scrollbar.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.5, anchor='n')
        response_list = tk.Listbox(self.command_frame, yscrollcommand=self.scrollbar.set)
        try:
            list_of_user = command_response.split('\n\n')
        except AttributeError:
            list_of_user = ['You do not have access to this command.']
        for element in list_of_user:
            response_list.insert(tk.END, element)
        response_list.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.5, anchor='n')
        self.scrollbar.config(command=response_list.yview)

    def print_help (self):
        self.help = tk.Tk()

        canvas = tk.Canvas(self.help, height=HEIGHT, width=WIDTH)
        canvas.pack()

        frame = tk.Frame(self.help, bg='gray', bd=5)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        button=tk.Button(frame, text="Quit", fg='red', command=lambda: self.quit_help())
        button.place(relx=0.1, rely=0.95, relwidth=0.1, relheight=0.05, anchor='n')

        self.help_msg = tk.Label(frame, font=('Courier', 12))
        self.help_msg.place(relx=0.5, rely=0, relwidth=0.9, relheight=0.9, anchor='n')

        self.help_msg['text'] = 'Available commands are: \n\n' + self.GUI_interpreter.print_command_table()
        
        self.help.mainloop()

    def quit_help (self):
        self.help.destroy()

    def login_page(self):
        self.loging_in = True

        self.user_login = tk.Tk()

        canvas = tk.Canvas(self.user_login, height=HEIGHT, width=WIDTH)
        canvas.pack()

        frame = tk.Frame(self.user_login, bg='gray', bd=5)
        frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.5, anchor='n')

        login = tk.Entry(frame)
        login.place(relx=0.45, rely=0.3, relwidth=0.5, relheight=0.1, anchor='n')

        password = tk.Entry(frame, show='*')
        password.place(relx=0.45, rely=0.45, relwidth=0.5, relheight=0.1, anchor='n')

        button=tk.Button(frame, text="Login", command=lambda: self.try_login(login.get(), password.get()))
        button.place(relx=0.8, rely=0.3, relwidth=0.1, relheight=0.25, anchor='n')

        self.login_msg = tk.Label(frame, fg='red', bg='gray', font=('Courier', 12))
        self.login_msg.place(relx=0.5, rely=0.6, relwidth=0.5, relheight=0.1, anchor='n')
        
        self.user_login.mainloop()

        return self.user_type

    def load_root_page (self):

        self.root_page = tk.Tk()

        canvas = tk.Canvas(self.root_page, height=HEIGHT, width=WIDTH)
        canvas.pack()

        self.command_frame = tk.Frame(self.root_page, bg='gray', bd=0.5)
        self.command_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        command = tk.Entry(self.command_frame)
        command.place(relx=0.5, rely=0.9, relwidth=0.5, relheight=0.05, anchor='n')

        button=tk.Button(self.command_frame, text="Execute", command=lambda: self.execute_command(command.get()))
        button.place(relx=0.82, rely=0.9, relwidth=0.1, relheight=0.05, anchor='n')

        help_me = tk.Button(self.command_frame, text="Help me", command=lambda: self.print_help())
        help_me.place(relx=0.1, rely=0.9, relwidth=0.1, relheight=0.05, anchor='nw')

        self.root_page.mainloop()


if __name__ == "__main__":
    my_gui = GUI()
    my_gui.login_page()
    my_gui.load_root_page()
    