import time
import speech_recognition as sr
import os
import webbrowser
import win32com.client
import datetime
import openai
from config import apikey
import pyautogui
import psutil
import speedtest
from twilio.rest import Client
from gui import create_gui, play_gif  # Import the GUI module

# Initialize speaker for speech output
speaker = win32com.client.Dispatch("SAPI.SPvoice")
speaker.speak("Welcome to Arsalan A I")

# Initialize chat string for logging the conversation
chatStr = ""

# Function to handle chatbot interaction
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Arsalan: {query}\n Arsalan A.I: "
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        )
        response_text = response['choices'][0]['message']['content']
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        # Fallback response when API fails
        response_text = "I'm sorry, I'm having trouble connecting to my AI service right now. Please try again later or use a different command."
    
    speaker.speak(response_text)
    chatStr += f"{response_text}\n"
    return response_text

# Function to handle AI prompt response
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *********\n\n"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response['choices'][0]['message']['content']
        print(response_text)
        text += response_text
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        response_text = "I'm sorry, I'm having trouble connecting to my AI service right now. Please try again later."
        text += response_text

    # Ensure 'Openai' folder exists
    os.makedirs("Openai", exist_ok=True)
    
    # Save response to a text file
    file_name = "".join(prompt.split("Artificial intelligence")[1:]).strip()
    with open(f"Openai/{file_name}.txt", "w") as f:
        f.write(text)
    
    return response_text

# Function to capture voice command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except Exception:
        return "Some Error Occurred. Sorry from Arsalan AI"

# Function to get keyboard input
def getKeyboardInput():
    print("Type your command (or 'exit' to quit):")
    return input().lower()

# Function to process commands
def process_command(query, gui=None):
    """Process a command and return the response"""
    response = ""
    
    # Opening specific websites
    sites = {
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.com",
        "google": "https://www.google.com",
        "instagram": "https://www.instagram.com"
    }
    
    site_opened = False
    for site, url in sites.items():
        if f"open {site}" in query:
            response = f"Opening {site} sir..."
            speaker.speak(response)
            webbrowser.open(url)
            site_opened = True
            break
            
    # Check the time
    if not site_opened and "the time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"Sir, the time is {current_time}"
        speaker.speak(response)
        
    # Handle AI interaction
    elif not site_opened and "using artificial intelligence" in query:
        response = ai(prompt=query)
        speaker.speak(response)
        
    # Play music
    elif not site_opened and "play music" in query:
        try:
            music_dir = "C:\\Users\\arsla\\Music"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
            response = "Playing music"
        except Exception as e:
            response = f"Sorry, I couldn't play music. Error: {e}"
        speaker.speak(response)
        
    # Volume control
    elif not site_opened and "increase volume" in query:
        pyautogui.press("volumeup")
        response = "Increasing the volume sir"
        speaker.speak(response)
    elif not site_opened and "decrease volume" in query:
        pyautogui.press("volumedown")
        response = "Decreasing the volume sir"
        speaker.speak(response)
    elif not site_opened and "mute" in query:
        pyautogui.press("volumemute")
        response = "Now the volume is mute sir"
        speaker.speak(response)
        
    # Open applications
    elif not site_opened and "open visual" in query:
        try:
            response = "Opening Visual Studio Code sir"
            speaker.speak(response)
            os.startfile("C:\\Users\\arsla\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
        except Exception as e:
            response = f"Sorry, I couldn't open Visual Studio Code. Error: {e}"
            speaker.speak(response)
    elif not site_opened and "open camera" in query:
        try:
            response = "Opening the Camera sir"
            speaker.speak(response)
            os.startfile("C:\\Users\\arsla\\OneDrive\\Desktop\\Camera")
        except Exception as e:
            response = f"Sorry, I couldn't open the camera. Error: {e}"
            speaker.speak(response)
    elif not site_opened and "open profile" in query:
        response = "Enter username to find profile"
        speaker.speak(response)
        username = input("Enter Instagram username: ")
        response = "Opening Instagram profile sir"
        speaker.speak(response)
        webbrowser.open(f"www.instagram.com/{username}")
        
    # Take a screenshot
    elif not site_opened and "take screenshot" in query:
        response = "Sir, please tell me the name for this screenshot file"
        speaker.speak(response)
        name = takeCommand().lower()
        response = "Please hold the screen for a few seconds, I am taking the screenshot"
        speaker.speak(response)
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        response = "Done, the screenshot is saved in your main folder."
        speaker.speak(response)
        
    # Check battery status
    elif not site_opened and "how much battery we have" in query:
        try:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            response = f"Sir, our system has {percentage}% battery"
        except Exception as e:
            response = f"Sorry, I couldn't check the battery status. Error: {e}"
        speaker.speak(response)
        
    # Default case for chatting
    elif not site_opened:
        response = chat(query)
    
    # Update GUI if available
    if gui:
        gui.add_message("Arsalan AI", response)
    
    return response

# Main function to control the flow
if __name__ == '__main__':
    print('Welcome to Arsalan A.I')
    
    # Create GUI
    root, gui = create_gui()
    
    # Set up callbacks for the GUI
    def on_send_message(message):
        process_command(message, gui)
    
    def on_voice_command():
        command = takeCommand()
        if command and command != "Some Error Occurred. Sorry from Arsalan AI":
            process_command(command, gui)
        return command
    
    gui.set_callbacks(on_send_message, on_voice_command)
    
    # Add welcome message to GUI
    gui.add_message("Arsalan AI", "Welcome to Arsalan AI Assistant! How can I help you today?")
    
    # Start the GUI main loop
    root.mainloop()
