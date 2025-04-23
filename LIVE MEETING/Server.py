import socket
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk,ImageGrab
from tkinter import Label, Tk, PhotoImage
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

server_socket_screen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_screen.bind((SERVER_HOST, SERVER_PORT_SCREEN))
server_socket_screen.listen()

server_socket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_video.bind((SERVER_HOST, SERVER_PORT_VIDEO))
server_socket_video.listen()

server_socket_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_audio.bind((SERVER_HOST, SERVER_PORT_AUDIO))
server_socket_audio.listen()

client_socket_screen, client_address_screen = server_socket_screen.accept()
client_socket_video, client_address_video = server_socket_video.accept()
client_socket_audio, client_address_audio = server_socket_audio.accept()

screen_sharing_enabled = threading.Event()
video_sharing_enabled = threading.Event()
audio_sharing_enabled = threading.Event()

root = None
label_screen = None

AUDIO_CHUNK = 1024
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS = 2

def receive_screen():
    global label_screen

    while True:
        try:
            size_data = client_socket_screen.recv(4)
            if not size_data:
                break
            size = int.from_bytes(size_data, byteorder='big')

            received_data = b""
            while len(received_data) < size:
                data_chunk = client_socket_screen.recv(min(size - len(received_data), 4096))
                if not data_chunk:
                    break
                received_data += data_chunk

            if len(received_data) < size:
                continue

            image = Image.open(BytesIO(received_data))
            photo = ImageTk.PhotoImage(image)

            label_screen.config(image=photo)
            label_screen.image = photo  # keep a reference to the image

            root.event_generate('<<UpdateImage>>', when='tail')  # Trigger image update event

        except Exception as e:
            print(e)
            break
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        client_socket_screen.close()
        client_socket_video.close()
        client_socket_audio.close()
        root.destroy()

def update_image(event):
    try:
        old_image = label_screen.image

        new_image = ImageTk.PhotoImage(old_image)

        label_screen.config(image=new_image)

        label_screen.image = new_image

        old_image.__del__()
    except AttributeError:
        pass




def start_video_sharing_client():
    global video_sharing_enabled
    video_sharing_enabled = True
    vid = cv2.VideoCapture(0)
    while video_sharing_enabled:
        try:
            # Capture video frame and send it to the client
            _, frame = vid.read()
            data = pickle.dumps(frame)
            message = struct.pack("Q", len(data)) + data
            client_socket_video.sendall(message)
        except Exception as e:
            print(e)
            break

def toggle_video_sharing_client():
    threading.Thread(target=start_video_sharing_client).start()

def receive_video_client():
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

def receive_audio():
    while audio_sharing_enabled.is_set():
        try:
            audio_data_size = client_socket_audio.recv(4)
            if not audio_data_size:
                break
            size = int.from_bytes(audio_data_size, byteorder='big')

            received_data = b""
            while len(received_data) < size:
                data_chunk = client_socket_audio.recv(min(size - len(received_data), 4096))
                if not data_chunk:
                    break
                received_data += data_chunk

            if len(received_data) < size:
                continue

            # Play the received audio
            sd.play(np.frombuffer(received_data, dtype=np.int16), samplerate=AUDIO_SAMPLE_RATE, channels=AUDIO_CHANNELS)
            sd.wait()

        except Exception as e:
            print(e)
            break

def capture_and_send_video():
    global client_socket_video

    cap = cv2.VideoCapture(0)  # Open the camera (0 is the default camera)

    while video_sharing_enabled.is_set():
        ret, frame = cap.read()

        # Serialize the frame and send it to the client
        frame_data = pickle.dumps(frame)
        message_size = struct.pack("Q", len(frame_data))
        client_socket_video.sendall(message_size + frame_data)

    cap.release()


def toggle_screen_sharing():
    screen_sharing_enabled.set()
    print("Screen Sharing enabled")

def toggle_video_sharing():
    video_sharing_enabled.set()
    print("Video Sharing enabled")

def toggle_audio_sharing():
    audio_sharing_enabled.set()
    print("Audio Sharing enabled")

def stop_screen_sharing():
    screen_sharing_enabled.clear()
    print("Screen Sharing disabled")

def stop_video_sharing():
    video_sharing_enabled.clear()
    print("Video Sharing disabled")

def stop_audio_sharing():
    audio_sharing_enabled.clear()
    print("Audio Sharing disabled")
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

def start_server():
    global root, label_screen

    root = tk.Tk()
    root.title("Screen, Video, and Audio Sharing Server")
    root.geometry("800x600")

    label_screen = tk.Label(root)
    label_screen.pack(expand="true")
    video_thread_client = threading.Thread(target=start_video_sharing_client)
    video_thread_client.start()

    receive_video_thread_client = threading.Thread(target=receive_video_client)
    receive_video_thread_client.start()

    screen_sharing_button = tk.Button(root, text="Toggle Screen Sharing", command=toggle_screen_sharing,width=20,height=2, bg="#4CAF50", fg="white")
    screen_sharing_button.pack(pady=10)

    video_sharing_button = tk.Button(root, text="Toggle Video Sharing", command=toggle_video_sharing,width=20,height=2,bg="#3498db", fg="white")
    video_sharing_button.pack(pady=10)

    audio_sharing_button = tk.Button(root, text="Toggle Audio Sharing", command=toggle_audio_sharing,width=20,height=2,bg="#e74c3c", fg="white")
    audio_sharing_button.pack(pady=10)
    
    screen_thread = threading.Thread(target=receive_screen)
    screen_thread.start()

    audio_thread = threading.Thread(target=receive_audio)
    audio_thread.start()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.bind('<<UpdateImage>>', update_image)
    root.mainloop()

# Start the server
start_server()