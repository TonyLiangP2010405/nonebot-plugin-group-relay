from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.log import logger
import json
from pathlib import Path

_plugin_information = {}
_plugin_state = None
STATE_FILE = Path(__file__).parent / "plugin_information.json"
open_switch = on_command("开启群聊监听", priority=10, block=True)
close_switch = on_command("关闭群聊监听", priority=10, block=True)
listener_group = on_command("", priority=10, block=True)

def _load_information():
    global _plugin_information
    if STATE_FILE.exists():
        try:
            _plugin_information = json.loads(STATE_FILE.read_text("utf-8"))
            _plugin_state = _plugin_information["plugin_state"]
        except Exception:
            _plugin_information = {"plugin_state": None}
            STATE_FILE.write_text(
                json.dumps({"plugin_state": ""}, ensure_ascii=False, indent=2),
                "utf-8",
            )
    else:
        STATE_FILE.write_text(
            json.dumps({"plugin_state":""}, ensure_ascii=False, indent=2),
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

@listener_group.handle()
async def listen_group_message_test(bot: Bot, event: Event):
    logger.info("teteteteteteetetetetetet", event.group_id)
    if event.group_id == 370464176:
        logger.info("teteteteteteetetetetetet", event.get_event_description())
        return