# -*- coding: utf-8 -*-

"""
图标最终安全审查模块

作用:

在生成REG之前，对最终图标字符串进行最后检查。

安全目标:

1. 防止错误路径
2. 防止错误DLL
3. 防止格式污染
4. 防止REG注入
5. 防止模块调用错误


本模块:
- 不生成REG
- 不修改注册表
- 不读取用户配置
"""


import os
import re





# =====================================================
# 固定系统图标格式
# =====================================================


SYSTEM_ICON_PATTERN = (

    r"^%SystemRoot%\\SystemResources\\"
    r"imageres\.dll\.mun,-\d+$"

)





# =====================================================
# 危险字符
# =====================================================


DANGEROUS_CHARS = [

    "\r",
    "\n",
    "\x00",
    '"'

]





# =====================================================
# 通用字符串安全检查
# =====================================================


def check_dangerous_string(
        value
):

    """
    防止REG注入
    """



    if value is None:

        return False,(
            "字符串为空"
        )



    for char in DANGEROUS_CHARS:


        if char in value:


            return False,(
                "检测到危险字符"
            )



    return True,""





# =====================================================
# 系统图标最终检查
# =====================================================


def check_system_icon(
        icon
):

    """
    检查系统图标

    只允许:

    %SystemRoot%\SystemResources\imageres.dll.mun,-184

    """



    ok,msg = check_dangerous_string(
        icon
    )


    if not ok:

        return False,msg




    if not re.fullmatch(
        SYSTEM_ICON_PATTERN,
        icon
    ):


        return False,(
            "系统图标格式错误\n\n"
            "必须为:\n"
            "%SystemRoot%\\SystemResources\\"
            "imageres.dll.mun,-数字"
        )



    return True,""





# =====================================================
# ICO最终检查
# =====================================================


def check_ico_icon(
        icon
):

    """
    自定义ICO最终检查

    """



    ok,msg = check_dangerous_string(
        icon
    )


    if not ok:

        return False,msg




    if not icon.lower().endswith(
        ".ico"
    ):

        return False,(
            "不是ICO文件"
        )



    if not os.path.exists(
        icon
    ):

        return False,(
            "ICO文件不存在"
        )



    if not os.path.isfile(
        icon
    ):

        return False,(
            "ICO路径不是文件"
        )



    return True,""





# =====================================================
# 最终统一入口
# =====================================================


def final_icon_security_check(
        icon
):

    """
    REG生成前必须调用

    """



    if not icon:


        return False,(
            "图标为空"
        )




    icon=icon.strip()



    # 系统图标

    if icon.startswith(
        "%SystemRoot%"
    ):


        return check_system_icon(
            icon
        )



    # ICO

    if icon.lower().endswith(
        ".ico"
    ):


        return check_ico_icon(
            icon
        )



    return False,(
        "未知图标类型"
    )