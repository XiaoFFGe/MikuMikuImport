import bpy

from MikuMikuImport_Pro.addons.MikuMikuImport_Pro.operators.make_presets import MakePresetsOperator, \
    MakePresets9Operator, MakePrytyOperator, MakePrehts9Operator, MakePrehkhts9Operator, InvertthenormalsOperator, \
    MakePrehOperator, MakePdtysOperator, MakePdtyOperator, Adaptivestrokes, FixAMDgraphicscardsynthesizerbug, \
    EdgePreviewOperator, RevokeEdgePreviewOperator, MMD2MMIEdgePreviewOperator, MakePresets7Operator, \
    MatchingmaterialsMMDmodelOperator
from MikuMikuImport_Pro.addons.MikuMikuImport_Pro.operators.Export import SaveAsBlendOperator
from MikuMikuImport_Pro.addons.MikuMikuImport_Pro.operators.make_presets import MakePresets1Operator, MakePresets2Operator, \
    MakePresets3Operator, MakePresets4Operator, MakePresets6Operator, MakePres4Operator
from MikuMikuImport_Pro.addons.MikuMikuImport_Pro.operators.render_presets import Render2Operator
from MikuMikuImport_Pro.addons.MikuMikuImport_Pro.panels import compare_version
from MikuMikuImport_Pro.common.i18n.i18n import i18n
from MikuMikuImport_Pro.addons.MikuMikuImport_Pro.config import __addon_name__

class presetsAddonPanel(bpy.types.Panel):
    bl_label = "Import MMD presets"
    bl_idname = "SCENE_PT_Default"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "MMI"

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        addon_prefs = context.preferences.addons[__addon_name__].preferences

        row = layout.row()
        row.scale_y = 2
        row.operator(Render2Operator.bl_idname, text="Import a render preset", icon='SHADING_RENDERED')

        obj = context.object
        if obj:
            mmi = obj.mmi
            layout.prop(mmi, "extras_enabled", text=i18n("Extras"), toggle=True, icon="PREFERENCES")
            if mmi.extras_enabled:
                layout.prop(mmi, "Post_processing_effect", text=i18n("Post-processing effect"))
                layout.prop(mmi, "Copy_object_data", text=i18n("Copy object data"))
                # 获取Blender的版本号
                version = bpy.app.version_string
                # 验证blender版本
                if compare_version(version, '4.1.99'):
                    layout.prop(addon_prefs, "boolean",text=i18n("Set the native Bloom"))

# 描边面板, UIList
class MMI_UL_StrokeList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        mmi = context.object.mmi

        # 去掉名称前面的“mmi-edge|”
        row.label(text=item.material.name if mmi.Display_All_name else item.material.name.replace("mmi-edge|", ""), icon='NODE_MATERIAL')

        node_tree = item.material.node_tree
        # 检查是否有材质
        if item.material:
            # 名称是否为“mmi-edge|”的前缀
            if item.material.name.startswith("mmi-edge|"):
                # 遍历节点
                for node in node_tree.nodes:
                    if node.type == "GROUP":
                        # 遍历输入
                        for input in node.inputs:
                            row.prop(input, "default_value", text="")

# 更新列表
class MMI_OT_UpdateStrokeList(bpy.types.Operator):
    bl_idname = "mmi.update_stroke_list"
    bl_label = "Update Stroke List"
    def execute(self, context):
        obj = bpy.context.object
        mmi_stroke = obj.mmi_stroke
        # 清除现有的列表
        mmi_stroke.clear()
        # 获取当前物体所有的材质
        materials = obj.material_slots
        # 遍历所有的材质
        for material in materials:
            # 是否是mmi-edge|开头的材质
            if material.material.name.startswith("mmi-edge|"):
                # 创建一个新的列表项
                new_item = mmi_stroke.add()
                # 设置材质
                new_item.material = material.material
        return {'FINISHED'}

class makeAddonPanel(bpy.types.Panel):
    bl_label = "make presets"
    bl_idname = "SCENE_PT_make_presets"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "MMI"
    # 指定父面板的 ID
    bl_parent_id = "SCENE_PT_Default"
    # 折叠面板
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        obj = context.object
        if obj:
            layout.label(text=i18n("Model presets"))
            layout.operator(MakePresets1Operator.bl_idname, icon='GREASEPENCIL')
            layout.label(text=i18n("Render presets"))
            mmi = obj.mmi
            if mmi.re_obj:
                # 仅当物体是空物体且名称为 'AAAAA' 时显示旋转控件
                if obj.type == 'EMPTY' and obj.name == "AAAAA":
                    layout.label(text=i18n("Please manually correct the rotation of the controller"))
                    col = layout.box()
                    col.prop(obj, "rotation_euler", index=0, text="X")  # X轴
                    col.prop(obj, "rotation_euler", index=1, text="Y")  # Y轴
                    col.prop(obj, "rotation_euler", index=2, text="Z")  # Z轴
                    # 显示子级约束的属性
                    layout.separator()
                    layout.label(text=i18n("positioning bone"))
                    for constraint in obj.constraints:
                        if constraint.type == 'CHILD_OF':
                            # 显示约束名称和目标物体属性
                            box = layout.box()
                            box.label(text= constraint.name, icon='CON_CHILDOF')
                            box.prop(constraint, "target", text="Target")
                            box.prop(constraint, "subtarget", text="Bone")

                    split = layout.split(factor=0.3)
                    split.operator(MakePdtysOperator.bl_idname)
            else:
                layout.operator(MakePrehOperator.bl_idname, icon='GREASEPENCIL')
                layout.prop(mmi, "ext_enabled", text=i18n("Extras"), toggle=True)
                if mmi.ext_enabled:
                    layout.operator(MakePresetsOperator.bl_idname, icon='OUTLINER_COLLECTION')
                    layout.operator(MakePresets2Operator.bl_idname)
                    layout.operator(MakePresets3Operator.bl_idname)
                    layout.operator(MakePresets4Operator.bl_idname)
                    layout.operator(MakePresets6Operator.bl_idname)
                    layout.operator(MakePdtyOperator.bl_idname)

            layout.label(text=i18n("material" if mmi.SRsampling else "Stroke"))

            obj = context.object

            row = layout.row()
            if not mmi.SRsampling:
                row.template_list("MMI_UL_StrokeList","",obj,"mmi_stroke",mmi,"Stroke_index",rows=5)

            else:
                hide_input_names = ['X', 'Z', '法线', '值(明度)']
                row = layout.row()
                row.prop(mmi, 'srMODE', expand=True)
                bl_break = False
                nodegroup_name = mmi.srMODE
                mat_slots = obj.material_slots
                for slot in mat_slots:
                    material = slot.material
                    # 节点树
                    node_tree = material.node_tree
                    # 打破循环
                    if bl_break:
                        continue
                    # 遍历节点
                    for node in node_tree.nodes:
                        if node.name == nodegroup_name:
                            box = layout.box()
                            # 遍历节点
                            for node1 in node.node_tree.nodes:
                                if node1.name == "Shadow_Ramp采样":
                                    # 遍历输入
                                    for input in node1.inputs:
                                        # 检查输入是否在隐藏列表中
                                        if input.name in hide_input_names:
                                            continue
                                        box.prop(input, "default_value", text=input.name)
                            bl_break = True
                            break

            row = layout.row(align=True)
            row.prop(mmi, "Display_All_name", text=i18n("Display All name"), toggle=True, icon='MENU_PANEL')
            row.prop(mmi, "SRsampling", text=i18n("SR sampling"), toggle=True, icon='EYEDROPPER')
            row = layout.row(align=True)
            row.operator(MMI_OT_UpdateStrokeList.bl_idname, icon='FILE_REFRESH')
            row.operator(InvertthenormalsOperator.bl_idname, icon='MOD_MESHDEFORM')

            row = layout.row(align=True)
            row.operator(EdgePreviewOperator.bl_idname, icon='ANTIALIASED')
            row.operator(RevokeEdgePreviewOperator.bl_idname, icon='TRASH')
            layout.operator(MMD2MMIEdgePreviewOperator.bl_idname, icon='FULLSCREEN_EXIT')

            layout.label(text=i18n("Export"))
            layout.operator(SaveAsBlendOperator.bl_idname, icon="FILEBROWSER")

class OtherfeaturesPanel(bpy.types.Panel):
    bl_label = "Other features"
    bl_idname = "SCENE_PT_make_presets_other_features"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "MMI"
    # 指定父面板的 ID
    bl_parent_id = "SCENE_PT_Default"
    # 折叠面板
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        addon_prefs = context.preferences.addons[__addon_name__].preferences

        layout.operator(MakePres4Operator.bl_idname)
        layout.operator(MakePresets7Operator.bl_idname)
        if addon_prefs.Developer_Options:
            layout.operator(FixAMDgraphicscardsynthesizerbug.bl_idname)
        if context.object:
            mmi = context.object.mmi
            layout.prop(mmi,"rve_gty",text=i18n("Adaptive strokes"),toggle=True)
            if mmi.rve_gty:
                layout.label(text=i18n("Face positioning"))
                split1 = layout.split(factor=0.65)
                split1.prop(mmi, "Face_positioning", text="")
                layout.label(text=i18n("Track the camera"))
                split1 = layout.split(factor=0.65)
                split1.prop(mmi,"Track_the_camera",text="")
                layout.prop(mmi,"rfd_ghu", text=i18n("Multi-camera mode"))

                flow = layout.column_flow(columns=2,align=True)
                flow.prop(mmi, "minimum_value_meters", text=i18n("Minimum distance"))

                flow.prop(mmi, "utmost_value_meters", text=i18n("utmost distance"))

                flow.prop(mmi, "minimum_Thickness", text=i18n("Minimum Thickness"))

                flow.prop(mmi, "utmost_Thickness", text=i18n("utmost Thickness"))

                layout.operator(Adaptivestrokes.bl_idname)

class MMIGenshinPanel(bpy.types.Panel):
    bl_label = "MMI Genshin"
    bl_idname = "SCENE_PT_mmi_genshin"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "MMI"

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        if context.object is not None and context.object.type == "MESH":
            if context.object.type == "MESH":
                mmi = context.object.mmi
                layout.prop(mmi, "filepath", text=i18n("Maps folder"))
                layout.operator(MakePrytyOperator.bl_idname)
                layout.prop(mmi,'Face_Shadow_Ramp',text=i18n('Face Shadow_Ramp'))
                flow = layout.column_flow(columns=3)
                flow.operator(MakePrehkhts9Operator.bl_idname)
                flow.operator(MakePresets9Operator.bl_idname)
                flow.operator(MakePrehts9Operator.bl_idname)
                layout.operator(InvertthenormalsOperator.bl_idname)

class MMI_UL_ImageList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        row = layout.row(align=True)

        # 图像选择器
        row.prop(item, "image", text="")

        row.label(text="", icon='LINKED')

        # 类型下拉菜单
        row.prop(item, "image_type", text="")

# 添加图像
class MMI_OT_AddImage(bpy.types.Operator):
    bl_idname = "mmi.add_image"
    bl_label = "Add Image"
    def execute(self, context):
        scene = context.scene
        new_item = scene.mmi_images.add()
        new_item.name = f"Image {len(scene.mmi_images)}"
        return {'FINISHED'}
# 删除图像
class MMI_OT_RemoveImage(bpy.types.Operator):
    bl_idname = "mmi.remove_image"
    bl_label = "Remove Image"
    def execute(self, context):
        mmi = context.object.mmi
        scene = context.scene
        scene.mmi_images.remove(mmi.image_index)
        return {'FINISHED'}

class AutomaticMatchingPanel(bpy.types.Panel):
    bl_label = "Automatic Matching"
    bl_idname = "SCENE_PT_Automatic_Matching"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "MMI"
    # 指定父面板的 ID
    bl_parent_id = "SCENE_PT_Default"
    # 折叠面板
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        mmi = context.object.mmi
        scene = context.scene
        # 图像列表
        row = layout.row()
        row.template_list(
            "MMI_UL_ImageList",
            "image_list",
            scene,
            "mmi_images",
            mmi,
            "image_index",
            rows=5,
        )
        # 添加按钮
        col = row.column(align=True)
        col.operator(MMI_OT_AddImage.bl_idname, icon='ADD', text="")
        # 删除按钮
        col.operator(MMI_OT_RemoveImage.bl_idname, icon='REMOVE', text="")

        layout.prop(mmi, 'Face_Shadow_Ramp', text=i18n('Face Shadow_Ramp'))
        layout.operator(MatchingmaterialsMMDmodelOperator.bl_idname)
