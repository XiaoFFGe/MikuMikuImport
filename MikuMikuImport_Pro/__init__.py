from .addons.MikuMikuImport_Pro import register as addon_register, unregister as addon_unregister

bl_info = {
    "name": 'MikuMikuImport Pro',
    "author": '小峰峰哥l',
    "blender": (3, 6, 0),
    "version": (4, 5, 0),
    "description": '导入MMD模型渲染预设',
    "tracker_url": 'https://space.bilibili.com/2109816568?spm_id_from=333.1007.0.0',
    "support": 'COMMUNITY',
    "category": 'Import-Export'
}

def register():
    addon_register()

def unregister():
    addon_unregister()

    