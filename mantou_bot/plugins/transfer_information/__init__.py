from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.log import logger



open_close_switch = on_command("开启群聊监听", priority=10, block=True)
listener_group = on_command("", priority=10, block=True)


@open_close_switch.handle()
async def send_group_message_test(bot: Bot, event: Event):
    if TRANSFER_INFORMATION_SWITCH:
        TRANSFER_INFORMATION_SWITCH = False
    else:
        TRANSFER_INFORMATION_SWITCH = True
    target_group_id = 370464176  # 例如 123456789
    logger.info("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    logger.info(event.get_event_description())
    # 要发送的文本内容
    content = "这是 NoneBot 主动给群发的一条测试消息"

    logger.info(event.group_id)
    if event.group_id == 370464176:
        logger.info("teteteteteteetetetetetet", event.get_event_description())

    # 通过 OneBot API 发送群消息
    await bot.send_group_msg(
        group_id=target_group_id,
        message=Message(content),
    )

    await open_close_switch.finish("已向目标群发送消息。")


@listener_group.handle()
async def listen_group_message_test(bot: Bot, event: Event):
    logger.info("teteteteteteetetetetetet", event.group_id)
    if event.group_id == 370464176:
        logger.info("teteteteteteetetetetetet", event.get_event_description())
        return