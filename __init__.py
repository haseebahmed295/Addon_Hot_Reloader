bl_info = {
    "name": "Addon Hot Reloader",
    "author": "haseebahmed295",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "Topbar > Hot Reloader",
    "description": "Reload a specific addon after a set time interval automatically.",
    "category": "Development",
}

import bpy
import sys
import importlib
from bpy.types import Operator, Panel, AddonPreferences
from bpy.props import FloatProperty, EnumProperty
from functools import partial

class ReloadAddon(Operator):
    """Reload an activated add-on."""
    bl_idname = "script.reload_addon"
    bl_label = "Reload Add-on"


    def execute(self, context):
        # Get the name of the addon package to reload.
        addon_prefs = context.preferences.addons[__package__].preferences
        package = addon_prefs.package_name
        
        if not package:
            self.report({'ERROR'}, "Reload Add-on: No addon selected.")
            return {'FINISHED'}

        # Get the addon's module.
        module = sys.modules.get(package)
        if not module:
            self.report({'ERROR'}, f"Reload Add-on: '{package}' not found or not activated.")
            return {'FINISHED'}
        
        # Call unregister() on the previously loaded addon.
        # Ensure that the new version of the addon is always reloaded by continuing.
        try:
            print(f"Un-registering: {package}")
            module.unregister()
        except Exception:
            import traceback
            print("----------------------------------------------------------------------")
            traceback.print_exc()
            self.report({'ERROR'}, "Reload Add-on: 'unregister()' threw an exception! " +
                "Restart may be required.")
            print("----------------------------------------------------------------------")
            
        # Reload and register the addon.
        print(f"Reloading: {package}")
        importlib.reload(module)

        print(f"Registering: {package}")
        try:
            module.register()
            self.report({'INFO'}, f"Reloaded Add-on: {package}")
        except Exception:
            import traceback
            print("----------------------------------------------------------------------")
            traceback.print_exc()
            self.report({'ERROR'}, "Reload Add-on: 'register()' threw an exception! " +
                "Restart may be required.")
            print("----------------------------------------------------------------------")

        return {'FINISHED'}

class StartTimerOperator(Operator):
    """Start the timer to reload the addon after the set interval."""
    bl_idname = "script.start_timer"
    bl_label = "Start Timer"

    _is_running = False
    _func = None
    def execute(self, context):
        if StartTimerOperator._is_running:
            bpy.app.timers.unregister(StartTimerOperator._func)
            StartTimerOperator._is_running = False
            self.report({'INFO'}, "Timer stopped.")
            return {'FINISHED'}

        addon_prefs = context.preferences.addons[__package__].preferences
        if not addon_prefs.package_name:
            self.report({'ERROR'}, "Please select an addon to reload.")
            return {'CANCELLED'}
        if addon_prefs.time_interval <= 0:
            self.report({'ERROR'}, "Time interval must be greater than 0.")
            return {'CANCELLED'}
        time = addon_prefs.time_interval
        StartTimerOperator._is_running = True
        # Register the timer
        StartTimerOperator._func = partial(self.reload_after_interval, time)
        bpy.app.timers.register(StartTimerOperator._func, first_interval=time)
        self.report({'INFO'}, f"Timer started for {time} seconds to reload {addon_prefs.package_name}.")
        return {'FINISHED'}
    
    @staticmethod
    def reload_after_interval(time):
        """Callback for the timer to reload the addon."""
        bpy.ops.script.reload_addon()
        return time

class HotReloaderMenu(Panel):
    bl_label = "Hot Reloader"
    bl_idname = "SCRIPT_PT_hot_reloader"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Hot Reloader"
    

    def draw(self, context):
        layout = self.layout
        addon_prefs = context.preferences.addons[__package__].preferences
        row = layout.row()
        col = row.column(align=True)
        col.scale_y = 1.5
        col.label(text="Select Add-on to Reload:")  
        col.label(text="Set Time Interval (seconds):")
        col.label(text="Start Timer:")
        col = row.column(align=True)
        col.scale_y = 1.5
        col.prop(addon_prefs, "package_name" , text="")
        col.prop(addon_prefs, "time_interval" , text="")
        if StartTimerOperator._is_running:
            col.operator("script.start_timer", text="Stop Timer", icon='PAUSE' , depress = True)
            return
        col.operator("script.start_timer" , icon='TIME')

def get_addon_enum_items(self, context):
    """Get list of enabled addons for enum."""
    items = []
    for addon_name in context.preferences.addons.keys():
        items.append((addon_name, addon_name, ""))
    return items

class HotReloaderPreferences(AddonPreferences):
    bl_idname = __package__

    package_name: EnumProperty(
        name="Addon to Reload",
        description="Select the addon to reload",
        items=get_addon_enum_items
    )

    time_interval: FloatProperty(
        name="Time Interval (seconds)",
        description="Time in seconds after which to reload the addon",
        default=5.0,
        min=0.1
    )
    
def draw_hot_reloader_button(self, context):
    if StartTimerOperator._is_running:
        self.layout.operator(StartTimerOperator.bl_idname, text="", icon='PAUSE' , depress = True)
    else:
        self.layout.operator(StartTimerOperator.bl_idname, text="", icon='TIME')

def register():
    bpy.utils.register_class(ReloadAddon)
    bpy.utils.register_class(StartTimerOperator)
    bpy.utils.register_class(HotReloaderMenu)
    bpy.utils.register_class(HotReloaderPreferences)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_hot_reloader_button)

def unregister():
    bpy.utils.unregister_class(ReloadAddon)
    bpy.utils.unregister_class(StartTimerOperator)
    bpy.utils.unregister_class(HotReloaderMenu)
    bpy.utils.unregister_class(HotReloaderPreferences)
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_hot_reloader_button)


if __name__ == "__main__":
    register()