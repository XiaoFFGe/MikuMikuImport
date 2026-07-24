import bpy
import os
import random
import string
from difflib import SequenceMatcher  # 用于计算两个序列的相似度

import bpy
import mathutils

from addons.MikuMikuImport_Pro.config import __addon_name__
from addons.MikuMikuImport_Pro.operators import mmi_object_name
from common.i18n.i18n import i18n


class Render2Operator(bpy.types.Operator):
    """Import a render preset"""
    bl_idname = "object.rendering_ops"
    bl_label = "Import a render preset"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        if context.active_object is not None:
            if context.active_object.type == 'MESH':
                return True
        return False

    #打开文件选择器
    filepath: bpy.props.StringProperty(
        subtype='FILE_PATH',
    )
    filter_folder: bpy.props.BoolProperty(
        default=True,
        options={'HIDDEN'}
    )
    filter_blender: bpy.props.BoolProperty(
        default=True,
        options={'HIDDEN'}
    )

    Legacy_face_positioning: bpy.props.BoolProperty(
        name="Legacy face positioning",
        default=False,
        description='旧版脸部定位'
    )
    Position_the_bones: bpy.props.StringProperty(
        name='Position the bones',
        subtype='FILE_NAME',
        description = '输入一个定位骨骼名称，留空则选择预设指定的默认骨骼'
    )
    Fuzzy: bpy.props.EnumProperty(
        name="Matching Pattern",
        items=[
            ('0', "模糊搜索", "模糊搜索"),
            ('1', "传统关联", "传统关联"),
        ],
        default='0',
        description="选择匹配模式"
    )

    def execute(self, context):
        global obj1, tyu, sun

        mmi = context.object.mmi
        addon_prefs = context.preferences.addons[__addon_name__].preferences

        # 提取文件路径
        filename = self.filepath.split('/')[-1]
        print("选择的文件路径:", filename)
        # 完整的文件路径
        file_path = filename
        # 获取路径部分
        directory_path = os.path.dirname(file_path)
        # 只保留路径
        print("路径:", directory_path)

        # 获取当前活动的物体
        active_object = bpy.context.view_layer.objects.active

        # 检查是否有活动物体，如果存在则打印名称
        if active_object:
            print("当前活动的物体：", active_object.name)
            Model = active_object.name

            # 获取所有选中的物体
            selected_objects = bpy.context.selected_objects

            # 验证是否至少有两个物体被选中：一个活动的和至少一个非活动的
            if len(selected_objects) > 1:
                # 打印除了活动物体之外的所有选中物体的名称
                for obj1 in selected_objects:
                    if obj1 != active_object:
                        tyu = obj1.name
                        print("不活动物体的名称：", tyu)
            else:
                print("没有非活动物体！获取活动物体的骨架修改器的目标的名称")
                if active_object.modifiers:
                    # 获取active_object的骨架修改器
                    for modifier in active_object.modifiers:
                        if modifier.type == 'ARMATURE':
                            armature_modifier = modifier
                            # 获取骨架修改器的目标
                            armature_object = armature_modifier.object
                            # 获取骨架修改器的目标的名称
                            tyu = armature_object.name
                            print("活动物体的骨架修改器的目标的名称：", tyu)
                            break
                else:
                    print("活动物体没有骨架修改器，获取活动物体的父级名称")
                    if active_object.parent is None or active_object.parent.type != 'ARMATURE':
                        print("模型没有关联骨架！")
                        self.report({'WARNING'}, "模型没有关联骨架！")
                        return {'FINISHED'}

                    # 获取活动物体的父级
                    parent_object = active_object.parent
                    # 获取父级的名称
                    tyu = parent_object.name
                    print("活动物体的父级名称：", tyu)

            global hidden_state
            global tyus

            tyus = bpy.data.objects.get(tyu)
            # 记住隐藏状态
            hidden_state = tyus.hide_get()

            # 取消隐藏
            tyus.hide_set(False)

            # 加选tyu
            bpy.data.objects[tyu].select_set(True)

            # 获取所有选中的物体
            selected_objects = bpy.context.selected_objects

            # 检查是否至少有两个物体被选中
            if len(selected_objects) != 2:
                print("只能选中模型和骨骼！")
                self.report({'WARNING'}, "只能选中模型和骨骼！")
                return {'FINISHED'}

            # 确保一个是网格模型，另一个是骨骼
            model_and_armature_selected = False
            for obj in selected_objects:
                if obj.type == 'MESH':
                    model = obj
                elif obj.type == 'ARMATURE':
                    armature = obj
            if 'model' in locals() and 'armature' in locals():
                model_and_armature_selected = True

            if not model_and_armature_selected:
                print("只能选中模型和骨骼！")
                self.report({'WARNING'}, "只能选中模型和骨骼！")
                return {'FINISHED'}
        else:
            print("没有活动物体被选中！")
            self.report({'WARNING'}, f"没有活动物体被选中！")
            return {'FINISHED'}

        def Additional_actions(A, B):
            """ 追加集合操作 """
            # 指定要追加的集合的名称
            collection_name = A
            directory = B

            # 构建集合的完整路径
            full_filepath = os.path.join(self.filepath, directory, collection_name)
            # 执行追加操作
            bpy.ops.wm.append(
                filepath=full_filepath,
                directory=os.path.join(self.filepath, directory),
                filename=collection_name
            )

        def Snap_and_move_object_matrix(obj1, obj2):
            """ 对象矩阵对齐和移动, obj1是obj2的父级 """

            # 计算obj2的矩阵世界矩阵
            obj2.matrix_local = obj1.matrix_world.inverted() @ obj2.matrix_world

            # 设置obj2的矩阵世界矩阵
            obj2.matrix_world = obj1.matrix_world @ obj2.matrix_local

        def Find_root_object(objs):
            """ 查找所有对象的根对象，返回一个根对象列表 """
            root_objects = []

            for obj in objs:

                obj_constraint_types = []

                # 检查对象是否有子级约束
                for constraint1 in obj.constraints:
                    obj_constraint_types.append(constraint1.type)

                # 检查对象是否有子级约束
                if 'CHILD_OF' not in obj_constraint_types:
                    # 检查对象是否有父级
                    if obj.parent is None:
                        root_objects.append(obj)

            return root_objects


        # 取消选择所有物体
        bpy.ops.object.select_all(action='DESELECT')

        mmi_object = []

        # 追加集合
        Additional_actions('【MMD预设】','Collection')

        # 获取当前选中的所有物体
        selected_objects = bpy.context.selected_objects

        print('追加物体：')

        # 遍历所有选中的物体
        for obj3 in selected_objects:

            print(obj3.name)

            # 加入mmi_object
            mmi_object.append(obj3)

            # 检查对象类型是否为灯
            if obj3.type == 'LIGHT':
                # 检查灯的类型是否为日光（Sun）
                if obj3.data.type == 'SUN':
                    # 打印灯的名称
                    print("日光灯名称：", obj3.name)
                    sun = obj3.name

        # 对齐矩阵
        for obj4 in Find_root_object(mmi_object):

            # 对齐矩阵
            Snap_and_move_object_matrix(active_object, obj4)

        # 创建一个转换表
        translator = str.maketrans('', '', string.punctuation)

        # 移除标点
        punctuation = sun.translate(translator)

        print('模型名称：',punctuation)

        # 找到物体
        shade_obj = bpy.data.objects.get(mmi_object_name["MMI_AAAAA"])

        new_name = ''
        if shade_obj:
            while True:
                # 生成一个五位的随机字母字符串
                random_letters = ''.join(random.choices(string.ascii_letters, k=5))
                # 构建新名称
                new_name = punctuation + " 脸部定位 " + random_letters
                # 检查新名称是否已存在
                name_exists = False
                for u_obj in bpy.data.objects:
                    if u_obj.name == new_name:
                        name_exists = True
                        break
                # 如果名称不存在，退出循环
                if not name_exists:
                    break
            shade_obj.name = new_name # 重命名物体
            # 打印新名称
            print("新名称:", shade_obj)

        # 取消选择所有物体
        bpy.ops.object.select_all(action='DESELECT')

        # 确保处于Object模式
        if bpy.context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # 获取名称为 'MMI_AAAA' 的物体
        obj = bpy.data.objects.get(mmi_object_name["MMI_AAAA"])

        material_offsets =None
        thickness_rounded = None
        vertex = None
        Stroke_merging = None

        if self.Fuzzy == '1':
            # 检查物体是否存在
            if obj:
                # 检查物体是否是网格类型
                if obj.type == 'MESH':
                    # 检查物体是否有修改器
                    if obj.modifiers:
                        # 遍历物体的所有修改器
                        for modifis in obj.modifiers:
                            # 检查修改器是否具有 material_offset 属性
                            if hasattr(modifis, 'material_offset'):
                                # 打印修改器的 name 和 material_offset 属性值
                                material_offsets = modifis.material_offset
                                print(f"修改器 '{modifis.name}' 的 material_offset 属性值为: {material_offsets}")

                                thickness_rounded = round(modifis.thickness, 2)
                                print(f"物体 '{obj.name}' 的 Solidify 修改器的厚度属性值为: {thickness_rounded}")

                                vertex = modifis.vertex_group
                                print(f"物体 '{obj.name}' 的 Solidify 修改器的vertex_group属性值为: {vertex}")

            else:
                print(f"物体 '{mmi_object_name['MMI_AAAA']}' 不存在。")
        elif self.Fuzzy == '0':
            # 检查物体是否存在
            if obj:
                # 检查物体是否是网格类型
                if obj.type == 'MESH':
                    # 检查物体是否有修改器
                    if obj.modifiers:
                        # 遍历物体的所有修改器
                        for modifis in obj.modifiers:
                            # 检查修改器是不是几何节点
                            if modifis.type == 'NODES':
                                # 通过接口索引设置参数
                                inputs = modifis.node_group.interface.items_tree
                                # 获取材质偏移
                                material_offsets = modifis[inputs['材质偏移'].identifier]
                                print(f"修改器 '{modifis.name}' 的材质偏移值为: {material_offsets}")
                                # 获取厚度
                                thickness_rounded = modifis[inputs['描边厚度'].identifier]
                                print(f"修改器 '{modifis.name}' 的厚度属性值为: {thickness_rounded}")
                                # 获取翻转面
                                vertex = modifis[inputs['翻转面'].identifier]
                                print(f"修改器 '{modifis.name}' 的翻转面属性值为: {vertex}")
                                # 描边合并
                                Stroke_merging = modifis[inputs['描边合并'].identifier]
                                print(f"修改器 '{modifis.name}' 的描边合并属性值为: {Stroke_merging}")
            else:
                print(f"物体 '{mmi_object_name['MMI_AAAA']}' 不存在。")

# ----------------------------------------------------------------------------------------------------------------------
        if self.Legacy_face_positioning :
            # 物体的名称列表
            object_names = (tyu, bpy.context.view_layer.objects.active.name)
            print('物体的名称列表', object_names)
            # 遍历场景中的所有物体
            for obj in bpy.data.objects:
                # 如果物体的名称在列表中
                if obj.name in object_names:
                    # 选择这个物体
                    obj.select_set(True)
                    # 设为活动对象
                    if obj.name == tyu:
                        bpy.context.view_layer.objects.active = obj

            # 确保处于姿势模式
            if bpy.context.active_object.mode != 'POSE':
                bpy.ops.object.mode_set(mode='POSE')

            # 获取骨骼对象
            armature_obj = bpy.data.objects[tyu]

            # 确保骨骼对象是选中的
            bpy.context.view_layer.objects.active = armature_obj

            # 获取骨骼中的"頭"骨骼部位（bone）
            bone_name = "頭"  # 这里假设骨骼部位名称是"頭"
            bone = armature_obj.pose.bones.get(bone_name)

            # 计算骨骼部位的世界空间位置坐标
            world_head_position = armature_obj.matrix_world @ bone.head

            # 打印坐标
            print(f"骨骼部位 {bone_name} 的世界空间位置坐标是:", world_head_position)

            # 根据名字选择物体
            obj = bpy.data.objects.get(shade_obj.name)
            if obj is not None:
                if obj.name not in bpy.context.view_layer.objects:
                    bpy.context.scene.collection.objects.link(obj)
                obj.select_set(True)
                # 设置为活动物体
                bpy.context.view_layer.objects.active = obj
                print(f"物体 '{obj.name}' 已被选择并设置为活动物体。")

            # 获取想要移动的物体
            object_to_move = bpy.data.objects.get(shade_obj.name)

            # 将物体移动到骨骼部位“頭”的世界空间位置坐标
            object_to_move.location = world_head_position

            # 打印确认信息
            print(f"物体 {object_to_move.name} 已经移动到位置 {object_to_move.location}")

            # 旋转值校正
            def add_copy_rotation_constraint(object_name, subtarget, name, mix_mode, influence):
                bpy.ops.object.constraint_add(type='COPY_ROTATION')
                constraint = bpy.context.object.constraints[-1]
                constraint.name = name
                bpy.context.object.constraints[name].target = bpy.data.objects[object_name]
                bpy.context.object.constraints[name].subtarget = subtarget
                bpy.context.object.constraints[name].mix_mode = mix_mode
                bpy.context.object.constraints[name].target_space = 'LOCAL_OWNER_ORIENT'
                bpy.context.object.constraints[name].euler_order = 'AUTO'
                bpy.context.object.constraints[name].owner_space = 'WORLD'
                bpy.context.object.constraints[name].influence = influence

            def check_and_add_constraint(object_name, bone_name, constraint_name, mix_mode, influence):
                obj = bpy.data.objects.get(object_name)
                if obj and obj.type == 'ARMATURE':
                    if obj.pose.bones.get(bone_name):
                        add_copy_rotation_constraint(object_name, bone_name, constraint_name, mix_mode, influence)
                    else:
                        print(f"物体没有找到 '{bone_name}' 的骨骼！")
                else:
                    print(f"找不到名称为 {object_name} 的物体，或者是非骨骼物体！")

            # 初始的旋转值校正约束添加
            add_copy_rotation_constraint(tyu, "頭", "旋转值校正", 'REPLACE', 1)
            add_copy_rotation_constraint(tyu, "全ての親", "旋转值校正 - 全ての親", 'ADD', 1)
            add_copy_rotation_constraint(tyu, "センター", "旋转值校正 - センター", 'ADD', 1)

            # 针对不同骨骼的检查和约束添加
            check_and_add_constraint(tyu, "センター2", "旋转值校正 - センター2", 'ADD', 1)
            check_and_add_constraint(tyu, "首", "旋转值校正 - 首", 'ADD', 1)
            check_and_add_constraint(tyu, "上半身", "旋转值校正 - 上半身", 'ADD', 1)
            check_and_add_constraint(tyu, "上半身2", "旋转值校正 - 上半身2", 'ADD', 1)
            check_and_add_constraint(tyu, "上半身3", "旋转值校正 - 上半身3", 'ADD', 1)
            check_and_add_constraint(tyu, "グルーブ", "旋转值校正 - グルーブ", 'ADD', 1)
            check_and_add_constraint(tyu, "グルーブ2", "旋转值校正 - グルーブ2", 'ADD', 1)

            # 物体的名字
            object_name = tyu
            # 根据名字选择物体
            obj = bpy.data.objects.get(object_name)
            if obj is not None:
                obj.select_set(True)
                # 设置为活动物体
                bpy.context.view_layer.objects.active = obj

            # 姿势模式
            bpy.ops.object.mode_set(mode='POSE')
            # 选择骨骼'頭'
            bone_to_select = bpy.context.object.data.bones.get('頭')

            if bone_to_select is not None:
                bone_to_select.select = True
                bone_to_select.select_head = True
                bone_to_select.select_tail = True
                bpy.context.object.data.bones.active = bpy.context.object.data.bones['頭']
                # 设置'MMI_AAAAA'为'頭'的子级
                bpy.ops.object.parent_set(type='BONE', keep_transform=False)

                # 退出姿势模式
                bpy.ops.object.mode_set(mode='OBJECT')

                # 遍历所有的物体，并取消选择
                for obj in bpy.context.view_layer.objects:
                    obj.select_set(False)
# ----------------------------------------------------------------------------------------------------------------------
        else:
            # 根据名字选择物体
            obj = bpy.data.objects.get(shade_obj.name)
            if obj is not None:
                if obj.name not in bpy.context.view_layer.objects:
                    bpy.context.scene.collection.objects.link(obj)
                obj.select_set(True)
                # 设置为活动物体
                bpy.context.view_layer.objects.active = obj
                print(f"物体 '{obj.name}' 已被选择并设置为活动物体。")

            # 获取目标物体
            obj = bpy.context.active_object

            subtarget_name = None

            if obj:
                # 遍历所有约束，筛选类型为 CHILD_OF 的约束
                child_of_constraints = [c for c in obj.constraints if c.type == 'CHILD_OF']

                if child_of_constraints:
                    for constraint in child_of_constraints:
                        # 获取父级物体和 subtarget（如果有）
                        parent_obj = constraint.target
                        subtarget_name = constraint.subtarget  # 通常是骨骼名称（如果父级是骨骼）

                        print(f"子级约束 '{constraint.name}' 的父级物体: {parent_obj.name if parent_obj else '无'}")
                        print(f"子级约束的 subtarget: {subtarget_name if subtarget_name else '无'}")
                else:
                    print(f"物体'{obj.name}'没有子级约束")

                # 清空所有约束
                obj.constraints.clear()
                print(f"已删除物体 {obj.name} 的所有约束")

            else:
                print("未找到物体")

            # 重命名
            if self.Position_the_bones: # 字符串""表示False
                subtarget_name = self.Position_the_bones
                print('定位骨骼：',self.Position_the_bones)

            # 获取当前激活的物体
            active_obj = bpy.context.active_object

            # 获取要作为父级的物体
            parent_obj = bpy.data.objects.get(tyu)

            if active_obj and parent_obj:
                # 添加子级约束
                active_obj.constraints.new(type='CHILD_OF')
                # 获取刚刚添加的约束
                last_constraint = active_obj.constraints[-1]
                # 设置约束
                last_constraint.name = '脸部定位-子级'
                bpy.context.object.constraints["脸部定位-子级"].target = parent_obj
                bpy.context.object.constraints["脸部定位-子级"].subtarget = subtarget_name
                bpy.ops.constraint.childof_set_inverse(constraint="脸部定位-子级", owner='OBJECT')
                bpy.ops.constraint.childof_clear_inverse(constraint="脸部定位-子级", owner='OBJECT')

                print(f"已为 {active_obj.name} 添加子级约束，父级为 {parent_obj.name}")
            else:
                print("未找到激活物体或父级物体")

        # 恢复隐藏状态
        tyus.hide_set(hidden_state)

        # 选择两个物体
        object_names = [mmi_object_name["MMI_AAAA"], active_object.name]

        # 遍历这两个物体名称
        for object_name in object_names:
            # 尝试获取场景中的物体
            obj = bpy.data.objects.get(object_name)
            # 如果物体存在，选择它
            if obj is not None:
                obj.select_set(True)

        # 设置列表中的第一个物体为活动物体
        if object_names:
            bpy.context.view_layer.objects.active = bpy.data.objects.get(object_names[0])


        # 核心代码
        if self.Fuzzy == '1':
            if mmi.Copy_object_data:
                bpy.ops.object.make_links_data(type='OBDATA')
            else:
                bpy.ops.object.make_links_data(type='MATERIAL')
                if vertex:
                    bpy.ops.object.data_transfer(data_type='VGROUP_WEIGHTS', layers_select_src=vertex, layers_select_dst='NAME', mix_mode='REPLACE')
        elif self.Fuzzy == '0':
            # 模糊匹配材质
            a_obj_list = []
            b_obj_list = []
            b_obj_edge_list = []

            a_obj = active_object

            b_obj = bpy.data.objects.get(object_names[0])

            for a_materials in active_object.data.materials:
                a_obj_list.append(a_materials.name)

            for b_materials in b_obj.data.materials:
                if not 'mmd_edge' in b_materials.name:
                    if not 'mmi-edge|' in b_materials.name:
                        b_obj_list.append(b_materials.name)

            for b_obj_edge_materials in b_obj.data.materials:
                if b_obj_edge_materials and b_obj_edge_materials.name.startswith('mmi-edge|'):
                    b_obj_edge_list.append(b_obj_edge_materials.name)

            print(a_obj_list)
            print(b_obj_list)
            print(b_obj_edge_list)

            def get_similarity(a, b, edge = False):
                u = {}
                if edge:
                    # 遍历两个列表，计算相似度
                    for i in a:
                        i1 = i.split('.', 1)[0]
                        for j in b:
                            j1 = j.split('.', 1)[0]
                            # 去掉前缀
                            j1 = j1.replace('mmi-edge|', '')
                            matches = SequenceMatcher(None, i1, j1).ratio()
                            if matches > 0.85:
                                print(f"{i} 和 {j} 的相似度为：{matches}")
                                u[i] = j
                else:
                    # 遍历两个列表，计算相似度
                    for i in a:
                        i1 = i.split('.', 1)[0]
                        for j in b:
                            j1 = j.split('.', 1)[0]
                            matches = SequenceMatcher(None, i1, j1).ratio()
                            if matches > 0.85:
                                print(f"{i} 和 {j} 的相似度为：{matches}")
                                u[i] = j
                return u

            S_dictionary = get_similarity(a_obj_list, b_obj_list)
            edge_dictionary = get_similarity(a_obj_list, b_obj_edge_list, edge=True)

            for key, value in S_dictionary.items():
                print(f"{key} 映射到 {value}")

                # 更换材质
                for slot in a_obj.material_slots:
                    if slot.material.name == key:
                        slot.material = bpy.data.materials.get(value)

            for key, value in edge_dictionary.items():
                print(f"{key} 映射到 {value}")

                for material in b_obj.data.materials:
                    if material.name == value:
                        a_obj.data.materials.append(material)


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

        # 定义一个列表
        object_names = [mmi_object_name["MMI_AAAA"], mmi_object_name["MMI_AAA"], mmi_object_name["MMI_AA"]]
        # 遍历物体名称列表，调用delete_object函数删除物体
        for object_name in object_names:
            delete_object(object_name)

        # 遍历所有的物体，并选择它们
        for obj in bpy.context.view_layer.objects:
            obj.select_set(True)
        # 遍历所有当前选中的物体
        for obj in bpy.context.selected_objects:
            # 检查物体是否为Light类型，且光源类型为Sun
            if obj.type == 'LIGHT' and obj.data.type == 'SUN':
                # 确保该物体被选中
                obj.select_set(True)
                # 激活该物体，使其成为活动物体
                bpy.context.view_layer.objects.active = obj

        def rename_object_using_selected_object_name(source_obj_name, target_obj):
            # 获取当前选中的物体的名称
            source_obj = next((o for o in bpy.data.objects if o.name == source_obj_name), None)
            if source_obj:
                # 设置目标物体的名称为选中物体的名称
                target_obj.name = source_obj.name

        def rename_collection_to_selected_object_name(collection_name):
            # 获取当前选中的物体
            selected_object = bpy.context.view_layer.objects.active
            if selected_object is None:
                print("当前未选择任何对象。")
                return

            # 获取指定集合
            collection = bpy.data.collections.get(collection_name)
            if collection is None:
                print(f"集合 '{collection_name}' 未找到。")
                return

            # 获取物体名称
            object_name = Model

            # 从场景中获取这个物体
            object = bpy.data.objects.get(object_name)
            # 计算物体的世界空间位置坐标
            world_position = object.matrix_world @ mathutils.Vector((0, 0, 0))

            # 输出世界空间位置坐标
            print(f"物体 {object_name} 的世界空间位置坐标是: {world_position.x:.4f}, {world_position.y:.4f}, {world_position.z:.4f}")
            # 目标位置坐标，增加Z轴2米
            target_location = (world_position.x, world_position.y, world_position.z + 2.0)

            # 日光灯名称
            lamp_name = sun

            # 获取场景
            scene = bpy.context.scene

            # 查找并移动日光灯
            lamp_obj = scene.objects.get(lamp_name)
            if lamp_obj and lamp_obj.type == 'LIGHT' and lamp_obj.data.type == 'SUN':
                # 设置位置
                lamp_obj.location = target_location
                print(f"日光灯 '{lamp_name}' 已移动到世界坐标: {target_location}")
            else:
                print(f"场景中未找到名为 '{lamp_name}' 的日光灯。")

            new1_name = selected_object.name
            collection.name = new1_name
            print(f"集合 '{collection_name}' 已重命名为 '{new1_name}'。")


        # 调用函数，将集合【MMD预设】的名称重命名为当前选中物体的名称
        rename_collection_to_selected_object_name("【MMD预设】")
        bpy.context.view_layer.objects.active = bpy.data.objects.get(active_object.name)

        # 获取当前上下文中的活动对象
        obj = active_object

        if self.Fuzzy == '1':
            # 检查对象是否存在
            if obj:
                # 检查对象是否已经有名为"自动描边"的修改器
                if "自动描边" not in obj.modifiers:
                    # 如果没有，添加一个Solidify修改器
                    bpy.ops.object.modifier_add(type='SOLIDIFY')
                    # 获取最后一个添加的修改器
                    modifier = obj.modifiers[-1]
                    # 重命名修改器
                    modifier.name = "自动描边"

            # 设置修改器的属性，例如厚度等
            if thickness_rounded:
                thickness_float = float(thickness_rounded)
                obj.modifiers["自动描边"].thickness = thickness_float
            if vertex:
                obj.modifiers["自动描边"].vertex_group = vertex
            obj.modifiers["自动描边"].offset = 1
            obj.modifiers["自动描边"].use_rim = False
            obj.modifiers["自动描边"].use_flip_normals = True
            if material_offsets:
                material_offset_value = int(material_offsets)
                obj.modifiers["自动描边"].material_offset = material_offset_value
            # 遍历所有的物体，并取消选择
            for obj in bpy.context.view_layer.objects:
                obj.select_set(False)
        elif self.Fuzzy == '0':
            # 检查对象是否存在
            if obj:
                # 检查对象是否已经有名为"MMI-边缘预览"的几何节点修改器
                if "MMI-边缘预览" not in obj.modifiers:
                    # 如果没有，添加一个Geometry Nodes修改器
                    new_modifier = obj.modifiers.new(name="MMI-边缘预览", type='NODES')
                    new_modifier.node_group = bpy.data.node_groups["MMI-自动描边"]

            inputs = new_modifier.node_group.interface.items_tree

            new_modifier[inputs["描边厚度"].identifier] = thickness_rounded
            new_modifier[inputs["翻转面"].identifier] = vertex
            new_modifier[inputs["材质偏移"].identifier] = material_offsets
            new_modifier[inputs["描边合并"].identifier] = Stroke_merging

        bpy.ops.object.select_all(action='DESELECT') # 取消所有物体的选择

        if mmi.Post_processing_effect:
            bpy.ops.object.maeg_ops()

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        # 在文件选择器右侧面板绘制自定义选项
        layout = self.layout
        layout.prop(self, 'Legacy_face_positioning',text=i18n('Legacy face positioning'))
        if self.Legacy_face_positioning == False:
            layout.prop(self, 'Position_the_bones',text=i18n('Position the bones'),icon='OBJECT_DATAMODE')

        layout.label(text=i18n('Material matching:'))
        layout.prop(self, 'Fuzzy', text=i18n('Matching Pattern'), expand=True)

# 为选中模型设置眼透
class SetEyeThroughSettings(bpy.types.Operator):
    bl_idname = "mmi.set_eye_through_settings"
    bl_label = "Set eye transparency"
    bl_description = "Set eye transparency for the selected model"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object and not context.active_object.mmi.is_eye_obj

    def execute(self, context):

        global collection, layer

        active_obj = bpy.context.active_object

        # 当前py 文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建完整路径
        filepath = os.path.join(current_dir, "bhp.blend")

        def Additional_actions(A, B):
            collection_name = A
            directory = B

            with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
                if B == 'Collection':
                    if collection_name in data_from.collections:
                        data_to.collections = [collection_name]
                elif B == 'NodeTree':
                    if collection_name in data_from.node_groups:
                        data_to.node_groups = [collection_name]

        # 检查当前场景是否存在名为 "MMI-眼透" 的几何节点组
        if "MMI-眼透" not in bpy.data.node_groups:
            Additional_actions("MMI-眼透", "NodeTree")

        # 检查当前场景是否有集合名称包含 "MMI眼透"
        has_mmi = any("MMI眼透" in col.name for col in bpy.context.scene.collection.children)

        if not has_mmi:
            # 新建集合
            collection = bpy.data.collections.new("MMI眼透")
            # 链接到当前场景的根集合下
            bpy.context.scene.collection.children.link(collection)
        else:
            # 如果集合已存在，直接使用
            for col in bpy.context.scene.collection.children:
                if  "MMI眼透" in col.name:
                    collection = col
                    break  # 找到即停

        coll2 = None
        coll2_new_bool = True

        for col in collection.children:

            if  f"MMI眼透-{active_obj.name}" in col.name:
                coll2 = col
                coll2_new_bool = False
                break  # 找到即停

        if coll2_new_bool:
            # 新建集合
            new_collection = bpy.data.collections.new(f"MMI眼透-{active_obj.name}")
            # 链接到MMI眼透集合下
            collection.children.link(new_collection)
            coll2 = new_collection

        eye_through_list = active_obj.mmi_eye_through_material

        for ml in eye_through_list:
            if ml.material:

                boll = True
                new_obj = None

                for objs in coll2.objects:
                    if objs.name in f"MMI_眼透-{ml.material.name}":
                        boll = False
                        new_obj = objs
                        break

                if boll:
                    # 新建MESH对象
                    mesh_data = bpy.data.meshes.new(name=f"MMI_眼透-{ml.material.name}")
                    new_obj = bpy.data.objects.new(name=f"MMI_眼透-{ml.material.name}", object_data=mesh_data)
                    # 链接到集合
                    coll2.objects.link(new_obj)

                if new_obj:
                    # 检查对象是否已经有名为"MMI-设置眼透"的几何节点修改器
                    if "MMI-设置眼透" not in new_obj.modifiers:
                        # 如果没有，添加一个Geometry Nodes修改器
                        new_modifier = new_obj.modifiers.new(name="MMI-设置眼透", type='NODES')
                        new_modifier.node_group = bpy.data.node_groups["MMI-眼透"]
                        inputs = new_modifier.node_group.interface.items_tree

                        new_modifier[inputs["Object"].identifier] = active_obj
                        new_modifier[inputs["Material"].identifier] = ml.material

                        new_obj.mmi.is_eye_obj = True

        # 检查当前场景是否存在名为 "MMI-眼透" 的视图层
        if "MMI-眼透" not in bpy.context.scene.view_layers:
            layer = bpy.context.scene.view_layers.new("MMI-眼透")
        else:
            layer = bpy.context.scene.view_layers["MMI-眼透"]

        for col in layer.layer_collection.children:
            if col.name != "MMI眼透":
                col.exclude = True

        for obj in bpy.context.view_layer.layer_collection.children:
            if obj.name == "MMI眼透":
                obj.exclude = True
                break

        if "MMI_EYE_X" not in layer.aovs:
            new_aov = layer.aovs.add()
            new_aov.name = "MMI_EYE_X"
        else:
            new_aov = layer.aovs["MMI_EYE_X"]

        new_aov.type = "COLOR"

        # 获取材质槽
        material_slots = active_obj.material_slots

        for ml in eye_through_list:
            if ml.material:
                for slot in material_slots:
                    if slot.material == ml.material:
                        # 获取节点树
                        node_tree = slot.material.node_tree
                        # 遍历节点树
                        for node in node_tree.nodes:
                            if node.type == 'OUTPUT_MATERIAL':
                                # 获取上一个节点
                                input1 = node.inputs.get('Surface')
                                if input1:
                                    # 顺着这个节点的输入端口，找到连接的节点
                                    connected_nodes = [link.from_node for link in input1.links] # 获取所有连接的节点 一条线（link）有两个端点：from_node：线从哪里来（起始节点）to_node：线到哪里去（目标节点）

                                    # 过滤出连接到输出的节点
                                    for connected_node in connected_nodes:
                                        if connected_node:

                                            # 检查当前节点树是否存在"MMI_{ml.material.name}_AOV"节点
                                            if f"MMI_{ml.material.name}_AOV" not in node_tree.nodes:

                                                # 新建AOV节点
                                                new_aov_node = node_tree.nodes.new(type='ShaderNodeOutputAOV')
                                                new_aov_node.name = f"MMI_{ml.material.name}_AOV"
                                                new_aov_node.location = (node.location.x, node.location.y+150)
                                                new_aov_node.aov_name = "MMI_EYE_X"
                                            else:
                                                new_aov_node = node_tree.nodes.get(f"MMI_{ml.material.name}_AOV")

                                            if new_aov_node:
                                                # 连接AOV节点到输出节点
                                                node_tree.links.new(new_aov_node.inputs[0], connected_node.outputs[0])

                                                if ml.eye_boolean:
                                                    # 删除AOV节点
                                                    node_tree.nodes.remove(new_aov_node)

                                            break
                            break

        # 1. 先提取出 eye_through_list 中的材质本体（Material 对象）
        eye_materials = {ml.material for ml in eye_through_list}  # 用集合，查找更快

        # 2. 收集要删除的
        to_remove = []
        ml_aov_remove = []

        for obj in coll2.objects:
            should_keep = False
            mat = None

            if obj.modifiers:
                for mod in obj.modifiers:
                    if mod.type == 'NODES' and mod.node_group:
                        # 获取 "Material" 输入接口的值
                        input_id = mod.node_group.interface.items_tree["Material"].identifier
                        mat = mod[input_id]

                        # 如果材质在保留列表中，标记为保留
                        if mat in eye_materials:
                            should_keep = True
                            break  # 只要找到一个匹配的修改器，就保留该物体

            if not should_keep:
                to_remove.append(obj)
                ml_aov_remove.append(mat)

        # 3. 删除
        for obj in to_remove:
            bpy.data.objects.remove(obj, do_unlink=True)

        # 4. 删除AOV节点
        for mat in ml_aov_remove:
            if mat:
                mat.node_tree.nodes.remove(mat.node_tree.nodes.get(f"MMI_{mat.name}_AOV"))

        return {'FINISHED'}