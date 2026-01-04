from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.log import logger
import json
from nonebot.params import CommandArg
from nonebot_plugin_localstore import get_plugin_data_file

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

    homepage="https://github.com/TonyLiangP2010405/nonebot-plugin-group-relay",

    supported_adapters={"~onebot.v11"},
)



_plugin_information = {}
_plugin_state = None


STATE_FILE = get_plugin_data_file("plugin_information.json")
open_switch = on_command("开启群聊监听", priority=10, block=True)
close_switch = on_command("关闭群聊监听", priority=10, block=True)
add_new_group = on_command("添加监听群组", priority=10, block=True)
remove_group = on_command("删除监听群组", priority=10, block=True)
transform_information = on_message(priority=10, block=True)

def _load_information():
    global _plugin_information
    global _plugin_state
    if STATE_FILE.exists():
        try:
            _plugin_information = json.loads(STATE_FILE.read_text("utf-8"))
            _plugin_state = _plugin_information["plugin_state"]
        except Exception:
            _plugin_information = {"plugin_state": None}
            STATE_FILE.write_text(
                json.dumps({"plugin_state": "", "groups": {}}, ensure_ascii=False, indent=2),
                "utf-8",
            )
    else:
        STATE_FILE.write_text(
            json.dumps({"plugin_state":"", "groups": {}}, ensure_ascii=False, indent=2),
            "utf-8",
        )


def _save_information():
    STATE_FILE.write_text(
        json.dumps(_plugin_information, ensure_ascii=False, indent=2),
        "utf-8",
    )

@open_switch.handle()
async def open_plugin(bot: Bot, event: Event):
    global _plugin_information
    _load_information()
    _plugin_information["plugin_state"] = True
    _save_information()
    content = "插件已开启"
    await bot.send_group_msg(
        group_id=event.group_id,
        message=Message(content),
    )


@close_switch.handle()
async def close_plugin(bot: Bot, event: Event):
    global _plugin_information
    _load_information()
    _plugin_information["plugin_state"] = False
    _save_information()
    content = "插件已关闭"
    await bot.send_group_msg(
        group_id=event.group_id,
        message=Message(content),
    )


@add_new_group.handle()
async def add_new_group(bot: Bot, event: Event, args: Message = CommandArg()):
    global _plugin_information
    new_group_id = args.extract_plain_text()
    _load_information()
    if new_group_id:
        if "groups" not in _plugin_information:
            _plugin_information["groups"] = {}
        if str(event.group_id) not in _plugin_information["groups"]:
            _plugin_information["groups"][event.group_id] = [new_group_id]
        else:
            _plugin_information["groups"][str(event.group_id)].append(new_group_id)
        _save_information()
        content = "添加监听群组成功"
        await bot.send_group_msg(
            group_id=event.group_id,
            message=Message(content),
        )
    else:
        content = "请重新输入命令并加上群号 例如 /添加群组 12345"
        await bot.send_group_msg(
            group_id=event.group_id,
            message=Message(content),
        )



@remove_group.handle()
async def remove_exist_group(bot: Bot, event: Event, args: Message = CommandArg()):
    global _plugin_information
    old_group_id = args.extract_plain_text()
    _load_information()
    if old_group_id:
        if "groups" not in _plugin_information:
            warning1 = "你的已经添加的群组是空，无法删除该群组"
            await bot.send_group_msg(
                group_id=event.group_id,
                message=Message(warning1),
            )
        else:
            if str(event.group_id) not in _plugin_information["groups"]:
                warning2 = "你的已经添加的群组是空，无法删除该群组"
                await bot.send_group_msg(
                    group_id=event.group_id,
                    message=Message(warning2),
                )
            else:
                if old_group_id in _plugin_information["groups"][str(event.group_id)]:
                    _plugin_information["groups"][str(event.group_id)].remove(old_group_id)
                    content = "删除群组 "+ old_group_id +" 成功"
                    if len(_plugin_information["groups"][str(event.group_id)]) == 0:
                        del _plugin_information["groups"][str(event.group_id)]
                    _save_information()
                    await bot.send_group_msg(
                        group_id=event.group_id,
                        message=Message(content),
                    )
                else:
                    warning3 = "你的已经添加的群组里面没有此群组，删除失败"
                    await bot.send_group_msg(
                        group_id=event.group_id,
                        message=Message(warning3),
                    )
    await remove_group.finish()


@transform_information.handle()
async def transformation_information(bot: Bot, event: Event):
    global _plugin_information, _plugin_state
    _load_information()
    logger.info(_plugin_information)
    _plugin_information["plugin_state"] = False
    if _plugin_state is not None and _plugin_state != False:
        if str(event.group_id) in _plugin_information["groups"]:
            sender_group_id = event.group_id
            group_info = await bot.get_group_info(group_id=sender_group_id)
            sender_group_name = group_info["group_name"]
            sender_name = event.sender.card
            sender_message = event.get_message()
            check_message = sender_message.extract_plain_text()
            logger.info(sender_name)
            if not sender_name:
                user_information = await bot.get_stranger_info(user_id=event.sender.user_id)
                sender_name = user_information["nickname"]
            if check_message != "/开启群聊监听" and check_message != "/关闭群聊监听" and check_message != "/添加监听群组" and check_message != "/删除监听群组":
                sender_information = f"来自群[{sender_group_id}] {sender_group_name}的 {sender_name} 说"
                receivers = _plugin_information["groups"][str(event.group_id)]
                for receiver in receivers:
                    await bot.send_group_msg(
                        group_id=receiver,
                        message=Message(sender_information),
                    )
                    await bot.send_group_msg(
                        group_id=receiver,
                        message=Message(sender_message),
                    )




