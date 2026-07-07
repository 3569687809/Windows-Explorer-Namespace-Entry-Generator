# Windows 此电脑自定义入口生成器


## 功能

- 在 Windows 文件资源管理器「此电脑」中创建自定义文件夹入口
- 支持：
  - 自定义名称
  - 自定义目标路径
  - 系统 DLL 图标
  - 自定义 ICO 图标
  - 自动生成 GUID
  - 自动生成 REG


## 原理

通过 Windows Shell Namespace 注册：

HKCU\Software\Classes\CLSID

并绑定：

{0E5AAE11-A475-4C5B-AB00-C66DE400274E}

实现 Explorer 文件夹入口。


## 支持系统

Windows 10
Windows 11
