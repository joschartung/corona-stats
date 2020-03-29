from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data

conf = data.confirmed_dict
dead = data.death_dict
rec = data.recover_dict

x = range(len(conf["US"]))
y_conf = conf["US"]
y_dead = dead["US"]
y_rec = rec["US"]


root = Tk()
root.title("Covid 19 Data")
fig, axs = plt.subplots(3,1,constrained_layout=True)
fig.suptitle("Covid 19 data: " + 'US')
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
sc = FigureCanvasTkAgg(fig, root)
sc.get_tk_widget().pack(side=LEFT,fill=BOTH)
root.mainloop()
root.exit()
