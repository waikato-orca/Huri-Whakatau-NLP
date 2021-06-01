import tkinter as tk

# ColorScale class that creates a slider scale with a color gradient
class ColorScale(tk.Canvas):
    def __init__(self, parent, val=0, height=13, width=80, variable=None, from_=0, to=1, command=None,
                 gradient='hue', **kwargs):
        tk.Canvas.__init__(self, parent, width=width, height=height, **kwargs)
        self.parent = parent
        self.max = to
        self.min = from_
        self.range = self.max - self.min
        self._variable = variable
        self.command = command
        self.color_grad = gradient
        self._variable = tk.IntVar(self)
        val = max(min(self.max, val), self.min)
        self._variable.set(val)
        
        self._variable.trace("w", self._update_val)

        self.gradient = tk.PhotoImage(master=self, width=width, height=height)
        
        self.bind('<Configure>', lambda e: self._draw_gradient(val))

    #Draws the gradient for the slider
    def _draw_gradient(self, val):
        self.delete("gradient")
        self.delete("cursor")
        del self.gradient
        width = self.winfo_width()
        height = self.winfo_height()

        self.gradient = tk.PhotoImage(master=self, width=width, height=height)

        line = []
        def f(i):
            factor = 255 / width
            r = 255 - (factor * i)
            b = factor * i
            tuple = (int(r), 0, int(b))
            line.append("#%02x%02x%02x" % tuple)

        for i in range(width):
            f(i)
        line = "{" + " ".join(line) + "}"
        self.gradient.put(" ".join([line for j in range(height)]))
        self.create_image(0, 0, anchor="nw", tags="gradient", image=self.gradient)
        self.lower("gradient")

        x = (val - self.min) / float(self.range) * width
        if x < 4:
            x = 4
        if x > width - 4:
            x = width - 4
        self.create_line(x, 0, x, height, width=4, fill='white', tags="cursor")
        self.create_line(x, 0, x, height, width=2, tags="cursor")

    #Updates the position of the slider pointer
    def _update_val(self, *args):
        val = int(self._variable.get())
        val = min(max(val, self.min), self.max)
        self.set(val)
        self.event_generate("<<HueChanged>>")

    #Gets the postition of the slider pointer
    def get(self):
        coords = self.coords('cursor')
        width = self.winfo_width()
        return round(self.range * coords[0] / width, 2)

    #Sets the position of the slider pointer
    def set(self, val):
        width = self.winfo_width()
        x = (val - self.min) / float(self.range) * width
        for s in self.find_withtag("cursor"):
            self.coords(s, x, 0, x, self.winfo_height())
        self._variable.set(val)