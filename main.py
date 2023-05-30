import os
import shutil
import tkinter as tk
import zipfile
import logging
from tkinter import messagebox, filedialog, Scrollbar, Checkbutton, IntVar
from datetime import datetime



# 윈도우즈에서의 마인크래프트 세이브 파일 위치
minecraft_dir = os.path.expandvars('%APPDATA%\\.minecraft\\saves')

# 백업 디렉토리 위치
backup_dir = os.path.expanduser('./MinecraftBackups')
if not os.path.exists(backup_dir):
    os.mkdir(backup_dir)
# 현재 날짜와 시간을 가져옴
now = datetime.now()

# 백업 파일 이름 형식 설정
backup_name = now.strftime("%Y%m%d%H%M%S")

# 로그 설정
logging.basicConfig(filename="backup_log.txt", level=logging.INFO,encoding='utf-8')
# 월드 리스트 생성
worlds = [f for f in os.listdir(minecraft_dir) if os.path.isdir(os.path.join(minecraft_dir, f))]

# 로고 파일 위치
logo_path = "minecraft_logo.png" # 로고 파일 경로를 변경해 주세요.

root = tk.Tk()
root.title("Minecraft Backup Creator")

if os.path.isfile(logo_path):
    root.iconphoto(False, tk.PhotoImage(file=logo_path))

root.geometry("500x500")

# 압축 선택 여부 변수
compress_var = IntVar()

def backup_minecraft():
    selected_world = world_listbox.curselection()
    if selected_world:
        source = os.path.join(minecraft_dir, worlds[selected_world[0]])
        destination = os.path.join(backup_dir, f"{worlds[selected_world[0]]}_{backup_name}")
        if compress_var.get():
            destination += ".zip"
            with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as zipf:
                for foldername, subfolders, filenames in os.walk(source):
                    for filename in filenames:
                        filepath = os.path.join(foldername, filename)
                        zipf.write(filepath, arcname=os.path.relpath(filepath, source))
        else:
            shutil.copytree(source, destination)
        logging.info(f"Backup created: {destination}")
        messagebox.showinfo("Backup Completed", f"Minecraft world backup has been created at {destination}!")
    else:
        messagebox.showinfo("No Selection", "No Minecraft world selected. Please select a world.")

def select_backup_dir():
    global backup_dir
    backup_dir = filedialog.askdirectory(initialdir=backup_dir)
    backup_dir_label.config(text=f"Backup Directory: {backup_dir}")
    messagebox.showinfo("Backup Directory Updated", f"Backup directory has been updated to {backup_dir}!")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=20, pady=10)

scrollbar = Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

world_listbox = tk.Listbox(frame, height=15, yscrollcommand=scrollbar.set)
world_listbox.pack(fill="both", expand=True)

scrollbar.config(command=world_listbox.yview)

for world in worlds:
    world_listbox.insert(tk.END, world)

select_button = tk.Button(root, text="Backup Selected World", command=backup_minecraft, 
                          bg="dark green", fg="white", activebackground="green", activeforeground="white", height=2, width=20)
select_button.pack(pady=10)

backup_dir_label = tk.Label(root, text=f"Backup Directory: {backup_dir}")
backup_dir_label.pack()

select_dir_button = tk.Button(root, text="Select Backup Directory", command=select_backup_dir, 
                              bg="dark blue", fg="white", activebackground="blue", activeforeground="white", height=2, width=20)
select_dir_button.pack(pady=10)

compress_checkbutton = Checkbutton(root, text="Compress Backup (ZIP)", variable=compress_var)
compress_checkbutton.pack(pady=10)

root.mainloop()
