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


---


# Networked Tic-Tac-Toe Game

## 📌 Introduction

The **Networked Tic-Tac-Toe Game** is a Python-based application that enables two players to play Tic-Tac-Toe over a network using socket programming. One player hosts the game as the server (playing as "X"), while the other connects as the client (playing as "O"). The game features a text-based interface, robust move validation, and real-time win/tie detection, with seamless communication facilitated by threading.

**Key Features:**
- **Network Play**: Supports two players over a TCP connection using `socket`.
- **Real-Time Interaction**: Uses `threading` for simultaneous move inputs and opponent updates.
- **Move Validation**: Ensures valid moves (within 0-2 range, empty spaces) to prevent errors.
- **Game Logic**: Detects wins (rows, columns, diagonals) and ties after 9 moves.
- **Simple Interface**: Displays the 3x3 board in the console with clear formatting.

This project showcases the power of socket programming in creating interactive, multiplayer gaming experiences.

## 🛠 Tech Stack

| *Layer*          | *Tools/Frameworks*         |
|-------------------|----------------------------|
| Programming       | Python                     |
| Networking        | socket                     |
| Concurrency       | threading                  |

## 🏛️ Overall Workflow

1. **Game Setup**: Player 1 hosts the game (`host_game`) on a specified host and port, while Player 2 connects (`connect_to_game`).
2. **Role Assignment**: Player 1 is assigned "X", and Player 2 is assigned "O".
3. **Move Exchange**: Players take turns entering moves (row, column) via the console, which are sent over the network to update the opponent’s board.
4. **Validation and Update**: The `check_valid_move` method verifies move validity, and `apply_move` updates the board state.
5. **Game Outcome**: The game checks for a win (`check_if_won`) or tie (`counter == 9`) after each move, ending when a condition is met.

![Workflow Diagram Placeholder]
*(Note: Include a diagram showing client-server connections, move exchange, and board updates for clarity.)*

## 📦 Libraries Used

- **socket**: For TCP-based network communication.
- **threading**: For handling concurrent move processing.
- **built-in**: No external dependencies required.

## 🏃‍♂️ Getting Started

Follow these steps to set up and run the Tic-Tac-Toe game on your local machine.

### 📋 Prerequisites

- Python 3.8 or higher.
- Two machines or terminals (for host and client).
- Git for repository cloning.

### 🧱 Setting Up Your Development Environment

1. **Install Git**:
   - Download and install Git from [git-scm.com](https://git-scm.com/).

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/TicTacToe-Networked.git

3. **No Dependencies: **:
   - The game uses Python’s standard library (socket, threading), so no additional installations are needed.
   
4. **Run the Game**:
   - Host the Game (Player 1): Execute the Player 1 script to start the server:
   ```bash
      python player1.py

- Ensure the script uses:
   ```bash
     game = TicTacToe()
     game.host_game("localhost", 9999)
  
- Connect as Client (Player 2): Execute the Player 2 script to connect to the server:
    ```bash
     python player2.py

- Ensure the script uses:
   ```bash
     game = TicTacToe()
     game.connect_to_game("localhost", 9999)
  

5. **Play the Game**:
   - Enter moves as row,column (e.g., 0,1 for row 0, column 1).
   - Valid inputs are 0, 1, or 2 for both row and column.


## 🧠 Remember

- Start the Player 1 script (server) before running the Player 2 script (client).
- Use the same port (e.g., 9999) for both players.
- The game assumes a stable network; connection issues may cause errors.
- The board is 0-indexed, so valid inputs are 0, 1, or 2.
- Replace YOUR-USERNAME in the clone command with your actual GitHub username.
  
