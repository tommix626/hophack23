import tkinter as tk
import cv2
from tkinter import ttk
from tkinter import PhotoImage
import threading

from yolo import ObjectTracker


def start_camera_feed():
    # Function to start the camera feed

    def update_camera_feed():
        _, frame = cap.read()
        if frame is not None:
            # Convert the OpenCV frame to a PhotoImage
            new_frame, _ = ot.get_rect(frame)
            photo = cv2_to_photoimage(new_frame)
            camera_label.config(image=photo)
            camera_label.image = photo  # Keep a reference
        if camera_running:
            camera_label.after(10, update_camera_feed)  # Update every 10 milliseconds

    global camera_running
    camera_running = True

    # Create a thread for the camera feed update
    cap = cv2.VideoCapture(0)  # Use the default camera (usually index 0)
    camera_thread = threading.Thread(target=update_camera_feed)
    camera_thread.daemon = True  # Set the thread as a daemon to exit when the main program exits
    camera_thread.start()


def stop_camera_feed():
    global camera_running
    camera_running = False

    # Update the camera label with a blank image
    blank_image = tk.PhotoImage(width=640, height=480)
    camera_label.config(image=blank_image)
    camera_label.image = blank_image


def cv2_to_photoimage(cv2_image):
    # Convert an OpenCV image (BGR format) to a PhotoImage
    return PhotoImage(data=cv2.imencode('.ppm', cv2_image)[1].tobytes())


def exit_program():
    stop_camera_feed()
    cap.release()  # Release the camera
    window.destroy()

ot = ObjectTracker()

# Create the main window
window = tk.Tk()
window.title("Webcam Feed Example")

# Create a button to start the camera feed
start_button = ttk.Button(window, text="Start Camera Feed", command=start_camera_feed)
start_button.pack()

# Create a button to stop the camera feed
stop_button = ttk.Button(window, text="Stop Camera Feed", command=stop_camera_feed)
stop_button.pack()

# Create a label to display the camera feed
camera_label = tk.Label(window)
camera_label.pack()

# Create an exit button
exit_button = ttk.Button(window, text="Exit", command=exit_program)
exit_button.pack()

# Initialize camera_running flag
camera_running = False

# Start the GUI main loop
window.mainloop()
