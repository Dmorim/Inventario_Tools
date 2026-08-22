from customtkinter import CTkToplevel


class ContainerManager:
    def __init__(self):
        self.containers = {}

    def _add_container(self, widget: CTkToplevel):
        self.containers[widget] = {"x": widget.winfo_x(), "y": widget.winfo_y(
        ), "width": widget.winfo_width(), "height": widget.winfo_height()}

    def __get_screen_geometry(self, widget: CTkToplevel):
        return {
            "width": widget.winfo_screenwidth(),
            "height": widget.winfo_screenheight(),
        }

    def _remover_container(self, widget: CTkToplevel):
        if widget in self.containers:
            del self.containers[widget]

    def _get_usable_geometry(self, widget: CTkToplevel):
        screen_geometry = self.__get_screen_geometry(widget)
        return {
            "width": screen_geometry["width"] * 0.8,
            "height": screen_geometry["height"] * 0.5,
        }

    def _update_container_geometry(self):
        for container in self.containers:
            self.containers[container] = {
                "x": container.winfo_x(),
                "y": container.winfo_y(),
                "width": container.winfo_width(),
                "height": container.winfo_height(),
            }

    def _put_widget_position_within_screen(self, widget: CTkToplevel):
        widget.update_idletasks()

        usable_geometry = self._get_usable_geometry(widget)
        screen_width = widget.winfo_screenwidth()
        screen_height = widget.winfo_screenheight()
        widget_width = 250
        widget_height = 80

        usable_width = min(screen_width, int(usable_geometry["width"]))
        usable_height = min(screen_height, int(usable_geometry["height"]))
        min_pos_x = 0 + (screen_width - usable_width) // 2
        max_pos_x = screen_width - (screen_width - usable_width) // 2
        min_pos_y = 0 + (screen_height - usable_height) // 2
        max_pos_y = screen_height - (screen_height - usable_height) // 2

        self._update_container_geometry()

        def position_is_available(x, y):
            for container, geometry in self.containers.items():
                if container is widget:
                    continue

                overlaps = (
                    x < geometry["x"] + geometry["width"]
                    and x + widget_width > geometry["x"]
                    and y < geometry["y"] + geometry["height"]
                    and y + widget_height > geometry["y"]
                )
                if overlaps:
                    return False

            return True

        step_x = int(max(1, widget_width)+(widget_width * 0.01))
        step_y = int(max(1, widget_height)+(widget_height * 0.41))

        for x in range(min_pos_x, max_pos_x + 1, step_x):
            for y in range(min_pos_y, max_pos_y + 1, step_y):
                if position_is_available(x, y):
                    return f"+{x}+{y}"

        raise RuntimeError("Não há espaço disponível para posicionar o widget")

    def posicionar_container(self, widget: CTkToplevel) -> str:
        position = self._put_widget_position_within_screen(widget)
        widget.geometry(f'250x80{position}')
        self._add_container(widget)
        return position

    def remover_container(self, widget: CTkToplevel):
        self._remover_container(widget)
