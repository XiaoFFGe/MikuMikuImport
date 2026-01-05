import os
import re
import bpy
from difflib import SequenceMatcher
from MikuMikuImport_Pro.addons.MikuMikuImport_Pro.config import __addon_name__
from MikuMikuImport_Pro.addons.MikuMikuImport_Pro.operators.Local_search_engines import search_files
from MikuMikuImport_Pro.addons.MikuMikuImport_Pro.panels import compare_version


class MakePresetsOperator(bpy.types.Operator):
    '''Name the collection as [MMD Preset]'''
    bl_idname = "object.make_presets_ops"
    bl_label = "Name the collection you're in【MMD预设】"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None

    def execute(self, context):

        # 获取所有选中的物体
        selected_objects = bpy.context.selected_objects

        # 遍历选中的物体
        for obj in selected_objects:
            # 获取物体所属的所有集合
            collections = obj.users_collection

            # 遍历所有集合并打印和重命名
            if collections:
                for collection in collections:
                    print(f"物体 {obj.name} 所属集合的名称: {collection.name}")
                    self.report({'INFO'}, f"物体 {obj.name} 所属集合的名称: {collection.name}")

                    # 尝试重命名集合
                    if collection.name != "【MMD预设】":
                        try:
                            collection.name = "【MMD预设】"
                            print(f"集合已重命名为: {collection.name}")
                            self.report({'INFO'}, f"集合已重命名为: {collection.name}")
                        except Exception:
                            print(f"物体{obj.name}没有属于任何集合。")
                            self.report({'WARNING'}, f"物体 {obj.name} 没有属于任何集合。")

        return {'FINISHED'}


class MakePresets1Operator(bpy.types.Operator):
    '''Handle related objects with one click'''
    bl_idname = "object.makes_presets_ops"
    bl_label = "Handle related objects with one click"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None

    def execute(self, context):

        # 遍历所有选中的物体
        for obj in bpy.context.selected_objects:
            # 检查物体是否为Empty类型
            if obj.type == 'EMPTY':
                print(f"{obj.name} 是一个MMD根物体。")
                # 检查物体名称是否为【MMD预设】
                if obj.name != '【MMD预设】':
                    print('不等于')
                else:
                    self.report({'INFO'}, f"{obj.name}已经被命名了")
                    return {'FINISHED'}
            else:
                print(f"{obj.name} 不是MMD根物体。")
                self.report({'WARNING'}, f"{obj.name}不是MMD根物体")
                return {'FINISHED'}

        # 获取所有灯光类型的物体
        lights = [obj for obj in bpy.data.objects if obj.type == 'LIGHT']

        # 获取所有选中物体的名称（并清理标点符号）
        selected_objects_names = [re.sub(r'[^\w\s]', '', obj.name) for obj in bpy.context.selected_objects]

        # 重命名灯光物体
        for i, light in enumerate(lights):
            if i < len(selected_objects_names):
                light.name = '__|【' + selected_objects_names[i] + "】|__"
                # 获取所有选中的物体
                selected_objects = bpy.context.selected_objects

                # 检查是否至少有一个物体被选中
                if selected_objects:
                    # 遍历所有选中的物体
                    for obj in selected_objects:
                        # 为每个物体生成新名称
                        obj.name = "【MMD预设】"
                        print(f"物体已重命名为：{obj.name}")
                else:
                    print("没有物体被选中！")
                    return {'FINISHED'}

                self.report({'INFO'}, f"已完成命名")
        return {'FINISHED'}


class MakePresets2Operator(bpy.types.Operator):
    '''Name the model'''
    bl_idname = "object.makess_presets_ops"
    bl_label = "Name the model"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        if context.active_object is not None:
            if context.active_object.type == 'MESH':
                return True
        return False

    def execute(self, context):

        # 获取当前活动的物体
        active_object = bpy.context.active_object
        if active_object.name == 'AAAA':
            print('已经被命名了')
            self.report({'INFO'}, f"{active_object.name}已经被命名了")
        else:
            # 更改物体名称
            if active_object is not None:
                active_object.name = 'AAAA'
                print(f"物体已重命名为 'AAAA'")
                self.report({'INFO'}, f"已重命名为 'AAAA'")

            else:
                print("没有活动的物体可以重命名。")

        return {'FINISHED'}


class MakePresets3Operator(bpy.types.Operator):
    '''Name the bones'''
    bl_idname = "object.maess_presets_ops"
    bl_label = "Name the bones"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        if context.active_object is not None:
            if context.active_object.type == 'ARMATURE':
                return True
        return False

    def execute(self, context):

        # 获取当前活动的物体
        active_object = bpy.context.active_object
        if active_object.name == 'AAA':
            print('已经被命名了')
            self.report({'INFO'}, f"{active_object.name}已经被命名了")
        else:
            # 更改物体名称
            if active_object is not None:
                active_object.name = 'AAA'
                print(f"物体已重命名为 'AAA'")
            else:
                print("没有活动的物体可以重命名。")
        return {'FINISHED'}


class MakePresets4Operator(bpy.types.Operator):
    '''Name the SDF controller'''
    bl_idname = "object.maegss_presets_ops"
    bl_label = "Name the SDF controller"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        if context.active_object is not None:
            if context.active_object.type == 'EMPTY':
                return True
        return False

    def execute(self, context):

        # 获取当前活动的物体
        active_object = bpy.context.active_object
        if active_object.name == 'AAAAA':
            print('已经被命名了')
            self.report({'INFO'}, f"{active_object.name}已经被命名了")
        else:
            # 更改物体名称
            if active_object is not None:
                active_object.name = 'AAAAA'
                print(f"物体已重命名为 'AAAAA'")
            else:
                print("没有活动的物体可以重命名。")
        return {'FINISHED'}


class MakePresets6Operator(bpy.types.Operator):
    '''Name the MMD root object'''
    bl_idname = "object.mvaegs_ops"
    bl_label = "Name the MMD root object"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        if context.active_object is not None:
            if context.active_object.type == 'EMPTY':
                return True
        return False

    def execute(self, context):

        # 获取活动物体名称
        active_object_name = context.active_object.name
        print('物体名称：', active_object_name)

        if active_object_name != "AA":

            # 获取所有灯光类型的物体
            lights = [obj for obj in bpy.data.objects if obj.type == 'LIGHT']

            # 获取所有选中物体的名称（并清理标点符号）
            selected_objects_names = [re.sub(r'[^\w\s]', '', obj.name) for obj in bpy.context.selected_objects]

            # 重命名灯光物体
            for i, light in enumerate(lights):
                if i < len(selected_objects_names):
                    light.name = '__|【' + selected_objects_names[i] + "】|__"

            # 重命名物体
            bpy.data.objects.get(active_object_name)
            context.active_object.name = "AA"
        else:
            print('已经被命名了')
            self.report({'INFO'}, f"已经被命名了")

        return {'FINISHED'}


class MakePresets7Operator(bpy.types.Operator):
    """Separate models by map"""
    bl_idname = "object.makefdy_presets_ops"
    bl_label = "Separate models by map"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        if context.active_object is not None:
            if context.active_object.type == 'MESH':
                return True
        return False

    def execute(self, context):

        # 调用操作
        bpy.ops.mmd_tools.convert_materials()
        bpy.ops.mmd_tools.separate_by_materials()

        # 创建一个字典来存储贴图名和对应的物体列表
        image_to_objects = {}

        # 获取当前选中的所有对象
        selected_objects = bpy.context.selected_objects

        # 遍历每个选中的对象
        for obj in selected_objects:
            # 获取对象的材质槽
            material_slots = obj.material_slots

            # 遍历每个材质槽
            for slot in material_slots:
                if slot.material:
                    material = slot.material
                    # 获取材质的节点树
                    node_tree = material.node_tree

                    # 遍历节点树中的所有节点
                    for node in node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            # 获取图像纹理节点的图像
                            image = node.image
                            # 如果这个贴图已经在字典中，就将当前物体加入到对应的列表中
                            if image.name in image_to_objects:
                                image_to_objects[image.name].append(obj)
                            else:
                                # 否则，创建一个新的列表，并将当前物体加入
                                image_to_objects[image.name] = [obj]

        # 现在，image_to_objects字典包含了每张贴图对应的物体列表
        # 接下来，对每组使用相同贴图的物体进行合并

        for image_name, objects in image_to_objects.items():
            if len(objects) > 1:  # 只有当有多于一个物体时才需要合并
                # 选择第一个物体作为基础，其他物体将被合并到它上面
                base_obj = objects[0]
                # 构建要合并的物体列表
                merge_objects = objects[1:]

                # 合并物体
                bpy.ops.object.select_all(action='DESELECT')  # 先取消选择所有物体
                for obj in merge_objects:
                    obj.select_set(True)  # 选择要合并的物体
                base_obj.select_set(True)  # 最后选择基础物体
                bpy.context.view_layer.objects.active = base_obj  # 设置活动物体为base_obj

                # 执行合并操作
                bpy.ops.object.join()

        print("合并完成！")

        return {'FINISHED'}


class MakePresets9Operator(bpy.types.Operator):
    '''genshin presets'''
    bl_idname = "object.genshin_presets_ops"
    bl_label = "Hair/发"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        mmi = context.object.mmi

        def search_engine(i):
            keywords = str(i).split()
            file_paths = search_files(keywords, mmi.filepath)
            for path in file_paths:
                print(path)
                return path

        # 贴图路径
        NormalMap = search_engine('Hair Normal')
        Diffuse = search_engine('Hair Diffuse')
        Lightmap = search_engine('Hair Light map')
        Shadow_Ramp = search_engine('Hair Shadow_Ramp')

        # 获取当前活动对象的活动材质
        mat = bpy.context.object.active_material
        if mat and mat.node_tree:
            # 获取节点树中的所有节点
            nodes = mat.node_tree.nodes
            # 逐个删除节点
            for node in nodes:
                mat.node_tree.nodes.remove(node)

        def Connect_the_nodes(node1, 端口1, node2, 端口2):
            # 查找名为1和2的节点
            node_1 = None
            node_2 = None
            for node in mat.node_tree.nodes:
                if node.name == node1:
                    node_1 = node
                elif node.name == node2:
                    node_2 = node

            # 如果找到两个节点，则连接它们的端口
            if node_1 and node_2:
                output_socket = node_1.outputs.get(端口1)
                input_socket = node_2.inputs.get(端口2)
                if output_socket and input_socket:
                    mat.node_tree.links.new(output_socket, input_socket)

        # 创建材质输出节点
        output_node = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
        # 设置节点位置
        output_node.location = (200, 0)

        # 创建节点组
        Group_node = mat.node_tree.nodes.new('ShaderNodeGroup')
        Group_node.location = (0, 0)
        my_group = bpy.data.node_groups["髮"]
        Group_node.node_tree = my_group
        Group_node.name = "髮"

        # 连续节点
        Connect_the_nodes(Group_node.name, '颜色', output_node.name, 'Surface')

        # 访问节点组内的节点
        Group_node_list = Group_node.node_tree.nodes
        # ————————————————————————————————————————————————————————————————————————————————————————
        if Diffuse is not None:
            # 遍历节点列表来找到名称为Diffuse的节点：
            Diffuse_node = None
            for node in Group_node_list:
                if node.name == "Diffuse":
                    Diffuse_node = node
                    break
            # 修改节点
            if Diffuse_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(Diffuse)
                # 替换贴图
                Diffuse_node.image = new_image
                # 修改Alpha通道为通道打包
                Diffuse_node.image.alpha_mode = 'CHANNEL_PACKED'
        # ————————————————————————————————————————————————————————————————————————————
        if Lightmap is not None:
            # 遍历节点列表来找到名称为Lightmap的节点：
            Lightmap_node = None
            for node in Group_node_list:
                if node.name == "Lightmap":
                    Lightmap_node = node
                    break
            # 修改节点
            if Lightmap_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(Lightmap)
                # 替换贴图
                Lightmap_node.image = new_image
                # 修改Alpha通道为通道打包
                Lightmap_node.image.alpha_mode = 'CHANNEL_PACKED'
                # 将色彩空间设置为'Non - Color'
                Lightmap_node.image.colorspace_settings.name = 'Non-Color'
        # ————————————————————————————————————————————————————————————————————————————
        if Shadow_Ramp is not None:
            # 遍历节点列表来找到名称为Shadow_Ramp的节点：
            Shadow_Ramp_node = None
            for node in Group_node_list:
                if node.name == "Shadow_Ramp":
                    Shadow_Ramp_node = node
                    break
            # 修改节点
            if Shadow_Ramp_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(Shadow_Ramp)
                # 替换贴图
                Shadow_Ramp_node.image = new_image
        # ——————————————————————————————————————————————————————————————————————————————
        if NormalMap is not None:
            # 遍历节点列表来找到名称为Normal Map的节点：
            NormalMap_node = None
            for node in Group_node_list:
                if node.name == "Normal Map":
                    NormalMap_node = node
                    break
            # 修改节点
            if NormalMap_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(NormalMap)
                # 替换贴图
                NormalMap_node.image = new_image
                # 将色彩空间设置为'Non - Color'
                NormalMap_node.image.colorspace_settings.name = 'Non-Color'
        # ————————————————————————————————————————————————————————————————————————————————————————

        # 切换材质槽
        array = context.object.active_material_index
        context.object.active_material_index = array + 1
        bpy.context.object.active_material.preview_render_type = 'FLAT'
        return {'FINISHED'}


class MakePrehts9Operator(bpy.types.Operator):
    '''genshin presets'''
    bl_idname = "object.genshin_body_ops"
    bl_label = "Body/身体"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        mmi = context.object.mmi

        def search_engine(i):
            keywords = str(i).split()
            file_paths = search_files(keywords, mmi.filepath)
            for path in file_paths:
                print(path)
                return path

        # 贴图路径
        NormalMap = search_engine('Body Normal')
        Diffuse = search_engine('Body Diffuse')
        Lightmap = search_engine('Body Light map')
        Shadow_Ramp = search_engine('Body Shadow_Ramp')

        # 获取当前活动对象的活动材质
        mat = bpy.context.object.active_material
        if mat and mat.node_tree:
            # 获取节点树中的所有节点
            nodes = mat.node_tree.nodes
            # 逐个删除节点
            for node in nodes:
                mat.node_tree.nodes.remove(node)

        def Connect_the_nodes(node1, 端口1, node2, 端口2):
            # 查找名为1和2的节点
            node_1 = None
            node_2 = None
            for node in mat.node_tree.nodes:
                if node.name == node1:
                    node_1 = node
                elif node.name == node2:
                    node_2 = node

            # 如果找到两个节点，则连接它们的端口
            if node_1 and node_2:
                output_socket = node_1.outputs.get(端口1)
                input_socket = node_2.inputs.get(端口2)
                if output_socket and input_socket:
                    mat.node_tree.links.new(output_socket, input_socket)

        # 创建材质输出节点
        output_node = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
        # 设置节点位置
        output_node.location = (200, 0)

        # 创建节点组
        Group_node = mat.node_tree.nodes.new('ShaderNodeGroup')
        Group_node.location = (0, 0)
        my_group = bpy.data.node_groups["衣服"]
        Group_node.node_tree = my_group
        Group_node.name = "衣服"

        # 连续节点
        Connect_the_nodes(Group_node.name, '结果', output_node.name, 'Surface')

        # 访问节点组内的节点
        Group_node_list = Group_node.node_tree.nodes
        # ————————————————————————————————————————————————————————————————————————————————————————
        if Diffuse is not None:
            # 遍历节点列表来找到名称为Diffuse的节点：
            Diffuse_node = None
            for node in Group_node_list:
                if node.name == "Diffuse":
                    Diffuse_node = node
                    break
            # 修改节点
            if Diffuse_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(Diffuse)
                # 替换贴图
                Diffuse_node.image = new_image
                # 修改Alpha通道为通道打包
                Diffuse_node.image.alpha_mode = 'CHANNEL_PACKED'
        # ————————————————————————————————————————————————————————————————————————————
        if Lightmap is not None:
            # 遍历节点列表来找到名称为Lightmap的节点：
            Lightmap_node = None
            for node in Group_node_list:
                if node.name == "Lightmap":
                    Lightmap_node = node
                    break
            # 修改节点
            if Lightmap_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(Lightmap)
                # 替换贴图
                Lightmap_node.image = new_image
                # 修改Alpha通道为通道打包
                Lightmap_node.image.alpha_mode = 'CHANNEL_PACKED'
                # 将色彩空间设置为'Non - Color'
                Lightmap_node.image.colorspace_settings.name = 'Non-Color'
        # ————————————————————————————————————————————————————————————————————————————
        if Shadow_Ramp is not None:
            # 遍历节点列表来找到名称为Shadow_Ramp的节点：
            Shadow_Ramp_node = None
            for node in Group_node_list:
                if node.name == "Shadow_Ramp":
                    Shadow_Ramp_node = node
                    break
            # 修改节点
            if Shadow_Ramp_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(Shadow_Ramp)
                # 替换贴图
                Shadow_Ramp_node.image = new_image
        # ——————————————————————————————————————————————————————————————————————————————
        if NormalMap is not None:
            # 遍历节点列表来找到名称为Normal Map的节点：
            NormalMap_node = None
            for node in Group_node_list:
                if node.name == "Normal Map":
                    NormalMap_node = node
                    break
            # 修改节点
            if NormalMap_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(NormalMap)
                # 替换贴图
                NormalMap_node.image = new_image
                # 将色彩空间设置为'Non - Color'
                NormalMap_node.image.colorspace_settings.name = 'Non-Color'
        # ————————————————————————————————————————————————————————————————————————————————————————

        # 切换材质槽
        array = context.object.active_material_index
        context.object.active_material_index = array + 1
        bpy.context.object.active_material.preview_render_type = 'FLAT'
        return {'FINISHED'}


class MakePrehkhts9Operator(bpy.types.Operator):
    '''genshin presets'''
    bl_idname = "object.genshin_face_ops"
    bl_label = "Face/脸"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        mmi = context.object.mmi

        def search_engine(i):
            keywords = str(i).split()
            file_paths = search_files(keywords, mmi.filepath)
            for path in file_paths:
                print(path)
                return path

        # 贴图路径
        Diffuse = search_engine('Face Diffuse')
        if mmi.Face_Shadow_Ramp == 'Hair':
            Shadow_Ramp = search_engine('Hair Shadow_Ramp')
        else:
            Shadow_Ramp = search_engine('Body Shadow_Ramp')
        SDF = search_engine('Face Light map')

        # 获取当前活动对象的活动材质
        mat = bpy.context.object.active_material
        if mat and mat.node_tree:
            # 获取节点树中的所有节点
            nodes = mat.node_tree.nodes
            # 逐个删除节点
            for node in nodes:
                mat.node_tree.nodes.remove(node)

        def Connect_the_nodes(node1, 端口1, node2, 端口2):
            # 查找名为1和2的节点
            node_1 = None
            node_2 = None
            for node in mat.node_tree.nodes:
                if node.name == node1:
                    node_1 = node
                elif node.name == node2:
                    node_2 = node

            # 如果找到两个节点，则连接它们的端口
            if node_1 and node_2:
                output_socket = node_1.outputs.get(端口1)
                input_socket = node_2.inputs.get(端口2)
                if output_socket and input_socket:
                    mat.node_tree.links.new(output_socket, input_socket)

        # 创建材质输出节点
        output_node = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
        # 设置节点位置
        output_node.location = (200, 0)

        # 创建节点组
        Group_node = mat.node_tree.nodes.new('ShaderNodeGroup')
        Group_node.location = (0, 0)
        my_group = bpy.data.node_groups["颜"]
        Group_node.node_tree = my_group
        Group_node.name = "颜"

        # 连续节点
        Connect_the_nodes(Group_node.name, '结果', output_node.name, 'Surface')

        # 访问节点组内的节点
        Group_node_list = Group_node.node_tree.nodes
        # ——————————————————————————————————————————————————————————————————————
        if Diffuse is not None:
            # 遍历节点列表来找到名称为Diffuse的节点：
            Diffuse_node = None
            for node in Group_node_list:
                if node.name == "Diffuse":
                    Diffuse_node = node
                    break
            # 修改节点
            if Diffuse_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(Diffuse)
                # 替换贴图
                Diffuse_node.image = new_image
                # 修改Alpha通道为通道打包
                Diffuse_node.image.alpha_mode = 'CHANNEL_PACKED'
        # ——————————————————————————————————————————————————————————————————————
        if Shadow_Ramp is not None:
            # 遍历节点列表来找到名称为Shadow_Ramp的节点：
            Shadow_Ramp_node = None
            for node in Group_node_list:
                if node.name == "Shadow_Ramp":
                    Shadow_Ramp_node = node
                    break
            # 修改节点
            if Shadow_Ramp_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(Shadow_Ramp)
                # 替换贴图
                Shadow_Ramp_node.image = new_image
        # ——————————————————————————————————————————————————————————————————————

        # 遍历节点列表来找到名称为SDF的节点：
        SDF_node = None
        for node in Group_node_list:
            if node.name == "SDF":
                SDF_node = node
                break
        my_group = bpy.data.node_groups["SDF"]
        SDF_node.node_tree = my_group
        # 访问节点组内的节点
        SDF_Group_node_list = SDF_node.node_tree.nodes

        # ————————————————————————————————————————————————————————————
        if SDF is not None:
            # 遍历节点列表来找到名称为SDF的节点：
            SDF_node = None
            for node in SDF_Group_node_list:
                if node.name == "SDF":
                    SDF_node = node
                    break
            # 修改节点
            if SDF_node:
                # 加载新的贴图
                new_image = bpy.data.images.load(SDF)
                # 替换贴图
                SDF_node.image = new_image
                # 将色彩空间设置为'Non-Color'
                SDF_node.image.colorspace_settings.name = 'Non-Color'

        # 切换材质槽
        array = context.object.active_material_index
        context.object.active_material_index = array + 1
        bpy.context.object.active_material.preview_render_type = 'FLAT'

        return {'FINISHED'}


class MakePrytyOperator(bpy.types.Operator):
    '''Load the node group'''
    bl_idname = "object.genshin_node_ops"
    bl_label = "Load the node group"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        Obj1 = context.active_object

        # 获取当前运行的Py文件的路径
        current_file_path = __file__
        # 获取当前Py文件所在的文件夹路径
        new_path = os.path.dirname(current_file_path)
        # 将当前文件夹路径和文件名组合成完整的文件路径
        file = 'bhp.blend'
        new_file_path = os.path.join(new_path, file)
        print(new_file_path)

        def Additional_actions(A, B, filepath):
            # 指定要追加的集合的名称
            collection_name = A
            directory = B

            # 构建集合的完整路径
            full_filepath = os.path.join(filepath, directory, collection_name)
            # 执行追加操作
            bpy.ops.wm.append(
                filepath=full_filepath,
                directory=os.path.join(filepath, directory),
                filename=collection_name
            )

        # 追加集合
        Additional_actions('一些东西', 'Collection', new_file_path)

        def delete_object(object_name):
            object_to_delete = bpy.data.objects.get(object_name)
            if object_to_delete is not None:
                bpy.context.view_layer.objects.active = object_to_delete
                # 遍历当前视图层中的所有物体
                for obj in bpy.context.view_layer.objects:
                    # 取消每个物体的选择状态
                    obj.select_set(False)
                # 将需要删除的物体设置为选中状态
                object_to_delete.select_set(True)
                # 执行删除物体的操作
                bpy.ops.object.delete()

        def delete_collection_and_move_to_parent(collection_name):
            target_coll = bpy.data.collections.get(collection_name)
            if not target_coll:
                print(f"集合 '{collection_name}' 不存在")
                return

            # 查找目标集合的所有父集合
            parent_collections = []
            for coll in bpy.data.collections:
                if target_coll.name in coll.children:
                    parent_collections.append(coll)

            # 如果目标集合没有父集合，默认转移到场景主集合
            if not parent_collections:
                parent_collections = [bpy.context.scene.collection]

            # 将对象和子集合转移到每个父集合
            for parent_coll in parent_collections:
                # 转移对象
                for obj in target_coll.objects[:]:  # 遍历副本避免修改问题
                    if obj.name not in parent_coll.objects:
                        parent_coll.objects.link(obj)
                    target_coll.objects.unlink(obj)

                # 转移子集合
                for child_coll in target_coll.children[:]:
                    if child_coll.name not in parent_coll.children:
                        parent_coll.children.link(child_coll)
                    target_coll.children.unlink(child_coll)

            # 解除目标集合的所有父级引用
            for coll in bpy.data.collections:
                if target_coll.name in coll.children:
                    coll.children.unlink(target_coll)

            # 删除目标集合
            bpy.data.collections.remove(target_coll)

        # 执行操作
        delete_collection_and_move_to_parent('一些东西')

        # 定义一个列表
        object_names = ["AAAA", "AAA", "AA"]
        # 遍历物体名称列表，调用delete_object函数删除物体
        for object_name in object_names:
            delete_object(object_name)

        # 激活物体
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = Obj1
        # 选择物体
        Obj1.select_set(True)

        return {'FINISHED'}


class MakePres4Operator(bpy.types.Operator):
    '''Post-processing effect'''
    bl_idname = "object.maeg_ops"
    bl_label = "Post-processing effect"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # 它遍历场景节点树中的所有节点，检查是否存在名称与传入参数相同的节点。如果存在则返回True，否则返回False。
        def node_exists(node_name):
            node_tree = bpy.context.scene.node_tree
            if node_tree is None:
                return False
            for node in node_tree.nodes:
                if node.name == node_name:
                    return True
            return False

        # 如果这两个节点中的任何一个存在，就直接返回{'CANCELLED'}
        if node_exists('后期处理') or node_exists('边缘光深度'):
            return {'CANCELLED'}

        # 获取当前运行的Py文件的路径
        current_file_path = __file__
        # 获取当前Py文件所在的文件夹路径
        new_path = os.path.dirname(current_file_path)
        # 将当前文件夹路径和文件名组合成完整的文件路径
        file = 'bhp.blend'
        new_file_path = os.path.join(new_path, file)
        print(new_file_path)

        def Additional_actions(A, B, filepath):
            # 指定要追加的集合的名称
            collection_name = A
            directory = B

            # 构建集合的完整路径
            full_filepath = os.path.join(filepath, directory, collection_name)
            # 执行追加操作
            bpy.ops.wm.append(
                filepath=full_filepath,
                directory=os.path.join(filepath, directory),
                filename=collection_name
            )

        # 设置色彩空间
        bpy.context.scene.display_settings.display_device = 'sRGB'
        bpy.context.scene.view_settings.view_transform = 'Standard'
        bpy.context.scene.view_settings.look = 'None'

        # 设置合成通道
        bpy.context.scene.view_layers["ViewLayer"].use_pass_z = True
        bpy.ops.scene.view_layer_add_aov()
        view_layer = bpy.context.scene.view_layers["ViewLayer"]
        new_aov = view_layer.aovs[-1]  # 新添加的AOV
        new_aov.name = "边缘光数据"

        bpy.context.area.ui_type = 'CompositorNodeTree'

        # 启用节点
        bpy.context.scene.use_nodes = True

        # 追加节点组
        Additional_actions('后期处理', 'NodeTree', new_file_path)
        Additional_actions('边缘光深度', 'NodeTree', new_file_path)

        # 获取合成节点树
        scene = bpy.context.scene
        node_tree = scene.node_tree

        # 遍历所有节点
        for node in node_tree.nodes:
            print(node.name, node.type)
            # 遍历所有节点的输入端口
            if node.inputs:
                for input in node.inputs:
                    print(f"节点 {node.name} 的输入端口 {input.name} 类型为 {input.type}")

            # 遍历所有节点的输出端口
            if node.outputs:
                for output in node.outputs:
                    print(f"节点 {node.name} 的输出端口 {output.name} 类型为 {output.type}")


        # 获取合成节点
        output_node = None
        for node in node_tree.nodes:

            if node.type == 'COMPOSITE':
                output_node = node
                break

        if output_node:
            print("节点名称：", output_node.name)

        # 获取预览器节点
        preview_node = None
        for node in node_tree.nodes:

            if node.type == 'VIEWER':
                preview_node = node
                break

        if preview_node:
            print("节点名称：", preview_node.name)

        if not output_node:
            self.report({'WARNING'}, "未找到合成节点。")
            return {'CANCELLED'}

        # 获取输入端口连接的节点
        def Get_the_input_node(node, i):
            image_input = node.inputs.get(i)
            if image_input:
                connected_nodes = [link.from_node for link in image_input.links]
                for node in connected_nodes:
                    return node.name
            else:
                print(f"合成节点没有连接到{i}输入端口的节点。")
                return 0

        # 获取输入端口连接的节点的输出端口名
        def Obtain_the_output_port_name(node, i):
            image_input = node.inputs.get(i)
            if image_input:
                connected_nodes = [link.from_node for link in image_input.links]
                for node1 in connected_nodes:
                    for output in node1.outputs:
                        for link in output.links:
                            if link.to_node == node:
                                return output.name

        def Connect_the_nodes(node1, 端口1, node2, 端口2):
            # 查找名为1和2的节点
            node_1 = None
            node_2 = None
            for node in node_tree.nodes:
                if node.name == node1:
                    node_1 = node
                elif node.name == node2:
                    node_2 = node

            # 如果找到两个节点，则连接它们的端口
            if node_1 and node_2:
                output_socket = node_1.outputs.get(端口1)
                input_socket = node_2.inputs.get(端口2)
                if output_socket and input_socket:
                    node_tree.links.new(output_socket, input_socket)

        #获取当前场景的渲染层节点名称
        def The_current_scene_rendernode():
            for node in bpy.context.scene.node_tree.nodes:
                if node.type == 'R_LAYERS':
                    scene = node.scene
                    if scene and scene.name == bpy.context.scene.name:
                        print("当前场景的渲染层节点名称：", node.name)
                        return node.name

        input_node = Get_the_input_node(output_node, 'Image')
        print(f"连接到合成节点Image输入端口的节点：{input_node}")

        print_node_output = Obtain_the_output_port_name(output_node, "Image")
        print(f"连接到合成节点Image输入端口的节点的输出端口名：{print_node_output}")

        # 创建节点组
        Group_node = node_tree.nodes.new('CompositorNodeGroup')
        Group_node.location = (0, 0)
        my_group = bpy.data.node_groups["后期处理"]
        Group_node.node_tree = my_group
        Group_node.name = "后期处理"

        Connect_the_nodes(input_node, print_node_output, "后期处理", 'Image')
        Connect_the_nodes("后期处理", 'Image', output_node.name, 'Image')
        if preview_node:
                Connect_the_nodes("后期处理", 'Image', preview_node.name, 'Image')

        # 创建节点组
        Group_node = node_tree.nodes.new('CompositorNodeGroup')
        Group_node.location = (-200, 0)
        my_group = bpy.data.node_groups["边缘光深度"]
        Group_node.node_tree = my_group
        Group_node.name = "边缘光深度"

        Connect_the_nodes("边缘光深度", 'Image', "后期处理", 'Image')
        Connect_the_nodes(input_node, print_node_output, '边缘光深度', 'Image')
        Connect_the_nodes(The_current_scene_rendernode(), 'Depth', '边缘光深度', 'Depth')
        Connect_the_nodes(The_current_scene_rendernode(), "边缘光数据", "边缘光深度", "边缘光数据")
        Connect_the_nodes(The_current_scene_rendernode(), "Alpha", output_node.name, "Alpha")


        # 获取Blender的版本号
        version = bpy.app.version_string
        # 验证blender版本
        if compare_version(version, '4.1.99'):
            # 设置原生辉光
            scene_1 = bpy.context.scene.eevee
            scene_1.use_bloom = True
            scene_1.bloom_threshold = 0.75
            scene_1.bloom_color = (1, 0.705734, 0.340661)
            scene_1.bloom_intensity = 0.05
            scene_1.bloom_knee = 0.7
            scene_1.bloom_radius = 7.6

        bpy.context.area.ui_type = 'VIEW_3D'
        bpy.context.space_data.shading.use_compositor = 'ALWAYS'

        return {'FINISHED'}


class InvertthenormalsOperator(bpy.types.Operator):
    '''Invert the normals'''
    bl_idname = "object.make_normals_ops"
    bl_label = "Invert the normals"

    def execute(self, context):

        # 全局变量"i"
        i = None

        # 遍历选中的物体的材质槽，检查名称为衣服的节点是否存在
        # 获取选中的物体
        selected_objects = context.selected_objects

        found = False

        # 遍历选中的物体
        for obj in selected_objects:
            # 检查物体是否有材质槽
            if hasattr(obj, "material_slots"):
                # 遍历材质槽
                for material_slot in obj.material_slots:
                    # 获取材质
                    material = material_slot.material
                    # 检查材质是否使用节点
                    if material and material.use_nodes:
                        # 遍历节点树
                        for node in material.node_tree.nodes:
                            if found:
                                break
                            # 检查节点名称是否为“衣服”
                            if node.name == "衣服":
                                print(f"在物体 {obj.name} 的材质 {material.name} 中找到名为 '衣服' 的节点。")
                                body_node = node
                                found = True
                                # 获取节点组
                                my_group = bpy.data.node_groups["衣服"]
                                body_node.node_tree = my_group
                                # 访问节点组内的节点
                                Group_node_list = body_node.node_tree.nodes
                                # 遍历节点列表来找到名称为Invert Color的节点：
                                Invert_node = None
                                for node in Group_node_list:
                                    if node.name == "Invert Color":
                                        Invert_node = node
                                        break
                                i = Invert_node.inputs["Fac"].default_value
                                # 修改节点
                                if Invert_node:
                                    if i == 1:
                                        Invert_node.inputs["Fac"].default_value = 0
                                    else:
                                        Invert_node.inputs["Fac"].default_value = 1

        found = False
        # 遍历选中的物体
        for obj in selected_objects:
            # 检查物体是否有材质槽
            if hasattr(obj, "material_slots"):
                # 遍历材质槽
                for material_slot in obj.material_slots:
                    # 获取材质
                    material = material_slot.material
                    # 检查材质是否使用节点
                    if material and material.use_nodes:
                        # 遍历节点树
                        for node in material.node_tree.nodes:
                            if found:
                                break
                            # 检查节点名称是否为“髮”
                            if node.name == "髮":
                                print(f"在物体 {obj.name} 的材质 {material.name} 中找到名为 '髮' 的节点。")
                                body_node = node
                                found = True
                                # 获取节点组
                                my_group = bpy.data.node_groups["髮"]
                                body_node.node_tree = my_group
                                # 访问节点组内的节点
                                Group_node_list = body_node.node_tree.nodes
                                # 遍历节点列表来找到名称为Invert Color的节点：
                                Invert_node = None
                                for node in Group_node_list:
                                    if node.name == "Invert Color":
                                        Invert_node = node
                                        break
                                # 修改节点
                                if Invert_node:
                                    if i == 1:
                                        Invert_node.inputs["Fac"].default_value = 0
                                    else:
                                        Invert_node.inputs["Fac"].default_value = 1

        return {'FINISHED'}


class MakePrehOperator(bpy.types.Operator):
    '''Handle related objects with one click'''
    bl_idname = "object.mayyrh_presets_ops"
    bl_label = "Handle related objects with one click"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        if context.active_object is not None:
            if context.active_object.type == 'EMPTY':
                return True
        return False

    def execute(self, context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        # 获取当前活动的物体
        active_object = bpy.context.active_object
        if active_object.name == 'AA':
            print('已经被命名了')
            self.report({'INFO'}, f"{active_object.name}已经被命名了")
        else:
            def delete_selected_child_rigidbodies(obj_name):
                # 获取当前选中物体
                selected_objs = bpy.context.selected_objects
                if not selected_objs:
                    print("错误：未选中任何物体")
                    return

                # 遍历所有选中物体
                for parent_obj in selected_objs:
                    # 查找直接子级中名为 obj_name 的物体
                    target_child = next((child for child in parent_obj.children
                                         if child.name == obj_name), None)

                    if not target_child:
                        print(f"'{parent_obj.name}' 的子级中未找到 rigidbodies")
                        continue

                    # 递归删除子级物体
                    def recursive_delete(obj):
                        # 先删除子物体（深度优先）
                        for child in obj.children:
                            recursive_delete(child)
                            print(f"删除子物体: {child.name}")
                            bpy.data.objects.remove(child, do_unlink=True)

                    recursive_delete(target_child)

                    # 删除目标物体本身
                    print(f"删除目标物体: {target_child.name}")
                    bpy.data.objects.remove(target_child, do_unlink=True)

                # 强制刷新大纲视图
                for area in bpy.context.window.screen.areas:
                    if area.type == 'OUTLINER':
                        area.tag_redraw()

            # 执行操作
            delete_selected_child_rigidbodies("rigidbodies")
            delete_selected_child_rigidbodies("joints")
            delete_selected_child_rigidbodies("temporary")

            # 更改物体名称
            if active_object is not None:
                # 命名根物体
                bpy.ops.object.mvaegs_ops()
                active_object = bpy.context.active_object
                # 取消全部选择
                bpy.ops.object.select_all(action='DESELECT')

                found = False
                # 遍历所有物体，查找名称包含'_mesh'的网格物体
                for obj in bpy.data.objects:
                    if obj.type == 'MESH' and '_mesh' in obj.name:
                        # 选中并激活物体
                        obj.select_set(True)
                        bpy.context.view_layer.objects.active = obj
                        # 执行操作
                        bpy.ops.object.makess_presets_ops()
                        # 取消选择
                        bpy.ops.object.select_all(action='DESELECT')
                        found = True
                        break

                # 如果未找到符合条件的物体
                if not found:
                    # 收集所有网格物体
                    mesh_objs = [obj for obj in bpy.data.objects if obj.type == 'MESH']
                    if mesh_objs:
                        # 选中所有网格物体
                        for obj in mesh_objs:
                            obj.select_set(True)
                            break
                        # 激活第一个网格物体
                        bpy.context.view_layer.objects.active = mesh_objs[0]
                        # 执行操作
                        bpy.ops.object.makess_presets_ops()
                        # 取消选择
                        bpy.ops.object.select_all(action='DESELECT')

                # 骨骼
                for obj in bpy.data.objects:
                    if obj.type == 'ARMATURE':
                        # 选中物体
                        obj.select_set(True)
                        # 激活物体
                        bpy.context.view_layer.objects.active = obj
                        # 执行操作
                        bpy.ops.object.maess_presets_ops()
                        # 检查定位骨骼
                        if obj and obj.type == 'ARMATURE' and obj.data.bones.get(addon_prefs.positioning_bone):
                            print(f"骨骼{addon_prefs.positioning_bone}存在")
                        else:
                            self.report({'WARNING'}, f"默认定位骨骼''{addon_prefs.positioning_bone}''不存在")

                        # 取消全部选择
                        bpy.ops.object.select_all(action='DESELECT')
                        break

                # SDF
                # 遍历所有物体，找到类型为 'EMPTY' 且名称里有 脸部定位 的物体
                for obj in bpy.data.objects:
                    if obj.type == 'EMPTY' and '脸部定位' in obj.name:
                        # 选中物体
                        obj.select_set(True)
                        # 激活物体
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.maegss_presets_ops()
                        bpy.ops.object.mdts_preset_ops()
                        mmi = context.object.mmi
                        mmi.re_obj = True
                bpy.ops.object.make_presets_ops()

            else:
                print("没有活动的物体可以重命名。")

        # 打包资源
        bpy.ops.file.pack_all()

        return {'FINISHED'}


class MakePdtyOperator(bpy.types.Operator):
    '''Add a face positioning constraint'''
    bl_idname = "object.mdts_preset_ops"
    bl_label = "Add a face positioning constraint"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        if context.active_object is not None:
            if context.active_object.type == 'EMPTY':
                return True
        return False

    def execute(self, context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        # 获取当前活动的物体
        active_object = bpy.context.active_object
        # 清空所有约束
        active_object.constraints.clear()
        print(f"已删除物体 {active_object.name} 的所有约束")
        # 添加子级约束
        bpy.ops.object.constraint_add(type='CHILD_OF')
        # 获取刚刚添加的约束
        new_constraint = active_object.constraints[-1]
        # 设置约束
        new_constraint.name = '脸部定位-子级'
        new_constraint.target = bpy.data.objects['AAA']
        new_constraint.subtarget = addon_prefs.positioning_bone
        bpy.ops.constraint.childof_set_inverse(constraint="脸部定位-子级", owner='OBJECT')
        bpy.ops.constraint.childof_clear_inverse(constraint="脸部定位-子级", owner='OBJECT')
        # 清空位置
        bpy.ops.object.location_clear(clear_delta=False)

        return {'FINISHED'}

class MakePdtysOperator(bpy.types.Operator):
    '''return'''
    bl_idname = "object.mdtos_preset_ops"
    bl_label = "return"

    def execute(self, context):
        mmi = context.active_object.mmi
        mmi.re_obj = False
        return {'FINISHED'}

class Adaptivestrokes(bpy.types.Operator):
    '''Adaptive strokes'''
    bl_idname = "object.adaptive_strokes_ops"
    bl_label = "Add Adaptive strokes"
    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        if context.active_object is not None:
            if context.active_object.type == 'MESH':
                return True
        return False

    def execute(self, context):

        mmi = context.object.mmi

        # 获取当前场景
        scene = bpy.context.scene

        def add_driver_to_solidify(A1,A2,A3,A4,A5,A6):
            # 获取当前激活的对象
            active_obj = bpy.context.active_object
            if not active_obj:
                print("当前没有激活的对象。")
                return

            # 尝试找到名为“自动描边”的实体化修改器，若没有则找第一个实体化修改器
            target_modifier = None
            block = False
            for modifier in active_obj.modifiers:
                if modifier.type == 'SOLIDIFY' and modifier.name == '自动描边':
                    target_modifier = modifier
                    break
            if not target_modifier:
                for modifier in active_obj.modifiers:
                    if modifier.type == 'SOLIDIFY':
                        target_modifier = modifier
                        break
            if not target_modifier:
                print("在激活对象中未找到实体化修改器,启动几何节点模式。")
                for modifier in active_obj.modifiers:
                    if modifier.type == 'NODES':
                        block = True
                        target_modifier = modifier
                        break
                if not target_modifier:
                    print("在激活对象中未找到几何节点修改器。")
                    return

            # 通过接口索引设置参数
            if compare_version(bpy.app.version_string, '4.1.99'):  # 检查版本
                inputs = target_modifier.node_group.inputs
            else:
                inputs = target_modifier.node_group.interface.items_tree

            Input = '["'+str(inputs["描边厚度"].identifier)+'"]'

            # 清除旧驱动
            if target_modifier:
                try:
                    if block:
                        target_modifier.driver_remove(Input)  # 移除旧驱动
                    else:
                        target_modifier.driver_remove("thickness")  # 移除旧驱动
                except:
                    pass

            # 获取物体
            obj_a1 = A1
            obj_a2 = A2
            if not obj_a1 or not obj_a2:
                print("未找到 A1 或 A2 物体。")
                return

            if block:
                # 添加驱动器
                fcurve = target_modifier.driver_add(Input)
                driver = fcurve.driver
            else:
                # 为实体化修改器的 thickness 属性添加驱动器
                fcurve = target_modifier.driver_add("thickness")
                driver = fcurve.driver

            # 添加一个变量
            var = driver.variables.new()
            var.name = "distance"
            var.type = 'LOC_DIFF'

            # 设置变量的目标对象
            target = var.targets[0]
            target.id = obj_a1
            target.transform_space = 'WORLD_SPACE'  # 设置为世界空间

            target = var.targets[1]
            target.id = obj_a2
            target.transform_space = 'WORLD_SPACE'  # 设置为世界空间

            # 设置驱动器表达式
            driver.expression = "distance"

            # 删除 F 曲线的所有修改器
            for mod in fcurve.modifiers:
                fcurve.modifiers.remove(mod)

            # 删除 F 曲线的所有关键帧
            fcurve.keyframe_points.clear()

            '''最小值'''
            # 添加关键帧 0，值为 0.08
            kf0 = fcurve.keyframe_points.insert(frame=A3, value=A4)
            # 设置插值方式为线性
            kf0.interpolation = 'LINEAR'

            '''最大值'''
            # 添加关键帧 20，值为 0.5
            kf20 = fcurve.keyframe_points.insert(frame=A5, value=A6)
            # 设置插值方式为线性
            kf20.interpolation = 'LINEAR'

        if mmi.rfd_ghu:
            Obj1 = context.active_object

            if mmi.Track_the_camera.name in bpy.data.objects:
                obj_b1 = mmi.Track_the_camera

                # 查找目标集合
                target_collection = None
                for collection in bpy.data.collections:
                    if mmi.Face_positioning.name in collection.objects:
                        target_collection = collection
                        break

                if target_collection:
                    # 生成基础名称（不含序号）
                    base_name = target_collection.name + "描边追踪"

                    # 创建正则匹配模式
                    pattern = re.compile(r'^{}(\.\d+)?$'.format(re.escape(base_name)))

                    # 仅遍历目标集合中的物体
                    to_remove = []
                    for obj in target_collection.objects:
                        if pattern.match(obj.name):
                            to_remove.append(obj)

                    # 删除匹配的物体
                    for obj in to_remove:
                        bpy.data.objects.remove(obj, do_unlink=True)

                    # 创建新空物体（此时名称不会冲突）
                    empty_obj = bpy.data.objects.new(base_name, None)
                    target_collection.objects.link(empty_obj) # 放入集合

                # 遍历场景中的所有相机
                for camera in bpy.data.cameras:
                    # 为新创建的空物体添加子级约束
                    child_constraint = empty_obj.constraints.new(type='CHILD_OF')
                    # 设置约束的目标物体为当前相机
                    child_constraint.target = bpy.data.objects.get(camera.name)
                    child_constraint.name = camera.name

                    # 激活空物体
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = empty_obj
                    # 选择空物体
                    empty_obj.select_set(True)
                    # 清除子级约束的逆矩阵
                    bpy.ops.constraint.childof_clear_inverse(constraint=child_constraint.name, owner='OBJECT')

                i = 0
                # 遍历所有标记
                for marker in scene.timeline_markers:
                    # 检查标记是否与相机关联
                    if marker.camera:
                        # 输出标记的名称、帧位置和关联的相机
                        print(f"标记名称: {marker.name}")
                        print(f"帧位置: {marker.frame}")
                        print(f"关联相机: {marker.camera.name}")
                        obj = empty_obj
                        # 遍历对象的所有约束
                        for constraint1 in obj.constraints:
                            # 匹配与标记相机同名的约束
                            if constraint1.name == marker.camera.name:
                                print(f"激活约束 - {constraint1.name}")

                                # 设置当前约束的权重为1（完全激活）
                                constraint1.influence = 1
                                # 插入关键帧（默认贝塞尔插值）
                                constraint1.keyframe_insert(data_path="influence", frame=marker.frame)

                                # 检查动画数据是否存在（防止空指针）
                                if obj.animation_data and obj.animation_data.action:
                                    # 遍历所有动画曲线
                                    for fcurve in obj.animation_data.action.fcurves:
                                        # 通过数据路径匹配目标曲线
                                        # path_from_id()生成形如 "constraints["ConstraintName"].influence" 的路径
                                        if fcurve.data_path == constraint1.path_from_id("influence"):
                                            # 遍历该曲线的所有关键帧点
                                            for keyframe in fcurve.keyframe_points:
                                                # 匹配当前帧的关键帧（x坐标为帧号）
                                                if keyframe.co.x == marker.frame:
                                                    # 设置插值模式为常量（阶梯式变化）
                                                    keyframe.interpolation = 'CONSTANT'
                                                    break  # 找到后退出循环

                                # 处理其他约束（非当前标记相机关联的约束）
                                for constraint2 in obj.constraints:
                                    if constraint2.name != marker.camera.name:
                                        print(f"禁用约束 - {constraint2.name}")
                                        # 设置其他约束权重为0（完全禁用）
                                        constraint2.influence = 0
                                        # 插入关键帧
                                        constraint2.keyframe_insert(data_path="influence", frame=marker.frame)

                                        # 重复相同的插值模式设置流程
                                        if obj.animation_data and obj.animation_data.action:
                                            for fcurve in obj.animation_data.action.fcurves:
                                                if fcurve.data_path == constraint2.path_from_id("influence"):
                                                    for keyframe in fcurve.keyframe_points:
                                                        if keyframe.co.x == marker.frame:
                                                            keyframe.interpolation = 'CONSTANT'
                                                            break
                        print("-" * 20)
                        i = i + 1
                print(i)

                # 激活物体
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = Obj1
                # 选择物体
                Obj1.select_set(True)
                # 执行操作
                add_driver_to_solidify(mmi.Face_positioning, empty_obj, mmi.minimum_value_meters, mmi.minimum_Thickness, mmi.utmost_value_meters, mmi.utmost_Thickness)
            else:
                print("未找到名为 '追踪相机' 的物体。")
        else:
            # 执行操作
            add_driver_to_solidify(mmi.Face_positioning,mmi.Track_the_camera, mmi.minimum_value_meters, mmi.minimum_Thickness, mmi.utmost_value_meters, mmi.utmost_Thickness)

        return {'FINISHED'}

class FixAMDgraphicscardsynthesizerbug(bpy.types.Operator):
    '''Fix AMD graphics card synthesizer bug'''
    bl_idname = "object.fix_synthesizer_ops"
    bl_label = "Fix AMD graphics card synthesizer bug"
    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        def process_nodes(nodes):
            for node in nodes:
                if node.type == 'TEX_IMAGE' and node.name != 'Shadow_Ramp':
                    node.interpolation = 'Smart'
                elif node.type == 'GROUP':
                    # 递归处理节点组内的节点
                    group_nodes = node.node_tree.nodes
                    process_nodes(group_nodes)

        # 获取场景中的所有对象
        all_objects = bpy.context.scene.objects

        for obj in all_objects:
            if obj.type == 'MESH':
                # 检查对象是否有材质插槽
                if obj.material_slots:
                    # 遍历对象的所有材质
                    for material_slot in obj.material_slots:
                        material = material_slot.material
                        if material and material.use_nodes:
                            nodes = material.node_tree.nodes
                            process_nodes(nodes)

        return {'FINISHED'}

# 边缘预览
class EdgePreviewOperator(bpy.types.Operator):
    '''Edge Preview'''
    bl_idname = "object.edge_preview_ops"
    bl_label = "Edge Preview"
    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        # 获取当前运行的Py文件的路径
        current_file_path = __file__
        # 获取当前Py文件所在的文件夹路径
        new_path = os.path.dirname(current_file_path)
        # 将当前文件夹路径和文件名组合成完整的文件路径
        file = 'bhp.blend'
        new_file_path = os.path.join(new_path, file)

        # 检查当前场景是否存在名为 "MMI-自动描边" 的几何节点组
        if not "MMI-自动描边" in bpy.data.node_groups:
            print("几何节点组 'MMI-自动描边' 不存在。")
            # 从Blend文件中追加节点组
            with bpy.data.libraries.load(new_file_path, link=False) as (data_from, data_to):
                data_to.node_groups = [name for name in data_from.node_groups if name == "MMI-自动描边"]

        # 检查当前场景是否存在名为 "MMI-Edge-Preview" 的材质节点组
        if not "MMI-Edge-Preview" in bpy.data.node_groups:
            print("材质节点组 'MMI-Edge-Preview' 不存在。")
            # 从Blend文件中追加节点组
            with bpy.data.libraries.load(new_file_path, link=False) as (data_from, data_to):
                data_to.node_groups = [name for name in data_from.node_groups if name == "MMI-Edge-Preview"]

        obj_A = context.active_object # 获取当前活动的物体

        obj_A_material_name = []

        e = True  # 标记是否存在'mmi-edge|'的前缀

        # 遍历物体所有的材质槽
        for material_slot in obj_A.material_slots:

            # 是否存在'mmi-edge|'的前缀
            if material_slot.material.name.startswith('mmi-edge|'):
                e = False
                break  # 找到匹配的材质槽，退出循环

            # 获取当前材质槽的材质
            material = material_slot.material
            # 获取材质的名称
            material_name = material.name
            # 将材质名称添加到列表中
            obj_A_material_name.append(material_name)

        # 材质数量
        obj_A_material_number = len(obj_A_material_name)
        print(f"物体 {obj_A.name} 的材质数量为 {obj_A_material_number}")

        # 新建材质
        for material_name in obj_A_material_name:

            if e:
                new_material = bpy.data.materials.new(name='mmi-edge|' + material_name)
                new_material.use_nodes = True  # 启用节点
                if compare_version(bpy.app.version_string, '4.1.99'):
                    new_material.blend_method = 'HASHED'
                    new_material.shadow_method = 'NONE'
            else:
                new_material = bpy.data.materials.get('mmi-edge|' + material_name)
                new_material.use_nodes = True

            # 删除所有的节点
            for node in new_material.node_tree.nodes:
                new_material.node_tree.nodes.remove(node)

            # 获取节点树
            node_tree = new_material.node_tree

            t = ['颜2', '面2', '二重', '睫', '口舌','齿', '眉', '白目', '目', '星目', '口', '舌', '眉睫', '目影', '目光', '瞳孔']

            u = 1

            for i in t:
                material_name_A1 = material_name.split('.', -1)[0]
                if i == material_name_A1:
                    u = 0
                elif '+' in material_name_A1:
                    u = 0

            # 节点组
            node_group = node_tree.nodes.new(type='ShaderNodeGroup')
            node_group.node_tree = bpy.data.node_groups["MMI-Edge-Preview"]
            node_group.location = (0, 0)
            node_group.inputs['Alpha'].default_value = u

            # 材质输出
            node_output = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
            node_output.location = (200, 0)

            # 链接节点
            links = node_tree.links
            link = links.new(node_group.outputs[0], node_output.inputs[0])

            # 新建材质槽
            if e:
                new_material_slot = obj_A.data.materials.append(new_material)

        # 几何节点
        if not 'MMI-边缘预览' in obj_A.modifiers:

            new_modifiers = obj_A.modifiers.new(name="MMI-边缘预览", type='NODES')
            new_modifiers.node_group = bpy.data.node_groups["MMI-自动描边"]

            # 通过接口索引设置参数
            if compare_version(bpy.app.version_string, '4.1.99'):  # 检查版本
                inputs = new_modifiers.node_group.inputs
            else:
                inputs = new_modifiers.node_group.interface.items_tree

            new_modifiers[inputs["描边厚度"].identifier] = 0.1
            new_modifiers[inputs["翻转面"].identifier] = True
            new_modifiers[inputs["材质偏移"].identifier] = obj_A_material_number
            new_modifiers[inputs["描边合并"].identifier] = 0.0001

            bpy.ops.mmi.update_stroke_list()

        return {'FINISHED'}

# 撤销边缘预览
class RevokeEdgePreviewOperator(bpy.types.Operator):
    '''revoke Edge Preview'''
    bl_idname = "object.revoke_edge_preview_ops"
    bl_label = ""
    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):

        obj_A = bpy.context.active_object  # 获取当前活动的物体

        # 收集需要删除的材质槽索引
        slots_to_remove = []
        for idx, material_slot in enumerate(obj_A.material_slots):
            material = material_slot.material
            if material and material.name.startswith("mmi-edge|"):
                slots_to_remove.append(idx)

        # 按逆序删除材质槽
        for idx in sorted(slots_to_remove, reverse=True):
            # 设置活动材质槽为当前索引
            obj_A.active_material_index = idx
            # 使用操作符删除活动材质槽
            bpy.ops.object.material_slot_remove()

        # 删除材质数据块
        materials_to_remove = [mat for mat in bpy.data.materials
                               if mat.name.startswith("mmi-edge|") and mat.users == 0]

        for material in materials_to_remove:
            bpy.data.materials.remove(material)

        # 遍历物体的所有修改器
        for modifier in obj_A.modifiers:
            # 检查修改器的名称是否为 "MMI-边缘预览"
            if modifier.name == "MMI-边缘预览":
                # 移除修改器
                obj_A.modifiers.remove(modifier)

        bpy.ops.mmi.update_stroke_list()

        return {'FINISHED'}

# MMD边缘预览转换到MMI
class MMD2MMIEdgePreviewOperator(bpy.types.Operator):
    '''MMD边缘预览转换到MMI'''
    bl_idname = "object.mmd2mmi_edge_preview_ops"
    bl_label = "Convert to MMI"
    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):

        # 获取当前运行的Py文件的路径
        current_file_path = __file__
        # 获取当前Py文件所在的文件夹路径
        new_path = os.path.dirname(current_file_path)
        # 将当前文件夹路径和文件名组合成完整的文件路径
        file = 'bhp.blend'
        new_file_path = os.path.join(new_path, file)

        # 检查当前场景是否存在名为 "MMI-自动描边" 的几何节点组
        if not "MMI-自动描边" in bpy.data.node_groups:
            print("几何节点组 'MMI-自动描边' 不存在。")
            # 从Blend文件中追加节点组
            with bpy.data.libraries.load(new_file_path, link=False) as (data_from, data_to):
                data_to.node_groups = [name for name in data_from.node_groups if name == "MMI-自动描边"]

        # 检查当前场景是否存在名为 "MMI-Edge-Preview" 的材质节点组
        if not "MMI-Edge-Preview" in bpy.data.node_groups:
            print("材质节点组 'MMI-Edge-Preview' 不存在。")
            # 从Blend文件中追加节点组
            with bpy.data.libraries.load(new_file_path, link=False) as (data_from, data_to):
                data_to.node_groups = [name for name in data_from.node_groups if name == "MMI-Edge-Preview"]

        active_obj = bpy.context.active_object # 获取当前活动的物体

        # 获取mmd_edge_preview实体化修改器
        thickness_rounded = 0
        material_offsets = 0
        use_flip_normals = True

        for modifier in active_obj.modifiers:
            if modifier.type == 'SOLIDIFY' and modifier.name == 'mmd_edge_preview':
                thickness_rounded = round(modifier.thickness, 2)
                material_offsets = modifier.material_offset
                use_flip_normals = modifier.use_flip_normals
                active_obj.modifiers.remove(modifier)
                break

        # 检查物体是否有材质
        if hasattr(active_obj.data, 'materials') and active_obj.data.materials:
            for mat_slot in active_obj.material_slots:
                mat = mat_slot.material

                # 节点树
                mmd_node_tree = mat.node_tree

                if mat and mat.name.startswith("mmd_edge."):
                    # 移除前缀并构造新名称
                    new_name = "mmi-edge|" + mat.name[len("mmd_edge."):]

                    # 检查新名称是否已存在
                    if new_name not in bpy.data.materials:
                        mat.name = new_name
                        mat.diffuse_color = (1.0, 1.0, 1.0, 1.0)  # 白色

                        mmd_node_edge = mmd_node_tree.nodes.get("mmd_edge_preview") # 获取节点

                        # 获取名为 "MMDEdgePreview" 节点组的Color输入
                        MMD_color_input = mmd_node_edge.inputs.get("Color").default_value

                        # 获取名为 "MMDEdgePreview" 节点组的Alpha输入
                        MMD_alpha_input = mmd_node_edge.inputs.get("Alpha").default_value

                        del_nodes = []

                        # 删除所有的节点，完成后再删掉
                        for node in mmd_node_tree.nodes:
                            del_nodes.append(node)

                        # 节点组
                        node_group = mmd_node_tree.nodes.new(type='ShaderNodeGroup')
                        node_group.name = "MMI-Edge-Preview"
                        node_group.node_tree = bpy.data.node_groups["MMI-Edge-Preview"]
                        node_group.location = (0, 0)

                        # 材质输出
                        mmi_ol = mmd_node_tree.nodes.new(type='ShaderNodeOutputMaterial')
                        mmi_ol.location = (200, 0)

                        # 链接节点
                        links = mmd_node_tree.links
                        link = links.new(node_group.outputs[0], mmi_ol.inputs[0])

                        # 设置节点组的输入值
                        node_group.inputs['Alpha'].default_value = MMD_alpha_input
                        node_group.inputs['Color'].default_value = MMD_color_input

                        # 删除列表中所有的节点
                        for node in del_nodes:
                            mmd_node_tree.nodes.remove(node)

        idx_list = []  # 用于存储需要删除的索引

        # 遍历材质槽索引
        for idx in range(len(active_obj.material_slots)):
            mat_slot = active_obj.material_slots[idx]
            mat = mat_slot.material
            if 'disabled' in mat.name:
                idx_list.append(idx)

        for idx in idx_list:
            mat_slot = active_obj.material_slots[idx]
            material = mat_slot.material  # 获取材质

            # 节点树
            mmd_node_tree = material.node_tree

            # 获取节点
            mmi_node_edge = mmd_node_tree.nodes.get("MMI-Edge-Preview")

            # 获取名为 "MMI-Edge-Preview" 节点组的Color输入
            MMI_color_input = mmi_node_edge.inputs.get("Color").default_value

            # 获取名为 "MMI-Edge-Preview" 节点组的Alpha输入
            MMI_alpha_input = mmi_node_edge.inputs.get("Alpha").default_value

            # 获取原名称
            old_idx = idx - material_offsets
            old_mat_slot = active_obj.material_slots[old_idx]
            old_mat_name = old_mat_slot.material.name
            # 新建材质
            new_material = bpy.data.materials.new(name='mmi-edge|' + old_mat_name)
            # 启用节点
            new_material.use_nodes = True
            # 启用背面剔除
            new_material.use_backface_culling = True
            # 更换材质
            active_obj.material_slots[idx].material = new_material

            if compare_version(bpy.app.version_string, '4.1.99'):
                new_material.blend_method = 'HASHED'
                new_material.shadow_method = 'NONE'

            # 删除所有的节点
            for node in new_material.node_tree.nodes:
                new_material.node_tree.nodes.remove(node)

            # 节点组
            node_group = new_material.node_tree.nodes.new(type='ShaderNodeGroup')
            node_group.name = "MMI-Edge-Preview"
            node_group.node_tree = bpy.data.node_groups["MMI-Edge-Preview"]
            node_group.location = (0, 0)
            # 材质输出
            mmi_shader = new_material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
            mmi_shader.location = (200, 0)
            # 链接节点
            links = new_material.node_tree.links
            link = links.new(node_group.outputs[0], mmi_shader.inputs[0])
            # 设置节点组的输入值
            node_group.inputs['Alpha'].default_value = MMI_alpha_input
            node_group.inputs['Color'].default_value = MMI_color_input

        # 遍历物体的所有修改器
        for modifier in active_obj.modifiers:
            # 检查修改器的名称是否为 "MMI-边缘预览"
            if modifier.name == "MMI-边缘预览":
                return {'FINISHED'}

        # 新建修改器
        new_modifiers = active_obj.modifiers.new(name="MMI-边缘预览", type='NODES')
        new_modifiers.node_group = bpy.data.node_groups["MMI-自动描边"]

        # 通过接口索引设置参数
        if compare_version(bpy.app.version_string, '4.1.99'):  # 检查版本
            inputs = new_modifiers.node_group.inputs
        else:
            inputs = new_modifiers.node_group.interface.items_tree

        new_modifiers[inputs["描边厚度"].identifier] = thickness_rounded
        new_modifiers[inputs["翻转面"].identifier] = use_flip_normals
        new_modifiers[inputs["材质偏移"].identifier] = material_offsets
        new_modifiers[inputs["描边合并"].identifier] = 0.0001

        bpy.ops.mmi.update_stroke_list()

        return {'FINISHED'}


class MatchingmaterialsMMDmodelOperator(bpy.types.Operator):
    '''Matching materials to MMD model'''
    bl_idname = "object.matching_materials_mmd_model_ops"
    bl_label = "Matching materials to MMD model"
    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    # 打开文件选择器
    directory: bpy.props.StringProperty(
        subtype='DIR_PATH',
    )
    filter_folder: bpy.props.BoolProperty(
        default=True,
        options={'HIDDEN'}
    )
    filter_image: bpy.props.BoolProperty(
        default=True,
        options={'HIDDEN'}
    )

    def execute(self, context):

        scene = context.scene
        mmi = context.object.mmi

        mmi.filepath = self.directory

        bpy.ops.object.genshin_node_ops()  # 执行genshin_node_ops

        png_name_idx = {}  # 图像文件的名称和材质槽索引
        image_types = {}  # 图像名称和模式
        operation_Mode = {}  # 操作模式

        # 获取当前活动对象
        obj = bpy.context.active_object

        print(self.directory)

        # 遍历材质槽
        for slot in obj.material_slots:
            mat = slot.material

            if mat and mat.use_nodes:  # 检查材质是否使用节点
                nodes = mat.node_tree.nodes

                # 查找名为'mmd_base_tex'的图像纹理节点
                tex_node = nodes.get("mmd_base_tex")

                if tex_node and tex_node.type == 'TEX_IMAGE':
                    if tex_node.image:
                        # 获取图像文件的名称
                        png_name_idx[slot.slot_index] = tex_node.image.name
                    else:
                        print(f"材质 '{mat.name}' 中'mmd_base_tex'节点未关联图像")
                else:
                    print(f"材质 '{mat.name}' 中未找到'mmd_base_tex'图像纹理节点")

        for i in scene.mmi_images:
            image_types[i.image.name] = i.image_type

        for key, value in png_name_idx.items():
            for key1, value1 in image_types.items():
                if value == key1:
                    operation_Mode[key] = value1

        # 遍历材质槽
        for slot in obj.material_slots:
            for key, value in operation_Mode.items():
                if slot.slot_index == key:
                    obj.active_material_index = key  # 设置当前材质槽索引
                    if value == "FACE":
                        bpy.ops.object.genshin_face_ops()
                    if value == "HAIR":
                        bpy.ops.object.genshin_presets_ops()
                    if value == "BODY":
                        bpy.ops.object.genshin_body_ops()
                    if value == "SKIP":
                        continue # 跳过匹配
                    print(f"材质 '{slot.material.name}' 对应的模式为 '{value}'")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
