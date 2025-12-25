from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="群消息中继",
    description=(
        "在多个群之间转发消息的插件："
        "可为每个监听群配置一个或多个目标群，将本群的普通消息同步到目标群。"
    ),
    usage="""
指令：
/开启群聊监听
    在当前群开启消息转发功能。开启后，本群的普通消息会被转发到已配置的目标群。

/关闭群聊监听
    在当前群关闭消息转发功能。

/添加监听群组 <群号>
    为当前群添加一个目标群，用于接收本群转发的消息。
    示例：/添加监听群组 123456789

/删除监听群组 <群号>
    从当前群的目标群列表中移除一个群。
    示例：/删除监听群组 123456789

说明：
- 插件会将当前群中的消息转发到配置的目标群。
- 当前实现为单向转发：哪个群开启了监听，就把该群的消息发往它配置的目标群列表。
- 指令消息本身不会被转发。
""".strip(),
    type="application",

    homepage="https://github.com/TonyLiangP2010405/nonebot-transfer-information",

    supported_adapters={"~onebot.v11"},
)