import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import os
from PIL import Image, ImageTk
import time

class AIAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arsalan AI Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create header
        self.header = tk.Label(
            self.main_frame, 
            text="Arsalan AI Assistant", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.header.pack(pady=10)
        
        # Create chat display area
        self.chat_display = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Arial", 12),
            bg="white",
            fg="#333333"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=10)
        self.chat_display.config(state=tk.DISABLED)
        
        # Create input frame
        self.input_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.input_frame.pack(fill=tk.X, pady=10)
        
        # Create input field
        self.input_field = tk.Entry(
            self.input_frame,
            font=("Arial", 12),
            bg="white",
            fg="#333333"
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message)
        
        # Create send button
        self.send_button = tk.Button(
            self.input_frame,
            text="Send",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Create status bar
        self.status_bar = tk.Label(
            self.main_frame,
            text="Ready",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666666",
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, pady=5)
        
        # Create mode selection
        self.mode_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.mode_frame.pack(fill=tk.X, pady=5)
        
        self.mode_label = tk.Label(
            self.mode_frame,
            text="Input Mode:",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666666"
        )
        self.mode_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.mode_var = tk.StringVar(value="keyboard")
        self.keyboard_radio = tk.Radiobutton(
            self.mode_frame,
            text="Keyboard",
            variable=self.mode_var,
            value="keyboard",
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        self.keyboard_radio.pack(side=tk.LEFT, padx=5)
        
        self.voice_radio = tk.Radiobutton(
            self.mode_frame,
            text="Voice",
            variable=self.mode_var,
            value="voice",
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        self.voice_radio.pack(side=tk.LEFT, padx=5)
        
        # Initialize callback functions
        self.on_send_message = None
        self.on_voice_command = None
        
        # Initialize voice listening thread
        self.voice_thread = None
        self.is_listening = False
        
        # Update status
        self.update_status("GUI initialized. Ready to use.")
    
    def set_callbacks(self, on_send_message, on_voice_command):
        """Set callback functions for handling messages and voice commands"""
        self.on_send_message = on_send_message
        self.on_voice_command = on_voice_command
    
    def update_status(self, message):
        """Update the status bar with a message"""
        self.status_bar.config(text=message)
    
    def add_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self, event=None):
        """Send a message from the input field"""
        message = self.input_field.get().strip()
        if message:
            self.input_field.delete(0, tk.END)
            self.add_message("You", message)
            
            if self.on_send_message:
                # Run the callback in a separate thread to avoid freezing the GUI
                threading.Thread(target=self.on_send_message, args=(message,)).start()
    
    def start_voice_listening(self):
        """Start listening for voice commands"""
        if not self.is_listening and self.on_voice_command:
            self.is_listening = True
            self.update_status("Listening for voice commands...")
            self.voice_thread = threading.Thread(target=self._voice_listening_loop)
            self.voice_thread.daemon = True
            self.voice_thread.start()
    
    def stop_voice_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        self.update_status("Voice listening stopped.")
    
    def _voice_listening_loop(self):
        """Background thread for voice recognition"""
        while self.is_listening:
            if self.on_voice_command:
                try:
                    command = self.on_voice_command()
                    if command and command != "Some Error Occurred. Sorry from Arsalan AI":
                        self.add_message("You (Voice)", command)
                except Exception as e:
                    print(f"Voice recognition error: {e}")
            time.sleep(0.1)
    
    def toggle_voice_listening(self):
        """Toggle voice listening on/off"""
        if self.mode_var.get() == "voice":
            self.start_voice_listening()
        else:
            self.stop_voice_listening()
    
    def update_mode(self, *args):
        """Update the input mode"""
        if self.mode_var.get() == "voice":
            self.start_voice_listening()
        else:
            self.stop_voice_listening()
    
    def play_gif(self, gif_path):
        """Play a GIF animation in the GUI"""
        # This is a placeholder for the play_gif function
        # You would need to implement this based on your specific needs
        pass

def create_gui():
    """Create and return a new GUI instance"""
    root = tk.Tk()
    gui = AIAssistantGUI(root)
    return root, gui

def play_gif(gif_path):
    """Function to play a GIF animation"""
    # This is a placeholder for the play_gif function
    # You would need to implement this based on your specific needs
    pass 