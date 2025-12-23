from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.log import logger
import json
from pathlib import Path

_plugin_state = None
STATE_FILE = Path(__file__).parent / "plugin_information.json"
open_switch = on_command("开启群聊监听", priority=10, block=True)
listener_group = on_command("", priority=10, block=True)

def _load_state():
    global _plugin_state
    if STATE_FILE.exists():
        try:
            _plugin_state = json.loads(STATE_FILE.read_text("utf-8"))
        except Exception:
            _plugin_state = None
    else:
        _plugin_state = None


def _save_state():
    STATE_FILE.write_text(
        json.dumps(_plugin_state, ensure_ascii=False, indent=2),
        "utf-8",
    )

@open_switch.handle()
async def open_plugin(bot: Bot, event: Event):
    global _plugin_state
    _load_state()
    _plugin_state = True
    _save_state()
    content = "插件已开启"
    await bot.send_group_msg(
        group_id=event.group_id,
        message=Message(content),
    )
    await open_switch.finish()


@listener_group.handle()
async def listen_group_message_test(bot: Bot, event: Event):
    logger.info("teteteteteteetetetetetet", event.group_id)
    if event.group_id == 370464176:
        logger.info("teteteteteteetetetetetet", event.get_event_description())
        return