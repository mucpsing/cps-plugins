# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2025-11-03 21:34:30.815694
# @Last Modified by: CPS
# @Last Modified time: 2025-11-03 21:34:30.815694
# @file_path "D:\CPS\IDE\JS_SublmieText\Data\Packages\cps-plugins\core"
# @Filename "createPyBuildByFloder.py"
# @Description: 功能描述
#
import os, sys

sys.path.append("..")
import json
from pathlib import Path
from os import path


def print_dict(obj: dict, indent: int = 4) -> str:
    import json

    print(json.dumps(obj, indent=indent, ensure_ascii=False))


def generate_python_build_config(scan_directory: str, output_path: str | None = None):
    """
    快捷函数：生成Python构建配置

    Args:
        scan_directory: 扫描Python解释器的目录
        output_path: 输出文件路径

    Returns:
        bool: 是否成功生成
    """
    print(f"🔍 正在扫描目录: {scan_directory}")

    interpreters = []
    base_dir = Path(scan_directory)

    if not base_dir.exists():
        print(f"❌ 错误: 目录 '{scan_directory}' 不存在")
        return False

    # 扫描Python解释器
    for item in base_dir.iterdir():
        if item.is_dir():
            python_exe = item / "python.exe"
            if python_exe.exists():
                interpreters.append({"name": item.name, "path": str(python_exe)})
                print(f"✅ 找到: {item.name}")

    if not interpreters:
        print("❌ 未找到任何Python解释器")
        return False

    # 生成配置
    config = {
        "cmd": ["python", "$file"],
        "file_regex": '^[ ]*File "(...*?)",line ([0-9]*)',
        "env": {"PYTHONIOENCODING": "utf-8"},
        "file_patterns": ["*.py"],
        "encoding": "utf-8",
        "selector": "source.python",
        "variants": [
            {
                "name": "python(output side)",
                "shell_cmd": 'start cmd /c "chcp 65001 & python ${file} & timeout /t 10 "',
            },
            {
                "name": "poetry run (内部调用)",
                "cmd": ["poetry", "run", "python", "${file}"],
            },
            {
                "name": "poetry run (外部调用)",
                "shell_cmd": 'start cmd /c "poetry run python ${file} & timeout /t 10"',
            },
            {
                "name": "pdm run (内部调用)",
                "cmd": ["pdm", "run", "python", "${file}"],
            },
            {
                "name": "pdm run (外部调用)",
                "shell_cmd": 'start cmd /c "pdm run python ${file} & timeout /t 10"',
            },
            {
                "name": "ArcMap py2.7 (内部调用)",
                "cmd": ["C:/Python27/ArcGIS10.2/python.exe", "${file}"],
            },
            {
                "name": "ArcMap py2.7 (外部调用)",
                "shell_cmd": 'start cmd /c "C:/Python27/ArcGIS10.2/python.exe ${file} & timeout /t 10"',
            },
        ],
    }

    # 为每个解释器添加变体
    new_variants = []
    for interpreter in interpreters:
        safe_name = interpreter["name"].replace(" ", "_").replace(".", "_")

        # 内部调用
        new_variants.append(
            {"name": f"{safe_name}-inside", "cmd": [interpreter["path"], "${file}"]}
        )

        # 外部调用
        new_variants.append(
            {
                "name": safe_name,
                "shell_cmd": f"start cmd /c \"chcp 65001 & \"{interpreter['path']}\" ${{file}} & timeout /t 10 \"",
            }
        )

    config["variants"] = config["variants"] + new_variants

    # 保存配置
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    else:
        print(f"🎉 配置已生成: {output_path}")
        print(f"📁 共找到 {len(interpreters)} 个Python解释器")
        print_dict(config)
    return True


if __name__ == "__main__":
    t = path.abspath(r"D:\CPS\python")
    generate_python_build_config(
        t, path.abspath("../.sublime/cps-plugins-python.sublime-build")
    )
