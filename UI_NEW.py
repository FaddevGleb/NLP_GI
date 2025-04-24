# -*- coding: utf-8 -*-


import dearpygui.dearpygui as dpg
import dearpygui_extend as dpgex

def LoadFonts():
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        default_font = dpg.add_font("M_PLUS_Rounded_1c/MPLUSRounded1c-Regular.ttf", 20)
        dpg.bind_font(default_font)


def SetStyle():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240, 240, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (0, 51, 102), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
            #dpg.add_theme_color(dpg.mvThemeCol_Text, (240, 240, 240), category=dpg.mvThemeCat_Core)  # Red text
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (234, 230, 202), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (234, 230, 202), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 51, 102), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (204, 102, 102), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (204, 102, 102), category=dpg.mvThemeCat_Core)
            #dpg.add_theme_color(dpg.mvThemeCol_Slider, (204, 102, 102), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category=dpg.mvThemeCat_Core)
            dpg.bind_theme(global_theme)
def CreateWindow():
    with dpg.window(label="dv", no_collapse=True, no_move=True, tag="Greeting", no_title_bar=True):
        with dpg.group(horizontal=True):
            dpg.add_button(label="File", tag="File")
            dpg.add_button(label="Text", tag="Main")
            dpg.add_text("Words")
            dpg.add_text("Typos")
    dpg.set_primary_window("Greeting", True)


def RunUI():
    dpg.create_context()
    LoadFonts()
    SetStyle()
    CreateWindow()
    dpg.create_viewport(title='BindWordXP', width=1080, height=920, clear_color=(230, 218, 166))
    dpg.toggle_viewport_fullscreen()

    dpg.toggle_viewport_fullscreen()
    #dpg.show_style_editor()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

RunUI()
