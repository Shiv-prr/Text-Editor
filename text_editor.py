import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from datetime import datetime
import os

current_file = None

def mark_modified(event=None):
    if text.edit_modified():
        if current_file:
            file_name = os.path.basename(current_file)
            root.title(f"* {file_name} - Txt Editor")
        else:
            root.title("* Untitled - Txt Editor")

        text.edit_modified(False)

def set_saved_state():
    text.edit_modified(False)
    if current_file:
        file_name = os.path.basename(current_file)
        root.title(f"{file_name} - Txt Editor")
    else:
        root.title("Untitled - Txt Editor")

def check_unsaved_changes():
    if text.get("1.0", tk.END).strip() and root.title().startswith("*"):

        result = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes.\n\n"
            "Do you want to save before continuing?"
        )

        if result is True:
            saved = save_file()

            if saved:
                return True
            else:
                return False

        elif result is False:
            return True
        
        else:
            return False
    return True

def new_file():
    global current_file

    if not check_unsaved_changes():
        return

    text.delete("1.0", tk.END)
    current_file = None
    update_title()
    set_saved_state()

def open_file():
    global current_file

    if not check_unsaved_changes():
        return
    file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )
    if file_path:
        try:
            with open(file_path, "r") as file:

                text.delete("1.0", tk.END)
                text.insert("1.0", file.read())
            current_file = file_path
            update_title()
            set_saved_state()
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not open file.\n\n{error}"
            )

def save_file():
    global current_file

    if current_file:
        file_path = current_file
    else:
        file_path = filedialog.asksaveasfilename(title="Save File",defaultextension=".txt",filetypes=[("Text Files", "*.txt"),("All Files", "*.*")])

    if not file_path:
        return False
    try:
        with open(file_path, "w") as file:
            file.write(text.get("1.0", tk.END))
        current_file = file_path
        update_title()
        set_saved_state()

        messagebox.showinfo("Success","File saved successfully!")
        return True
    
    except Exception as error:
        messagebox.showerror("Error",f"Could not save file.\n\n{error}")
        return False
    
def save_as_file():
    global current_file

    file_path = filedialog.asksaveasfilename(title="Save As",defaultextension=".txt",filetypes=[("Text Files", "*.txt"),("All Files", "*.*")])

    if not file_path:
        return False

    try:
        with open(file_path, "w") as file:
            file.write(text.get("1.0", tk.END))

        current_file = file_path
        update_title()
        set_saved_state()

        messagebox.showinfo("Success","File saved successfully!")
        return True
    except Exception as error:
        messagebox.showerror("Error",f"Could not save file.\n\n{error}")
        return False
    
def undo():
    try:
        text.edit_undo()
    except tk.TclError:
        pass

def redo():
    try:
        text.edit_redo()
    except tk.TclError:
        pass

def update_clock():
    current_time = datetime.now().strftime("%I:%M:%S %p")

    clock_label.config(text=current_time)
    root.after(1000, update_clock)

def update_statistics(event=None):
    content = text.get("1.0", tk.END).strip()
    words = len(content.split())
    characters = len(content)

    word_label.config(text=f"Words: {words}")
    character_label.config(text=f"Characters: {characters}")

def find_text():
    search_word = simpledialog.askstring("Find","Enter text to search:")
    if search_word:
        text.tag_remove("search","1.0",tk.END)
        start_pos = "1.0"

        while True:
            start_pos = text.search(search_word,start_pos,stopindex=tk.END,nocase=True)

            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_word)}c"

            text.tag_add("search",start_pos,end_pos)
            start_pos = end_pos
        text.tag_config("search",background="yellow",foreground="black")

def replace_text():
    find_word = simpledialog.askstring("Replace","Text to find:")

    if not find_word:
        return
    
    replace_word = simpledialog.askstring("Replace","Replace with:")

    if replace_word is None:
        return

    content = text.get("1.0",tk.END)
    new_content = content.replace(find_word,replace_word)
    text.delete("1.0",tk.END)
    text.insert("1.0",new_content)

def update_line_numbers(event=None):
    line_numbers.config(state="normal")

    line_numbers.delete("1.0",tk.END)
    total_lines = int(text.index("end-1c").split(".")[0])
    numbers = "\n".join(str(i)for i in range(1, total_lines + 1))

    line_numbers.insert("1.0",numbers)
    line_numbers.config(state="disabled")

def increase_font():
    global font_size

    font_size += 1
    text.config(
        font=("Helvetica", font_size)
    )
    line_numbers.config(
        font=("Helvetica", font_size)
    )
    font_label.config(
        text=f"Font: {font_size}px"
    )

def decrease_font():
    global font_size
    if font_size > 8:
        font_size -= 1
        text.config(
            font=("Helvetica", font_size)
        )
        line_numbers.config(
            font=("Helvetica", font_size)
        )
        font_label.config(
            text=f"Font: {font_size}px"
        )

def reset_font():
    global font_size
    font_size = 15
    text.config(
        font=("Helvetica", font_size)
    )
    line_numbers.config(
        font=("Helvetica", font_size)
    )
    font_label.config(
        text=f"Font: {font_size}px"
    )

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        root.config(bg="#2b2b2b")

        top_bar.config(bg="#2b2b2b")
        clock_label.config(bg="#2b2b2b",fg="white")

        editor_frame.config(bg="#2b2b2b")
        text.config(bg="#1e1e1e",fg="white",insertbackground="white")
        line_numbers.config(bg="#2b2b2b",fg="white")

        status_bar.config(bg="#2b2b2b")
        word_label.config(bg="#2b2b2b",fg="white")
        character_label.config(bg="#2b2b2b",fg="white")

    else:
        root.config(bg="white")
        top_bar.config(bg="white")

        clock_label.config(bg="white",fg="black")

        editor_frame.config(bg="white")
        text.config(bg="white",fg="black",insertbackground="black")

        line_numbers.config(bg="#f0f0f0",fg="gray")
        status_bar.config(bg="white")
        word_label.config(bg="white",fg="black")

        character_label.config(bg="white",fg="black")

def update_cursor_position(event=None):
    position = text.index(tk.INSERT)

    line, column = position.split(".")
    position_label.config(text=f"Ln: {line}, Col: {column}")

def insert_tab(event):
    text.insert(tk.INSERT, "    ")
    return "break"

def auto_indent(event):
    current_line = text.get("insert linestart","insert lineend")

    indentation = len(current_line) - len(current_line.lstrip())
    text.insert(tk.INSERT,"\n" + (" " * indentation))
    return "break"

def show_about():
    messagebox.showinfo(
        "About Txt Editor",
        "Txt Editor\n\n"
        "A simple cross-platform text editor\n"
        "built using Python and Tkinter.\n\n"
        "Version 1.0\n\n"
        "Created by Shiv Pratap"
    )

def update_title():
    if current_file:
        file_name = os.path.basename(current_file)
        root.title(
            f"{file_name} - Txt Editor"
        )
    else:
        root.title(
            "Untitled - Txt Editor"
        )

def change_font(font_name):
    global font_family
    font_family = font_name

    text.config(font=(font_family, font_size))
    line_numbers.config(font=(font_family, font_size))

def toggle_bold():
    try:
        start = text.index("sel.first")
        end = text.index("sel.last")

        if "bold" in text.tag_names(start):
            text.tag_remove("bold", start, end)
        else:
            text.tag_add("bold", start, end)
        update_text_style(start, end)
    except tk.TclError:
        messagebox.showwarning(
            "Bold",
            "Please select some text first."
        )

def toggle_italic():
    try:
        start = text.index("sel.first")
        end = text.index("sel.last")

        if "italic" in text.tag_names(start):
            text.tag_remove("italic", start, end)
        else:
            text.tag_add("italic", start, end)
        update_text_style(start, end)
    except tk.TclError:
        messagebox.showwarning(
            "Italic",
            "Please select some text first."
        )

def toggle_underline():
    try:
        start = text.index("sel.first")
        end = text.index("sel.last")

        if "underline" in text.tag_names(start):
            text.tag_remove("underline", start, end)
        else:
            text.tag_add("underline", start, end)
    except tk.TclError:
        messagebox.showwarning(
            "Underline",
            "Please select some text first."
        )

def update_text_style(start, end):
    current_tags = text.tag_names(start)

    is_bold = "bold" in current_tags
    is_italic = "italic" in current_tags

    if is_bold and is_italic:
        font_style = ("bold", "italic")
    elif is_bold:
        font_style = "bold"
    elif is_italic:
        font_style = "italic"
    else:
        font_style = "normal"

    text.tag_configure("bold",font=(font_family, font_size, font_style))
    text.tag_configure("italic",font=(font_family, font_size, font_style))

def quit_app():
    if check_unsaved_changes():
        root.destroy()

# WINDOW
root = tk.Tk()
root.title("Untitled - Txt Editor")
root.geometry("800x600")
root.configure(bg="white")
font_size = 15
font_family = "Helvetica"
dark_mode = False

# MENU
menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0)
edit_menu = tk.Menu(menu, tearoff=0)
view_menu = tk.Menu(menu, tearoff=0)
font_menu = tk.Menu(view_menu, tearoff=0)
help_menu = tk.Menu(menu, tearoff=0)

menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Edit", menu=edit_menu)
menu.add_cascade(label="View", menu=view_menu)
menu.add_cascade(label="Help", menu=help_menu)

file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As",command=save_as_file)
file_menu.add_separator()

edit_menu.add_command(label="Undo",command=undo)
edit_menu.add_command(label="Redo",command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Find",command=find_text)
edit_menu.add_command(label="Replace",command=replace_text)
edit_menu.add_separator()
edit_menu.add_command(label="Bold",command=toggle_bold)
edit_menu.add_command(label="Italic",command=toggle_italic)
edit_menu.add_command(label="Underline",command=toggle_underline)

view_menu.add_command(label="Increase Font",command=increase_font)
view_menu.add_command(label="Decrease Font",command=decrease_font)
view_menu.add_separator()
view_menu.add_command(label="Reset Font",command=reset_font)
view_menu.add_separator()
view_menu.add_command(label="Toggle Dark Mode",command=toggle_dark_mode)
view_menu.add_separator()
view_menu.add_cascade(label="Font",menu=font_menu)

font_menu.add_command(label="Helvetica",command=lambda: change_font("Helvetica"))
font_menu.add_command(label="Arial",command=lambda: change_font("Arial"))
font_menu.add_command(label="Courier",command=lambda: change_font("Courier"))
font_menu.add_command(label="Times",command=lambda: change_font("Times"))

help_menu.add_command(label="About",command=show_about)

file_menu.add_command(label="Quit", command=quit_app)

# TOP BAR
top_bar = tk.Frame(root,bg="white")
top_bar.pack(fill=tk.X)

# DIGITAL CLOCK
clock_label = tk.Label(top_bar,text="",font=("Helvetica", 12),bg="white",fg="black")
clock_label.pack(side=tk.RIGHT,padx=10)

editor_frame = tk.Frame(root, bg="white")
editor_frame.pack(side=tk.TOP,expand=True,fill=tk.BOTH)

# TEXT EDITOR
text = tk.Text(editor_frame, wrap=tk.NONE, font=(font_family, font_size), fg="black", bg="white", insertbackground="black",undo=True)
text.tag_configure("bold",font=(font_family, font_size, "bold"))
text.tag_configure("italic",font=(font_family, font_size, "italic"))
text.tag_configure("underline",underline=True)

scrollbar = tk.Scrollbar(editor_frame,orient=tk.VERTICAL,command=text.yview)
horizontal_scrollbar = tk.Scrollbar(editor_frame,orient=tk.HORIZONTAL,command=text.xview)

line_numbers = tk.Text(editor_frame,width=4,padx=5,takefocus=0,border=0,state="disabled",bg="#f0f0f0",fg="gray",font=(font_family, font_size))

# STATUS BAR
status_bar = tk.Frame(root,bg="white")
status_bar.pack(side=tk.BOTTOM,fill=tk.X)

word_label = tk.Label(status_bar,text="Words: 0",bg="white",fg="black")
word_label.pack(side=tk.LEFT,padx=10,pady=5)
character_label = tk.Label(status_bar,text="Characters: 0",bg="white",fg="black")
character_label.pack(side=tk.LEFT,padx=10,pady=5)
font_label = tk.Label(status_bar,text=f"Font: {font_size}px",bg="white",fg="black")
font_label.pack(side=tk.LEFT,padx=10,pady=5)
position_label = tk.Label(status_bar,text="Ln: 1, Col: 0",bg="white",fg="black")
position_label.pack(side=tk.RIGHT, padx=10, pady=5)

# TEXT EDITOR
line_numbers.pack(side=tk.LEFT,fill=tk.Y)
text.config(yscrollcommand=scrollbar.set,xscrollcommand=horizontal_scrollbar.set)

scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
horizontal_scrollbar.pack(side=tk.BOTTOM,fill=tk.X)
text.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)

text.bind("<KeyRelease>", update_cursor_position)
text.bind("<ButtonRelease-1>", update_cursor_position)

# Text modify hone par tracking
text.bind("<<Modified>>",mark_modified)
text.bind("<KeyRelease>",update_statistics)
text.bind("<Tab>", insert_tab)
text.bind("<Return>", auto_indent)
text.bind("<<Modified>>",update_line_numbers,add="+")
text.bind("<KeyRelease>", update_cursor_position)
text.bind("<ButtonRelease-1>", update_cursor_position)

# KEYBOARD SHORTCUTS
root.bind("<Command-n>", lambda event: new_file())
root.bind("<Control-n>", lambda event: new_file())

root.bind("<Command-o>", lambda event: open_file())
root.bind("<Control-o>", lambda event: open_file())

root.bind("<Command-s>", lambda event: save_file())
root.bind("<Control-s>", lambda event: save_file())

root.bind("<Command-Shift-S>", lambda event: save_as_file())
root.bind("<Control-Shift-S>", lambda event: save_as_file())

root.bind("<Command-z>", lambda event: undo())
root.bind("<Control-z>", lambda event: undo())

root.bind("<Command-Shift-Z>", lambda event: redo())
root.bind("<Control-Shift-Z>", lambda event: redo())
root.bind("<Control-y>", lambda event: redo())

root.bind("<Command-q>", lambda event: quit_app())
root.bind("<Control-q>", lambda event: quit_app())

root.bind("<Command-f>", lambda event: find_text())
root.bind("<Control-f>", lambda event: find_text())

root.bind("<Command-h>", lambda event: replace_text())
root.bind("<Control-h>", lambda event: replace_text())

# Window close button ke liye bhi warning
root.protocol("WM_DELETE_WINDOW",quit_app)

set_saved_state()
update_clock()
update_line_numbers()
root.mainloop()