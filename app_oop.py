import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data
import regression

class Win1:
    def __init__(self,master):
        self.master = master
        self.master.geometry("300x300")
        self.frame = tk.Frame(self.master)
        # add code for dropdown below
        self.tkvar = tk.StringVar(self.master)
        self.choices = [k for k in data.confirmed_dict.keys()]
        self.choices.insert(0, "None")
        self.tkvar.set("US")
        self.popup_menu = tk.OptionMenu(self.master, self.tkvar, *self.choices)
        tk.Label(self.master, text="Pick a Country").pack(side=tk.TOP)
        self.popup_menu.pack(side=tk.TOP)
        self.tkvar.trace('w',self.change_dropdown)
        self.button = tk.Button(self.frame, text="Click here to view data", command = lambda: self.new_window("2",Win2))
        self.quitb = tk.Button(self.frame, text="Click here to quit", command = self.close_window).pack(side=tk.BOTTOM)
        self.button.pack(side=tk.RIGHT)
        self.svar = tk.StringVar(self.master)
        tk.Label(self.master,text="Enter a Country").pack(side=tk.TOP)
        self.var = tk.Entry(self.master,textvariable=self.svar).pack(side=tk.TOP)
        self.frame.pack()
    def new_window(self, number, _class):
        self.new = tk.Toplevel(self.master)
        if self.tkvar.get() == "None":
            if self.svar.get().capitalize() in self.choices or self.svar.get().upper() in self.choices:
                _class(self.new, number,self.svar)
            else:
                tk.Label(self.master, text="please enter a valid country", fg='red').pack(side=tk.LEFT)
        else:
            _class(self.new, number, self.tkvar)
    def change_dropdown(self, *args):
        print(self.tkvar.get())
    def close_window(self):
        self.master.destroy()
class Win2:
    def __init__(self, master, number, country):
        self.master = master
        self.master.geometry("600x600")
        self.frame = tk.Frame(self.master)
        if str(country.get()).lower() != 'us':
            c = str(country.get()).capitalize()
        else:
            c = str(country.get()).upper()
        conf = data.confirmed_dict
        dead = data.death_dict
        rec = data.recover_dict
        x = range(len(conf[c]))
        y_conf = conf[c]
        y_dead = dead[c]
        y_rec = rec[c]
        conf_pred = regression.nonlinear_regression(c, "confirmed")
        death_pred = regression.nonlinear_regression(c, "dead")
        rec_pred = regression.nonlinear_regression(c, "recovered")
        y_conf_pred = conf_pred["y_poly_pred"]
        y_conf_r2 = conf_pred["r2"]
        y_dead_pred = death_pred["y_poly_pred"]
        y_dead_r2 = death_pred["r2"]
        y_rec_pred = rec_pred["y_poly_pred"]
        y_rec_r2 = rec_pred["r2"]
        cur_conf = y_conf[-1]
        cur_dead = y_dead[-1]
        cur_rec = y_rec[-1]
        fig, axs = plt.subplots(3,1,constrained_layout=True)
        fig.suptitle("Covid 19 Data: " +c)
        axs[0].plot(x, y_conf, 'o', c='y')
        axs[0].plot(x, y_conf_pred, c="g", label="r^2: {}".format(y_conf_r2))
        axs[0].set_title('confirmed vs. time')
        axs[0].set_xlabel("days since 1/22/2020")
        axs[0].set_ylabel("# of confirmed cases")
        axs[0].legend(loc="upper left")
        axs[1].plot(x, y_dead, 'o',c='r')
        axs[1].plot(x, y_dead_pred, c='g', label="r^2: {}".format(y_dead_r2))
        axs[1].set_title('deaths vs. time')
        axs[1].set_xlabel('days since 1/22/2020')
        axs[1].set_ylabel('# of deaths')
        axs[1].legend(loc="upper left")
        axs[2].plot(x, y_rec, 'o', c='g')
        axs[2].plot(x, y_rec_pred, c='y', label="r^2: {}".format(y_rec_r2))
        axs[2].set_title('recovered vs. time')
        axs[2].set_xlabel('days since 1/22/2020')
        axs[2].set_ylabel('# of recoveries')
        axs[2].legend(loc="upper left")
        self.sc = FigureCanvasTkAgg(fig, self.frame)

        self.retext = tk.Label(self.master, text="Recoveries: {}".format(cur_rec)).pack(side=tk.BOTTOM)
        self.detext = tk.Label(self.master, text="Deaths: {}".format(cur_dead)).pack(side=tk.BOTTOM)
        self.conftext = tk.Label(self.master, text="Confirmed Cases: {}".format(cur_conf)).pack(side=tk.BOTTOM)
        self.quit = tk.Button(self.frame, text= "Quit this window", command = self.close_window).pack(side=tk.BOTTOM)
        self.sc.get_tk_widget().pack(side=tk.LEFT,fill=tk.BOTH)
        self.frame.pack()
    def close_window(self):
        self.master.destroy()

root = tk.Tk()
root.title("Covid 19 Tracker")
root.iconbitmap("img/coronavirus.ico")
app = Win1(root)
root.mainloop()
