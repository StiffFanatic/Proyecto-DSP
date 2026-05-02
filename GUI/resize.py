from PIL import ImageTk

class Resizer:
    def __init__(self, widget, image):
        self.widget = widget
        self.image = image
        self.widget.bind("<Configure>", self._resize)

    def _resize(self, event):
        if event.width < 10 or event.height < 10:
            return

        resized = self.image.resize((event.width, event.height))
        photo = ImageTk.PhotoImage(resized)
        self.widget.config(image=photo)
        self.widget.image = photo