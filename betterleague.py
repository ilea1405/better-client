import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import pyautogui
import time
import threading
import cv2
import numpy as np


league_path = "C:/Riot Games/League of Legends/LeagueClient.exe"



# Global flag to control the loop
running = True

def is_league_installed():
    global league_path
    if os.path.exists(league_path):
        print("League of Legends is installed on this PC.")
        return True
    else:
        print("League of Legends is not installed on this PC.")
        league_path = filedialog.askopenfilename(title="Select LeagueClient.exe")
        if league_path:
            print("LeagueClient.exe file selected:", league_path)
        else:
            print("No file selected.")
        return False
        
def draw_buttons():
    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12, 'bold'), borderwidth='4')
    style.configure('TLabel', background='red', font=('Helvetica', 12, 'bold'))

    start_game_button = ttk.Button(window, text="Start Game", command=open_league)
    accept_game_button = ttk.Button(window, text="Accept Game", command=accept_game)
    quit_league_button = ttk.Button(window, text="Quit League", command=quit_league)

    start_game_button.pack(pady=10)
    accept_game_button.pack(pady=10)
    quit_league_button.pack(pady=10)
    
def open_league():
    global league_path
    print(league_path)
    print("Start Game button clicked")
    # open the LeagueClient.exe file
    os.startfile(league_path)

def accept_game():
    def locate_and_click():
        global running
        running = True
        seconds = 0
        MIN_MATCH_COUNT = 10

        # Load the image file
        accept_img = cv2.imread('accept.png', 0)
        sift = cv2.xfeatures2d.SIFT_create()

        # Find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(accept_img, None)

        while running:
            try:
                # Update the status label
                status_label.config(text="Accepting", bg="green")

                # Capture a screenshot
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

                # Find the keypoints and descriptors with SIFT
                kp2, des2 = sift.detectAndCompute(screenshot, None)

                # FLANN parameters
                FLANN_INDEX_KDTREE = 0
                index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
                search_params = dict(checks=50)

                flann = cv2.FlannBasedMatcher(index_params, search_params)
                matches = flann.knnMatch(des1, des2, k=2)

                # Store all the good matches as per Lowe's ratio test.
                good = []
                for m, n in matches:
                    if m.distance < 0.7 * n.distance:
                        good.append(m)

                if len(good) > MIN_MATCH_COUNT:
                    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

                    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                    matchesMask = mask.ravel().tolist()

                    h, w = accept_img.shape
                    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                    dst = cv2.perspectiveTransform(pts, M)

                    center_location = (int(np.mean(dst[:, 0, 0])), int(np.mean(dst[:, 0, 1])))
                    for _ in range(3):  # Click 3 times
                        pyautogui.click(center_location)
                        time.sleep(0.5)  # Wait for 0.5 seconds
                    print("done clicking")

                    # Stop the search and update the status label
                    running = False
                    status_label.config(text="Not accepting", bg="red")
                    return
            except Exception as e:
                print(f"An error occurred: {e}")
            time.sleep(1)
            seconds += 1
            if seconds == 10:
                # Update the status label
                status_label.config(text="Not accepting", bg="red")
                return False

    # Create a new thread for the image recognition task
    thread = threading.Thread(target=locate_and_click)
    thread.start()

def quit_league():
    print("Quit League button clicked")
    # close the LeagueClient.exe file
    os.system('taskkill /f /im "LeagueClient.exe"')
    os.system('taskkill /f /im "RiotClientServices.exe"')
    time.sleep(0.25)

def on_close():
    global running
    running = False
    window.destroy()

# Create the tkinter window
window = tk.Tk()
window.title("Better League")
window.configure(bg="gray")
window.geometry("300x200")  # Set the window size to 200x200
# Add this line after creating your window
status_label = tk.Label(window, text="Not accepting", bg="red")
status_label.pack()
draw_buttons()
is_league_installed()

# Bind the on_close function to the close event
window.protocol("WM_DELETE_WINDOW", on_close)

# Start the tkinter event loop
window.mainloop()