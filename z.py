#from PIL import Image, ImageTk
import tkinter as tk
from PIL import Image, ImageTk
import serial
import time
import os
from PIL import ImageEnhance



root = tk.Tk()

THEME = {
    "mode": "light",

    # ------------------- LIGHT THEME -------------------
    "light": {
        # MAIN UI
        "bg": "#F5F7FB",               # slightly tinted white (not pure white)
        "fg": "#1A1A1A",

        # SIDEBAR (different shade!)
        "sidebar_bg": "#FFFFFF",       # bright white
        "sidebar_fg": "#1A1A1A",
        "sidebar_button_bg": "#E9EDF5",
        "sidebar_button_fg": "#1A1A1A",
        "sidebar_button_hover": "#D7DEEA",

        # FRAMES / CARDS
        "frame_bg": "#FFFFFF",
        "border": "#DADDE2",

        # BUTTONS
        "button_bg": "#FFFFFF",
        "button_fg": "#1A1A1A",
        "button_hover": "#EAEAEA",

        # INPUT BOX
        "textbox_bg": "#FFFFFF",
        "textbox_fg": "#000000",
        "textbox_border": "#BCC5D2",

        # ACCENT
        "accent": "#4A6CF7"
    },

    # ------------------- DARK THEME (NEON) -------------------
    "dark": {
        # MAIN UI
        "bg": "#0A0F1F",          # deep midnight blue
        "fg": "#E3E8FF",          # soft off-white

        # SIDEBAR
        "sidebar_bg": "#11182C",  # slightly brighter than main bg
        "sidebar_fg": "#E3E8FF",
        "sidebar_button_bg": "#1A2340",
        "sidebar_button_fg": "#E3E8FF",
        "sidebar_button_hover": "#223058",

        # FRAMES / CARDS
        "frame_bg": "#11182C",
        "border": "#223058",

        # BUTTONS
        "button_bg": "#1A2340",
        "button_fg": "#E3E8FF",
        "button_hover": "#223058",

        # INPUT BOX
        "textbox_bg": "#1A2340",
        "textbox_fg": "#E3E8FF",
        "textbox_border": "#223058",

        # ACCENT
        "accent": "#00D4FF",

        # STATUS
        "error": "#FF4E88",
        "success": "#4CFF85"
    }
}



root.title("ASL Robotic Hand")
root.geometry("1100x700")  # width x height
root.resizable(False, False)

root.config(bg="#0A0F1F")



#---CONNECT TO ARDUINO---

#----++++++++++---------- C H A N G E  T H E  P O R T -----------++++++++++----
try:
    arduino = serial.Serial('/dev/cu.usbmodem1101', 9600) # CHANGE THE PORT 
    #python3 -m serial.tools.list_ports

    time.sleep(2)
    print("✅ Connected to Arduino!")
except Exception as e:
    arduino = None
    print("⚠️ Could not connect to Arduino:", e)
#----++++++++++---------- C H A N G E  T H E  P O R T -----------++++++++++----


# Sidebar frame
#sidebar = tk.Frame(root, bg="#11182C", width=200)  # width fixed & height=700
sidebar = tk.Frame(root, name="sidebar")
sidebar.pack(side="left", fill="y")  # sticks to left, fills vertically

# Main frame (where content changes)
main_frame = tk.Frame(root, bg="#0A0F1F", width=900, height=700) #F0F8FF
main_frame.pack(side="right", fill="both", expand=True)

# Function to clear old widgets
def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

'''
# Function to clear the main frame
def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()


# Functions for each button
def show_home():
    clear_main_frame()
    tk.Label(main_frame, text="🏠 Home Page", bg="#F0F8FF", font=("Arial", 20, "bold")).pack(pady=50)

def show_settings():
    clear_main_frame()
    tk.Label(main_frame, text="⚙️ Settings Page", bg="#F0F8FF", font=("Arial", 20, "bold")).pack(pady=50)
'''
# ---------- TEXT TO ASL PAGE ----------
def show_text_to_asl():
    clear_main_frame()

    title = tk.Label(
        main_frame,
        text="Text to ASL Converter",
        bg="#F0F8FF",
        font=("Arial", 20, "bold"),
        fg="#071E35"
    )
    title.pack(pady=30)

    tk.Label(
        main_frame,
        text="Enter text below to convert:",
        bg="#2D455A",
        font=("Arial", 14)
    ).pack(pady=10)

    text_box = tk.Text(main_frame, height=5, width=50, font=("Arial", 14))
    text_box.pack(pady=10)

    status_label = tk.Label(main_frame, text="", bg="#F0F8FF", font=("Arial", 12), fg="green")
    status_label.pack(pady=10)

    def convert_text():
        text = text_box.get("1.0", tk.END).strip()

        if text:
            status_label.config(text=f"🖐 Converting: {text}", fg="green")

            if arduino:
                try:
                    arduino.write(text.encode())
                    print(f"📤 Sent to Arduino: {text}")
                    convert_btn.config(bg="#90EE90")
                    root.after(500, lambda: convert_btn.config(bg="white"))
                except Exception as e:
                    status_label.config(text=f"⚠️ Error sending to Arduino: {e}", fg="red")
                    print("⚠️ Error sending to Arduino:", e)
            else:
                status_label.config(text="⚠️ Arduino not connected.", fg="red")
                print("⚠️ Arduino not connected.")
        else:
            status_label.config(text="⚠️ Please enter some text.", fg="red")


    convert_btn = tk.Button(
        main_frame,
        text="Convert to ASL",
        command=convert_text,
        bg="white",
        fg="black",
        font=("Arial", 14),
        relief="ridge"
    )
    convert_btn.pack(pady=20)   

    # Back Button
    tk.Button(main_frame, text="⬅ Back",
              font=("Arial", 12), bg="white", fg="black",
              command=show_home).place(x=20, y=20)          

# ---------- HOME PAGE ----------
def show_home():
    clear_main_frame()
    
    
    tk.Label(main_frame, text="🏠 Home Page", bg="#26373A", font=("Arial", 20, "bold")).pack(pady=50)
    tk.Button(main_frame, text="Toggle Theme", command=toggle_theme).pack(pady=10)



# ---------- SETTINGS PAGE ----------
def show_settings_dup():
    clear_main_frame()
    tk.Label(main_frame, text="⚙️ Settings Page", bg="#F0F8FF", font=("Arial", 20, "bold")).pack(pady=50)

def show_settings():
    clear_main_frame()
    apply_theme(main_frame)   # apply current theme

    # ---------- TITLE ----------
    title = tk.Label(
        main_frame,
        text="Settings",
        font=("Arial", 24, "bold"),
    )
    title.pack(pady=20)

    # ========== THEME SECTION ==========
    theme_frame = tk.Frame(main_frame)
    theme_frame.pack(pady=15, fill="x", padx=30)
    apply_theme(theme_frame)

    tk.Label(theme_frame, text="Theme", font=("Arial", 16, "bold")).pack(anchor="w")

    tk.Button(
        theme_frame,
        text="Toggle Light/Dark Mode",
        font=("Arial", 14),
        command=toggle_theme
    ).pack(anchor="w", pady=8)

    # ========== ANIMATION SECTION ==========
    anim_frame = tk.Frame(main_frame)
    anim_frame.pack(pady=15, fill="x", padx=30)
    apply_theme(anim_frame)

    tk.Label(anim_frame, text="Animations", font=("Arial", 16, "bold")).pack(anchor="w")

    animation_var = tk.BooleanVar(value=True)

    tk.Checkbutton(
        anim_frame,
        text="Enable pop / fade-in animations",
        font=("Arial", 14),
        variable=animation_var
    ).pack(anchor="w", pady=8)

    # ========== IMAGE SIZE SECTION ==========
    size_frame = tk.Frame(main_frame)
    size_frame.pack(pady=15, fill="x", padx=30)
    apply_theme(size_frame)

    tk.Label(size_frame, text="Image Size", font=("Arial", 16, "bold")).pack(anchor="w")

    img_size_var = tk.StringVar(value="medium")

    sizes = [("Small (80px)", "small"),
             ("Medium (100px)", "medium"),
             ("Large (130px)", "large")]

    for text, value in sizes:
        tk.Radiobutton(
            size_frame,
            text=text,
            variable=img_size_var,
            value=value,
            font=("Arial", 14)
        ).pack(anchor="w")

    # ========== HELP SECTION ==========
    help_frame = tk.Frame(main_frame)
    help_frame.pack(pady=15, fill="x", padx=30)
    apply_theme(help_frame)

    tk.Label(help_frame, text="Help", font=("Arial", 16, "bold")).pack(anchor="w")

    tk.Label(
        help_frame,
        text="• Type any text in English (A–Z, 0–9) to convert.\n"
             "• Show Alphabet displays all ASL letters.\n"
             "• Use settings to change theme or image size.",
        justify="left",
        font=("Arial", 13)
    ).pack(anchor="w", pady=8)

    # ========== ABOUT SECTION ==========
    about_frame = tk.Frame(main_frame)
    about_frame.pack(pady=20, fill="x", padx=30)
    apply_theme(about_frame)

    tk.Label(about_frame, text="About This App", font=("Arial", 16, "bold")).pack(anchor="w")

    tk.Label(
        about_frame,
        text="ASL Fingerspelling App\nVersion 1.0\nCreated by Aayushi ❤️",
        justify="left",
        font=("Arial", 13)
    ).pack(anchor="w", pady=8)

    # ========== BACK BUTTON ==========
    tk.Button(
        main_frame,
        text="⬅ Back",
        font=("Arial", 12),
        command=show_home
    ).place(x=20, y=20)


# ---------- ABOUT PAGE ----------
def show_about():
    clear_main_frame()
    tk.Label(main_frame, text="ℹ️ About Page", bg="#F0F8FF", font=("Arial", 20, "bold")).pack(pady=50)

# ---------- CHEAT SHEET ----------
def show_asl_alphabet():
    clear_main_frame()

    # Title
    tk.Label(
        main_frame,
        text="ASL Alphabet (A–Z, 0–9)",
        bg="#F0F8FF",
        font=("Arial", 20, "bold"),
        fg="#071E35"
    ).pack(pady=20)

    # Frame for gallery
    gallery_frame = tk.Frame(main_frame, bg="#F0F8FF")
    gallery_frame.pack(pady=10, fill="both", expand=True)

    image_folder = "asl_images"
    image_refs = []

    # Characters to display
    chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    row = 0
    col = 0
    max_cols = 8  # images per row

    for char in chars:
        image_path = os.path.join(image_folder, f"{char}.png")

        if os.path.exists(image_path):
            img = Image.open(image_path).resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            image_refs.append(photo)

            # Label with character name + image
            container = tk.Frame(gallery_frame, bg="#F0F8FF")
            container.grid(row=row, column=col, padx=15, pady=15)

            lbl_img = tk.Label(container, image=photo, bg="#F0F8FF")
            lbl_img.pack()

            lbl_text = tk.Label(container, text=char, font=("Arial", 12, "bold"),
                                bg="#F0F8FF", fg="#071E35")
            lbl_text.pack()

        col += 1
        if col >= max_cols:
            col = 0
            row += 1

    gallery_frame.image_refs = image_refs  # prevent garbage collection

    # Back button
    tk.Button(
        main_frame,
        text="⬅ Back",
        font=("Arial", 12),
        bg="white",
        fg="black",
        relief="ridge",
        command=show_home
    ).place(x=20, y=20)


# --- Simple POP animation for images ---
def pop_in(widget, scale=1.0):
    if scale >= 1.15:   # stop at 115%
        widget.scale = 1.0  
        return  

    try:
        widget.tk.call(widget, "scale", 0, 0, scale, scale)
    except:
        pass  # in case Tk doesn't support scale on your version

    widget.after(20, lambda: pop_in(widget, scale + 0.03))


def fade_in(widget, pil_image, duration=300, steps=10):
    """
    Smooth fade-in animation for image labels.
    widget: the tk.Label containing the image
    pil_image: the original PIL image
    duration: total animation duration (ms)
    steps: how many fade steps
    """
    step_time = duration // steps
    enhancer = ImageEnhance.Brightness(pil_image)

    # store references so image isn't garbage-collected
    if not hasattr(widget, "fade_refs"):
        widget.fade_refs = []

    def animate(step=0):
        if step > steps:
            return

        factor = step / steps  # 0 → 1 brightness
        bright_img = enhancer.enhance(factor)
        photo = ImageTk.PhotoImage(bright_img)

        widget.configure(image=photo)
        widget.fade_refs.append(photo)

        widget.after(step_time, lambda: animate(step + 1))

    animate()

# ---------- SHOW ALPHABETS ----------
def show_asl_images_w_grid():
    clear_main_frame()

    tk.Label(main_frame, text="ASL Fingerspelling Output",
             bg="#F0F8FF", font=("Arial", 20, "bold"), fg="#071E35").pack(pady=20)

    input_box = tk.Text(main_frame, height=3, width=40, font=("Arial", 14))
    input_box.pack(pady=10)

    images_frame = tk.Frame(main_frame, bg="#223058") #bg
    images_frame.pack(pady=20, fill="both", expand=True)

    def convert_to_images():
        for widget in images_frame.winfo_children():
            widget.destroy()

        text = input_box.get("1.0", tk.END).strip().upper()
        image_folder = "asl_images"
        image_refs = []

        row = 0
        col = 0
        max_cols = 8

        # ---- Loop through words first ----
        for word in text.split(" "):
            for char in word:
                if char.isalnum():
                    image_path = os.path.join(image_folder, f"{char}.png")

                    if os.path.exists(image_path):
                        img = Image.open(image_path).resize((100, 100))
                        photo = ImageTk.PhotoImage(img)
                        image_refs.append(photo)

                        lbl = tk.Label(images_frame, image=photo, bg="#F0F8FF")
                        lbl.grid(row=row, column=col, padx=10, pady=10)

                        # --- POP IN ANIMATION HERE ---
                        #pop_in(lbl)
                        fade_in(lbl, img)


                        col += 1
                        if col >= max_cols:
                            col = 0
                            row += 1
                    else:
                        print(f"⚠️ No image for {char}")

            # ---- REAL WORD SPACER (this creates visible gap) ----
            spacer = tk.Label(images_frame, bg="#223058", width=2) #space
            spacer.grid(row=row, column=col, padx=20)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        images_frame.image_refs = image_refs

    tk.Button(main_frame, text="Show ASL Images",
              font=("Arial", 14), bg="white", fg="black",
              command=convert_to_images).pack(pady=10)

    tk.Button(main_frame, text="⬅ Back",
              font=("Arial", 12), bg="white", fg="black",
              command=show_home).place(x=20, y=20)

def show_asl_images_line():
    clear_main_frame()

    # Title
    tk.Label(main_frame, text="ASL Fingerspelling Output",
             bg="#F0F8FF", font=("Arial", 20, "bold"), fg="#071E35").pack(pady=20)

    # Text box
    input_box = tk.Text(main_frame, height=3, width=40, font=("Arial", 14))
    input_box.pack(pady=10)

    # Frame to display images
    images_frame = tk.Frame(main_frame, bg="#F0F8FF")
    images_frame.pack(pady=20)

    def convert_to_images():
        # Clear old images if present
        for widget in images_frame.winfo_children():
            widget.destroy()

        text = input_box.get("1.0", tk.END).strip().upper()

        # store image references so Tkinter does not garbage-collect them
        image_refs = []

        image_folder = "asl_images"

        for word in text.split(" "):
            for char in word:
                if char.isalnum():
                    image_path = os.path.join(image_folder, f"{char}.png")

                    if os.path.exists(image_path):
                        img = Image.open(image_path).resize((100, 100))
                        photo = ImageTk.PhotoImage(img)
                        image_refs.append(photo)

                        lbl = tk.Label(images_frame, image=photo, bg="#F0F8FF")
                        lbl.pack(side="left", padx=5)
                    else:
                        print(f"⚠️ No image for {char}")
            
            # extra gap between words
            spacer = tk.Label(images_frame, width=2, bg="#F0F8FF")
            spacer.pack(side="left", padx=25)

        # save reference list to frame to prevent garbage deletion
        images_frame.image_refs = image_refs

    # Convert Button
    tk.Button(main_frame, text="Show ASL Images",
              font=("Arial", 14), bg="white", fg="black",
              command=convert_to_images).pack(pady=10)

    # Back Button
    tk.Button(main_frame, text="⬅ Back",
              font=("Arial", 12), bg="white", fg="black",
              command=show_home).place(x=20, y=20)

def apply_theme(widget):
    mode = THEME["mode"]
    t = THEME[mode]

    wname = widget.winfo_name()
    wclass = widget.winfo_class()

    # ------------------------------------------------
    # MAIN WINDOW BACKGROUND
    # ------------------------------------------------
    try:
        widget.config(bg=t["bg"])
    except:
        pass

    # ------------------------------------------------
    # SIDEBAR
    # ------------------------------------------------
    if wname == "sidebar":  
        try: widget.config(bg=t["sidebar_bg"])
        except: pass

    if wname == "sidebar_title":
        try:
            widget.config(bg=t["sidebar_bg"], fg=t["sidebar_fg"])
        except:
            pass

    # SIDEBAR BUTTONS
    if wname.startswith("sidebar_btn"):
        try:
            widget.config(bg=t["sidebar_button_bg"], fg=t["sidebar_button_fg"], activebackground=t["sidebar_button_hover"])
        except:
            pass

    # ------------------------------------------------
    # FRAMES / CARDS
    # ------------------------------------------------
    if wclass == "Frame":
        try:
            widget.config(bg=t["frame_bg"])
        except:
            pass

    # ------------------------------------------------
    # LABELS
    # ------------------------------------------------
    if wclass == "Label":
        try:
            widget.config(bg=t["bg"], fg=t["fg"])
        except:
            pass

    # ------------------------------------------------
    # INPUT BOX
    # ------------------------------------------------
    if wclass == "Text" or wclass == "Entry":
        try:
            widget.config(
                bg=t["textbox_bg"],
                fg=t["textbox_fg"],
                insertbackground=t["textbox_fg"],
                highlightbackground=t["textbox_border"],
                highlightcolor=t["textbox_border"]
            )
        except:
            pass

    # ------------------------------------------------
    # STANDARD BUTTONS
    # ------------------------------------------------
    if wclass == "Button" and not wname.startswith("sidebar_btn"):
        try:
            widget.config(
                bg=t["button_bg"],
                fg=t["button_fg"],
                activebackground=t["button_hover"]
            )
        except:
            pass

    # ------------------------------------------------
    # RECURSIVE — APPLY TO ALL CHILDREN
    # ------------------------------------------------
    for child in widget.winfo_children():
        apply_theme(child)

'''
def apply_theme(widget):
    mode = THEME["mode"]
    t = THEME[mode]

    # 1️⃣ APPLY TO MAIN WINDOW / GENERIC BACKGROUND
    try:
        widget.config(bg=t["bg"])
    except:
        pass

    # 2️⃣ LABEL
    if widget.winfo_class() == "Label":
        try:
            widget.config(bg=t["bg"], fg=t["fg"])
        except:
            pass

    # 3️⃣ BUTTON
    if widget.winfo_class() == "Button":
        try:
            widget.config(
                bg=t["button_bg"],
                fg=t["button_fg"],
                activebackground=t["button_hover"],
                activeforeground=t["button_fg"]
            )
        except:
            pass

    # 4️⃣ FRAME / CARD
    if widget.winfo_class() == "Frame":
        try:
            widget.config(bg=t["frame_bg"])
        except:
            pass

    # 5️⃣ ENTRY (input box)
    if widget.winfo_class() == "Entry":
        try:
            widget.config(
                bg=t["textbox_bg"],
                fg=t["textbox_fg"],
                insertbackground=t["textbox_fg"],
                highlightbackground=t["textbox_border"],
                highlightcolor=t["textbox_border"]
            )
        except:
            pass

    # 6️⃣ TEXT widget
    if widget.winfo_class() == "Text":
        try:
            widget.config(
                bg=t["textbox_bg"],
                fg=t["textbox_fg"],
                insertbackground=t["textbox_fg"]
            )
        except:
            pass

    # 7️⃣ SIDEBAR (you must give sidebar a custom className or widget name)
    # Example: sidebar_frame = tk.Frame(root, name="sidebar")
    if str(widget) == ".sidebar" or widget.winfo_name() == "sidebar":
        try:
            widget.config(bg=t["sidebar_bg"])
        except:
            pass

    # 8️⃣ SIDEBAR BUTTONS
    if "sidebar_btn" in widget.winfo_name():
        try:
            widget.config(
                bg=t["sidebar_button_bg"],
                fg=t["sidebar_button_fg"],
                activebackground=t["sidebar_button_hover"]
            )
        except:
            pass

    # RECURSIVELY APPLY THEME TO CHILDREN
    for child in widget.winfo_children():
        apply_theme(child)
'''
def toggle_theme():
    THEME["mode"] = "dark" if THEME["mode"] == "light" else "light"
    apply_theme(root)


# widgets inside sidebar
#label = tk.Label(sidebar, text="Menu", name="sidebar_title")
#label.pack(pady=20)

label = tk.Label(sidebar, text="Menu", name="sidebar_title", font=("Arial", 16, "bold"))
label.pack(pady=20)

btn1 = tk.Button(sidebar, text="Home", name="sidebar_btn_home", relief="flat", command=show_home)
btn1.pack(pady=10, padx=20, fill="x")

btn2 = tk.Button(sidebar, text="Text-to-ASL", name="sidebar_btn_text", relief="flat", command=show_text_to_asl)
btn2.pack(pady=10, padx=20, fill="x")

btn3 = tk.Button(sidebar, text="Show Alphabet", name="sidebar_btn_alpha", relief="flat", command=show_asl_images_w_grid)
btn3.pack(pady=10, padx=20, fill="x")

btn4 = tk.Button(sidebar, text="About", name="sidebar_btn_about", relief="flat", command=show_asl_alphabet)
btn4.pack(pady=10, padx=20, fill="x")

btn5 = tk.Button(sidebar, text="Settings", name="sidebar_btn_settings", relief="flat", command=show_settings)
btn5.pack(pady=10, padx=20, fill="x")

'''
label = tk.Label(sidebar, text="Menu", bg="#F8F8F3", fg="#223058", font=("Arial", 16, "bold"))
label.pack(pady=20)

btn1 = tk.Button(sidebar, text="Home", bg="#1A2340", fg="#223058", relief="flat", command=show_home)
btn1.pack(pady=10, padx=20, fill="x")

btn2 = tk.Button(sidebar, text="Text-to-ASL", bg="#1A2340", fg="#223058", relief="flat", command=show_text_to_asl)
btn2.pack(pady=10, padx=20, fill="x")

btn3 = tk.Button(sidebar, text="Show Alphabet", bg="#1A2340", fg="#223058", relief="flat", command=show_asl_images_w_grid)
btn3.pack(pady=10, padx=20, fill="x")

btn4 = tk.Button(sidebar, text="About", bg="#1A2340", fg="#223058", relief="flat", command=show_asl_alphabet)
btn4.pack(pady=10, padx=20, fill="x")

btn5 = tk.Button(sidebar, text="Settings", bg="#1A2340", fg="#223058", relief="flat", command=show_settings)
btn5.pack(pady=10, padx=20, fill="x")
'''
show_home()

root.mainloop()


'''
#bg_image = tk.PhotoImage(file="background.gif")  # change name

img = Image.open("background.gif")   # or .png / .jpg
img = img.resize((600, 400))         # match window size
bg = ImageTk.PhotoImage(img)

label = tk.Label(root, image=bg_image)
label.place(x=0, y=0, relwidth=1, relheight=1)
 
'''

'''
    def convert_text():
        text = text_box.get("1.0", tk.END).strip()

        if text:
            status_label.config(text=f"🖐 Converting: {text}", fg="green")

            # ✅ Send the text to Arduino (if connected)
            if arduino:
                try:
                    arduino.write(text.encode())  # send text as bytes
                    print(f"📤 Sent to Arduino: {text}")
                    convert_btn.config(bg="#90EE90")  # light green feedback
                    root.after(500, lambda: convert_btn.config(bg="white"))  # back to normal after 0.5s
                except Exception as e:
                    print("⚠️ Error sending to Arduino:", e)
            else:
                print("⚠️ Arduino not connected.")
        else:
            status_label.config(text="⚠️ Please enter some text.", fg="red")
        '''
'''
    def convert_text():
        text = text_box.get("1.0", tk.END).strip()
        if text:
            status_label.config(text=f"🖐 Converting: {text}", fg="green")
        else:
            status_label.config(text="⚠️ Please enter some text.", fg="red")
'''
'''
pramodsarai@SSD-Air-1 python % /usr/local/bin/python3 /Users/pramodsarai/Desktop/python/z.py
⚠️ Could not connect to Arduino: [Errno 2] could not open port /dev/cu.usbmodem1101: [Errno 2] No such file or directory: '/dev/cu.usbmodem1101'
pramodsarai@SSD-Air-1 python % /usr/local/bin/python3 /Users/pramodsarai/Desktop/python/z.py
⚠️ Could not connect to Arduino: [Errno 2] could not open port /dev/cu.usbmodem1101: [Errno 2] No such file or directory: '/dev/cu.usbmodem1101'
⚠️ Arduino not connected.
⚠️ Arduino not connected.
pramodsarai@SSD-Air-1 python % 
'''
'''
# --- 2️⃣ DISPLAY ASL IMAGES ---
def show_asl_images_dup():
    clear_main_frame()

    text_box = tk.Text(main_frame, height=5, width=50, font=("Arial", 14))
    text_box.pack(pady=10)
    text = text_box.get("1.0", tk.END).strip().upper()

    tk.Label(main_frame, text=f"ASL for: {text}", bg="#F0F8FF",
                font=("Arial", 18, "bold"), fg="#071E35").pack(pady=20)
    
    images_frame = tk.Frame(main_frame, bg="#F0F8FF")
    images_frame.pack(pady=20)

    image_folder = "asl_images"
    images = []

    for word in text.split(" "):  # split by space
        for char in word:
            if char.isalnum():
                image_path = os.path.join(image_folder, f"{char}.png")
                try:
                    img = Image.open(image_path)
                    img = img.resize((100, 100))
                    photo = ImageTk.PhotoImage(img)
                    images.append(photo)

                    lbl = tk.Label(images_frame, image=photo, bg="#F0F8FF")
                    lbl.pack(side="left", padx=5)
                except FileNotFoundError:
                    print(f"⚠️ Image not found for: {char}")

        # add extra gap between words
        spacer = tk.Label(images_frame, width=2, bg="#F0F8FF")
        spacer.pack(side="left", padx=20)
"""    
    for char in text:
        if char.isalnum():  # only letters and numbers
            image_path = os.path.join(image_folder, f"{char}.png")
            try:
                img = Image.open(image_path)
                img = img.resize((100, 100))
                photo = ImageTk.PhotoImage(img)
                images.append(photo)

                lbl = tk.Label(images_frame, image=photo, bg="#F0F8FF")
                lbl.pack(side="left", padx=5)
            except FileNotFoundError:
                print(f"⚠️ Image not found for: {char}")
"""
                
    if not images:
        tk.Label(main_frame, text="⚠️ No valid letters or numbers to display.",
                    bg="#F0F8FF", fg="red", font=("Arial", 12)).pack(pady=10)
        

        # --- Back button (top-left corner) ---
    back_btn = tk.Button(
        main_frame,
        text="⬅ Back",
        command=show_home,  
        bg="white",
        fg="black",
        font=("Arial", 12),
        relief="ridge"
    )
    back_btn.place(x=20, y=20)  # top-left corner
   
    '''