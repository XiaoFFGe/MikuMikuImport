import os


# 本地文件搜索引擎
def search_files(keywords, directory):
    # 用于存储搜索结果的列表
    results = []
    # 遍历指定目录及其子目录下的所有文件和文件夹
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 获取文件的完整路径
            file_path = os.path.join(root, file)
            match = True
            # 对每个关键词进行检查
            for keyword in keywords:
                # 如果关键词不在文件名中，则标记为不匹配
                if keyword not in file:
                    match = False
                    break
            # 如果所有关键词都在文件名中且文件名不包含'EffectHair'、'EffectBody'，则将文件路径添加到结果列表
            if match and 'EffectHair' not in file:
                if match and 'EffectBody' not in file:
                    results.append(file_path)
    # 返回搜索结果列表
    return results

if __name__ == '__main__':
    # 获取用户输入的关键词，以空格分隔并转换为列表
    keywords = input("请输入关键词，多个关键词用空格分隔: ").split()
    # 在指定目录下搜索包含关键词的文件路径
    file_paths = search_files(keywords, r'D:\Backup\Documents\Characters\Furina\Default')
    # 输出搜索到的文件路径
    for path in file_paths:
        print(path)