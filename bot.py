import discord
from discord.ext import commands

import traceback

import config

bot = commands.Bot(command_prefix=config.PREFIX, intents=discord.Intents.all())
bot.config = config
bot.cmdlog = True
bot.http.token = config.TOKEN

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Ready....'))
    
    bot._ext = ["jishaku", "cogs.cmds"]
    
    for ext in bot._ext:
        try:
            bot.load_extension(ext)
        except Exception as exc:
            print(f"[Error] {ext} load failed → {exc}")
        else:
            print(f"[System] {ext} load")

    await bot.change_presence(activity=discord.Activity(name='りんごさーばー', type=discord.ActivityType.playing))
    print('[System] Enabled RingoServerBot v1.0')

#cmdlog
@bot.event
async def on_command(ctx):
    if isinstance(ctx.message.channel, discord.DMChannel):
        e = discord.Embed(title="CommandLog", color=0x2ecc71, timestamp=ctx.message.created_at)
        e.add_field(name="実行場所", value="DM")
        e.add_field(name="実行ユーザー名", value=f"{ctx.author} \n({ctx.author.id})")
        e.add_field(name="実行日時:", value=ctx.message.created_at.strftime('%Y/%m/%d %H:%M:%S'))
        e.add_field(name="実行コマンド", value=f"```{ctx.message.content}```", inline=False)
        e.add_field(name="実行チャンネル", value=f"@{ctx.author.name} ({ctx.channel.id})")
        e.set_thumbnail(url=ctx.author.avatar_url_as(static_format="png"))
        await bot.get_channel(config.LOGCH).send(embed=e)
        
        if bot.cmdlog:
            print(f"[Log] {ctx.author} ({ctx.author.id}) -> {ctx.message.content} in @{ctx.author.name} ({ctx.channel.id})")
    else:
        e = discord.Embed(title="CommandLog", color=0x2ecc71, timestamp=ctx.message.created_at)
        e.set_thumbnail(url=ctx.author.avatar_url_as(static_format="png"))
        e.add_field(name="実行サーバー", value=f"{ctx.guild.name} \n({ctx.guild.id})")
        e.add_field(name="実行ユーザー名", value=f"{ctx.author} \n({ctx.author.id})")
        e.add_field(name="実行日時", value=ctx.message.created_at.strftime('%Y/%m/%d %H:%M:%S'))
        e.add_field(name="実行コマンド", value=f"```{ctx.message.content}```", inline=False)
        e.add_field(name="実行チャンネル", value=f"#{ctx.channel.name} \n({ctx.channel.id})")
        await bot.get_channel(config.LOGCH).send(embed=e)
        
        if bot.cmdlog:
            print(f"[Log] {ctx.author} ({ctx.author.id}) -> {ctx.message.content} in {ctx.guild.name} ({ctx.guild.id}) #{ctx.channel.name} ({ctx.channel.id})")

#error log
@bot.event
async def on_command_error(ctx, error):
    #command error handling by jun50

    e = discord.Embed(title="Error Information", color=0x2ecc71, timestamp=ctx.message.created_at)
                                
    traceback_error = f"```{''.join(traceback.TracebackException.from_exception(error).format())}```"
    if len(str(traceback_error)) >= 1024:
        er = f"```py\n{error}\n```"
    else:
        er = traceback_error

    if isinstance(ctx.message.channel, discord.DMChannel):
        e.set_thumbnail(url=ctx.author.avatar_url_as(static_format=("png")))
        e.add_field(name="実行場所", value=f"DM")
        e.add_field(name="実行ユーザー名", value=f"{ctx.author} \n({ctx.author.id})")
        e.add_field(name="実行日時", value=ctx.message.created_at.strftime('%Y/%m/%d %H:%M:%S'))
        e.add_field(name="実行コマンド", value=f"```{ctx.message.content}```")
        e.add_field(name="エラー内容", value=er, inline=False)
    else:
        e.set_thumbnail(url=ctx.author.avatar_url_as(static_format=("png")))
        e.add_field(name="実行サーバー", value=f"{ctx.guild.name} \n({ctx.guild.id})")
        e.add_field(name="実行ユーザー名", value=f"{ctx.author} \n({ctx.author.id})")
        e.add_field(name="実行日時", value=ctx.message.created_at.strftime('%Y/%m/%d %H:%M:%S'))
        e.add_field(name="実行コマンド", value=f"```{ctx.message.content}```")
        e.add_field(name="チャンネル",value=f"{ctx.channel.mention} \n({ctx.channel.id})")
        e.add_field(name="メッセージリンク", value="[{0}]({0})".format(ctx.message.jump_url.replace("discordapp", "discord")), inline=False)
        e.add_field(name="エラー内容", value=er, inline=False)
        
    log = await bot.get_channel(config.ERRORCH).send(embed=e)
    
    e = discord.Embed(title="Error - unknown", description=f"{er}", color=0x2ecc71, timestamp=ctx.message.created_at)
    e.set_footer(text=f"エラーID: {log.id}")
                                
    try:
        return await ctx.reply(embed=e)
    except:
        try:
            return await ctx.author.send(embed=e)
        except:
            return

#起動時の処理
print(f"[System] Enabling RingoServerBot v{config.VERSION}")
bot.run(bot.http.token)
