import socket
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageGrab
import cv2
import pickle
import struct
from io import BytesIO
import sounddevice as sd
import numpy as np

SERVER_HOST = '192.168.194.207'
SERVER_PORT_SCREEN = 5051
SERVER_PORT_VIDEO = 9999
SERVER_PORT_AUDIO = 5052

AUDIO_CHUNK = 1024
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS = 2

client_socket_screen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_screen.connect((SERVER_HOST, SERVER_PORT_SCREEN))

client_socket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_video.connect((SERVER_HOST, SERVER_PORT_VIDEO))

client_socket_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_audio.connect((SERVER_HOST, SERVER_PORT_AUDIO))

screen_sharing_enabled = False
video_sharing_enabled = False
audio_sharing_enabled = False

root = None
label_screen = None
label_video = None


def start_screen_sharing():
    global screen_sharing_enabled
    while True:
        try:
         
            screen = ImageGrab.grab()
            screen = screen.resize((600, 400))
            photo = ImageTk.PhotoImage(screen)
            label_screen.config(image=photo)
            label_screen.image = photo
            photo_data = BytesIO()
            screen.save(photo_data, format='JPEG')
            photo_data = photo_data.getvalue()
            size = len(photo_data).to_bytes(4, byteorder='big')
            client_socket_screen.sendall(size + photo_data)
        except Exception as e:
            print(e)
            break


def start_video_sharing():
    global video_sharing_enabled
    video_sharing_enabled = True
    vid = cv2.VideoCapture(0)
    while video_sharing_enabled:
        try:
            # Capture video frame and send it to the server
            _, frame = vid.read()
            data = pickle.dumps(frame)
            message = struct.pack("Q", len(data)) + data
            client_socket_video.sendall(message)
        except Exception as e:
            print(e)
            break



def receive_video():
    while True:
        try:
            data_size = client_socket_video.recv(8)
            if not data_size:
                break
            msg_size = struct.unpack("Q", data_size)[0]

            data = b""
            while len(data) < msg_size:
                packet = client_socket_video.recv(min(msg_size - len(data), 4 * 1024))
                if not packet:
                    break
                data += packet

            if len(data) < msg_size:
                continue

            frame_data = data[:msg_size]
            frame = pickle.loads(frame_data)
            cv2.imshow('RECEIVING VIDEO', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(e)
            break
def start_audio_sharing():
    global audio_sharing_enabled
    audio_sharing_enabled = True
    with sd.OutputStream(samplerate=AUDIO_SAMPLE_RATE, channels=AUDIO_CHANNELS, dtype=np.int16) as stream:
        while audio_sharing_enabled:
            try:
                audio_chunk, overflowed = stream.read(AUDIO_CHUNK)
                audio_data = audio_chunk.tobytes()
                size = len(audio_data).to_bytes(4, byteorder='big')
                client_socket_audio.sendall(size + audio_data)
                print(f"Sent audio data size: {len(size + audio_data)}")
            except Exception as e:
                print(f"Audio send error: {e}")
                break

def toggle_screen_sharing():
    threading.Thread(target=start_screen_sharing).start()

def toggle_video_sharing():
    threading.Thread(target=start_video_sharing).start()
    threading.Thread(target=receive_video).start()

def toggle_audio_sharing():
    threading.Thread(target=start_audio_sharing).start()

def stop_screen_sharing():
    global screen_sharing_enabled
    screen_sharing_enabled = False

def stop_video_sharing():
    global video_sharing_enabled
    video_sharing_enabled = False

def stop_audio_sharing():
    global audio_sharing_enabled
    audio_sharing_enabled = False

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        client_socket_screen.close()
        client_socket_video.close()
        client_socket_audio.close()
        root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Screen, Video, and Audio Sharing Client")
root.geometry("800x600")

label_screen = tk.Label(root)
label_screen.pack(expand="true")

label_video = tk.Label(root)
label_video.pack(expand="true")


start_screen_sharing_button = tk.Button(root, text="Start Screen Sharing", command=toggle_screen_sharing,width=20, height=2, bg="#4CAF50", fg="white")
start_screen_sharing_button.pack(pady=10)


stop_screen_sharing_button = tk.Button(root, text="Stop Screen Sharing", command=stop_screen_sharing, width=20, height=2,bg="#e74c3c", fg="white")
stop_screen_sharing_button.pack(pady=10)

start_video_sharing_button = tk.Button(root, text="Start Video Sharing", command=toggle_video_sharing, width=20, height=2,bg="#3498db", fg="white")
start_video_sharing_button.pack(pady=10)

stop_video_sharing_button = tk.Button(root, text="Stop Video Sharing", command=stop_video_sharing, width=20, height=2,bg="#e74c3c", fg="white")
stop_video_sharing_button.pack(pady=10)

start_audio_sharing_button = tk.Button(root, text="Start Audio Sharing", command=toggle_audio_sharing, width=20, height=2,bg="#3498db", fg="white")
start_audio_sharing_button.pack(pady=10)

stop_audio_sharing_button = tk.Button(root, text="Stop Audio Sharing", command=stop_audio_sharing, width=20, height=2,bg="#e74c3c", fg="white")
stop_audio_sharing_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()