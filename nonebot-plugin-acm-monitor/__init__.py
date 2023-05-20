import nonebot
import requests
import re
import random
import httpx
from nonebot import on_command, on_message, on_regex, export
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent, Event,PrivateMessageEvent
from nonebot.adapters.onebot.v11.utils import unescape
from nonebot.params import State
from nonebot.rule import to_me
from .base import *
from nonebot import require
import asyncio
import time

proname = on_command("取外号")
getname = on_command("看本名")

@proname.handle()
async def proname_handler(bot: Bot, event: Event):
    temp = str(event.get_message()).split()
    if len(temp) != 3:
        await proname.finish("取外号请发送三段消息：取外号、本名、外号名~")

    name1 = temp[1].strip().casefold().title()
    name2 = temp[2].strip().casefold().title()
    names.setname(name2, name1)

    await proname.finish(f"{name1} 的外号已被设置为 {temp[2]} ~")

@getname.handle()
async def proname_handler(bot: Bot,event: Event):
    temp = str(event.get_message())[3:].strip().casefold().title()
    res = names.getname(temp)
    if res == -1:
        await getname.finish("这个外号还没有人使用哦~")
    await getname.finish(f"{temp} 的本名是 {res} 哦~")
    

scheduler = require("nonebot_plugin_apscheduler").scheduler

config = nonebot.get_driver().config

async def cf_get_last_problem(name):
    data = -1
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    async with httpx.AsyncClient(timeout=None, headers=headers) as client:
        url = f"https://codeforces.com/api/user.status?handle={name}&page=1"
        resp = await client.get(url)
        try:
            data = resp.json()
        except:
            print("有内鬼!" + name)
            print(resp.text)

        if data == -1 or data["status"] != "OK" or len(data["result"]) == 0:
            data = -1
    if data == -1:
        return -1
    return data["result"][0]

async def luogu_get_last_problem(name):
    url = f"https://www.luogu.com.cn/record/list?pid=&language=&orderBy=0&user={name}&page=1"

    key = {
        "__client_id": config.luogu_client_id,
        "_uid": config.luogu_uid,
        "login_referer": config.luogu.login_referer
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    async with httpx.AsyncClient(timeout=None) as client:
        data = await client.get(url, cookies=key, headers=headers)
        res = re.finditer(r'pid%22%3A%22(?P<t1>.*?)%22', str(data.content))
        flag = False
        for i in res:
            flag = True
            ans = i.group("t1")
            break
        if not flag:
            ans = ''
    return ans


# who = {"3191128724", "1143957699"}
luogu = on_command("看洛谷卷王")
lg_bukanle = on_command("停看洛谷卷王")
lg_showout = on_command("当前洛谷卷王")

juanwang = on_command("看cf卷王")
bukanle = on_command("停看cf卷王")
showout = on_command("当前cf卷王")

@luogu.handle()
async def luogu_handler1(bot: Bot, event: PrivateMessageEvent):
    await luogu.finish("抱歉,当前仅支持群聊看卷王哦~")

@juanwang.handle()
async def juanwang_handler1(bot: Bot, event: PrivateMessageEvent):
    await juanwang.finish("抱歉,当前仅支持群聊看卷王哦~")

@juanwang.handle()
async def juanwang_handler2(bot: Bot, event: GroupMessageEvent):
    name = str(event.get_message())[5:].strip()
    if len(name) == 0:
        await juanwang.finish("请说明要看哪位卷王哦~")
    s = re.search('[\w|\x80-\xff]*', name).group()
    if name != s:
        await juanwang.finish("请不要输入奇怪的字符哦~")
    newname = name.casefold().title()
    if names.getname(newname) != -1:
        newname = names.getname(newname)
    # if user in who:
    #     await juanwang.finish("抱歉,您一个人都不能看~")

    # if newname == "Calanosay" or name == "434015":
    #     await juanwang.finish("抱歉，这位卷王由于特殊原因，不能看")
    if newname in Codeforces.getall():
        await juanwang.finish("这位卷王已经被人盯上了哦,你不能再看他了(可能是其他群聊的人喔)")
    last = await cf_get_last_problem(newname)
    if last == -1:
        await juanwang.finish("未查到该卷王或该卷王无提交记录~")
    if "contestId" not in last:
        await juanwang.finish("该卷王由于上次做的题目非常规题目，暂无法查看。")
    contest = last["contestId"]
    problem = last['problem']['index']
    now = "CF" + str(contest) + problem
    Codeforces.setlast(newname, now)
    Codeforces.setlastvp(newname, "qefqef")
    Codeforces.addpeople(newname)
    tp = last['author']["participantType"]
    if tp == "VIRTUAL" or tp == "CONTESTANT":
        Codeforces.setlastvp(newname, contest)
    # doing.add(newname)
    Codeforces.setGroup(newname, event.group_id)
    await juanwang.send(f"现在开始持续关注CF卷王{newname}啦！如果想停止,请说停看卷王某某某~")


cnt = 0
async def crawl(user):
    global cnt
    cnt += 1
    await asyncio.sleep(cnt * 1)
    if cnt == len(Codeforces.getall()):
        cnt = 0
    st = time.time()    
    now = await cf_get_last_problem(user)
    ed = time.time()
    print("现在正在执行:" + user + "的CF任务，耗时" + str(ed - st))
    if now == -1:
        return
    if "contestId" not in now:
        return
    tp = now['author']["participantType"]
    contest = now["contestId"]

    if tp == "VIRTUAL" or tp == "CONTESTANT":
        if contest != Codeforces.getlastvp(user):
            Codeforces.setlastvp(user, contest)
            flag = "VP"
            if tp == "CONTESTANT":
                flag = "打CF比赛"
            await nonebot.get_bot().send_group_msg(message=Message(f"卷王{user}又开始{flag}了！他参赛的场次编号为 {contest}"),
                                                   group_id=int(Codeforces.getGroup(user)))
    elif tp == "PRACTICE":
        problem = now['problem']['index']
        now = "CF" + str(contest) + problem
        if now != Codeforces.getlast(user):
            Codeforces.setlast(user, now)
            await nonebot.get_bot().send_group_msg(message=Message(f"卷王{user}又开始做题了！他现在在做{now}"),
                                                   group_id=int(Codeforces.getGroup(user)))
            

@luogu.handle()
async def luogu_handler2(bot: Bot, event: GroupMessageEvent):
    name = str(event.get_message())[5:].strip()
    s = re.search('[\w|\x80-\xff]*', name).group()
    if name != s:
        await luogu.finish("请不要输入奇怪的字符哦~")
    newname = name.casefold().title()
    user = str(event.get_user_id())
    # if user in who:
    #     await juanwang.finish("抱歉,您一个人都不能看~")

    if len(name) == 0:
        await luogu.finish("请说明要看哪位卷王哦~")
    # if name == "Calanosay" or name == "434015":
    #     await juanwang.finish("抱歉，这位卷王由于特殊原因，不能看")
    if names.getname(newname) != -1:
        newname = names.getname(newname)
    if newname in Luogu.getall():
        await luogu.finish("这位卷王已经被人盯上了哦,你不能再看他了(可能是其他群聊的人喔)")
    last = await luogu_get_last_problem(newname)
    if len(last) == 0:
        await luogu.finish("未查到该卷王或这位卷王已限制了搜索权限~")
    Luogu.setlast(newname, last)
    Luogu.addpeople(newname)
    Luogu.setGroup(newname, event.group_id)
    await luogu.send(f"现在开始持续关注洛谷卷王{newname}啦！如果想停止,请说停看卷王某某某")


@scheduler.scheduled_job('interval', minutes=3, max_instances=200)
async def cf_handler():#cf自动执行
    await asyncio.gather(*(crawl(x) for x in Codeforces.getall()))


@scheduler.scheduled_job('interval', minutes=1,max_instances=61)
async def luogu_handler():#洛谷自动执行
    for user in Luogu.getall():
        now = await luogu_get_last_problem(user)
        print("现在正在执行:" + user + "的洛谷任务，题目为" + now)
        if len(now) == 0:
            continue
        if now[:2] == "CF":
            continue
        if now != Luogu.getlast(user):
            Luogu.setlast(user, now)
            await nonebot.get_bot().send_group_msg(message=Message(f"卷王{user}又开始做题了！他现在在做{now}"),
                                                   group_id=int(Luogu.getGroup(user)))


@lg_bukanle.handle()
async def lg_bukanle_handler(bot: Bot, event: Event):
    name = str(event.get_message())[6:].strip().casefold().title()
    if names.getname(name) != -1:
        name = names.getname(name)
    # if event.get_user_id() not in bot.config.superusers:
    #     await bukanle.finish("只有超管才能指挥我~")
    if name.casefold().title() not in Luogu.getall():
        await lg_bukanle.finish("没人在看这位卷王哦~")
    Luogu.delpeople(name)
    await lg_bukanle.finish(f"好的，我已经没有在看洛谷卷王{name}啦！")


@lg_showout.handle()
async def lg_showout_handler(bot: Bot, event: Event):
    List=[]
    for i in Luogu.getall():
        if Luogu.getGroup(i) == event.group_id:
            List.append(i)
    if len(List) == 0:
        await lg_showout.finish("现在本群还没有洛谷卷王哦~")
    text = f"当前本群洛谷卷王有{len(List)}位："
    idx = 0
    for i in List:
        idx += 1
        text = text + f"\n{idx}:{i}"
        if idx == 10:
            text = text + f"\n......"
            break
    await lg_showout.finish(text)

@bukanle.handle()
async def bukanle_handler(bot: Bot, event: Event):
    name = str(event.get_message())[6:].strip().casefold().title()
    if names.getname(name) != -1:
        name = names.getname(name)
    # if event.get_user_id() not in bot.config.superusers:
    #     await bukanle.finish("只有超管才能指挥我~")
    if name.casefold().title() not in Codeforces.getall():
        await bukanle.finish("没人在看这位卷王哦~")
    Codeforces.delpeople(name)
    await bukanle.finish(f"好的，我已经没有在看CF卷王{name}啦！")


@showout.handle()
async def showout_handler(bot: Bot, event: GroupMessageEvent):
    List = []
    for i in Codeforces.getall():
        if Codeforces.getGroup(i) == event.group_id:
            List.append(i)
    if len(List) == 0:
        await showout.finish("当前本群CF还没有卷王哦~")
    text = f"现在本群CF卷王有{len(List)}位："
    idx = 0
    for i in List:
        idx += 1
        text = text + f"\n{idx}:{i}"
        if idx == 10:
            text = text + "\n......"
            break
    await showout.finish(text)