# -*- coding: utf-8 -*-

"""
输入安全验证模块

负责:
1. 名称检查
2. 路径检查
3. REG安全字符检查

本模块:
- 不生成文件
- 不修改注册表
- 不执行任何系统操作

所有返回格式统一:

(True, "")
(False, "错误原因")
"""


import os
import re



# =====================================================
# 常量
# =====================================================


# 显示名称最大长度

MAX_NAME_LENGTH = 80



# 路径最大长度

MAX_PATH_LENGTH = 260



# REG字符串禁止字符

REG_DANGEROUS_CHARS = [

    "\r",
    "\n",
    "\x00"

]



# Windows文件名禁止字符

WINDOWS_INVALID_NAME_CHARS = [

    "\\",
    "/",
    ":",
    "*",
    "?",
    '"',
    "<",
    ">",
    "|"

]





# =====================================================
# 通用字符串检查
# =====================================================


def check_empty(value, name):

    """
    检查空输入
    """

    if value is None:

        return False, (
            f"{name}不能为空"
        )


    if not str(value).strip():

        return False, (
            f"{name}不能为空"
        )


    return True, ""





# =====================================================
# 名称验证
# =====================================================


def validate_name(name):

    """
    检查显示名称

    示例:

    Minecraft服务器

    """



    ok,msg = check_empty(
        name,
        "名称"
    )


    if not ok:

        return False,msg



    name = str(name).strip()



    if len(name) > MAX_NAME_LENGTH:

        return False,(
            f"名称长度超过限制\n"
            f"最大 {MAX_NAME_LENGTH} 字符"
        )



    for char in WINDOWS_INVALID_NAME_CHARS:


        if char in name:

            return False,(
                "名称包含Windows非法字符:\n"
                +
                char
            )



    for char in REG_DANGEROUS_CHARS:


        if char in name:

            return False,(
                "名称包含危险控制字符"
            )



    return True,""





# =====================================================
# 路径验证
# =====================================================


def validate_path(path):

    """
    检查目标文件夹路径

    示例:

    D:\\MC_Server

    """



    ok,msg = check_empty(
        path,
        "路径"
    )


    if not ok:

        return False,msg



    path = str(path).strip()

    # 统一Windows路径格式
    path = path.replace(
        "/",
        "\\"
    )


    if len(path) > MAX_PATH_LENGTH:

        return False,(
            "路径长度超过Windows限制"
        )



    # Windows盘符检查

    if not re.match(
        r"^[A-Za-z]:\\",
        path
    ):


        return False,(
            "路径格式错误\n\n"
            "正确示例:\n"
            "D:\\MC_Server"
        )



    for char in REG_DANGEROUS_CHARS:


        if char in path:

            return False,(
                "路径包含危险控制字符"
            )



    # 检查非法路径字符

    for char in [
        '"',
        "<",
        ">",
        "|"
    ]:


        if char in path:

            return False,(
                f"路径包含非法字符: {char}"
            )



    return True,""





# =====================================================
# REG注入检查
# =====================================================


def validate_reg_string(value, name="字符串"):

    """
    防止写入REG时注入其他键值

    """



    if value is None:

        return False,(
            f"{name}为空"
        )



    value=str(value)



    dangerous=[

        "\n",
        "\r",
        "\x00"

    ]



    for char in dangerous:


        if char in value:

            return False,(
                f"{name}包含危险字符"
            )



    return True,""





# =====================================================
# GUID格式检查
# =====================================================


def validate_guid(guid):

    """
    检查GUID格式

    示例:

    {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}

    """



    if not guid:

        return False,"GUID为空"



    pattern = (
        r"^\{"
        r"[0-9A-Fa-f]{8}-"
        r"[0-9A-Fa-f]{4}-"
        r"[0-9A-Fa-f]{4}-"
        r"[0-9A-Fa-f]{4}-"
        r"[0-9A-Fa-f]{12}"
        r"\}$"
    )



    if not re.match(
        pattern,
        guid
    ):

        return False,(
            "GUID格式错误"
        )


    return True,""





# =====================================================
# 文件路径安全检查
# =====================================================


def validate_output_file(path):

    """
    检查生成REG文件位置

    """



    ok,msg = check_empty(
        path,
        "输出路径"
    )


    if not ok:

        return False,msg



    folder=os.path.dirname(
        os.path.abspath(path)
    )



    if not os.path.exists(folder):

        return False,(
            "输出目录不存在"
        )



    return True,""