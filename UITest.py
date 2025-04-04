import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO


def create_plot():
    # Создаем фигуру Matplotlib
    fig, ax = plt.subplots()
    x = np.linspace(0, 2 * np.pi, 100)
    ax.plot(x, np.sin(x), label='sin(x)')
    ax.plot(x, np.cos(x), label='cos(x)')
    ax.legend()

    # Сохраняем в буфер памяти
    buf = BytesIO()
    fig.savefig(buf, format='rgba', dpi=80, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    # Преобразуем в формат DearPyGui
    buf.seek(0)
    data = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    width, height = fig.canvas.get_width_height()

    return data, width, height


def update_plot():
    # Обновление текстуры
    data, width, height = create_plot()
    dpg.set_value("plot_texture", [width, height, data])


dpg.create_context()
data, width, height = create_plot()

with dpg.texture_registry():
    dpg.add_static_texture(
        width=width,
        height=height,
        default_value=data,
        tag="plot_texture"
    )

with dpg.window(label="Matplotlib Example"):
    dpg.add_image("plot_texture")
    dpg.add_button(label="Обновить график", callback=update_plot)

dpg.create_viewport(title='Matplotlib Integration', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()