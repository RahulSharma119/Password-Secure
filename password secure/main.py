import csv
from random import random
import tkinter as tk
from tkinter.ttk import Radiobutton


#GUI app class
class App(tk.Tk):
    def __init__(self) :
        super().__init__()
        self.title("Password Protect")# setting the title on the window
        self.geometry('700x500')# setting the dimensions for the window

        self.home_frame = tk.Frame(self) # the home screen when the app opens

        self.store_btn = tk.Button(self.home_frame,text='Store Password',command=self.store_password)# button to go to interface for storing password
        self.store_btn.pack()

        self.get_btn = tk.Button(self.home_frame,text='Show Password',command=self.get_password)# button to go to interface for getting the password
        self.get_btn.pack()

        self.home_frame.pack(fill='both',anchor=tk.CENTER)#finally show the home page

    def store_password(self):
        self.home_frame.pack_forget()# to remove the home screen

        self.store_frame = tk.Frame(self)# to screen for storing password

        #encryotion key input declare
        key_label = tk.Label(self.store_frame,text="Encryption Key  ",bd=10)
        key_label.pack()
        self.key_input=tk.Entry(self.store_frame, text="", bd=10)
        self.key_input.pack()

        #Password input declare
        pass_label = tk.Label(self.store_frame,text="Password  ",bd=10)
        pass_label.pack()
        self.pass_input = tk.Entry(self.store_frame,text="",bd=10)
        self.pass_input.pack()

        #field for password input declare
        field_label = tk.Label(self.store_frame,text="Field For Password  ",bd=10)
        field_label.pack()
        self.field_input = tk.Entry(self.store_frame,text="",bd=10)
        self.field_input.pack()

        #section to display the error or output
        self.notice_label = tk.Label(self.store_frame,text="",bd=10)
        self.notice_label.pack()

        #btn to start storing the password
        submit_btn = tk.Button(self.store_frame,text="Store",command=self.encrypt_and_store)
        submit_btn.pack()
        self.store_frame.pack(fill='x')



    def get_password(self):
        self.home_frame.pack_forget()# to remove the home screen
        self.show_frame = tk.Frame(self)# to screen to show password

        err = self.get_fields()# declares as self.dict the fields and encrypted password or returns error
        if err:
            self.notice_label = tk.Label(self.show_frame,text=err,bd=10)#error shown in the screen
            self.notice_label.pack()
            self.show_frame.pack(fill='x')
            return

        #encryotion key input declare
        key_label = tk.Label(self.show_frame,text="Encryption Key  ",bd=10)
        key_label.pack()
        self.key_input=tk.Entry(self.show_frame, text="", bd=10)
        self.key_input.pack()

        #field radio-button input declare
        field_label = tk.Label(self.show_frame,text="Select Field of Password  ",bd=10)
        field_label.pack()
        self.field_input = tk.StringVar()#variable where selected radiobutton value will be stored
        self.field_input.set("")# setting initial value to empty string
        self.field_radio_button = []#list for radiobuttons 
        for key in self.dict:
            r = Radiobutton(self.show_frame,text=key,variable=self.field_input,value=key)#declaring each radio-button options
            r.pack()
            self.field_radio_button.append(r)

        #section to display the error or output
        self.notice_label = tk.Label(self.show_frame,text="",bd=10)
        self.notice_label.pack()
        
        #button to take inputs and get the output or error
        submit_btn = tk.Button(self.show_frame,text="Show",command=self.decrypt_and_show)
        submit_btn.pack()

        self.show_frame.pack(fill='x')
        


    def encrypt_and_store(self):
        self.notice_label['text'] = "" #setting initial output or error field empty
        key = self.key_input.get().strip()#getting the key to encrypt
        if key == "":#if key field is empty empty shows message in screen
            self.notice_label['text'] = "Please enter the Encryption Key."
            return
        password = self.pass_input.get().strip()#pass to encrypted
        if password == "":
            self.notice_label['text'] = "Please enter the Password."
            return
        field = self.field_input.get().strip().lower() #the field of password
        if field == "":
            self.notice_label['text'] = "Please enter the Field for Password."
            return
        try:
            file = open("./password_file.key","r+")
        except FileNotFoundError:
            file = open("./password_file.key",'w+')
        except OSError:
            self.notice_label['text'] = "Cannot open the password key file."
            return
        for line in csv.reader(file):
            if len(line) > 0 and line[0] == field:
                field = "" # if field already present then need another field
                break
        file.close()
        if field == "":
            self.notice_label['text'] = "Field Already Exists."
            # self.field_input['text'] = ""
            return
        file = open("./password_file.key","a")
        enpass = "" #encrypted password variable to be stored in file
        pos = ord(key[0])%20 #getting the position for the actual password to store among dummy letters
        for letter in password:
            letter = ord(letter) # converting the character to ascii value
            # print(letter,end=" ")
            for k in key:
                k = ord(k) # converting the character to ascii value
                letter = letter ^ k #xor of each password letter with every letter in key
            letter = chr(letter) # converting the ascii value to character
            crypt="" #to place actual character between dummy letters
            for i in range(0,pos):
                crypt += chr(int(random()*82)+45) # dummy letters with range 45 to 127
            crypt += letter
            for i in range(pos+1,20):
                crypt += chr(int(random()*82)+45)
            enpass += crypt
        writer = csv.writer(file)
        writer.writerow([field,enpass]) # appending the encrypted password to file eith field
        file.close()
        self.notice_label['text'] = "Successfully Stored the Password."


    # to declare the fields and encrypted passwords as self.dict 
    def get_fields(self):
        try:
            file = open("./password_file.key")
        except Exception as err:
            return err
        self.dict = {}
        for line in csv.reader(file):
            if len(line) > 0:
                field = line[0]
                enpass = ""
                i=1
                while i < len(line):
                    enpass += line[i]
                    i+=1
                self.dict[field] = enpass
        file.close()


    #to decrypt the password and show
    def decrypt_and_show(self):
        self.notice_label['text'] = ""
        key = self.key_input.get().strip()#getting the key to decrypt
        if key == "":# if key field is empty then a message is displayed
            self.notice_label['text'] = "Please enter the Encryption Key."
            return
        field = self.field_input.get()# getting the field whose password to decrypt
        if field == "":
            self.notice_label['text'] = "Please select the Field."
            return
        try:
            file = open("./password_file.key")
        except Exception as err:
            self.notice_label['text'] = "Cannot open the password key file."
            return
        enpass = self.dict[field]# the encrypted password
        password = ""
        pos = ord(key[0])%20 #getting the exact pos of the password chars between the dummy
        i = pos
        while i < len(enpass):
            # print(ord(enpass[i]),end=" ")
            letter = ord(enpass[i]) #converting encrypted letter to ascii 
            for k in key:
                k = ord(k)
                letter = letter ^ k #decrypting the letter
            password += chr(letter)
            i += 20
        self.notice_label['text'] = f"The Password for {field} is {password}"# showing the output in screen





if __name__ == "__main__":
    app = App()
    app.mainloop()
    # while(True):
    #     a = int(input("Enter\n1 - Store a password\n2 - Get a password\n0 - exit\n"))
    #     if a == 1:
    #         key = input("Enter the Encryption key: ").strip()#key to encrypt and decrypt
    #         password = input("Enter the password: ").strip()#pass to encrypt
    #         field = None #the domain of password
    #         while field == None:
    #             field = input("Enter the field for password: ").strip().lower()
    #             try:
    #                 file = open("./password_file.key","r+")
    #             except FileNotFoundError:
    #                 file = open("./password_file.key",'w+')
    #             except OSError:
    #                 print("Cannot open the password key file.")
    #                 sys.exit(1)
    #             for line in csv.reader(file):
    #                 if len(line) > 0 and line[0] == field:
    #                     field = None
    #                     break
    #             file.close()
    #             if field == None:
    #                 print("Field Already Exists.")
    #                 continue
    #             file = open("./password_file.key","a")
    #             enpass = "" #encrypted password to be stored in file
    #             pos = ord(key[0])%20
    #             for letter in password:
    #                 letter = ord(letter)
    #                 # print(letter,end=" ")
    #                 for k in key:
    #                     k = ord(k)
    #                     letter = letter ^ k
    #                 letter = chr(letter)
    #                 crypt="" #encrypt for each character in actual password
    #                 for i in range(0,pos):
    #                     crypt += chr(int(random()*82)+45)
    #                 crypt += letter
    #                 for i in range(pos+1,20):
    #                     crypt += chr(int(random()*82)+45)
    #                 enpass += crypt
    #             writer = csv.writer(file)
    #             writer.writerow([field,enpass])
    #             file.close()
    #     elif a == 2:
    #         key = input("Enter the Encryption key: ")#key to encrypt and decrypt
    #         field = input("Enter the field for password: ").strip().lower()
    #         try:
    #             file = open("./password_file.key")
    #         except Exception as err:
    #             print(f"{err}")
    #             sys.exit(1)
    #         enpass = ""
    #         for line in csv.reader(file):
    #             if len(line) > 0 and line[0] == field:
    #                 i=1
    #                 while i < len(line):
    #                     enpass += line[i]
    #                     i+=1
    #                 break
    #         file.close()
    #         if enpass == "":
    #             print("Field did not match any in document try again!!")
    #         else:
    #             password = ""
    #             pos = ord(key[0])%20
    #             i = pos
    #             while i < len(enpass):
    #                 # print(ord(enpass[i]),end=" ")
    #                 letter = ord(enpass[i]) 
    #                 for k in key:
    #                     k = ord(k)
    #                     letter = letter ^ k
    #                 password += chr(letter)
    #                 i += 20
    #             print(password)
    #     else:
    #         break
