from tkinter import *  # Importing the tkinter library for GUI
from PIL import Image, ImageTk  # Importing the PIL library to handle images
import speech_recognition as sr  # Importing the speech recognition library
import webbrowser  # Importing the webbrowser module to open URLs
import os  # Importing the os module to handle operating system interactions
import platform  # Importing the platform module to get system-specific information
import serial  # Importing the pyserial library to handle serial communication
import time  # Importing the time module to handle time delays
import threading  # Importing the threading module to handle concurrent execution

# Function to handle Arduino communication
def arduino():
    arduino_port = 'COM3'  # Replace with your port
    baud_rate = 9600  # Match the baud rate with Arduino

    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Wait for the connection to establish

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(f"Received from Arduino: {line}")
                if line == "1":
                    print("Arduino triggered")
                    song = micStart()
                    send_data = f"{song}"
                    ser.write((send_data + '\n').encode('utf-8'))
                    print(f"Sent to Arduino: {send_data}")

                    # Clear the buffer and reset line after processing
                    ser.flushInput()
                    line = ""

    except KeyboardInterrupt:
        print("Program interrupted")

    finally:
        ser.close()

# Songs list
songs_list = {
    "dilaw": "https://youtu.be/N8wWGeKGeYY?si=CNzaP9xMdxJ8a8JP",
    "romcom": "https://youtu.be/C9xK2CQKcbo?si=Wl_Lfqap9yD6GKwz",
    "walang alam": "https://youtu.be/3uw0hJwCmfI?si=Z2P98gnDlnslbw4c",
    "tingin": "https://youtu.be/oOJNLIR5nwQ?si=zUqI-Xx-GjWJzOmT",
    "buwan": "https://www.youtube.com/watch?v=f1cCpqOnc8c",
    "fallen": "https://youtu.be/F1u0rzWYYFc?si=sLMHfhAwbc_O1yrV",
    "mundo": "https://youtu.be/tu8vdo6G62o?si=jHnYIdNymilSsEVt",
    "ere": "https://youtu.be/EQJzDPAFVqU?si=BZ-viQYWTLNWR0Xn",
    "lihim": "https://youtu.be/R_sVqEj1pJM?si=yzOJvFCUIIcSDyZj",
    "tadhana": "https://youtu.be/MJd_6nqxIYw?si=QoXvsnM5Ln9Q1f32",
    "tahanan": "https://youtu.be/kkhXR-PdCnI?si=GtlRAvSz7nhpAQo9",
    "beer": "https://youtu.be/C8twukz-0g0?si=9YEmpEMtRM9RbQPc",
    "pasilyo": "https://youtu.be/ZGUtHVzi1qI?si=eykaa8dYvRyyhHOb",
    "magbalik": "https://youtu.be/4JWM7QW0NIM?si=A94_gHCFtc0Pb8y5",
    "migraine": "https://youtu.be/8sF9f1bMNo8?si=p9ksaQfTLsaWt4Tb",
    "jopay": "https://youtu.be/MfEaylAx7Mk?si=wvdOS1K57gj8eQYh",
    "antukin": "https://youtu.be/cuwo5-Mea8c?si=Y895m8Xncrh9Mcfg",
    "babaero": "https://youtu.be/TGOkM5fbAss?si=_JPFI2XK5mXZHW49",
    "saturn": "https://youtu.be/EkwcFOLrlkE?si=anHs2Hp_aZUmy4-r",
    "all of me": "https://youtu.be/6VoT-KrseHA?si=dvlDibTOHDTz6y2u"
}

# Function to recognize speech
def recognize_speech_from_mic(recognizer, microphone, timeout=5, phrase_time_limit=3):
    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Please speak now...")

        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return {"success": False, "error": "Listening timed out", "transcription": None}

        response = {"success": True, "error": None, "transcription": None}

        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            response["error"] = "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            response["error"] = f"Could not request results from Google Speech Recognition service; {e}"
            response["success"] = False

        return response

# Function to start the microphone and listen for commands
def micStart():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        response = recognize_speech_from_mic(recognizer, microphone)
        if not response["success"]:
            print("Error: ", response["error"])
        else:
            print("You said: " + response["transcription"])
            song_title = response["transcription"].lower()

            if song_title in songs_list:
                url = songs_list[song_title]
                webbrowser.open_new(url)
                print(song_title)
                return song_title
            elif response["transcription"].lower() == "close":
                print("Exiting...")
                system = platform.system()
                if system == "Windows":
                    os.system("taskkill /im brave.exe /f")
                elif system == "Darwin":
                    os.system("pkill brave")
                elif system == "Linux":
                    os.system("pkill brave")
            else:
                print("Song not found in the list.")

    except TypeError:
        print("An error occurred")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")

# Function to create the GUI
def create_gui():
    # List of songs to display in the GUI
    songs = [
        "Dilaw - Maki",
        "Romcom - Rob Daniel",
        "Walang Alam - Hev Abi",
        "Tingin - Cup Of Joe",
        "Buwan - Juan Karlos Labajo",
        "Fallen - Lola Amour",
        "Mundo - IV of Spades",
        "Ere - Juan Karlos Labajo (JK)",
        "Lihim - Arthur Miguel",
        "Tadhana - Up Dharma Down",
        "Tahanan - Adie",
        "Beer - Itchyworms",
        "Pasilyo - SunKissed Lola",
        "Magbalik - Callalily",
        "Migraine - Moonstar88",
        "Jopay - Mayonnaise",
        "Antukin - Rico Blanco",
        "Babaero - Hev Abi",
        "Saturn - SZA",
        "All of Me - John Legend"
    ]

    # Create a formatted string of song titles to display in the GUI
    label_text = "\n".join([f"{i+1}. {song}" for i, song in enumerate(songs)])

    # Initialize the main window
    root = Tk()
    root.title("KATCHI")
    root.geometry("1400x660")

    # Header settings
    header = Frame(root, bg="#810404", height=80)
    header.pack(fill=BOTH)
    title = Label(header, text="K  A  T  C  H  I", font=("Helvetica", 36), bg="#810404", fg="white")
    title.pack(padx=10)
    subtitle = Label(header, text="Karaoke Access Transformed, Creating Harmonious Interactions",
                     font=("Helvetica", 10), bg="#810404", fg="white")
    subtitle.pack(padx=10)

    # Body settings
    body = Frame(root, bg="#d3cfcf", height=500)
    body.pack(fill=BOTH, expand=True)

    # Left side for song list
    sideLeft_songlistFrame = Frame(body, bg="#d3cfcf", height=500, width=700)
    sideLeft_songlistFrame.pack(side=LEFT, fill=Y)
    Slist = Label(sideLeft_songlistFrame, text="List Of Songs", font=("Helvetica", 20), bg="#d3cfcf")
    Slist.pack(padx=10)
    labelS = Label(sideLeft_songlistFrame, text=label_text, wraplength=700, justify=LEFT, font=("Helvetica", 15), bg="#d3cfcf", width=50)
    labelS.pack(anchor=W, padx=10, pady=10)

    # Right side for instructions
    sideRight_Instruction = Frame(body, bg="#f2a1a1", height=250, width=700)
    sideRight_Instruction.pack(side=TOP, fill=BOTH, expand=True)
    instructions_text = """Instructions: To use the voice-controlled karaoke program, start by launching the program, which displays a list of 20 songs. After pressing the button, the voice command will function. To play a song, say the title exactly as listed on the screen (e.g., "Dilaw"), and the program will open a browser to play the karaoke version on YouTube in full-screen mode. To stop the song, simply say "Close" and the program will close the browser window, ending the playback. For the best experience, speak clearly and minimize background noise to ensure accurate voice recognition. Enjoy your karaoke session!"""

    label = Label(sideRight_Instruction, text=instructions_text, justify=LEFT, bg="#f2a1a1", wraplength=750, font=("helvetica", 15))
    label.pack(padx=20, pady=10)

    # Bottom for displaying image
    picture = Frame(body, bg="#d3cfcf", height=250, width=700)
    picture.pack(side=BOTTOM, fill=BOTH, expand=True)
    gif_path = "main/katchi.jpeg"  # Replace with the actual path to your image file
    gif = Image.open(gif_path)
    photo = ImageTk.PhotoImage(gif)

    label = Label(picture, image=photo)
    label.place(x=0, y=0, relwidth=1, relheight=1, anchor='nw')

    # Footer settings
    footer = Frame(root, bg="#810404", height=80)
    footer.pack(fill=BOTH)

    root.mainloop()

# Running the Arduino communication and GUI in separate threads
if __name__ == "__main__":
    threading.Thread(target=arduino, daemon=True).start()  # Start the Arduino communication in a separate thread
    create_gui()  # Create and display the GUI
