# -*- coding: utf-8 -*-

"""
Windows 此电脑入口生成器

程序入口文件

负责:
1. 启动GUI
2. 捕获启动异常
3. 保存错误日志

注意:
本文件不直接操作注册表
本文件不生成REG
本文件不处理用户输入

所有功能由其他模块负责
"""


import os
import sys
import traceback
from datetime import datetime



# =====================================================
# 程序信息
# =====================================================

APP_NAME = "Windows 此电脑入口生成器"


LOG_FILE = "error.log"



# =====================================================
# 错误日志
# =====================================================

def write_error_log(error):

    """
    保存异常信息

    防止程序闪退后无法定位问题
    """

    try:

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:


            f.write(
                "\n"
                +
                "=" * 60
                +
                "\n"
            )


            f.write(
                datetime.now()
                .strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )


            f.write(
                "\n\n"
            )


            f.write(
                error
            )


            f.write(
                "\n"
            )


    except:

        # 日志写入失败时不能再次崩溃
        pass





# =====================================================
# 主启动函数
# =====================================================

def main():

    try:


        # 延迟导入
        # 防止模块错误导致无法捕获

        from gui import start_gui



        start_gui()



    except Exception:


        error = traceback.format_exc()


        write_error_log(
            error
        )


        # GUI模式下不能直接打印窗口关闭
        try:

            import tkinter.messagebox as box


            box.showerror(
                APP_NAME,
                (
                    "程序启动失败\n\n"
                    "错误已经保存到:\n"
                    +
                    os.path.abspath(
                        LOG_FILE
                    )
                )
            )


        except:


            print(error)





# =====================================================
# 程序入口
# =====================================================

if __name__ == "__main__":

    main()