import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import dataset
import regression
import scrape


# TODO: rewrite this to take advantage of grid system
class Win1:
    def __init__(self,master):
        self.master = master
        self.master.geometry("300x300")
        self.frame = tk.Frame(self.master)
        # add code for dropdown below
        self.data = dataset.Data()
        self.tkvar = tk.StringVar(self.master)
        self.choices = [k for k in self.data.confirmed_dict.keys()]
        self.choices.insert(0, "None")
        self.tkvar.set("US")
        self.popup_menu = tk.OptionMenu(self.master, self.tkvar, *self.choices)
        tk.Label(self.master, text="Pick a Country").pack(side=tk.TOP)
        self.popup_menu.pack(side=tk.TOP)
        self.tkvar.trace('w',self.change_dropdown)
        self.button = tk.Button(self.frame, text="Click here to view data", command = lambda: self.new_window("2",Win2))
        self.quitb = tk.Button(self.frame, text="Click here to quit", command = self.close_window).pack(side=tk.BOTTOM)
        self.scrapebt = tk.Button(self.frame, text="Click here to update data", command = scrape.main).pack(side=tk.BOTTOM)
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
            _class(self.new, number, self.tkvar, self.data)
    def change_dropdown(self, *args):
        print(self.tkvar.get())
    def close_window(self):
        self.master.destroy()
class Win2:
    def __init__(self, master, number, country, data):
        self.master = master
        self.master.attributes('-fullscreen', True)
        self.frame = tk.Frame(self.master)
        self.data = data
        c = str(country.get())
        conf = self.data.confirmed_dict
        dead = self.data.death_dict
        rec = self.data.recover_dict
        x = range(len(conf[c]))
        y_conf = conf[c]
        y_dead = dead[c]
        y_rec = rec[c]
        cur_conf = y_conf[-1]
        cur_dead = y_dead[-1]
        cur_rec = y_rec[-1]
        dead_conf_per = 0
        rec_conf_per = 0
        if cur_dead > 0 and cur_conf > 0 and cur_rec > 0:
            dead_conf_per = (cur_dead / cur_conf) * 100
            rec_conf_per = (cur_rec / cur_conf) * 100
        fig, axs = plt.subplots(1,3,constrained_layout=True, figsize=(20,20))
        conf_pred = 0
        rec_pred = 0
        dead_pred = 0
        try:
            # everything here deals with regression
            conf_reg = regression.Exp(self.data, c, 0)
            dead_reg = regression.Exp(self.data, c, 1)
            rec_reg = regression.Exp(self.data, c, 2)
            conf_reg.exp_reg()
            dead_reg.exp_reg()
            rec_reg.exp_reg()
        except:
            print("could not analyze this data")
        try:
            # everything here plots the regression models
            axs[0].plot(x, conf_reg.y_pred, c='k',label="r^2: {:.2f}".format(conf_reg.r2))
            axs[1].plot(x, dead_reg.y_pred,c='k',label="r^2: {:.2f}".format(dead_reg.r2))
            axs[2].plot(x, rec_reg.y_pred, c='k',label="r^2: {:.2f}".format(rec_reg.r2))
        except:
            print("could not plot data")
        try:
            # everything here predicts tomorrows numbers
            conf_pred = conf_reg.predict(len(x))
            dead_pred = dead_reg.predict(len(x))
            rec_pred = rec_reg.predict(len(x))
        except:
            print("could not predict")

        fig.suptitle("Covid 19 Data: " +c)
        y_data = [y_conf, y_dead, y_rec]
        titles = ['confirmed vs. time', 'deaths vs. time', 'recovered vs. time']
        x_label = "days since 1/22/2020"
        y_labels = ["# of confirmed cases", "# of deaths", "# of recoveries"]
        scat_colors = ['y', 'r', 'g']
        for i in range(len(axs)):
            axs[i].scatter(x, y_data[i], s=30, c=scat_colors[i], edgecolors='k')
            axs[i].set_title(titles[i])
            axs[i].set_xlabel(x_label)
            axs[i].set_ylabel(y_labels[i])
            axs[i].legend(loc="upper left")
        self.sc = FigureCanvasTkAgg(fig, self.frame)
        self.retext = tk.Label(self.master, text="Recoveries: {}({:.2f}%) Prediction: {:.2f}".format(cur_rec, rec_conf_per, rec_pred)).pack(side=tk.BOTTOM)
        self.detext = tk.Label(self.master, text="Deaths: {}({:.2f}%) Prediction: {:.2f}".format(cur_dead, dead_conf_per, dead_pred)).pack(side=tk.BOTTOM)
        self.conftext = tk.Label(self.master, text="Confirmed Cases: {} Prediction: {:.2f}".format(cur_conf, conf_pred)).pack(side=tk.BOTTOM)

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
