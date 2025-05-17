import customtkinter as ctk # type: ignore
from datetime import datetime


#window creation
window = ctk.CTk()

ctk.set_appearance_mode("dark")
window.title("Mirror")
window.geometry('1800x1200')

#widget creation
#time
time = ctk.StringVar()

def update_time():
    current_time = datetime.now().strftime('%I:%M:%S %p').lstrip('0')  # Remove leading zero from hour
    time.set(current_time)
    window.after(1000, update_time)

def set_slider_width(event):
    new_width = int(window.winfo_width() * 0.8)
    slider.configure(width=new_width)

label = ctk.CTkLabel(
    window,
    text="Mirror",
    text_color="white",
    corner_radius=10,
    fg_color="transparent",
    font=("Cormorant", 60),
    textvariable= time
)
label.place(relx=0.5, rely=0.08, anchor="center")
#volume

slider = ctk.CTkSlider(
    window,
    from_=20,
    to=100,
    number_of_steps=10,
    command=lambda value: label.configure(text=f"Volume: {value}"),
    width=300  # Temporary default width
)
slider.place(relx=0.5, rely=0.35, anchor="center")

# Bind window resizing to slider resizing
window.bind("<Configure>", set_slider_width)
slider.place(relx=0.5, rely=0.9, anchor="center")
update_time()
window.mainloop()