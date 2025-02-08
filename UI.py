import dearpygui.dearpygui as dpg
import dearpygui_extend as dpgex

class Window():
    def __init__(self):
        self.window = 0
        self.selectedFile = ""
        self.selectedMode = ""
        self.latinOnly = False
        self.model = 0
        self.resultType = 0
    def FakePicture(self): #TEST ONLY! REMOVE AFTER!
        texture_data = []
        for i in range(0, 100 * 100):
            texture_data.append(255 / 255)
            texture_data.append(0)
            texture_data.append(255 / 255)
            texture_data.append(255 / 255)
        return texture_data

    def ToggleWindow(self, page=0):
        match page:
            case 0:
                dpg.set_primary_window("Greeting", True)
            case 1:
                dpg.set_primary_window("FileChoice", True)
            case 2:
                dpg.set_primary_window("ModeChoice", True)
            case 3:
                dpg.set_primary_window("PreparationChoice", True)
            case 4:
                dpg.set_primary_window("FiltModResChoice", True)
            case 5:
                dpg.set_primary_window("TopResults", True)
            case 6:
                dpg.set_primary_window("FileResults", True)
            case 9:
                dpg.set_primary_window("GraphResults", True)
            case 8:
                dpg.set_primary_window("VectorDialogue", True)
            case 7:
                 dpg.set_primary_window("AllResults", True)
        dpg.configure_item("Greeting", show=(page == 0))
        dpg.configure_item("FileChoice", show=(page == 1))
        dpg.configure_item("ModeChoice", show=(page == 2))
        dpg.configure_item("PreparationChoice", show=(page == 3))
        dpg.configure_item("FiltModResChoice", show=(page == 4))
        dpg.configure_item("TopResults", show=(page == 5))
        dpg.configure_item("FileResults", show=(page == 6))
        dpg.configure_item("GraphResults", show=(page == 9))
        dpg.configure_item("VectorDialogue", show=(page == 8))
        dpg.configure_item("AllResults", show=(page == 7))



    def CreateWindows(self):
        def CreateTopResultWindow():

            def GraphTopResult(sender, appData):
                self.ToggleWindow(9)

            def ToFiltModResChoice():
                self.ToggleWindow(4)

            with dpg.window(label="Top 25 results", no_collapse=True, width=800, height=600, no_move=True, tag="TopResults"):
                with dpg.group(horizontal=False):
                    dpg.add_text("HERE SHOULD BE RESULTS")
                    dpg.add_button(label="See the answer as a graph.", callback=GraphTopResult)

                dpg.add_button(label="Back", width=100, callback=ToFiltModResChoice, tag="BFiltModResChoiceTopResultsWindow")

        def CreateFileResultWindow():
            def GraphTopResult(sender, appData):
                self.ToggleWindow(9)

            def ToFiltModResChoice():
                self.ToggleWindow(4)

            with dpg.window(label="Top 25 results", no_collapse=True, width=800, height=600, no_move=True,
                            tag="FileResults"):
                with dpg.group(horizontal=False):
                    dpg.add_text("Enter the filename for a result file")
                    dpg.add_input_text(label="filename")
                    dpg.add_button(label="See the answer as a graph.", callback=GraphTopResult)

                dpg.add_button(label="Back", width=100, callback=ToFiltModResChoice, tag="BFiltModResChoiceFileResultsWindow")

        def CreateGraphResultWindow():
            with dpg.window(label="Graph results", no_collapse=True, width=800, height=600, no_move=True,
                            tag="GraphResults"):

                with dpg.texture_registry(show=False):
                    dpg.add_static_texture(width=100, height=100, default_value=self.FakePicture(), tag="texture_tag")

                dpg.add_image("texture_tag")

        def CreateVectorResultDialogueWindow():

            def ToFiltModResChoice():
                self.ToggleWindow(4)

            def GraphTopResult(sender, appData):
                self.ToggleWindow(9)

            with dpg.window(label="Vector dialogue", no_collapse=True, width=800, height=600, no_move=True,
                            tag="VectorDialogue"):
                with dpg.group(horizontal=False):
                    dpg.add_text("Enter the word in raw text format")
                    dpg.add_input_text(label="word")
                    dpg.add_button(label="See the answer as a graph.", callback=GraphTopResult)

                dpg.add_button(label="Back", width=100, callback=ToFiltModResChoice, tag="BFiltModResChoiceVectorResultWindow")


        def CreatePrintAllResultWindow():

            def ToFiltModResChoice():
                self.ToggleWindow(4)

            def GraphTopResult(sender, appData):
                self.ToggleWindow(9)

            with dpg.window(label="Top 25 results", no_collapse=True, width=800, height=600, no_move=True,
                            tag="AllResults"):
                with dpg.group(horizontal=False):
                    dpg.add_text("HERE SHOULD BE RESULTS")
                    dpg.add_button(label="See the answer as a graph.", callback=GraphTopResult)

                dpg.add_button(label="Back", width=100, callback=ToFiltModResChoice, tag="BFiltModResChoiceARW")


        def CreateModelFilteringResultChoiceWindow():
            with dpg.window(label="Filtering, Model & Result type Choice", no_collapse=True, width=800, height=600, no_move=True,
                            tag="FiltModResChoice"):

                def ToPreparationChoice():
                    self.ToggleWindow(3)

                def ToResultChoice():
                    self.ToggleWindow(self.resultType + 5)

                def CallbackModelChoiceEn(sender, appData):
                    print(sender, appData)
                    self.model = 0

                def CallbackModelChoiceRu(sender, appData):
                    self.model = 1

                def CallbackResultChoiceTop25(sender, appData):
                    self.resultType = 0

                def CallbackResultChoiceFile(sender, appData):
                    self.resultType = 1

                def CallbackResultChoiceAll(sender, appData):
                    self.resultType = 2

                def CallbackResultChoiceVector(sender, appData):
                    self.resultType = 3

                with dpg.group(horizontal=True):
                    with dpg.group(horizontal=False):
                        dpg.add_text("Select model")
                        dpg.add_button(label="en_core_web_lg", callback=CallbackModelChoiceEn)
                        dpg.add_button(label="ru_core_news_lg", callback=CallbackModelChoiceRu)

                    with dpg.group(horizontal=False):
                        dpg.add_text("Select result format")
                        dpg.add_button(label="top 25", callback=CallbackResultChoiceTop25)
                        dpg.add_button(label="store in a file", callback=CallbackResultChoiceFile)
                        dpg.add_button(label="print all", callback=CallbackResultChoiceAll)
                        dpg.add_button(label="vector", callback=CallbackResultChoiceVector)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Back", width=100, callback=ToPreparationChoice, tag="BtoPreparationChoice")
                    dpg.add_button(label="Result", width=100, callback=ToResultChoice, tag="FtoResult")

        def CreatePreparationChoiceWindow():
            with dpg.window(label="Text Preparation Choice", no_collapse=True, width=800, height=600, no_move=True, tag="PreparationChoice"):
                dpg.add_text(
                    "Select one of the options below regarding text processing...\n\
ru: Leave only Cyrillic characters\n\
en: Leave only Latin characters\n\
skip: Do nothing and skip processing the text")

                def ToModeChoice():
                    self.ToggleWindow(2)

                def ToFiltModResChoice():
                    self.ToggleWindow(4)

                def CallbackModeChoice(sender, appData):
                    print(appData, sender)
                    self.selectedMode = sender - 296

                def CallbackLatinOnly(sender, appData):
                    print(sender, appData)
                    self.latinOnly = appData

                with dpg.group(horizontal=True):
                    with dpg.group(horizontal=False):
                        dpg.add_button(label="ru", width=150, callback=CallbackModeChoice)
                        dpg.add_button(label="en", width=150, callback=CallbackModeChoice)
                        dpg.add_button(label="skip", width=150, callback=CallbackModeChoice)
                    dpg.add_checkbox(label="Leave only basic latin?(en only)", default_value=False, callback=CallbackLatinOnly)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Back", width=100, callback=ToModeChoice, tag="BtoModeChoice")
                    dpg.add_button(label="Next", width=100, callback=ToFiltModResChoice, tag="FtoFiltModResChoice")

        def CreateModeChoiceWindow():
            with dpg.window(label="Mode Choice", no_collapse=True, width=800, height=600, no_move=True, tag="ModeChoice"):
                dpg.add_text(
                    "Please choose one of the following options...\n words: Calculate the frequency of individual words\
                    \n combos: Process word combinations of selected length \n vectors: Use words vectors of a trained model to find similar words")

                def ToFileChoice():
                    self.ToggleWindow(1)

                def ToPreparationChoice():
                    self.ToggleWindow(3)

                def CallbackModeChoice(sender, appData):
                    print(appData, sender)
                    self.selectedMode = sender - 296

                with dpg.group(horizontal=False):
                    dpg.add_button(label="words", width=150, callback=CallbackModeChoice)
                    dpg.add_button(label="combos", width=150, callback=CallbackModeChoice)
                    dpg.add_button(label="vectors", width=150, callback=CallbackModeChoice)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Back", width=100, callback=ToFileChoice, tag="BtoFileChoice")
                    dpg.add_button(label="Next", width=100, callback=ToPreparationChoice, tag="FtoPreparationChoice")


        def CreateFileChoiceWindow():
            with dpg.window(label="File Choice", no_collapse=True, width=800, height=600, no_move=True, tag="FileChoice"):
                dpg.add_text(
                    "Select a text file encoded with UTF-8. If later on you encounter an error specific to\nyour input file try to edit the file first.", parent="FileChoice", tag="fileChoiceText")

                def _callback_file_selected(sender, app_data):
                    print("Selected file:", app_data[0])
                    selectedFile = app_data[0]

                def ToGreeting():
                    self.ToggleWindow(0)

                def ToModeChoice():
                    self.ToggleWindow(2)

                dpgex.add_file_browser(
                    tag="file_browser_id",
                    callback=_callback_file_selected,
                    default_path=".",
                    height=400,
                    parent="FileChoice"
                )
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Back", width=100, callback=ToGreeting, tag="BtoGreeting")
                    dpg.add_button(label="Next", width=100, callback=ToModeChoice, tag="FtoModeChoice")
                self.window += 1


        def CreateGreetingWindow():
            with dpg.window(label="Greeting", no_collapse=True, width=800, height=600, no_move=True, tag="Greeting"):
                dpg.add_text("  Welcome to QuickNLPFreqTool: Basic Python NLP and Analysis Script v. 0.8.1.\n\
                    You can get an overview and version history on the Github page.\n\
                    The script will guide you through its process with different options mainly \n\
                    centered around Russian or English language models to use. Be aware that \n\
                    sometimes the script has to be run several times with different settings \n\
                    for you to get the desired output.Also note that while the script has been \n\
                    tested on Russian and English texts and various exceptions have been added\n\
                    it's not guaranteed to work every time.\n", tag="greetingText")

                def ToFileChoice():
                    self.ToggleWindow(1)


                dpg.add_button(label="Next", width=100, callback=ToFileChoice, tag="FtoFileChoise")
                self.window = 0

        CreateGreetingWindow()
        CreateFileChoiceWindow()
        CreateModeChoiceWindow()
        CreatePreparationChoiceWindow()
        CreateModelFilteringResultChoiceWindow()
        CreateFileResultWindow()
        CreateVectorResultDialogueWindow()
        CreateGraphResultWindow()
        CreateTopResultWindow()
        CreatePrintAllResultWindow()
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


def RunUI():
    dpg.create_context()
    window = Window()
    LoadFonts()
    SetStyle()
    window.CreateWindows()
    window.ToggleWindow()
    dpg.create_viewport(title='Custom Title', width=800, height=600, clear_color=(230, 218, 166))
    dpg.toggle_viewport_fullscreen()
    #dpg.show_style_editor()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

RunUI()