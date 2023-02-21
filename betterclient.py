import tkinter as tk
import os, pyautogui, time, threading
from tkinter import filedialog, messagebox

# Set the file path for the text file containing account information
ACCOUNTS_FILE = 'accounts.txt'

def find_client():
    global file_path
    file_path = filedialog.askopenfilename(initialdir="C:/", title="Select LeagueClient.exe", filetypes=(("League of Legends Client", "LeagueClient.exe"), ("all files", "*.*")))
            
    # Check that the user selected the correct file
    if os.path.basename(file_path) == "LeagueClient.exe":
        print(file_path)
    else:
        file_path = None
    with open('path.txt', 'w') as f:
        f.write(file_path)

def start_client():
    global res
    f = open("path.txt", "r")
    if f is not None:
        res = f.read()
        os.startfile(res)

# Define the function to close the League of Legends client
def close_client():
    global res
    os.system('taskkill /f /im "LeagueClient.exe"')
    os.system('taskkill /f /im "RiotClientServices.exe"')
    time.sleep(2)
    os.startfile(res)

# Define the function to handle button clicks
def handle_click(account):
    # Load the account information from the text file
    with open(ACCOUNTS_FILE, 'r') as f:
        for line in f:
            if account in line:
                username, password = line.strip().split(':')[1:]
                break
        else:
            messagebox.showerror('Error', f'Account "{account}" not found in file')
            return

    # Log in to the League of Legends client with the account information
    login(username, password)

# Define the function to log in to the League of Legends client with the given credentials
def login(username, password):
    username_box = pyautogui.locateCenterOnScreen("username_box.png")
    pyautogui.click(username_box)
    pyautogui.write(username)
    pyautogui.press('tab')
    pyautogui.write(password)
    pyautogui.press('enter')

def auto_accept():
    accept_but = None
    while (accept_but == None):
            time.sleep(1)
            accept_but = pyautogui.locateCenterOnScreen("accept.png", grayscale=True, confidence=0.5)
    pyautogui.click(accept_but)

def open_file():
    os.startfile('accounts.txt')


root = tk.Tk()
root.geometry("500x500")
root.title('BetterClient')

frame = tk.Frame(master=root)
frame.pack(pady=10, padx=10)

accounts_frame = tk.Frame(master=root)
accounts_frame.pack(pady=10, padx=10)

# Create the buttons
find_button = tk.Button(master=frame, text='Find Client', command=find_client)
find_button.pack(pady=10, padx=10)
start_button = tk.Button(master=frame, text='Start Client', command=start_client)
start_button.pack(pady=10, padx=10)
accept_button = tk.Button(master=frame, text='Auto Accept Game', command=auto_accept)
accept_button.pack(pady=10, padx=10)
close_button = tk.Button(master=frame, text='Dodge', command=close_client)
close_button.pack(pady=10, padx=10)
open_button = tk.Button(master=frame, text='Open Accounts File', command=open_file)
open_button.pack(pady=10, padx=10)

# Create the account login buttons
account_buttons_frame = tk.Frame(master=accounts_frame)
account_buttons_frame.pack()

with open(ACCOUNTS_FILE, 'r') as f:
    for line in f:
        account = line.strip().split(':')[0]
        button = tk.Button(account_buttons_frame, text=account, command=lambda account=account: handle_click(account))
        button.pack(side='left', pady=10, padx=10)



# Start the main event loop
root.mainloop()