from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message, require
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.log import logger
import json
from nonebot.params import CommandArg
require("nonebot_plugin_localstore")
from nonebot_plugin_localstore import get_plugin_data_file  # noqa: E402


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


open_switch = on_command("开启群聊监听", priority=10, block=True)
close_switch = on_command("关闭群聊监听", priority=10, block=True)
add_new_group = on_command("添加监听群组", priority=10, block=True)
remove_group = on_command("删除监听群组", priority=10, block=True)
transform_information = on_message(priority=10, block=True)


def get_state_file():
    return get_plugin_data_file("plugin_information.json")


def _ensure_default():
    return {"plugin_state": False, "groups": {}}


def _load_information():
    global _plugin_information, _plugin_state

    state_file = get_state_file()
    if state_file.exists():
        try:
            _plugin_information = json.loads(state_file.read_text("utf-8"))
        except Exception:
            _plugin_information = _ensure_default()
            state_file.write_text(
                json.dumps(_plugin_information, ensure_ascii=False, indent=2),
                "utf-8",
            )
    else:
        _plugin_information = _ensure_default()
        state_file.write_text(
            json.dumps(_plugin_information, ensure_ascii=False, indent=2),
            "utf-8",
        )

    _plugin_state = _plugin_information.get("plugin_state", False)


def _save_information():
    get_state_file().write_text(
        json.dumps(_plugin_information, ensure_ascii=False, indent=2),
        "utf-8",
    )


@open_switch.handle()
async def open_plugin(bot: Bot, event: Event):
    global _plugin_information
    _load_information()
    _plugin_information["plugin_state"] = True
    _save_information()
    await bot.send_group_msg(group_id=event.group_id, message=Message("插件已开启"))


@close_switch.handle()
async def close_plugin(bot: Bot, event: Event):
    global _plugin_information
    _load_information()
    _plugin_information["plugin_state"] = False
    _save_information()
    await bot.send_group_msg(group_id=event.group_id, message=Message("插件已关闭"))


@add_new_group.handle()
async def add_new_group(bot: Bot, event: Event, args: Message = CommandArg()):
    global _plugin_information
    new_group_id = args.extract_plain_text().strip()
    _load_information()

    if new_group_id:
        _plugin_information.setdefault("groups", {})
        _plugin_information["groups"].setdefault(str(event.group_id), [])

        if new_group_id not in _plugin_information["groups"][str(event.group_id)]:
            _plugin_information["groups"][str(event.group_id)].append(new_group_id)

        _save_information()
        await bot.send_group_msg(group_id=event.group_id, message=Message("添加监听群组成功"))
    else:
        await bot.send_group_msg(
            group_id=event.group_id,
            message=Message("请重新输入命令并加上群号 例如 /添加监听群组 12345"),
        )


@remove_group.handle()
async def remove_exist_group(bot: Bot, event: Event, args: Message = CommandArg()):
    global _plugin_information
    old_group_id = args.extract_plain_text().strip()
    _load_information()

    if not old_group_id:
        await remove_group.finish()

    groups = _plugin_information.get("groups", {})
    cur = groups.get(str(event.group_id))

    if not cur:
        await bot.send_group_msg(group_id=event.group_id, message=Message("你的已经添加的群组是空，无法删除该群组"))
        await remove_group.finish()

    if old_group_id in cur:
        cur.remove(old_group_id)
        if len(cur) == 0:
            del groups[str(event.group_id)]
        _plugin_information["groups"] = groups
        _save_information()
        await bot.send_group_msg(group_id=event.group_id, message=Message(f"删除群组 {old_group_id} 成功"))
    else:
        await bot.send_group_msg(group_id=event.group_id, message=Message("你的已经添加的群组里面没有此群组，删除失败"))

    await remove_group.finish()


@transform_information.handle()
async def transformation_information(bot: Bot, event: Event):
    global _plugin_information, _plugin_state
    _load_information()
    logger.info(_plugin_information)

    # 注意：你原来这里每次都会把 plugin_state 置 False，会导致永远转发不了
    # _plugin_information["plugin_state"] = False

    if _plugin_state:
        if str(event.group_id) in _plugin_information.get("groups", {}):
            sender_group_id = event.group_id
            group_info = await bot.get_group_info(group_id=sender_group_id)
            sender_group_name = group_info["group_name"]

            sender_name = getattr(event.sender, "card", None)
            sender_message = event.get_message()
            check_message = sender_message.extract_plain_text().strip()

            if not sender_name:
                user_information = await bot.get_stranger_info(user_id=event.sender.user_id)
                sender_name = user_information["nickname"]

            # 这里最好用 startswith 判断指令，避免带参数时漏掉
            if check_message not in {
                "/开启群聊监听",
                "/关闭群聊监听",
                "/添加监听群组",
                "/删除监听群组",
            }:
                sender_information = f"来自群[{sender_group_id}] {sender_group_name}的 {sender_name} 说"
                receivers = _plugin_information["groups"][str(event.group_id)]
                for receiver in receivers:
                    await bot.send_group_msg(group_id=int(receiver), message=Message(sender_information))
                    await bot.send_group_msg(group_id=int(receiver), message=Message(sender_message))