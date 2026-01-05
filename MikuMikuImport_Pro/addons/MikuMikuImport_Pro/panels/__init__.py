import re

# 版本比较
def compare_version(version1, version2):
    parts1 = []
    parts2 = []
    for part in re.split('[.-]', version1):
        try:
            num = int(part)
        except ValueError:
            num = 0
        parts1.append(num)
    for part in re.split('[.-]', version2):
        try:
            num = int(part)
        except ValueError:
            num = 0
        parts2.append(num)
    min_length = min(len(parts1), len(parts2))
    for i in range(min_length):
        if parts1[i] < parts2[i]:
            return True
        elif parts1[i] > parts2[i]:
            return False
    return len(parts1) < len(parts2)
