import os
import sys
import warnings
import customtkinter as ctk
import create_encodings
import train
import webcam
import threading

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.base")

class RedirectOutput:
    """Redirects console output to the GUI."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        if message != '\n':  # Avoid adding empty new lines
            self.text_widget.configure(state="normal")  # Make writable temporarily
            self.text_widget.insert(ctk.END, message+"\n")  # Insert message
            self.text_widget.see(ctk.END)  # Auto-scroll to the bottom
            self.text_widget.configure(state="disabled")  # Set back to read-only

    def flush(self):
        pass  # Required for compatibility with sys.stdout and sys.stderr

# Function to call the create_encodings script
def call_Encoding():
    result_label.configure(text="Running Create Encoding...")
    threading.Thread(target=create_encodings.run, daemon=True).start()  

# Function to call the train script
def call_Train():
    result_label.configure(text="Running Train...")
    threading.Thread(target=train.run, daemon=True).start()  

# Function to call the webcam script
def call_webcam():
    result_label.configure(text="Starting Webcam...")
    threading.Thread(target=webcam.run, daemon=True).start()  

# Function to quit the application
def quit_application():
    app.quit()  # Quit the main loop and close the window

# Create the customtkinter application
ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")  

app = ctk.CTk()  # Initialize the main window
app.geometry("600x450")  # Set the window size
app.title("Employee Attendance System")

# Add buttons to call scripts
button = ctk.CTkButton(
    master=app,
    text="Create Encoding",
    command=call_Encoding,
    width=200,
    height=40
)
button.pack(pady=10)

button = ctk.CTkButton(
    master=app,
    text="Train",
    command=call_Train,
    width=200,
    height=40
)
button.pack(pady=10)

button = ctk.CTkButton(
    master=app,
    text="Start Attendance",
    command=call_webcam,
    width=200,
    height=40
)
button.pack(pady=10)

# Add a label to display the result
result_label = ctk.CTkLabel(
    master=app,
    text="Click a button to run the respective script.",
    width=400,
    height=20,
    anchor="center"
)
result_label.pack(pady=10)

# Add a Text widget for console output
console_output = ctk.CTkTextbox(
    master=app,
    width=500,
    height=200,
    font=("Courier", 12)
)
console_output.pack(pady=10, padx=10)

# Redirect stdout and stderr to the Text widget
sys.stdout = RedirectOutput(console_output)
sys.stderr = RedirectOutput(console_output)

# Add a Quit button
quit_button = ctk.CTkButton(
    master=app,
    text="Quit",
    command=quit_application,  # Function to quit the app
    width=200,
    height=40,
    fg_color="red"  # Red color for quit button for emphasis
)
quit_button.pack(pady=10)

# Run the application
app.mainloop()
