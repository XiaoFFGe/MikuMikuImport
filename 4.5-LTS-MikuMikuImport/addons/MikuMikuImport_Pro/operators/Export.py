import bpy


class SaveAsBlendOperator(bpy.types.Operator):
    """Export presets"""
    bl_idname = "scene.save_as_blend"
    bl_label = "Export presets"

    # 打开文件选择器
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_blender: bpy.props.BoolProperty(default=True, options={'HIDDEN'})
    filter_folder: bpy.props.BoolProperty(default=True,options={'HIDDEN'})

    def invoke(self, context, event):
        if not self.filepath or not self.filepath.lower().endswith('.blend'):
            blend_filepath = context.blend_data.filepath
            if blend_filepath:
                self.filepath = bpy.path.ensure_ext(blend_filepath, ".blend")
            else:
                self.filepath = "Untitled.blend"
        wm = context.window_manager
        wm.fileselect_add(self)

        return {'RUNNING_MODAL'}

    def execute(self, context):
        bpy.ops.wm.save_as_mainfile(filepath=self.filepath, check_existing=True, filter_blender=True)
        return {'FINISHED'}