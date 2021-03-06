#this script is dedicated to the public domain under CC0 (https://creativecommons.org/publicdomain/zero/1.0/)
#do whatever you want with it! -Bram

#   TODO
#-precision mode for rotation
#-draw on screen handles that fit with Blender's transform tools

bl_info = {
    "name": "BRM UVTools",
    "category": "UV",
    "author": "Bram Eulaers",
    "description": "Edit selected faces'UVs directly inside the 3D Viewport. WIP. Check for updates @leukbaars",
    "version": (0, 7)
}

if 'bpy' not in locals():
    import bpy
    from bpy.props import EnumProperty, BoolProperty, FloatProperty
    from . import BRM_UVTranslate, BRM_UVRotate, BRM_UVScale, BRM_UVExtend, BRM_UVStitch, BRM_UVTransfer, BRM_UVMoveToEdge,BRM_Utils
else:
    from importlib import reload
    reload(BRM_UVTranslate)
    reload(BRM_UVRotate)
    reload(BRM_UVScale)
    reload(BRM_UVExtend)
    reload(BRM_UVStitch)
    reload(BRM_UVTransfer)
    reload(BRM_UVMoveToEdge)
    reload(BRM_Utils)


uvmenutype = [("SUBMENU", "Submenu", ""),
              ("INDIVIDUAL", "Individual Entries", "")]


class BRMUVToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    pixel_snap = BoolProperty(
        name="UV Pixel Snap",
        description="Translate Pixel Snapping",
        default=False
    )

    move_snap = FloatProperty(
        name="UV Move Snap",
        description="Translate Scale Subdivision Snap Size",
        default=4
    )
    scale_snap = FloatProperty(
        name="UV Scale Snap",
        description="Scale Snap Size",
        default=2
    )
    rotate_snap = FloatProperty(
        name="UV Rotate Snap",
        description="Rotate Angle Snap Size",
        default=45
    )

    show_panel_tools = BoolProperty(
        name="Show Tools in UV Panel",
        default=True
    )

    adduvmenu = BoolProperty(name="Add BRM UVTools to UV Menu", default=True)
    individualorsubmenu = EnumProperty(name="Individual or Sub-Menu", items=uvmenutype, default="SUBMENU")

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)

        row = column.row()
        row.prop(self, "adduvmenu")
        if self.adduvmenu:
            row.prop(self, "individualorsubmenu", expand=True)

        column.prop(self, "show_panel_tools")
        column.prop(self, "pixel_snap")


class BRM_UVPanel(bpy.types.Panel):
    """UV Tools Panel Test!"""
    bl_label = "BRM UV Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Shading / UVs'
    bl_context = "mesh_edit"

    @classmethod
    def poll(cls, context):
        prefs = bpy.context.user_preferences.addons[__name__].preferences
        return prefs.show_panel_tools

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='FACESEL_HLT')

    def draw(self, context):
        addon_prefs = prefs()
        layout = self.layout

        col = layout.column(align=True)
        col.label(text="Viewport UV tools:")
        row = col.row(align = True)
        row.operator("uv.brm_uvtranslate", text="Move", icon="MAN_TRANS")
        row = row.row(align = True)
        row.prop(addon_prefs, 'move_snap', text="")
        

        row = col.row(align = True)
        row.operator("uv.brm_uvscale", text="Scale", icon="MAN_SCALE")
        row = row.row(align = True)
        row.prop(addon_prefs, 'scale_snap', text="")

        row = col.row(align = True)
        row.operator("uv.brm_uvrotate", text="Rotate", icon="MAN_ROT")
        row = row.row(align = True)
        row.prop(addon_prefs, 'rotate_snap', text="")

        layout.prop(addon_prefs, "pixel_snap", text = 'Move Pixel Snap')
        #col.prop(addon_prefs, "pixel_snap", text = 'Move Pixel Snap', icon = 'FORCE_TEXTURE') 
        
        col = layout.column(align=True)

        col.operator("uv.brm_uvextend", text="Extend", icon="MOD_SHRINKWRAP")
        col.operator("uv.brm_uvstitch", text="Stitch", icon="MOD_TRIANGULATE")
        col.operator("uv.brm_uvtransfer", text="Transfer", icon="MOD_UVPROJECT")

        col.label(text="Move to UV edge:")
        row = col.row(align = True)
        op = row.operator("uv.brm_uvmovetoedge", text=" ", icon="TRIA_UP_BAR")
        op.direction="up"
        op = row.operator("uv.brm_uvmovetoedge", text=" ", icon="TRIA_DOWN_BAR")
        op.direction="down"
        op = row.operator("uv.brm_uvmovetoedge", text=" ", icon="TRIA_LEFT_BAR")
        op.direction = "left"
        op = row.operator("uv.brm_uvmovetoedge", text=" ", icon="TRIA_RIGHT_BAR")
        op.direction = "right"
        

class BRM_UVMenu(bpy.types.Menu):
    bl_label = "BRM UV Tools"
    
    
    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("uv.brm_uvtranslate", text="UVTranslate", icon="MAN_TRANS")
        col.operator("uv.brm_uvrotate", text="UVRotate", icon="MAN_ROT")
        col.operator("uv.brm_uvscale", text="UVScale", icon="MAN_SCALE")
        col.operator("uv.brm_uvextend", text="UVExtend", icon="MOD_SHRINKWRAP")
        col.operator("uv.brm_uvstitch", text="UVStitch", icon="MOD_TRIANGULATE")
        col.operator("uv.brm_uvtransfer", text="Transfer", icon="MOD_UVPROJECT")


def uv_menu_func(self, context):
    if prefs().adduvmenu:
        if prefs().individualorsubmenu == "SUBMENU":
            self.layout.menu("BRM_UVMenu")
        else:
            layout = self.layout

            col = layout.column()
            col.operator_context = 'INVOKE_DEFAULT'
            col.operator("uv.brm_uvtranslate", text="UVTranslate", icon="MAN_TRANS")
            col.operator("uv.brm_uvrotate", text="UVRotate", icon="MAN_ROT")
            col.operator("uv.brm_uvscale", text="UVScale", icon="MAN_SCALE")
            col.operator("uv.brm_uvextend", text="UVExtend", icon="MOD_SHRINKWRAP")
            col.operator("uv.brm_uvstitch", text="UVStitch", icon="MOD_TRIANGULATE")
            col.operator("uv.brm_uvtransfer", text="Transfer", icon="MOD_UVPROJECT")

        self.layout.separator()


def prefs():
    return bpy.context.user_preferences.addons[__name__].preferences


def register():
    bpy.utils.register_class(BRMUVToolsPreferences)
    bpy.utils.register_class(BRM_UVMenu)
    bpy.utils.register_class(BRM_UVPanel)
    bpy.utils.register_class(BRM_UVTranslate.UVTranslate)
    bpy.utils.register_class(BRM_UVRotate.UVRotate)
    bpy.utils.register_class(BRM_UVScale.UVScale)
    bpy.utils.register_class(BRM_UVExtend.UVExtend)
    bpy.utils.register_class(BRM_UVStitch.UVStitch)
    bpy.utils.register_class(BRM_UVTransfer.UVTransfer)
    bpy.utils.register_class(BRM_UVMoveToEdge.UVMoveToEdge)

    if prefs().adduvmenu:
        bpy.types.VIEW3D_MT_uv_map.prepend(uv_menu_func)


def unregister():
    bpy.utils.unregister_class(BRMUVToolsPreferences)
    bpy.utils.unregister_class(BRM_UVMenu)
    bpy.utils.unregister_class(BRM_UVPanel)
    bpy.utils.unregister_class(BRM_UVTranslate.UVTranslate)
    bpy.utils.unregister_class(BRM_UVRotate.UVRotate)
    bpy.utils.unregister_class(BRM_UVScale.UVScale)
    bpy.utils.unregister_class(BRM_UVExtend.UVExtend)
    bpy.utils.unregister_class(BRM_UVStitch.UVStitch)
    bpy.utils.unregister_class(BRM_UVTransfer.UVTransfer)
    bpy.utils.unregister_class(BRM_UVMoveToEdge.UVMoveToEdge)


if __name__ == "__main__":
    register()
