import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from math import log10

def convert_power_to_dBm(power, unit):
    if unit == "mW":
        return 10 * log10(power)
    elif unit == "W":
        return 10 * log10(1000 * power)
    elif unit == "dBW": #decibel Watt
        return power + 30
    elif unit == "dBm": #decibel milliWatt
        return power


def convert_frequency_to_Hz(frequency, unit):
    if unit == "GHz":
        return frequency * 1e9
    elif unit == "MHz":
        return frequency * 1e6


def convert_distance_to_meters(distance, unit):
    if unit == "km":
        return 1000 * distance
    elif unit == "meter":
        return distance
    elif unit == "feet":
        return 0.3048 * distance
    elif unit == "miles":
        return 1609.34 * distance
    elif unit == "yards":
        return 0.9144 * distance
    elif unit == "inches":
        return 0.0254 * distance

def calculate_received_power():
    try:
        # Get user input values
        transmit_power = float(transmit_power_entry.get())
        transmit_power_unit = power_unit_var.get()

        frequency = float(frequency_entry.get())
        frequency_unit = frequency_unit_var.get()

        distance = float(distance_entry.get())
        distance_unit = distance_unit_var.get()

        gain_transmitter = float(gain_transmitter_entry.get())
        gain_receiver = float(gain_receiver_entry.get())

        # Convert input values to standard units
        transmit_power_dBm = convert_power_to_dBm(transmit_power, transmit_power_unit)
        frequency_Hz = convert_frequency_to_Hz(frequency, frequency_unit)
        distance_meters = convert_distance_to_meters(distance, distance_unit)

        # Friis Transmission Equation
        received_power = transmit_power_dBm + gain_transmitter + gain_receiver + 20 * log10(3e8 / (4 * 3.1415 * frequency_Hz * distance_meters))

        # Update the result label
        result_label.config(text=f"Received Power: {received_power:.3f} dBm")

        # Update the animation
        update_animation(distance_meters)

    except ValueError:
        result_label.config(text="Please enter valid numeric values.")


def update_animation(distance_meters):
    canvas.delete("all")

    # transmitter
    canvas.create_oval(50, 200, 70, 220, fill="red", outline="red")
    canvas.create_text(60, 230, text="Transmitter", fill="red")

    #receiver
    canvas.create_oval(400, 200, 420, 220, fill="blue", outline="blue")
    canvas.create_text(410, 230, text="Receiver", fill="blue")

    #path
    canvas.create_line(70, 210, 400, 210, fill="black", dash=(4, 2))

    #distance
    canvas.create_text(235, 220, text=f"{distance_meters:.2f} meters", fill="black")


# Create the main window
window = tk.Tk()
window.title("Friis Transmission Calculator with Animation")

style = ThemedStyle(window)

# Configure column and row weights for responsiveness
for i in range(3):
    window.grid_columnconfigure(i, weight=1)

for i in range(8):
    window.grid_rowconfigure(i, weight=1)

ttk.Label(window, text="Transmit Power:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
transmit_power_entry = ttk.Entry(window)
transmit_power_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.NSEW)

power_units = ["mW", "W", "dBW", "dBm"]
power_unit_var = tk.StringVar()
power_unit_var.set("dBm")
power_unit_menu = ttk.Combobox(window, textvariable=power_unit_var, values=power_units)
power_unit_menu.grid(row=0, column=2, padx=10, pady=5, sticky=tk.NSEW)

ttk.Label(window, text="Frequency:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
frequency_entry = ttk.Entry(window)
frequency_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.NSEW)

frequency_units = ["GHz", "MHz"]
frequency_unit_var = tk.StringVar()
frequency_unit_var.set("GHz")
frequency_unit_menu = ttk.Combobox(window, textvariable=frequency_unit_var, values=frequency_units)
frequency_unit_menu.grid(row=1, column=2, padx=10, pady=5, sticky=tk.NSEW)

ttk.Label(window, text="Distance:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
distance_entry = ttk.Entry(window)
distance_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.NSEW)

distance_units = ["km", "meter", "feet", "miles", "yards", "inches"]
distance_unit_var = tk.StringVar()
distance_unit_var.set("meter")
distance_unit_menu = ttk.Combobox(window, textvariable=distance_unit_var, values=distance_units)
distance_unit_menu.grid(row=2, column=2, padx=10, pady=5, sticky=tk.NSEW)

ttk.Label(window, text="Transmitter Gain (dB):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
gain_transmitter_entry = ttk.Entry(window)
gain_transmitter_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.NSEW)

ttk.Label(window, text="Receiver Gain (dB):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
gain_receiver_entry = ttk.Entry(window)
gain_receiver_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.NSEW)

# Button to calculate received power
calculate_button = ttk.Button(window, text="Calculate", command=calculate_received_power, style="TButton")
calculate_button.grid(row=5, column=0, columnspan=3, pady=10, sticky=tk.NSEW)

# Result
result_label = ttk.Label(window, text="")
result_label.grid(row=6, column=0, columnspan=3, pady=5, sticky=tk.NSEW)

# Canvas for animation
canvas = tk.Canvas(window, width=500, height=300, bg="white")
canvas.grid(row=7, column=0, columnspan=3, pady=10, sticky=tk.NSEW)

window.mainloop()
