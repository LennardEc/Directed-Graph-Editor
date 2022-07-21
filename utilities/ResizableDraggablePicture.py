from kivy.graphics.transformation import Matrix
from kivy.uix.scatter import Scatter


class ResizableDraggablePicture(Scatter):
    def on_touch_down(self, touch):
        # Override Scatter's `on_touch_down` behavior for mouse scroll
        if touch.is_mouse_scrolling:
            factor = None
            if touch.button == 'scrolldown':
                if self.scale < self.scale_max:
                    factor = 1.1
            elif touch.button == 'scrollup':
                if self.scale > self.scale_min:
                    factor = 1 / 1.1
            if factor is not None:
                self.apply_transform(Matrix().scale(factor, factor, factor), anchor=touch.pos)
        # If some other kind of "touch": Fall back on Scatter's behavior
        else:
            super(ResizableDraggablePicture, self).on_touch_down(touch)