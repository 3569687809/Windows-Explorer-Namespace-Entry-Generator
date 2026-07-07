# -*- coding: utf-8 -*-

"""
GUI主界面

负责:
- 用户交互
- 调用其他模块

不直接处理:
- GUID算法
- REG模板
- 图标安全规则
"""


import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import sys
import os

# =================================================
# 窗口图标
# =================================================

def resource_path(relative_path):

    if hasattr(
        sys,
        "_MEIPASS"
    ):

        return os.path.join(
            sys._MEIPASS,
            relative_path
        )

    return os.path.join(
        os.path.abspath("."),
        relative_path
    )



def set_window_icon(window):

    icon_path = resource_path(
        os.path.join(
            "assets",
            "app.ico"
        )
    )


    if os.path.exists(icon_path):

        try:

            window.iconbitmap(
                icon_path
            )

        except Exception:

            pass

from validator import (
    validate_name,
    validate_path
)


from icon_manager import (
    validate_icon_source
)


from guid_manager import (
    generate_guid
)


from reg_builder import (
    build_reg_content,
    save_reg_file
)


from utils import (
    unique_filename,
    restart_explorer,
    import_reg_file,
    extract_guid_from_reg,
    remove_namespace_guid
)




root=None


log_box=None


name_entry=None
path_entry=None


icon_mode_var=None


icon_index_entry=None
custom_icon_entry=None





# =====================================================
# 日志
# =====================================================

def log(text):

    log_box.config(
        state="normal"
    )

    log_box.insert(
        tk.END,
        text+"\n"
    )

    log_box.see(
        tk.END
    )

    log_box.config(
        state="disabled"
    )



# =====================================================
# 选择ERG并删除对应GUID
# =====================================================
def remove_reg_entry():


    file=filedialog.askopenfilename(

        title="选择REG文件",

        filetypes=[

            (
                "注册表文件",
                "*.reg"
            )

        ]

    )


    if not file:

        return



    ok,guid=extract_guid_from_reg(
        file
    )


    if not ok:

        messagebox.showerror(
            "错误",
            guid
        )

        return



    confirm=messagebox.askyesno(

        "确认删除",

        f"发现GUID:\n\n{guid}\n\n是否删除?"

    )


    if not confirm:

        return



    ok,msg=remove_namespace_guid(
        guid
    )


    if ok:

        log(msg)


        messagebox.showinfo(
            "完成",
            "入口已删除"
        )


    else:

        messagebox.showerror(
            "失败",
            msg
        )



# =====================================================
# 浏览路径
# =====================================================

def browse_folder():


    path=filedialog.askdirectory()


    if path:

        path_entry.delete(
            0,
            tk.END
        )

        path_entry.insert(
            0,
            path
        )





# =====================================================
# 浏览ICO
# =====================================================

def change_icon_mode():

    mode = icon_mode_var.get()


    if mode == "system":

        # 启用系统编号
        icon_index_entry.config(
            state="normal"
        )


        # 禁用ICO路径
        custom_icon_entry.config(
            state="disabled"
        )


    elif mode == "ico":

        # 禁用系统编号
        icon_index_entry.config(
            state="disabled"
        )


        # 启用ICO路径
        custom_icon_entry.config(
            state="normal"
        )

def browse_icon():

    file=filedialog.askopenfilename(
        filetypes=[
            (
                "ICO图标",
                "*.ico"
            )
        ]
    )


    if file:

        custom_icon_entry.delete(
            0,
            tk.END
        )

        custom_icon_entry.insert(
            0,
            file
        )


        # 自动切换到自定义ICO模式
        icon_mode_var.set(
            "ico"
        )


        change_icon_mode()




# =====================================================
# 获取当前图标
# =====================================================

def get_icon():
    mode = icon_mode_var.get()

    if mode == "system":

        return validate_icon_source(
            "system",
            icon_index_entry.get()
        )


    elif mode == "ico":

        return validate_icon_source(
            "ico",
            custom_icon_entry.get()
        )


    else:

        return False, "未知图标模式"





# =====================================================
# 收集数据
# =====================================================

def collect_data():


    name=name_entry.get()

    path=path_entry.get()



    ok,msg=validate_name(
        name
    )


    if not ok:

        raise Exception(msg)



    ok,msg=validate_path(
        path
    )


    if not ok:

        raise Exception(msg)




    ok,icon=get_icon()


    if not ok:

        raise Exception(icon)



    guid=generate_guid(
        os.getcwd()
    )



    return (
        name,
        path,
        icon,
        guid
    )





# =====================================================
# 预览REG
# =====================================================

def preview_reg():


    try:

        name,path,icon,guid=collect_data()


        content=build_reg_content(
            name,
            path,
            icon,
            guid
        )



        win=tk.Toplevel(
            root
        )


        win.title(
            "REG预览"
        )


        win.geometry(
            "600x500"
        )


        box=tk.Text(
            win
        )


        box.pack(
            expand=True,
            fill="both"
        )


        box.insert(
            "1.0",
            content
        )


        box.config(
            state="disabled"
        )



    except Exception as e:


        messagebox.showerror(
            "错误",
            str(e)
        )



# =====================================================
# 选择reg文件
# =====================================================
def import_and_restart():


    file=filedialog.askopenfilename(

        title="选择REG文件",

        filetypes=[

            (
                "注册表文件",
                "*.reg"
            )

        ]

    )


    if not file:

        return



    ok,msg=import_reg_file(
        file
    )


    if not ok:


        messagebox.showerror(
            "导入失败",
            msg
        )

        return



    log(
        msg
    )



    restart=messagebox.askyesno(

        "导入完成",

        "是否立即重启资源管理器刷新?"

    )



    if restart:


        ok,msg=restart_explorer()


        if ok:

            log(msg)


        else:

            messagebox.showerror(
                "失败",
                msg
            )




# =====================================================
# 重启资源管理器
# =====================================================
def restart_explorer_gui():


    ok,msg = restart_explorer()


    if ok:

        log(
            msg
        )


        messagebox.showinfo(
            "完成",
            msg
        )


    else:

        log(
            "失败:"
            +
            msg
        )


        messagebox.showerror(
            "失败",
            msg
        )





# =====================================================
# 生成REG
# =====================================================

def generate_reg():


    try:


        name,path,icon,guid=collect_data()



        content=build_reg_content(
            name,
            path,
            icon,
            guid
        )



        folder=filedialog.askdirectory()



        if not folder:

            return



        filename=name+".reg"


        output=os.path.join(
            folder,
            filename
        )



        output=unique_filename(
            output
        )



        save_reg_file(
            output,
            content
        )



        log(
            "生成成功:"
            +
            output
        )


        messagebox.showinfo(
            "完成",
            output
        )



    except Exception as e:


        log(
            "错误:"
            +
            str(e)
        )


        messagebox.showerror(
            "生成失败",
            str(e)
        )

# =====================================================
# GUI启动
# =====================================================

def start_gui():

        global root
        global log_box

        global name_entry
        global path_entry

        global icon_mode_var
        global icon_index_entry
        global custom_icon_entry



        # =================================================
        # 图标模式切换
        # 系统图标 / 自定义ICO 二选一
        # =================================================

        def change_icon_mode():

            mode = icon_mode_var.get()

            if mode == "system":

                icon_index_entry.config(
                    state="normal"
                )

                custom_icon_entry.config(
                    state="disabled"
                )



            elif mode == "ico":

                icon_index_entry.config(
                    state="disabled"
                )

                custom_icon_entry.config(
                    state="normal"
                )

        # =================================================
        # 创建窗口
        # =================================================

        root = tk.Tk()

        set_window_icon(
            root
        )

        root.title(
            "Windows此电脑入口生成器"
        )

        root.geometry(
            "550x600"
        )

        # =================================================
        # 基础信息区域
        # =================================================

        info_frame = ttk.LabelFrame(
            root,
            text="基本信息"
        )

        info_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ttk.Label(
            info_frame,
            text="名称"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        name_entry = ttk.Entry(
            info_frame,
            width=50
        )

        name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        name_entry.insert(
            0,
            "Minecraft服务器"
        )

        # =================================================
        # 目标路径区域
        # =================================================

        path_frame = ttk.LabelFrame(
            root,
            text="目标路径"
        )

        path_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        path_entry = ttk.Entry(
            path_frame,
            width=50
        )

        path_entry.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        path_entry.insert(
            0,
            r"D:\MC_Server"
        )

        ttk.Button(
            path_frame,
            text="浏览文件夹",
            command=browse_folder
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        # =================================================
        # 图标设置区域
        # =================================================

        icon_frame = ttk.LabelFrame(
            root,
            text="图标设置"
        )

        icon_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        icon_mode_var = tk.StringVar(
            value="system"
        )

        ttk.Radiobutton(
            icon_frame,
            text="系统图标组编号",
            variable=icon_mode_var,
            value="system",
            command=change_icon_mode
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        icon_index_entry = ttk.Entry(
            icon_frame,
            width=20
        )

        icon_index_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        icon_index_entry.insert(
            0,
            "-184"
        )

        ttk.Radiobutton(
            icon_frame,
            text="自定义ICO",
            variable=icon_mode_var,
            value="ico",
            command=change_icon_mode
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        custom_icon_entry = ttk.Entry(
            icon_frame,
            width=40
        )

        custom_icon_entry.grid(
            row=1,
            column=1,
            padx=5
        )

        custom_icon_entry.config(
            state="disabled"
        )

        ttk.Button(
            icon_frame,
            text="选择ICO",
            command=browse_icon
        ).grid(
            row=1,
            column=2,
            padx=5
        )

        # =================================================
        # 功能按钮区域
        # 两列排列
        # =================================================

        button_frame = ttk.LabelFrame(
            root,
            text="工具操作"
        )

        button_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        buttons = [

            ("预览REG", preview_reg),

            ("生成REG", generate_reg),

            ("选择REG并导入", import_and_restart),

            ("选择REG并删除入口", remove_reg_entry),

            ("重启资源管理器", restart_explorer_gui)

        ]

        for index, (text, command) in enumerate(buttons):
            ttk.Button(
                button_frame,
                text=text,
                command=command,
                width=22
            ).grid(

                row=index // 2,

                column=index % 2,

                padx=5,

                pady=5

            )

        # =================================================
        # 日志区域
        # =================================================

        log_frame = ttk.LabelFrame(
            root,
            text="运行日志"
        )

        log_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        log_box = tk.Text(
            log_frame,
            height=8,
            state="disabled"
        )

        log_box.pack(
            fill="both",
            expand=True
        )

        log(
            "模块加载完成"
        )

        # =================================================
        # 启动GUI
        # =================================================

        root.mainloop()