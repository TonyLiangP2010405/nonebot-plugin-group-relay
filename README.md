<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-group-relay

_✨ NoneBot 插件简单描述 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/TonyLiangP2010405/nonebot-plugin-group-relay.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-group-relay">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-group-relay.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

这是一个 nonebot2 插件项目的模板库, 你可以直接使用本模板创建你的 nonebot2 插件项目的仓库

## 📖 介绍

`nonebot-plugin-group-relay` 是一个用于 **在多个 QQ 群之间中继 / 转发消息** 的 NoneBot2 插件。

你可以将若干个群绑定到同一个“中继通道”，插件会自动将指定类型的消息在这些群之间同步，实现类似“跨群群聊”“信息广播”的效果，适合：

- 多个主题相近的交流群之间共享聊天内容

插件基于 OneBot v11 协议实现，支持常见的 NoneBot2 适配器配置，开箱即用。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot_plugin_group_relay

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot_plugin_group_relay
</details>
打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-group-relay"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:--:|:----:|:----:|
| 配置项1 | 无  | 无 | 配置说明 |
| 配置项2 | 否  | 无 | 配置说明 |

## 🎉 使用
### 指令表
| 指令 |   权限   | 需要@ | 范围 | 说明 |
|:-----:|:------:|:----:|:----:|:----:|
| `/开启群聊监听` |  群成员   | 是 | 群聊 | 在当前群开启消息转发功能，本群的普通消息会被转发到已配置的目标群。 |
| `/关闭群聊监听` |  群成员   | 是 | 群聊 | 在当前群关闭消息转发功能，停止向目标群转发本群消息。 |
| `/添加监听群组 <群号>` |  群成员   | 是 | 群聊 | 为当前群添加一个目标群，用于接收本群转发的消息。示例：`/添加监听群组 123456789` |
| `/删除监听群组 <群号>` |  群成员   | 是 | 群聊 | 从当前群的目标群列表中移除一个群。示例：`/删除监听群组 123456789` |

