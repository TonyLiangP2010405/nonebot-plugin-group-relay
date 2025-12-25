from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.log import logger
import json
from pathlib import Path

from nonebot.params import CommandArg

_plugin_information = {}
_plugin_state = None
STATE_FILE = Path(__file__).parent / "plugin_information.json"
open_switch = on_command("开启群聊监听", priority=10, block=True)
close_switch = on_command("关闭群聊监听", priority=10, block=True)
add_new_group = on_command("添加监听群组", priority=10, block=True)
remove_group = on_command("删除监听群组", priority=10, block=True)

def _load_information():
    global _plugin_information
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
    await open_switch.finish()

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
    await close_switch.finish()

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
    await add_new_group.finish()


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