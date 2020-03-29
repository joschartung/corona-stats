import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data

class Win1:
    def __init__(self,master):
        self.master = master
        self.master.geometry("500x500")
        self.frame = tk.Frame(self.master)
        # add code for dropdown below
        self.tkvar = tk.StringVar(self.master)
        self.choices = data.confirmed_dict.keys()
        self.tkvar.set("US")
        self.popup_menu = tk.OptionMenu(self.master, self.tkvar, *self.choices)
        tk.Label(self.master, text="Pick a Country").pack(side=tk.LEFT)
        self.popup_menu.pack(side=tk.LEFT)
        self.tkvar.trace('w',self.change_dropdown)
        self.button = tk.Button(self.frame, text="Click here to view data", command = lambda: self.new_window("2",Win2))
        self.button.pack(side=tk.RIGHT)
        self.frame.pack()
    def new_window(self, number, _class):
        self.new = tk.Toplevel(self.master)
        _class(self.new, number, self.tkvar)
    def change_dropdown(self, *args):
        print(self.tkvar.get())
class Win2:
    def __init__(self, master, number, country):
        self.master = master
        self.master.geometry("500x500")
        self.frame = tk.Frame(self.master)
        c = str(country.get())
        self.quit = tk.Button(self.frame, text= "Quit this window", command = self.close_window)
        self.quit.pack(side=tk.LEFT)

        conf = data.confirmed_dict
        dead = data.death_dict
        rec = data.recover_dict

        x = range(len(conf[c]))
        y_conf = conf[c]
        y_dead = dead[c]
        y_rec = rec[c]

        fig, axs = plt.subplots(3,1,constrained_layout=True)
        fig.suptitle("Covid 19 data: " +c)
        axs[0].plot(x, y_conf, 'o', c='y')
        axs[0].set_title('confirmed vs. time')
        axs[0].set_xlabel("days since 1/22/2020")
        axs[0].set_ylabel("# of confirmed cases")
        axs[1].plot(x, y_dead, 'o',c='r')
        axs[1].set_title('deaths vs. time')
        axs[1].set_xlabel('days since 1/22/2020')
        axs[1].set_ylabel('# of deaths')
        axs[2].plot(x, y_rec, 'o', c='g')
        axs[2].set_title('recovered vs. time')
        axs[2].set_xlabel('days since 1/22/2020')
        axs[2].set_ylabel('# of recoveries')
        self.sc = FigureCanvasTkAgg(fig, self.frame)
        self.sc.get_tk_widget().pack(side=tk.LEFT,fill=tk.BOTH)
        self.frame.pack()
    def close_window(self):
        self.master.destroy()

root = tk.Tk()
root.title("Covid 19 Tracker")
app = Win1(root)
root.mainloop()
