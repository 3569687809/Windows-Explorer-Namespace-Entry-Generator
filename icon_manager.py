# -*- coding: utf-8 -*-

"""
图标管理模块

负责:

1. Windows系统图标生成
2. ICO文件验证

安全设计:

系统图标:
    固定路径
    用户只能输入编号

自定义图标:
    只允许ICO
    限制大小

本模块:
    不操作注册表
    不生成REG
"""


import os
import re





# =====================================================
# Windows系统图标固定模板
# =====================================================


SYSTEM_ICON_PREFIX = (
    r"%SystemRoot%\SystemResources\imageres.dll.mun,"
)



# ICO最大大小

MAX_ICON_SIZE = (
    1024 * 1024
)





# =====================================================
# 系统图标
# =====================================================


def build_system_icon(index):

    """
    根据编号生成系统图标路径

    输入:
        -184

    输出:
        %SystemRoot%\SystemResources\imageres.dll.mun,-184

    """



    if index is None:

        return False, (
            "图标编号不能为空"
        )



    index=str(index).strip()



    # 必须负数

    if not re.fullmatch(
        r"-\d+",
        index
    ):


        return False,(
            "系统图标编号错误\n\n"
            "格式:\n"
            "-184"
        )



    return True, (
        SYSTEM_ICON_PREFIX
        +
        index
    )





# =====================================================
# 系统图标最终格式检查
# =====================================================


def validate_system_icon(icon):

    """
    二次检查

    防止其他模块错误调用

    """



    pattern=(

        r"^%SystemRoot%\\SystemResources\\"
        r"imageres\.dll\.mun,-\d+$"

    )



    if not re.match(
        pattern,
        icon
    ):

        return False,(
            "系统图标格式非法"
        )



    return True,""





# =====================================================
# 自定义ICO检查
# =====================================================


def validate_custom_icon(path):

    """
    检查用户ICO文件

    """



    if not path:

        return False,(
            "图标路径为空"
        )



    path=os.path.abspath(
        path
    )



    if not os.path.exists(
        path
    ):

        return False,(
            "图标文件不存在"
        )



    if not os.path.isfile(
        path
    ):

        return False,(
            "路径不是文件"
        )



    ext=os.path.splitext(
        path
    )[1].lower()



    if ext != ".ico":

        return False,(
            "只允许ICO格式"
        )



    try:


        size=os.path.getsize(
            path
        )


    except Exception:


        return False,(
            "无法读取文件大小"
        )




    if size <=0:

        return False,(
            "图标文件为空"
        )



    if size > MAX_ICON_SIZE:

        return False,(
            "图标文件过大\n\n"
            "最大允许:\n"
            "1MB"
        )



    return True,path





# =====================================================
# 统一入口
# =====================================================


def validate_icon_source(
        mode,
        value
):

    """
    统一图标验证

    mode:

        system
        ico

    """



    if mode=="system":


        return build_system_icon(
            value
        )



    elif mode=="ico":


        return validate_custom_icon(
            value
        )



    else:


        return False,(
            "未知图标模式"
        )