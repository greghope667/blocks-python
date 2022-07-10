#!/usr/bin/env python3
import dearpygui.dearpygui as dpg
import editor

def setup():
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

def show():
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def window():
    with dpg.window(label="Title Goes Here"):
        dpg.add_text("Test text")
        dpg.add_button(label="Button", callback=lambda: print("Button"))
        dpg.add_button(label="New", callback=window)
        dpg.add_button(label="Block", callback=lambda: editor.draw_block(editor.basic_block_1i1o()))
        dpg.add_input_text(label="input")

def imnode():
    with dpg.window(label="Tutorial", width=400, height=400, no_close=True, minimap=True, minimap_location=dpg.mvNodeMiniMap_Location_BottomRight):
        editor.draw_scene(editor.Scene())

import dearpygui.demo as demo
def main():

    setup()
    window()
    demo.show_demo()
    imnode()
    show()

main()