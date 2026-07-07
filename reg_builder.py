# -*- coding: utf-8 -*-

"""
REG生成模块

职责:

1. 生成Windows注册表文件
2. 生成前最终安全检查
3. 保存.reg文件

安全原则:

- 不导入注册表
- 不执行reg.exe
- 不修改系统
- 只生成文本文件
"""


import os


from validator import (
    validate_name,
    validate_path,
    validate_guid,
    validate_reg_string
)


from icon_security import (
    final_icon_security_check
)


# =====================================================
# REG路径转义
# =====================================================

def escape_reg_path(path):

    """
    将Windows路径转换成REG格式

    输入:
        D:\下载

    输出:
        D:\\下载
    """


    # 去除首尾空格
    path = str(path).strip()


    # 统一斜杠
    path = path.replace(
        "/",
        "\\"
    )


    # REG文件需要双反斜杠
    path = path.replace(
        "\\",
        "\\\\"
    )


    return path




# =====================================================
# REG模板
# =====================================================


REG_TEMPLATE = r'''Windows Registry Editor Version 5.00


[HKEY_CURRENT_USER\Software\Classes\CLSID\{GUID}]
@="{NAME}"
"System.IsPinnedToNameSpaceTree"=dword:00000001


[HKEY_CURRENT_USER\Software\Classes\CLSID\{GUID}\DefaultIcon]
@="{ICON}"


[HKEY_CURRENT_USER\Software\Classes\CLSID\{GUID}\Instance]
"CLSID"="{0E5AAE11-A475-4C5B-AB00-C66DE400274E}"


[HKEY_CURRENT_USER\Software\Classes\CLSID\{GUID}\Instance\InitPropertyBag]
"TargetFolderPath"="{PATH}"


[HKEY_CURRENT_USER\Software\Classes\CLSID\{GUID}\ShellFolder]
"Attributes"=dword:f080004d


[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{GUID}]


'''





# =====================================================
# REG字符转义
# =====================================================


def escape_reg_string(value):

    """
    REG字符串转义

    防止:
    \
    "

    破坏格式
    """

    value=value.replace(
        "\\",
        "\\\\"
    )


    value=value.replace(
        '"',
        '\\"'
    )


    return value





# =====================================================
# 最终数据检查
# =====================================================


def validate_all(
        name,
        path,
        icon,
        guid
):


    checks=[


        validate_name(
            name
        ),


        validate_path(
            path
        ),


        validate_guid(
            guid
        ),


        validate_reg_string(
            name,
            "名称"
        ),


        validate_reg_string(
            path,
            "路径"
        ),


    ]



    for ok,msg in checks:


        if not ok:

            return False,msg




    # 最终图标检查

    ok,msg = final_icon_security_check(
        icon
    )


    if not ok:

        return False,msg



    return True,""



# =====================================================
# Windows路径转换为REG格式
# =====================================================

def escape_reg_path(path):

    """
    Windows路径转换

    输入:
        D:\下载

    输出:
        D:\\下载
    """


    # 转字符串
    path = str(path)


    # 去除首尾空格
    path = path.strip()


    # 统一路径分隔符
    path = path.replace(
        "/",
        "\\"
    )


    # REG需要双反斜杠
    path = path.replace(
        "\\",
        "\\\\"
    )


    return path




# =====================================================
# 生成REG文本
# =====================================================


def build_reg_content(
        name,
        path,
        icon,
        guid
):


    # =================================================
    # 数据总检查
    # =================================================

    ok,msg = validate_all(
        name,
        path,
        icon,
        guid
    )


    if not ok:


        raise ValueError(
            msg
        )



    # =================================================
    # 处理路径
    # =================================================

    path = escape_reg_path(
        path
    )



    # =================================================
    # 创建REG内容
    # =================================================

    content = REG_TEMPLATE



    # =================================================
    # GUID替换
    # =================================================

    content = content.replace(
        "{GUID}",
        guid
    )



    # =================================================
    # 名称替换
    # =================================================

    content = content.replace(
        "{NAME}",
        escape_reg_string(
            name
        )
    )



    # =================================================
    # 路径替换
    # =================================================

    content = content.replace(
        "{PATH}",
        path
    )



    # =================================================
    # 图标替换
    # =================================================

    content = content.replace(
        "{ICON}",
        escape_reg_string(
            icon
        )
    )



    return content





# =====================================================
# 防覆盖文件名
# =====================================================


def safe_output_path(path):


    if not os.path.exists(
        path
    ):

        return path



    base,ext=os.path.splitext(
        path
    )


    index=1


    while True:


        new_path=(
            base
            +
            "_"
            +
            str(index)
            +
            ext
        )


        if not os.path.exists(
            new_path
        ):

            return new_path



        index+=1





# =====================================================
# 保存REG文件
# =====================================================


def save_reg_file(
        output,
        content
):


    output=safe_output_path(
        output
    )



    try:


        with open(
            output,
            "w",
            encoding="utf-16"
        ) as f:

            f.write(
                content
            )


    except Exception as e:


        raise IOError(
            "REG写入失败:\n"
            +
            str(e)
        )



    return output