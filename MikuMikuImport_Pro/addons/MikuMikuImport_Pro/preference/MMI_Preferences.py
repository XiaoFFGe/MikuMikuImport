import os

import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import AddonPreferences
from MikuMikuImport_Pro.common.i18n.i18n import i18n

from ..config import __addon_name__


class MMIPreferences(AddonPreferences):
    # this must match the add-on name (the folder name of the unzipped file)
    bl_idname = __addon_name__

    # https://docs.blender.org/api/current/bpy.props.html
    # The name can't be dynamically translated during blender programming running as they are defined
    # when the class is registered, i.e. we need to restart blender for the property name to be correctly translated.
    positioning_bone: StringProperty(
        name="The default face positioning bone",
        default="頭",
        subtype='FILE_NAME',
        description='插件会自动选择这个骨骼',
    )
    number: IntProperty(
        name="Int Config",
        default=2,
    )
    boolean: BoolProperty(
        name="",
        default=True,
        description="设置原生辉光",
    )
    Developer_Options: BoolProperty(
        name="",
        default=False,
        description="开发人员选项",
    )

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.prop(self,'positioning_bone',text=i18n('The default face positioning bone'))
        layout.prop(self,'Developer_Options',text=i18n('Developer Options'))