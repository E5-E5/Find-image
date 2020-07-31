import tkinter
import PIL
from PIL import ImageGrab, Image, ImageTk
from tensorflow import keras
import tensorflow as tf
import numpy as np


def game():
    def find_image(model, image_file):
        label_names = ["Человек", "Солнце", "Яблоко", "Ёлка", "Карандаш"]

        global an
        img = keras.preprocessing.image.load_img(image_file,
                                                 target_size=(128, 128))
        img_arr = np.expand_dims(img, axis=0) / 255.0
        result = np.array(model.predict_classes(img_arr))
        print("Result: %s", label_names[result[0]])
        an = label_names[result[0]]

    def paint(event):
        x1 = event.x - brush_size
        x2 = event.x + brush_size
        y1 = event.y - brush_size
        y2 = event.y + brush_size
        w.create_oval(x1, y1, x2, y2,
                      fill=color, outline=color)

    def save():
        x = root.winfo_rootx() + w.winfo_x()
        y = root.winfo_rooty() + w.winfo_y()
        x1 = x + 900
        y1 = y + 700
        PIL.ImageGrab.grab().crop((x + 45, y + 47, x1, y1 + 10)).save('sh.png')
        root.destroy()
        nonlocal check
        model = tf.keras.models.load_model('keras_model.h5')
        find_image(model, "sh.png")
        check = 1

    def rest_no():
        nonlocal restart
        restart = 0
        window.destroy()

    def rest_yes():
        nonlocal restart
        restart = 1
        window.destroy()

    def answer():
        nonlocal lbl_res
        lbl_res = tkinter.Label(res, text=("Я думаю вы нарисовали:\n" + an))
        lbl_res.pack()

        btn1 = tkinter.Button(res, text="Ok", width=20, command=res.destroy)
        btn1.pack(side=tkinter.BOTTOM)

    ####################
    main_menu.destroy()
    ########
    window = tkinter.Tk()
    window.resizable(width=False, height=False)

    window.title("Список объектов")
    window.geometry("300x100")
    lbl = tkinter.Label(window, text="Объекты, которые можно рисовать:\n Солнце, Человек, Яблоко, Карандаш, Ёлка")
    btn = tkinter.Button(window, text="Ok", width=20, command=window.destroy)

    x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
    y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
    window.wm_geometry("+%d+%d" % (x - 100, y))
    lbl.pack()
    btn.pack(side=tkinter.BOTTOM)
    window.mainloop()
    ###############
    while True:
        root = tkinter.Tk()
        root.title("Время рисовать")
        root.resizable(width=False, height=False)
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 3.5
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 4
        root.wm_geometry("+%d+%d" % (x - 100, y))
        check = 0
        w = tkinter.Canvas(root,
                           width=canvas_width,
                           height=canvas_height,
                           bg="white",
                           cursor='spraycan')
        w.bind("<B1-Motion>", paint)
        clear_btn = tkinter.Button(text="clear", width=10,
                                   command=lambda: w.delete("all"))
        w.grid(row=2, column=0,
               columnspan=7, padx=5,
               pady=5)
        w.columnconfigure(6, weight=1)
        w.rowconfigure(2, weight=1)
        clear_btn.grid(row=0, column=3, sticky=tkinter.S)
        root.after(10_000, save)
        root.mainloop()
        #############################
        if check:
            res = tkinter.Tk()
            res.resizable(width=False, height=False)

            res.title("Результат")
            res.geometry("300x75")
            lbl_res = tkinter.Label(res, text="Я думаю вы нарисовали:")
            x = (res.winfo_screenwidth() - res.winfo_reqwidth()) / 2
            y = (res.winfo_screenheight() - res.winfo_reqheight()) / 2
            res.wm_geometry("+%d+%d" % (x - 100, y))
            lbl_res.pack()

            res.after(1000, answer)
            lbl_res.after(1000, lbl_res.destroy)

            res.mainloop()
        #############################
        window = tkinter.Tk()
        window.resizable(width=False, height=False)

        window.title("Перезагрузка?")
        window.geometry("300x75")
        lbl = tkinter.Label(window, text="Желаете начать заного?")
        restart = 0
        btn_no = tkinter.Button(window, text="Нет", width=10, command=rest_no)
        btn_yes = tkinter.Button(window, text="Да", width=10, command=rest_yes)
        lbl.pack()
        x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
        y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
        window.wm_geometry("+%d+%d" % (x - 100, y))
        btn_no.pack(side=tkinter.RIGHT)
        btn_yes.pack(side=tkinter.LEFT)
        window.mainloop()

        if restart == 0:
            break
        restart = 0
    global ex
    ex = 0


def info():

    main_menu.destroy()
    inf = tkinter.Tk()
    inf.title("DaFi")
    inf.resizable(width=False, height=False)

    inf.geometry("500x150")
    lbl = tkinter.Label(inf, text="В этой игре вам предстоит рисовать рисунки.\n "
                                  "Но придётся это делать очеь быстро и одновременно чётко\n\n"
                                  "Вам будет дано 10 секунд, чтобы нарисовать ваш рисунок, и после чего ИИ \n"
                                  "скажет что вы нарисовали по его мнению.")
    btn_back = tkinter.Button(inf, text="Назад", width=10, command=inf.destroy)
    x = (inf.winfo_screenwidth() - inf.winfo_reqwidth()) / 2
    y = (inf.winfo_screenheight() - inf.winfo_reqheight()) / 2
    inf.wm_geometry("+%d+%d" % (x - 100, y))
    lbl.pack()
    btn_back.pack(side=tkinter.RIGHT)
    inf.mainloop()

    global ex
    ex = 0


def close():
    main_menu.destroy()
    global ex
    ex = 1


ex = 0
an = ''
restart = 0
canvas_width = 700
canvas_height = 500
brush_size = 3
color = "black"
check = 0
while True:
    main_menu = tkinter.Tk()
    main_menu.title("DaFi")
    main_menu.geometry("300x200")
    main_menu.resizable(width=False, height=False)
    canvas = tkinter.Canvas(main_menu)
    image = ImageTk.PhotoImage(Image.open('main.jpg'))

    canvas.create_image(2, 2, image=image)
    canvas.pack()

    btn_game = tkinter.Button(main_menu, text="Начать игру", width=10, command=game)
    btn_info = tkinter.Button(main_menu, text="Информация", width=10, command=info)
    btn_exit = tkinter.Button(main_menu, text="Выход", width=10, command=close)
    x = (main_menu.winfo_screenwidth() - main_menu.winfo_reqwidth()) / 2
    y = (main_menu.winfo_screenheight() - main_menu.winfo_reqheight()) / 2
    main_menu.wm_geometry("+%d+%d" % (x - 100, y))
    btn_game.place(x=110, y=35, width=85, height=30)
    btn_info.place(x=110, y=80, width=85, height=30)
    btn_exit.place(x=110, y=125, width=85, height=30)
    if ex:
        break
    ex = 1
    main_menu.mainloop()
