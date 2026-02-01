import bpy
from bpy.props import *

# 定义图像类型枚举
IMAGE_TYPES = [
    ('FACE', "face", "脸部"),
    ('HAIR', "hair", "头发"),
    ('BODY', "body", "身体"),
    ('MANUAL', 'Manual', '手动'),
    ('SKIP', "skip", "跳过匹配"),
]

class MMIImageItem(bpy.types.PropertyGroup):
    image: bpy.props.PointerProperty(
        type=bpy.types.Image,
        name="Image",
        description="选择一个图像"
    )

    # 添加集合元素的属性定义
    image_type: bpy.props.EnumProperty(
        name="",
        items=IMAGE_TYPES,
        default='FACE'
    )


class MMI_property(bpy.types.PropertyGroup):
    extras_enabled: BoolProperty(
        name="Extras Enabled",
        default=False
    )
    Post_processing_effect: BoolProperty(
        name="Post-processing effect",
        default=True
    )
    filepath: StringProperty(
        name="",
        subtype='DIR_PATH',
        description="选择一个文件夹"
    )

    Face_Shadow_Ramp: EnumProperty(
        name="Face Shadow_Ramp",
        items=[('Body','Body/身体',''),('Hair','Hair/发','')],
        default='Body',
        description="脸部Shadow_Ramp"
    )

    ext_enabled: BoolProperty(
        name="Extras Enabled",
        default=False
    )
    Copy_object_data: BoolProperty(
        name="",
        default=False,
        description="这将删除模型的所有关键帧"
    )
    re_obj: BoolProperty(
        name="",
        default=False
    )
    Track_the_camera: PointerProperty(
        type=bpy.types.Object,
        name="Track the camera",
        description="Track the camera",
    )
    Face_positioning: PointerProperty(
        type=bpy.types.Object,
        name="Face positioning",
        description="Face positioning",
    )
    rve_gty: BoolProperty(
        name="",
        default=False
    )
    rfd_ghu: BoolProperty(
        name="",
        default=False
    )
    minimum_value_meters:FloatProperty(
        name="Minimum distance",
        unit='LENGTH',
        default=0,
    )
    minimum_Thickness:FloatProperty(
        name="Minimum Thickness",
        unit='LENGTH',
        default=0.08,
    )
    utmost_value_meters:FloatProperty(
        name="utmost distance",
        unit='LENGTH',
        default=20,
    )
    utmost_Thickness:FloatProperty(
        name="utmost Thickness",
        unit='LENGTH',
        default=0.5,
    )
    image_index: bpy.props.IntProperty(
        default=-1
    )
    Stroke_index: bpy.props.IntProperty(
        default=-1
    )
    Display_All_name:BoolProperty(
        name="Display All name",
        default=False
    )
    SRsampling:BoolProperty(
        name="SR sampling",
        default=False
    )
    srMODE:EnumProperty(
        name="SR sampling",
        items=[
            ('颜','颜',''),
            ('髮','髮',''),
            ('衣服','衣服',''),
        ],
        default='颜'
    )

    # 预设模板
    preset_Template: bpy.props.StringProperty(
        name="Preset Template",
        default="",
        description="选择一个预设模板，空白默认使用默认预设",
        subtype='FILE_PATH',
    )


class MMIStrokeitem(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(
        type=bpy.types.Material,
        name="Material",
    )