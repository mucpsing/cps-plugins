# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date:
# @Last Modified by: CPS
# @Last Modified time: 2024-06-04 15:27:51.767280
# @file_path "W:\CPS\IDE\SublimeText\JS_SublmieText\Data\Packages\cps-plugins"
# @Filename "main.py"
# @Description: 自用插件，与本人开发的其他插件作为配置形式存在
#


import sublime, sublime_plugin
import os, re


from .core import helper
from .core import utils

PLUGIN_NAME = "cps-plugins"
SETTING_KEY = "cps_print_param"
SETTINGS_PRINT_PARAM = {}
DEFAULT_SETTINGS_FILE = "cps.sublime-settings"


if int(sublime.version()) < 3176:
    raise ImportWarning("This plugin does not support the current version. Please use sublime Text 3176 or later")


def plugin_loaded():
    global SETTINGS_PRINT_PARAM, DEFAULT_SETTINGS_FILE, SETTING_KEY
    SETTINGS_PRINT_PARAM = SettingManager(SETTING_KEY, DEFAULT_SETTINGS_FILE)


class SettingManager:
    def __init__(self, setting_key: str, default_settings: str):
        self.setting_key = setting_key
        self.default_settings = default_settings
        self.default_settings_path = os.path.join(sublime.packages_path(), "cps-plugins", ".sublime", default_settings)

        self.data = {}

        sublime.set_timeout_async(self.plugin_loaded_async)

    def __getitem__(self, key: str, default={}):
        if key in self.data:
            return self.data.get(key, default)
        else:
            return {}

    def get(self, key: str, default={}):
        return self.__getitem__(key, default)

    def plugin_loaded_async(self):
        """
        @Description Listening to user configuration files
        """
        with open(self.default_settings_path, "r", encoding="utf8") as f:
            self.data = sublime.decode_value(f.read()).get(self.setting_key, {})

        # Reading existing configurations
        user_settings = sublime.load_settings(self.default_settings)
        # Adding configuration update events
        user_settings.add_on_change(self.default_settings, self._on_settings_change)
        # 将最新的配置更新到内部的data，最终以data为准
        # Updating the latest configuration to the internal data, and ultimately relying on the data as the final authority
        utils.recursive_update(self.data, user_settings.to_dict()[self.setting_key])

    def _on_settings_change(self):
        new_settings = sublime.load_settings(self.default_settings).get(self.setting_key, {})

        utils.recursive_update(self.data, new_settings)

        return self


class CpsTestCommand(sublime_plugin.TextCommand):
    def run(self, edit, str: str = ""):
        view = self.view
        # get currt line
        print(helper.get_currt_selection(view))

        windows = sublime.active_window()

        print(sublime.open_dialog(lambda x: x))


# print a variable
class CpsPrintParam(sublime_plugin.TextCommand):
    def run(self, edit):
        global SETTINGS_PRINT_PARAM
        if not SETTINGS_PRINT_PARAM:
            print("配置读取失败")
            return
        settings = SETTINGS_PRINT_PARAM

        view = self.view

        # 获取当前行的region
        currt_region: sublime.Region = self.view.sel()[0]
        currt_line_region = view.full_line(currt_region)

        # 获取下一行
        newt_line_start: int = currt_line_region.b

        # 获取关键字
        select_str = self.view.substr(currt_region)
        if not select_str or len(select_str) <= 0:
            return print("没有任何选择")

        # 获取前置缩进
        currt_line_str = self.view.substr(currt_line_region)

        # 提取前缩进
        res = re.compile(r"^(\s*)?(.*)").findall(currt_line_str)
        if res and len(res) > 0:
            indent = res[0][0]
        else:
            indent = ""

        # 根据不同格式插入不同
        name, ext = os.path.splitext(view.file_name())
        for each in settings.data.values():
            if ext in each["exts"]:
                insert_tmpl = each["template"]
                view.insert(
                    edit,
                    newt_line_start,
                    f"{indent}{insert_tmpl.format(param=select_str)}",
                )
                break


# 打开当前文件的文件夹
class CpsOpenCurrtFolder(sublime_plugin.TextCommand):
    def run(self, edit):
        print("打开当前文件夹")
        # 调用当前激活的窗口来执行 run_command命令(无法使用 self.view 调用 run_command)
        fdir, fname = os.path.split(self.view.file_name())
        sublime.active_window().run_command("open_dir", {"dir": fdir})


# 设置语法
class CpsSetSyntaxCommand(sublime_plugin.TextCommand):
    def run(self, edit, syntax):
        syntaxDict = {
            "html": "Packages/HTML/HTML.sublime-syntax",
            "vue": "Packages/Vue Syntax Highlight/Vue Component.sublime-syntax",
            "js": "Packages/JavaScriptNext - ES6 Syntax/JavaScriptNext.tmLanguage",
        }
        if syntax:
            self.view.set_syntax_file(syntaxDict[syntax])


# 打开配置文件
class CpsEditSettingCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, base_file: str, package_name: str):
        sublime.active_window().run_command(
            "edit_settings",
            {
                "base_file": os.path.join(sublime.packages_path(), __package__, ".sublime", base_file),
                "default": '{\n  "' + package_name + '":{\n    /*请在插件名称内选项内添加自定义配置*/\n    \n  }\n}',
            },
        )


# 去除当前打开的py文件注释
class RemoveCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # 获取当前文件的语法
        syntax = self.view.settings().get("syntax").lower()

        # 检查语法是否为 Python
        if "python" in syntax or utils.is_python():
            # 获取文件内容
            full_content = self.view.substr(sublime.Region(0, self.view.size()))

            # 按行分割文件内容
            lines = full_content.split("\n")

            # 获取第一行
            first_line = lines[0]

            # 去除除第一行以外的所有注释
            new_lines = [first_line] + [line for line in lines[1:] if not line.strip().startswith("#")]

            # 将修改后的内容写回文件
            new_content = "\n".join(new_lines)
            self.view.replace(edit, sublime.Region(0, self.view.size()), new_content)


class RemoveCommentsEventListener(sublime_plugin.EventListener):
    def on_context_menu(self, context, menu):
        # 如果右键菜单的上下文包含 "text" 类型，表示右键的是文本内容
        if "text" in context:
            # 获取当前视图
            view = sublime.active_window().active_view()

            # 获取当前文件的语法
            if view:
                syntax = view.settings().get("syntax")

                # 如果语法为 Python，添加 "Remove Comments" 菜单项
                if "Python" in syntax:
                    menu.append("Remove Comments", {"command": "remove_comments"})
