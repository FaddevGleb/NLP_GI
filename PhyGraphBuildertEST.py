import dearpygui.dearpygui as dpg
import dearpygui_extend as dpgex
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

def update():
    dpg.set_item_pos("listOfVariables", (dpg.get_viewport_width() - 200, 30))
    dpg.set_item_pos("FToInputValues",  (680, dpg.get_viewport_height()-75))

class Window:
    def __init__(self):
        self.VariablesMeashurments = {}
        self.ListOfExperimentalValues = []
        self.experimentNumber = 1
        self.flp1 = True

    def graphResult(self):
        # Создаем фигуру с точным размером 400x400 пикселей
        plt.figure(figsize=(4, 4), dpi=100)
        ax = plt.gca()

        # Проверяем наличие данных для построения
        if len(self.ListOfExperimentalValues) == 0:
            # Возвращаем пустой белый холст, если данных нет
            return np.ones((400, 400, 4), dtype=np.float32)

        try:
            # Извлекаем названия переменных
            variables = list(self.VariablesMeashurments.keys())

            # Для случая с двумя переменными (X-Y график)
            if len(variables) >= 2:
                x_vals = [float(exp[variables[0]]) for exp in self.ListOfExperimentalValues]
                y_vals = [float(exp[variables[1]]) for exp in self.ListOfExperimentalValues]

                # Построение графика
                ax.scatter(x_vals, y_vals, color='darkred')
                ax.plot(x_vals, y_vals, '--', alpha=0.5)
                ax.set_xlabel(f"{variables[0]} ({self.VariablesMeashurments[variables[0]]})")
                ax.set_ylabel(f"{variables[1]} ({self.VariablesMeashurments[variables[1]]})")
                ax.set_title("Experimental Results")
                ax.grid(True, linestyle='--', alpha=0.7)

            # Для одной переменной (гистограмма/линейный график)
            elif len(variables) == 1:
                values = [float(exp[variables[0]]) for exp in self.ListOfExperimentalValues]
                ax.plot(values, marker='o', color='darkred')
                ax.set_ylabel(f"{variables[0]} ({self.VariablesMeashurments[variables[0]]})")
                ax.set_title("Experimental Values Progression")
                ax.grid(True, linestyle='--', alpha=0.7)

            # Сохраняем график в буфер
            buf = BytesIO()
            plt.savefig(buf, format='rgba', bbox_inches='tight', pad_inches=0.1)
            buf.seek(0)

            # Преобразуем в numpy array и нормализуем значения
            img_array = np.frombuffer(buf.getvalue(), dtype=np.uint8)
            img_array = img_array.reshape(400, 400, 4) / 255.0
            plt.close()

            return img_array.astype(np.float32)

        except Exception as e:
            print(f"Error generating graph: {e}")
            return np.ones((400, 400, 4), dtype=np.float32)

    def appendVariablesMeashurments(self, var, meash):
        print(var, meash)
        self.VariablesMeashurments[var] = meash
        print(self.VariablesMeashurments)

    def ToggleWindow(self, page):
        dpg.configure_item("V&M", show=(page == 0))
        if page == 1:
            dpg.configure_item("EV", show=True)
        if page == 2:
            dpg.configure_item("GraphResults", show=True)

    def CreateWindows(self):
        def CreateExperimentValuesAndMeasurmentsWindow():

            page = 0

            def SubmitVariableMeashurment():
                self.appendVariablesMeashurments(dpg.get_value(varName), dpg.get_value(meashName))
                #self.VariablesMeashurments[dpg.get_value(varName)] = dpg.get_value(meashName)
                dpg.set_value("success", "Succesfuly added variable & meashurment")
                textOfVarMesh = '\n'.join([var + " " + meash for var, meash in self.VariablesMeashurments.items()])
                dpg.set_value("listOfVariables", "List of variables\n" + textOfVarMesh)

            def Forward():
                if self.flp1:
                    CreateWindowInputingResults()
                    self.flp1 = False
                self.ToggleWindow(page+1)

            with dpg.window(label="Variables names & meashurments", no_collapse=True, no_move=True, height=600, width=800, tag="V&M"):
                with dpg.group(horizontal=True):
                    with dpg.group(horizontal=False):
                        with dpg.group(horizontal=True):
                            dpg.add_text("enter variable name & its meashurments")
                        with dpg.group(horizontal=True):
                            varName = dpg.add_input_text(tag="variable_name", width=80, default_value="")
                            meashName = dpg.add_input_text(tag="variable_meashurments", width=80)
                        dpg.add_button(label="submit", tag="submit", callback=SubmitVariableMeashurment)
                        dpg.add_text(default_value="", label="", tag="success")
                    dpg.add_text(default_value="", label="", tag="listOfVariables")
                    #dpg.set_item_pos("listOfVariables", [300, dpg.get_viewport_width()-100])
                dpg.add_button(label="Continue", tag="FToInputValues", callback=Forward)

        def CreateWindowInputingResults():
            page = 1

            def Forward():
                CreateGraphWindow()
                self.ToggleWindow(page+1)

            def Back():
                self.ToggleWindow(page-1)

            def WriteExperimentalValues():
                listOfInputValuesTags = list(self.VariablesMeashurments.keys())
                experimentValues = {}

                for i in listOfInputValuesTags:
                    experimentValues[i] = dpg.get_value(i)

                self.ListOfExperimentalValues.append(experimentValues)

                for i in listOfInputValuesTags:
                    dpg.set_value(i, "")

                strExperimentValues =""
                for i in range(len(self.ListOfExperimentalValues)):
                    strExperimentValues += f"Experiment :{i+1}\n"
                    for tag, val in self.ListOfExperimentalValues[i].items():
                        strExperimentValues += f"{tag}: {val}\n"
                print(strExperimentValues)
                dpg.set_value("experimentValues", strExperimentValues)

            with dpg.window(label="Experimental values", no_collapse=True, no_move=True, height=600, width=800, tag="EV"):
                listOfInputValuesTags = []
                print(self.VariablesMeashurments)
                self.experimentNumber = 1
                with dpg.group(horizontal=True):
                    with dpg.group(horizontal=False):
                        for var, meash in self.VariablesMeashurments.items():
                            print("a")
                            with dpg.group(horizontal=True):
                                dpg.add_input_text(label=var, default_value="", tag=var, width=100)
                                listOfInputValuesTags.append(var)
                        dpg.add_button(label="submit", tag="submitValues", callback=WriteExperimentalValues)
                    dpg.add_text(default_value="", label="", tag="experimentValues")
                    dpg.set_item_pos("experimentValues",(dpg.get_viewport_width() - 200, 30))
                dpg.add_button(label="Continue", tag="FToGraph", callback=Forward)
                dpg.add_button(label="Back", tag="BToVariablesMeashurments", callback=Back)
                dpg.set_item_pos("FToGraph", (680, dpg.get_viewport_height() - 75))
                dpg.set_item_pos("BToVariablesMeashurments", (10, dpg.get_viewport_height() - 75))

        def CreateGraphWindow():
            with dpg.window(label="Graph results", no_collapse=True, width=800, height=600, no_move=True,
                            tag="GraphResults"):
                with dpg.texture_registry(show=False):
                    dpg.add_static_texture(width=400, height=400, default_value=self.graphResult(), tag="texture_tag")

                dpg.add_image("texture_tag")

        CreateExperimentValuesAndMeasurmentsWindow()



def LoadFonts():
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        default_font = dpg.add_font("C:\Windows\Fonts\Bahnschrift.ttf", 20)
        dpg.bind_font(default_font)


def SetStyle():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (234, 230, 202), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (123, 63, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (234, 230, 202), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (234, 230, 202), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (204, 102, 102), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (204, 102, 102), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (204, 102, 102), category=dpg.mvThemeCat_Core)
            #dpg.add_theme_color(dpg.mvThemeCol_Slider, (204, 102, 102), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category=dpg.mvThemeCat_Core)
            dpg.bind_theme(global_theme)


dpg.create_context()
dpg.create_viewport(title='Custom Title', width=800, height=600, clear_color=(230, 218, 166))
dpg.set_viewport_resize_callback(update)
window = Window()
LoadFonts()
SetStyle()
window.CreateWindows()
window.ToggleWindow(0)
dpg.toggle_viewport_fullscreen()
#dpg.show_style_editor()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()