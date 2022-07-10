from __future__ import annotations
from blocks import *
import dearpygui.dearpygui as dpg
import log

log.Log.flags.add("LINK")
linklog = log.Log("LINK")

# callback runs when user attempts to connect attributes
def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    linklog(sender, app_data)
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)

# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    # app_data -> link_id
    linklog(sender, app_data)
    dpg.delete_item(app_data)

def draw_input_node(k:str, i:InPort): 
    with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input):
        dpg.add_text(k)

def draw_output_mode(k:str, o:OutPort):
    with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
        dpg.add_text(k)

def draw_block(b: Node) -> None:
    with dpg.node(parent="Editor Window", label="Node 1"):
        for k,v in b.inputs.items():
            with dpg.node_attribute():
                dpg.add_input_float(label=k, width=150)

        for k,v in b.outputs.items():
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_input_float(label=k, width=150)
        
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_input_text(multiline=True, width=150)

def draw_scene(scene:Scene) -> None:
    with dpg.node_editor(tag="Editor Window", callback=link_callback, delink_callback=delink_callback, minimap=True, minimap_location=dpg.mvNodeMiniMap_Location_BottomRight):
        for b in scene.blocks:
            draw_block(b)