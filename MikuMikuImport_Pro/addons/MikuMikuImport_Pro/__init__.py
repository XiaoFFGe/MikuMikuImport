import bpy
from bpy.app.handlers import persistent

from .config import __addon_name__
from .i18n.dictionary import dictionary
from .propertygroup.MMI_PropertyGroup import MMI_property, MMIImageItem, MMIStrokeitem
from ...common.class_loader import auto_load
from ...common.class_loader.auto_load import add_properties, remove_properties
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary

# Add-on info
bl_info = {
    "name": "MikuMikuImport Pro",
    "author": "小峰峰哥l",
    "blender": (3, 6, 0),
    "version": (4, 5, 2),
    "description": "导入MMD模型渲染预设",
    "tracker_url": "https://space.bilibili.com/2109816568?spm_id_from=333.1007.0.0",
    "support": "COMMUNITY",
    "category": "Import-Export"
}

_addon_properties = {}

# 全局变量存储历史选择状态
_last_selected_objs = set()

@persistent
def update_stroke(scene):
    global _last_selected_objs
    # 获取当前选中对象的名称集合
    current_selected = {obj.name for obj in bpy.context.selected_objects}
    # 检查选择状态是否变化
    if current_selected != _last_selected_objs:
        _last_selected_objs = current_selected
        if bpy.context.object and bpy.context.object.type == 'MESH':
            bpy.ops.mmi.update_stroke_list()

def register():
    print("正在注册")  # 打印正在注册的提示信息
    # 注册类
    auto_load.init()
    auto_load.register()
    add_properties(_addon_properties)
    bpy.utils.register_class(MMI_property)
    bpy.types.Object.mmi = bpy.props.PointerProperty(type=MMI_property)
    bpy.utils.register_class(MMIImageItem)
    bpy.types.Scene.mmi_images = bpy.props.CollectionProperty(type=MMIImageItem)
    bpy.utils.register_class(MMIStrokeitem)
    bpy.types.Object.mmi_stroke = bpy.props.CollectionProperty(type=MMIStrokeitem)
    # 注册更新列表的回调函数
    bpy.app.handlers.depsgraph_update_post.append(update_stroke)

    # 国际化（多语言支持相关操作）
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)

    print("{}插件已安装。".format(bl_info["name"]))


def unregister():

    # 国际化（多语言支持相关操作）
    bpy.app.translations.unregister(__addon_name__)

    # 注销类
    auto_load.unregister()
    remove_properties(_addon_properties)
    del bpy.types.Object.mmi
    bpy.utils.unregister_class(MMI_property)
    del bpy.types.Scene.mmi_images
    bpy.utils.unregister_class(MMIImageItem)
    del bpy.types.Object.mmi_stroke
    bpy.utils.unregister_class(MMIStrokeitem)
    # 注销更新列表的回调函数
    bpy.app.handlers.depsgraph_update_post.remove(update_stroke)

    print("{}插件已卸载。".format(bl_info["name"]))