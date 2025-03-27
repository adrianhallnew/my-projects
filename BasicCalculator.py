import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

def handle_button_click(clicked_button_text):
    current_text = result_var.get()

    if clicked_button_text == "=":
        try:
            expression = current_text.replace("÷","/").replace("×","*")
            result = eval(expression)
            
            # Check if result is an integer
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            result_var.set(result)
            
        except Exception as e:
            result_var.set("Error")

    elif clicked_button_text == "C":
        result_var.set("")
    elif clicked_button_text == "%":
        try:
            current_number = float(current_text)
            result_var.set(current_number / 100)
        except ValueError:
            result_var.set("Error")
    elif clicked_button_text == "±":
        try:
            current_number = float(current_text)
            result_var.set(-current_number)
        except ValueError:
            result_var.set("Error")
    else:
        result_var.set(current_text + clicked_button_text)

root = tk.Tk()
root.title("Calculator")
root.configure(bg="#222222")  # Dark background for the entire window

# Custom display solution using Label instead of Entry
# This gives more control over the font appearance
main_frame = tk.Frame(root, bg="#222222", padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a frame specifically for the display
display_frame = tk.Frame(main_frame, bg="#222222", highlightthickness=1, highlightbackground="#555555")
display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=20)

# Create the result variable
result_var = tk.StringVar()
result_var.set("")  # Start with empty display

# Create a custom label for display with the thin, elegant font
display_label = tk.Label(
    display_frame,
    textvariable=result_var,
    font=("Helvetica", 60, "normal"),  # Thin, large font similar to your screenshot
    bg="#222222",                      # Dark background
    fg="#FFFFFF",                      # White text
    anchor="e",                        # Right-aligned text
    padx=20,                           # Padding on the sides
    pady=20                            # Padding top/bottom
)
display_label.pack(fill=tk.BOTH, expand=True)

# Create custom styles for different button types
style = ttk.Style()
style.theme_use('clam')  # Use clam theme as base

# Configure number buttons
style.configure("Number.TButton", 
                font=("Helvetica", 24),
                background="#333333", 
                foreground="#FFFFFF",
                borderwidth=0,
                padding=10)
style.map("Number.TButton",
         background=[('active', '#444444')],
         relief=[('pressed', 'flat'), ('!pressed', 'flat')])

# Configure operation buttons
style.configure("Operation.TButton", 
                font=("Helvetica", 24, "bold"),
                background="#FF9500", 
                foreground="#FFFFFF",
                borderwidth=0,
                padding=10)
style.map("Operation.TButton",
         background=[('active', '#FFB143')],
         relief=[('pressed', 'flat'), ('!pressed', 'flat')])

# Configure special buttons
style.configure("Special.TButton", 
                font=("Helvetica", 24),
                background="#A5A5A5", 
                foreground="#000000",
                borderwidth=0,
                padding=10)
style.map("Special.TButton",
         background=[('active', '#C1C1C1')],
         relief=[('pressed', 'flat'), ('!pressed', 'flat')])

# Configure equals button
style.configure("Equals.TButton", 
                font=("Helvetica", 24, "bold"),
                background="#FF9500", 
                foreground="#FFFFFF",
                borderwidth=0,
                padding=10)
style.map("Equals.TButton",
         background=[('active', '#FFB143')],
         relief=[('pressed', 'flat'), ('!pressed', 'flat')])

# Define button mappings with proper styling
buttons = [
    ("C", 1, 0, "Special.TButton"), 
    ("±", 1, 1, "Special.TButton"), 
    ("%", 1, 2, "Special.TButton"), 
    ("÷", 1, 3, "Operation.TButton"),
    ("7", 2, 0, "Number.TButton"), 
    ("8", 2, 1, "Number.TButton"), 
    ("9", 2, 2, "Number.TButton"), 
    ("×", 2, 3, "Operation.TButton"),
    ("4", 3, 0, "Number.TButton"), 
    ("5", 3, 1, "Number.TButton"), 
    ("6", 3, 2, "Number.TButton"), 
    ("-", 3, 3, "Operation.TButton"),
    ("1", 4, 0, "Number.TButton"), 
    ("2", 4, 1, "Number.TButton"), 
    ("3", 4, 2, "Number.TButton"), 
    ("+", 4, 3, "Operation.TButton"),
    ("0", 5, 0, "Number.TButton", 2), 
    (".", 5, 2, "Number.TButton"), 
    ("=", 5, 3, "Equals.TButton")
]

# Create buttons using the styling information
for button_info in buttons:
    button_text, row, col = button_info[:3]
    button_style = button_info[3]
    colspan = button_info[4] if len(button_info) > 4 else 1
    
    button = ttk.Button(
        main_frame, 
        text=button_text, 
        command=lambda text=button_text: handle_button_click(text), 
        style=button_style
    )
    
    button.grid(
        row=row, 
        column=col, 
        columnspan=colspan, 
        sticky="nsew", 
        padx=8,
        pady=8
    )

# Configure grid weights for proper expansion
for i in range(6):
    main_frame.grid_rowconfigure(i, weight=1)

for i in range(4):
    main_frame.grid_columnconfigure(i, weight=1)

# Set window dimensions
width = 500
height = 700
root.geometry(f"{width}x{height}")

# Make window resizable
root.resizable(True, True)
root.minsize(400, 600)

# Add keyboard and keypad bindings
def key_press(event):
    key = event.char
    keysym = event.keysym
    
    # Handle numeric keys (both keyboard and keypad)
    if key.isdigit():
        handle_button_click(key)
    # Handle operators
    elif key in ['+', '-', '*', '/']:
        if key == '*':
            handle_button_click('×')
        elif key == '/':
            handle_button_click('÷')
        else:
            handle_button_click(key)
    # Handle decimal point
    elif key == '.':
        handle_button_click('.')
    # Handle percent
    elif key == '%':
        handle_button_click('%')
    # Handle equals and enter
    elif keysym in ['Return', 'equal']:
        handle_button_click('=')
    # Handle backspace/delete/escape for clear
    elif keysym in ['BackSpace', 'Delete', 'Escape']:
        handle_button_click('C')
    # Handle keypad specific keys
    elif keysym == 'KP_0':
        handle_button_click('0')
    elif keysym == 'KP_1':
        handle_button_click('1')
    elif keysym == 'KP_2':
        handle_button_click('2')
    elif keysym == 'KP_3':
        handle_button_click('3')
    elif keysym == 'KP_4':
        handle_button_click('4')
    elif keysym == 'KP_5':
        handle_button_click('5')
    elif keysym == 'KP_6':
        handle_button_click('6')
    elif keysym == 'KP_7':
        handle_button_click('7')
    elif keysym == 'KP_8':
        handle_button_click('8')
    elif keysym == 'KP_9':
        handle_button_click('9')
    elif keysym == 'KP_Divide':
        handle_button_click('÷')
    elif keysym == 'KP_Multiply':
        handle_button_click('×')
    elif keysym == 'KP_Subtract':
        handle_button_click('-')
    elif keysym == 'KP_Add':
        handle_button_click('+')
    elif keysym == 'KP_Decimal':
        handle_button_click('.')
    elif keysym == 'KP_Enter':
        handle_button_click('=')

# Bind the key_press function to handle all keypresses
root.bind("<Key>", key_press)

root.mainloop()