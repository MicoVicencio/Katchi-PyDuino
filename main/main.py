from tkinter import *  # Importing the tkinter library for GUI
from PIL import Image, ImageTk  # Importing the PIL library to handle images
import speech_recognition as sr  # Importing the speech recognition library
import os  # Importing the os module to handle operating system interactions
import platform  # Importing the platform module to get system-specific information
import serial  # Importing the pyserial library to handle serial communication
import time  # Importing the time module to handle time delays
import threading  # Importing the threading module to handle concurrent execution
import vlc

# Global VLC media player instance
media = None

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
    "bakit part 2": r"C:\ann cute\songs\BAKIT PART 2 - MAYONNAISE (karaoke version).mp4",
    "romcom": r"C:\ann cute\songs\RomCom by Rob Deniel (Karaoke Version).mp4",
    "walang alam": r"C:\ann cute\songs\Walang Alam - Hev Abi (Karaoke).mp4",
    "tingin": r"C:\ann cute\songs\Tingin Cup of Joe Ft  Janine Teñoso Karaoke.mp4",
    "buwan": r"C:\ann cute\songs\Juan Karlos - Buwan (Karaoke Version).mp4",
    "fallen": r"C:\ann cute\songs\FALLEN - Lola Amour (KARAOKE VERSION).mp4",
    "mundo": r"C:\ann cute\songs\MUNDO - IV Of Spades (KARAOKE VERSION).mp4",
    "ere": r"C:\ann cute\songs\juan karlos - ERE (Karaoke Version).mp4",
    "lihim": r"C:\ann cute\songs\Arthur Miguel - Lihim (Karaoke Version).mp4",
    "tadhana": r"C:\ann cute\songs\TADHANA - Up Dharma Down (KARAOKE VERSION).mp4",
    "tahanan": r"C:\ann cute\songs\Adie - Tahanan (Karaoke).mp4",
    "beer": r"C:\ann cute\songs\Beer - Itchyworms (KARAOKE).mp4",
    "sana": r"C:\ann cute\songs\I Belong to the Zoo - Sana (Karaoke Version).mp4",
    "magbalik": r"C:\ann cute\songs\Callalily - Magbalik (Karaoke Version).mp4",
    "migraine": r"C:\ann cute\songs\Moonstar88 - Migraine (Karaoke Version).mp4",
    "jopay": r"C:\ann cute\songs\JOPAY - Mayonnaise (KARAOKE VERSION).mp4",
    "antukin": r"C:\ann cute\songs\Rico Blanco - Antukin (Karaoke-Acoustic Instrumental).mp4",
    "babaero": r"C:\ann cute\songs\BABAERO - gins&melodies ft. Hev Abi (Karaoke).mp4",
    "saturn": r"C:\ann cute\songs\SZA - Saturn (Karaoke Version).mp4",
    "all of me": r"C:\ann cute\songs\John Legend - All Of Me (Karaoke Version).mp4"
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
    global media  # Use the global media instance

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    while True:
      try:
        response = recognize_speech_from_mic(recognizer, microphone)
        if not response["success"]:
            print("Error: ", response["error"])
        else:
            print("You said: " + response["transcription"])
            song_title = response["transcription"].lower()

            if song_title in songs_list:
                url = songs_list[song_title]
                media = vlc.MediaPlayer(url)
                media.play()
                print(song_title)
                return song_title
            elif response["transcription"].lower() == "close":
                if media:
                    media.stop()
                print("Exiting...")
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
        "Bakit part 2 - Mayonaise",
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
        "Sana - I Belong To The Zoo",
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
    gif_path = "C:\\Users\\Mico\\Desktop\\CALCU JAVASCRIPT\\main\\katchi.jpeg"  # Replace with the actual path to your image file
    gif = Image.open(gif_path)
    photo = ImageTk.PhotoImage(gif)

    label = Label(picture, image=photo)
    label.place(x=0, y=0, relwidth=1, relheight=1, anchor='nw')

    # Footer settings
    footer = Frame(root, bg="#810404", height=80)
    footer.pack(fill=BOTH)
    footer_text = Label(footer, text="© 2023 KATCHI Karaoke. All Rights Reserved.", font=("Helvetica", 12), bg="#810404", fg="white")
    footer_text.pack(padx=10)

    root.mainloop()

# Running the Arduino communication and GUI in separate threads
if __name__ == "__main__":
    threading.Thread(target=micStart, daemon=True).start()  # Start the Arduino communication in a separate thread
    create_gui()  # Create and display the GUI
