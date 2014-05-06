import matplotlib
import matplotlib.pyplot as plot

class Visualize(object):
    ''' Usage example:
        v = Visualize()
        v.plot_estimate_list(estimate_list)
        v.plot_actual_list(actual_list)
        v.show()
    '''
    
    def __init__(self, estimate_color = "red", 
                       estimate_marker = "o", 
                       actual_color = "blue",
                       actual_marker = "o"):
        self.estimate_color = estimate_color
        self.estimate_marker = estimate_marker
        self.actual_color = actual_color
        self.actual_marker = actual_marker
        self.fig = plot.figure()
        plot.ylim(0,96)
        plot.xlim(0,92)
        self.subplot = self.fig.add_subplot(111)
        
    def plot_estimate(self, x, y):
        self.subplot.plot(x, y, color=self.estimate_color, marker=self.estimate_marker)
        
    def plot_target(self, x, y):
        self.subplot.plot(x, y, color=self.actual_color, marker=self.actual_marker)
        
    def plot_list(self, list, color, marker):
        for point in list:
            x = point[0]
            y = point[1]
            self.subplot.plot(x, y, linestyle = '--', linewidth = 1, color=color, marker=marker)
        #self.subplot.plot([x for x,y in list], [y for x,y in list], linestyle = '--', linewidth = 1, color=color, marker=marker)
            
    def plot_estimate_list(self, list):
        self.plot_list(list, self.estimate_color, self.estimate_marker)
        
    def plot_actual_list(self, list):
        self.plot_list(list, self.actual_color, self.actual_marker)

    def show(self):
        plot.show()
