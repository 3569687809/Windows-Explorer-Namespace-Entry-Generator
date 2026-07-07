# -*- coding: utf-8 -*-

"""
GUID管理模块

负责:

1. 生成Windows CLSID
2. 扫描已有REG文件
3. 防止GUID重复

安全原则:

- 不修改注册表
- 不创建文件
- 不执行系统命令
"""


import os
import re
import uuid



# =====================================================
# 常量
# =====================================================


GUID_PATTERN = (
    r"\{"
    r"[0-9A-Fa-f]{8}-"
    r"[0-9A-Fa-f]{4}-"
    r"[0-9A-Fa-f]{4}-"
    r"[0-9A-Fa-f]{4}-"
    r"[0-9A-Fa-f]{12}"
    r"\}"
)





# =====================================================
# GUID格式检查
# =====================================================


def validate_guid(guid):

    """
    检查GUID是否符合Windows CLSID格式
    """

    if not guid:

        return False



    return bool(
        re.match(
            GUID_PATTERN,
            guid
        )
    )





# =====================================================
# 扫描REG文件
# =====================================================


def scan_existing_guids(folder):

    """
    扫描目录中的所有REG文件

    返回:
    set()

    """



    result=set()



    # 目录不存在直接返回

    if not os.path.exists(folder):

        return result



    if not os.path.isdir(folder):

        return result




    try:

        files=os.listdir(
            folder
        )


    except Exception:

        return result




    for filename in files:


        # 只处理REG

        if not filename.lower().endswith(
            ".reg"
        ):

            continue



        filepath=os.path.join(
            folder,
            filename
        )



        try:


            # 优先UTF-16
            try:

                with open(
                    filepath,
                    "r",
                    encoding="utf-16"
                ) as f:

                    content=f.read()



            except UnicodeError:


                with open(
                    filepath,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    content=f.read()





            matches=re.findall(
                GUID_PATTERN,
                content
            )



            for guid in matches:


                guid=guid.upper()



                if validate_guid(
                    guid
                ):

                    result.add(
                        guid
                    )



        except Exception:


            # 单个文件损坏不影响整体

            continue



    return result





# =====================================================
# 生成GUID
# =====================================================


def generate_guid(check_folder):

    """
    生成唯一GUID

    无限循环直到没有重复
    """



    existing = scan_existing_guids(
        check_folder
    )



    while True:


        new_guid = (
            "{"
            +
            str(
                uuid.uuid4()
            ).upper()
            +
            "}"
        )



        if not validate_guid(
            new_guid
        ):

            continue



        if new_guid not in existing:

            return new_guid





# =====================================================
# 检查指定GUID是否存在
# =====================================================


def guid_exists(
        guid,
        folder
):

    """
    外部调用检查
    """



    if not validate_guid(
        guid
    ):

        return True



    return (
        guid.upper()
        in
        scan_existing_guids(
            folder
        )
    )