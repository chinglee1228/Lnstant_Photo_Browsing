import tkinter as tk
import os
import glob
from tkinter import filedialog
from PIL import Image, ImageTk

# 主視窗
win = tk.Tk()
win.title('Preview')
win.geometry('400x950')
win_height = 500
win_width = 390

sw = win.winfo_screenwidth() -10 # 取得視窗高度
sh = win.winfo_screenheight() - 10  # 取得視窗寬度
x = (sw - win_height) / 2
y = (sh - win_width) / 2

# 全域變數
file_path = ''
img_files = []
img_num = 0
img_num2 = 0
file_extension = '.jpg'
refresh_interval = 1000  # 1秒鐘
# -----------------------------------
top_frame = tk.Frame(win)
top_frame.pack()
top2 = tk.Frame(win)
top2.pack()
bottom_frame = tk.Frame(win)
bottom_frame.pack(side=tk.BOTTOM)
topmos = tk.StringVar()
update = tk.StringVar()
now = tk.StringVar()

# -----------------------------------

def ontop():
    global opentop
    opentop = topmos.get()
    win.attributes('-topmost', opentop)  # 置頂
    print(opentop)


def loadFile():
    global file_path, img_files, img_num
    file_path = filedialog.askdirectory(parent=win, initialdir=os.getcwd(), title="請選擇資料夾")
    loadFile_en.delete(0, 'end')
    loadFile_en.insert(0, file_path)
    #img_files = glob.glob(os.path.join(file_path,"*.jpg"))
    #img_files = [file for file in os.listdir(file_path) if  'left' in file or 'right' in file and file.lower().endswith(file_extension)]
    #img_files = sorted(img_files, key=os.path.getctime, reverse=True)
    current_files = glob.glob(os.path.join(file_path,"*.jpg"))
    if not current_files :
        print('資料夾中無照片')
        tk.messagebox.showinfo('提示', '資料夾中無照片')
    else:
        update_image()
    update_folder_periodically()



def update_folder_periodically():
    global img_files,img_num,file_path
    current_files = glob.glob(os.path.join(file_path,"*.jpg"))
    #img_files =glob.glob(os.path.join(file_path, "*left*","*right*"))
    #current_files = [file for file in os.listdir(file_path) if  'left' in file or 'right' in file and file.lower().endswith(file_extension)]
    # 根据文件的最后修改时间进行排序，最新的文件排在前面
    current_files2 = sorted(current_files, key=os.path.getctime, reverse=True)
    if img_files != current_files2:
        img_files = current_files2
        img_num = 0
        update_image()
        print('時間排序:', current_files2) 
        print('編號:',img_num)              
    print('刷新')    
    win.after(refresh_interval,update_folder_periodically)


def update_image():
    print(img_num)
    img_num2 = img_num
    img_num2 += 1
    print(img_num2)
    img = img_cut(img_files[img_num], img_box_w, img_box_h)
    img_box.configure(image=img)
    img_box.image = img
    img3 = img_cut(img_files[img_num2], img_box_w, img_box_h)
    img_box2.configure(image=img3)
    img_box2.image = img3
    photonum.config(text=str(img_num + 1) + '/' + str(len(img_files)))

    

def front_img():
    global img_num
    img_num -= 2
    if img_num < 0:
        img_num = len(img_files) - 1
    update_image()

def next_img():
    global img_num
    img_num += 2
    if img_num == len(img_files):
        img_num = 0
    update_image()

def img_cut(img, max_w, max_h):
    img_orignal = Image.open(img)
    w, h = img_orignal.size
    f1 = 1.0 * max_w / w
    f2 = 1.0 * max_h / h
    factor = min([f1, f2])
    img_w = int(w * factor)
    img_h = int(h * factor)
    img_open = img_orignal.resize((img_w, img_h))
    img_png = ImageTk.PhotoImage(img_open)
    return img_png 

def img_cut2(img, max_w, max_h):
    img_orignal = Image.open(img)
    w, h = img_orignal.size
    f1 = 1.0 * max_w / w
    f2 = 1.0 * max_h / h
    factor = min([f1, f2])
    img_w = int(w * factor)
    img_h = int(h * factor)
    img_open = img_orignal.resize((img_w, img_h))
    img_png = ImageTk.PhotoImage(img_open)
    return img_png

def openupdate():
    global update
    global refresh_interval
    openup = update.get() 
    print(openup)
    if openup != 'True' :    
        refresh_interval = 10000  # 1秒鐘
        #update_folder_periodically() 
    else:
        refresh_interval = 1000
             
#頂層元件
lb = tk.Label(top_frame, text="請選取資料夾", bg="grey", fg="white", height=1)
lb.pack(side=tk.LEFT)
loadFile_en = tk.Entry(top_frame, width=20)
loadFile_en.pack(side=tk.LEFT)
loadFile_btn = tk.Button(top_frame, text="...", height=1, command=loadFile)
loadFile_btn.pack(side=tk.LEFT)

toptcheck = tk.Checkbutton(top_frame, text="置頂", state="normal", variable=topmos, onvalue='True', offvalue='False', command=ontop)
toptcheck.pack(side=tk.LEFT)
toptcheck.deselect()

updatecheck = tk.Checkbutton(top_frame, text="自動刷新", state="normal", variable=update, onvalue='True', offvalue='False', command=openupdate)
updatecheck.pack(side=tk.LEFT)
#updatecheck.deselect()

# 檢視器參數
img_box_x = 0
img_box_y = 0
img_box_w = win_width
img_box_h = win_height - 50
img_box_bg = '#313335'

# 相片檢視介面
#img2 = img_cut(os.path.join(file_path, "H:/DIY/photo/1.jpg"), img_box_w, img_box_h)  # 預設圖片
img3 = img_cut2(os.path.join(file_path, "H:\DIY\python\YC.L.PNG"), img_box_w, img_box_h)  # 預設圖片
img_box2 = tk.Label(win, bg=img_box_bg, width=img_box_w, height=img_box_h, image=img3)
img_box2.pack(side=tk.BOTTOM)
img2 = img_cut(os.path.join(file_path, "H:\DIY\python\YC.L.PNG"), img_box_w, img_box_h)  # 預設圖片
img_box = tk.Label(win, bg=img_box_bg, width=img_box_w, height=img_box_h, image=img2)
img_box.pack(side=tk.BOTTOM)


frontbut = tk.Button(bottom_frame, text='上一張', fg='black', command=front_img)
frontbut.pack(side=tk.LEFT)
nextbut = tk.Button(bottom_frame, text='下一張', fg='black', command=next_img)
nextbut.pack(side=tk.LEFT)
#photonum.config(text=str(img_num + 1) + '/' + str(len(img_files)))
photonum = tk.Label(bottom_frame,text=str(img_num + 1) + '/0')
photonum.pack(side=tk.LEFT)
#leftnum = tk.Label(bottom_frame,text=img_num)
#leftnum .pack(side=tk.BOTTOM)


win.after(0, update_folder_periodically)
win.mainloop()
