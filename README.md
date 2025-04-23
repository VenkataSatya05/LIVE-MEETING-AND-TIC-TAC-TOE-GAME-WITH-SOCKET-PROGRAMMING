# LIVE-MEETING-AND-TIC-TAC-TOE-GAME-WITH-SOCKET-PROGRAMMING

# Live Meeting with Socket Programming

## 📌 Introduction

The **Live Meeting with Socket Programming** is a Python-based application designed to facilitate real-time collaboration through screen sharing, video streaming, and audio sharing. Featuring an intuitive graphical user interface (GUI) built with Tkinter, the system leverages socket programming to establish robust communication channels between a server and multiple clients. This enables seamless data exchange for remote meetings, making it ideal for educational institutions, corporate environments, and virtual events.

**Key Features:**
- **Screen Sharing**: Captures and transmits the user's screen in real-time using PIL and socket communication.
- **Video Streaming**: Streams webcam video using OpenCV for face-to-face interaction.
- **Audio Sharing**: Transmits microphone audio using the `sounddevice` library for clear communication.
- **GUI Interface**: Tkinter-based interface for easy control of sharing features (start/stop toggles).
- **Real-Time Communication**: Socket programming ensures low-latency data exchange.
- **Scalability**: Supports multiple concurrent connections for versatile meeting scenarios.

This system enhances remote collaboration by providing a dynamic, interactive platform for real-time communication.

## 🛠 Tech Stack

| *Layer*            | *Tools/Frameworks*         |
|---------------------|----------------------------|
| Frontend (GUI)      | Tkinter                    |
| Computer Vision     | OpenCV                     |
| Image Processing    | PIL (Pillow), PyAutoGUI    |
| Audio Processing    | sounddevice                |
| Networking          | socket                     |
| Concurrency         | threading                  |

## 🏛️ Overall Workflow

1. **Server Setup**: The server initializes three sockets for screen, video, and audio sharing, listening on distinct ports (5051, 9999, 5052).
2. **Client Connection**: Clients connect to the server using the specified IP and ports, establishing communication channels.
3. **Data Sharing**:
   - **Screen**: Clients capture and send resized screen images; the server displays them in a Tkinter label.
   - **Video**: Clients stream webcam frames; the server displays them using OpenCV.
   - **Audio**: Clients send microphone audio chunks; the server plays them using `sounddevice`.
4. **GUI Control**: Users toggle sharing features (screen, video, audio) via Tkinter buttons on both server and client interfaces.
5. **Termination**: Closing the GUI prompts confirmation, shuts down sockets, and terminates threads.

![Workflow Diagram Placeholder]
*(Note: Include a diagram showing server-client connections, data streams, and GUI interactions for clarity.)*

## 📦 Libraries Used

- **Tkinter**: For the graphical user interface.
- **OpenCV**: For capturing and displaying video streams.
- **PIL (Pillow)**: For handling and transmitting screen images.
- **PyAutoGUI**: For screen capture in the client application.
- **sounddevice**: For recording and playing audio streams.
- **socket**: For TCP-based network communication.
- **threading**: For concurrent handling of screen, video, and audio streams.
- **pickle**: For serializing video frame data.
- **struct**: For packing/unpacking data sizes in network communication.
- **numpy**: For processing audio data arrays.

## 🏃‍♂️ Getting Started

Follow these steps to set up and run the Live Meeting system on your local machine.

### 📋 Prerequisites

- Python 3.8 or higher.
- A webcam and microphone for video and audio sharing.
- Git for repository cloning.

### 🧱 Setting Up Your Development Environment

1. **Install Git**:
   - Download and install Git from [git-scm.com](https://git-scm.com/).

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Live-Meeting-Socket-Programming.git
   
3. **Install Dependencies**:
   - Navigate to the project directory and install required libraries:
   ```bash
   pip install opencv-python pillow pyautogui sounddevice numpy

4. **Run the Application**:
   - Execute the server script to start listening for client connections:
   ```bash
   python server.py

5. **Default Teacher Credentials**:
   - On another machine or terminal, execute the client script to connect to the server:
   ```bash
   python client.py
   
6. **Use the GUI**:
   - On the server, toggle screen, video, or audio sharing to view client streams.
   - On the client, start/stop sharing features to send data to the server.

###  🧠 Remember
- Ensure the server is running before starting the client.
- Use the correct IP address and ports (5051 for screen, 9999 for video, 5052 for audio) in the client code.
- A webcam and microphone are required for video and audio functionality.
- The server and client must be on the same network for local testing.
- Replace YOUR-USERNAME in the clone command with your actual GitHub username.
   
