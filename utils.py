# -*- coding: utf-8 -*-

"""
通用工具模块

负责:

1. 文件操作
2. 时间处理
3. 路径处理
4. 备份

本模块:

- 不操作注册表
- 不生成REG内容
- 不处理用户输入逻辑
"""


import os
import shutil
import re

from datetime import datetime





# =====================================================
# 时间
# =====================================================


def get_time_string():

    """
    返回安全时间字符串

    示例:

    2026-07-07_13-20-30

    """

    return datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )





# =====================================================
# 文件名清理
# =====================================================


def sanitize_filename(
        name
):

    """
    清理Windows非法文件名字符

    防止生成失败
    """



    invalid_chars=[

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



    for c in invalid_chars:

        name=name.replace(
            c,
            "_"
        )



    return name.strip()





# =====================================================
# 创建目录
# =====================================================


def ensure_directory(
        path
):

    """
    确保目录存在
    """



    if not os.path.exists(
        path
    ):


        os.makedirs(
            path,
            exist_ok=True
        )


    return path





# =====================================================
# 安全写文件
# =====================================================


def safe_write_text(
        path,
        content,
        encoding="utf-16"
):


    """
    安全写入文本

    """



    folder=os.path.dirname(
        os.path.abspath(path)
    )



    ensure_directory(
        folder
    )



    with open(
        path,
        "w",
        encoding=encoding
    ) as f:


        f.write(
            content
        )



    return path





# =====================================================
# 安全读取文件
# =====================================================


def safe_read_text(
        path
):


    """
    自动尝试读取文本

    """



    encodings=[

        "utf-16",
        "utf-8",
        "gbk"

    ]



    for enc in encodings:


        try:


            with open(
                path,
                "r",
                encoding=enc
            ) as f:


                return f.read()



        except:

            continue



    return None





# =====================================================
# 文件备份
# =====================================================


def backup_file(
        source,
        backup_folder
):


    """
    创建文件备份

    """



    if not os.path.exists(
        source
    ):

        return None



    ensure_directory(
        backup_folder
    )



    filename=os.path.basename(
        source
    )


    time=get_time_string()



    new_name=(

        time
        +
        "_"
        +
        filename

    )



    target=os.path.join(
        backup_folder,
        new_name
    )



    shutil.copy2(
        source,
        target
    )


    return target





# =====================================================
# 文件唯一名称
# =====================================================


def unique_filename(
        path
):


    """
    防止覆盖文件

    """



    if not os.path.exists(
        path
    ):

        return path



    base,ext=os.path.splitext(
        path
    )


    index=1



    while True:


        new=(

            base
            +
            "_"
            +
            str(index)
            +
            ext

        )



        if not os.path.exists(
            new
        ):

            return new



        index+=1





# =====================================================
# 文件大小检查
# =====================================================


def check_file_size(
        path,
        max_size
):


    """
    通用文件大小检查
    """



    if not os.path.exists(
        path
    ):

        return False



    if not os.path.isfile(
        path
    ):

        return False



    return (
        os.path.getsize(path)
        <=
        max_size
    )




# =====================================================
# 重启Windows资源管理器
# =====================================================

def restart_explorer():

    """
    重启Windows Explorer

    用于刷新:
    - 此电脑导航栏
    - CLSID命名空间入口
    - 文件资源管理器缓存

    """

    import subprocess
    import time


    try:

        # 关闭资源管理器

        subprocess.run(
            [
                "taskkill",
                "/f",
                "/im",
                "explorer.exe"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


        time.sleep(
            1
        )


        # 重新启动

        subprocess.Popen(
            [
                "explorer.exe"
            ]
        )


        return True,"资源管理器已重启"



    except Exception as e:


        return False,str(e)




# =====================================================
# 导入REG文件
# =====================================================

def import_reg_file(path):

    """
    导入.reg文件

    """

    import subprocess


    if not path.lower().endswith(
        ".reg"
    ):

        return False,"只能导入REG文件"


    if not os.path.isfile(
        path
    ):

        return False,"文件不存在"



    try:


        result=subprocess.run(

            [
                "reg",
                "import",
                path
            ],

            capture_output=True,

            text=True

        )


        if result.returncode != 0:


            return False,result.stderr



        return True,"REG导入成功"



    except Exception as e:


        return False,str(e)



# =====================================================
# 从REG文件读取GUID
# =====================================================

def extract_guid_from_reg(path):

    """
    从.reg文件中提取CLSID GUID
    """

    if not path.lower().endswith(".reg"):

        return False,"不是REG文件"


    try:

        with open(
            path,
            "r",
            encoding="utf-16"
        ) as f:

            content=f.read()


    except Exception as e:

        return False,str(e)



    match=re.search(

        r"CLSID\\\{([A-Fa-f0-9\-]{36})\}",

        content

    )


    if not match:

        return False,"未找到GUID"


    guid=match.group(1)


    return True,guid.upper()



# =====================================================
# 删除自定义入口
# =====================================================

def remove_namespace_guid(guid):


    import subprocess



    keys=[

        rf"HKCU\Software\Classes\CLSID\{{{guid}}}",


        rf"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{{{guid}}}",


        rf"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{{{guid}}}"

    ]



    result=[]


    for key in keys:


        p=subprocess.run(

            [
                "reg",
                "delete",
                key,
                "/f"
            ],

            capture_output=True,

            text=True

        )


        if p.returncode==0:

            result.append(
                "删除成功:"+key
            )


    return True,"\n".join(result)