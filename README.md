# CPS Sublime Text 自用插件合集

<div>
    <img flex="left" src="https://img.shields.io/badge/python-%3E%3D3.8.0-3776AB"/>
    <img flex="left" src="https://img.shields.io/badge/Sublime%20Text-FF9800?style=flat&logo=Sublime%20Text&logoColor=white"/>
    <img flex="left" src="https://img.shields.io/github/license/caoxiemeihao/electron-vite-vue?style=flat"/>
</div>

虽然大多数功能插件市场都已存在，但是很多插件的功能要么是配置太复杂，要么是很久不更新，用起来很不爽。为了自己码代码爽，讲一些自己常用的功能集成插件。

## 注意
本组织所有插件均是几年前作品，插件原始仓库:https://gitee.com/Capsion-ST-PLugins/sublime_testt

2022年11月将代码进行了再整理，很多功能sublimetext上也有更加完善的插件，现在喜欢捣鼓编辑器的朋友建议转战vscode。

## 插件列表：

| 插件名称                 | 主要功能                                                     | 快捷键     |
| ------------------------ | ------------------------------------------------------------ | ---------- |
| cps_pulgins              | 以下所有插件的依赖，基础插件<br>快速打开当前文件的目录（win）<br/>集成配置菜单<br/>自动更新以下列表中的其他插件 | `alt + e`  |
| cps_run_commands         | 快速弹出一个命令输入框，带历史记录                           | `alt + F1` |
| cps_comments_creator     | 快速生成代码注释头部，支持`js`、`py`等，具体语言可以自己加入 | `alt + q`  |
| cps_beautify             | 格式化代码，主要使用`prettier`引擎，后续考虑集成`eslint`     | 保存时生效 |
| cps_auto_switch_language | 每次切换进编辑器时，自动切换输入为英文环境                   | 自动生效   |
| cps_update_channel_v3    | 自动更新`channel_v3.json`文件，自动关联到配置中              | 自动生效   |
| cps_fileheader           | 插入文件头信息，支持自定义模板，自定义关联格式               | `alt + f`  |

> 上述功能可能早已有现成的且成熟的插件在插件市场，不过因为老外写的插件很多配置都是英文，而且配置往往比较复杂，为了将学习成本降至0，同时做到**自己用的爽**，对的，最重要的还是**自己用的爽**，所以才重造轮子。

# 使用|Usage

## cps_update_channel_v3

![readme](screenshot/auto-update-channel1.gif)

![local](http://localhost:45462/image/auto-update-channel1.gif)

## cps_run_commands

- **便捷的快速输入常用命令**
  ![](screenshot/step1.gif)

- **历史记录功能**
  默认记录100条，最高500条
  ![](screenshot/step2.gif)


- **快速的搜索历史记录**
  ![](screenshot/step3.gif)
  ![](screenshot/step4.gif)

## cps_comments_creator

![](screenshot/cps_comments_creator1.gif)
