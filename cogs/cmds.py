import discord
from discord.ext import commands

import traceback
import time

class cmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.auth_first = bot.get_channel(612341252863688852)
        self.auth_end = bot.get_channel(612341302369189896)
        self.rule_ch = bot.get_channel(557445671351877633)
    
    #auth embed
    @commands.command()
    @commands.is_owner()
    async def authembed(self, ctx, channel:commands.TextChannelConverter=None):
        msg = await ctx.send("> 処理中...")
        
        if not channel:
            return await msg.edit(content=f"> チャンネルを入力してください。")
        
        if self.bot.config.AUTHEMBED:
            return await msg.edit(content="> すでに認証Embedがあります。")
            
        e = discord.Embed(title="Ringo Server Authentication", description=f"{self.rule_ch.mention} に同意する場合はリアクションをクリックしてください。", color=ctx.guild.me.color)
        
        m = await channel.send(embed=e)
        await m.add_reaction("✅")
        
        return await msg.edit(content=f"{channel.mention} に認証Embedを送信しました。")
    
    #reac
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.bot.config.AUTHEMBED:
            if str(payload.emoji) == "✅":
                print("[System] Role added.")
                await payload.member.add_roles(discord.utils.get(ctx.guild.roles, name="Checked"), reason="[System] Authentication first.")
    
    #auth
    @commands.command()
    async def auth(self, ctx):
        auth_role = discord.utils.get(ctx.guild.roles, name="Member")
        check_role =  discord.utils.get(ctx.guild.roles, name="Checked")
        
        if auth_role in ctx.author.roles:
            return await ctx.send("> すでに認証されています。")
        
        if check_role in ctx.author.roles:
            return await ctx.send("> すでに第一段階の認証が完了しています。")
        
        await ctx.author.add_roles(auth_role, reason="[System] Authentication complete.")

    #eval
    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, cmd=None):
        if not cmd:
            return await ctx.send("> 評価するコードを入力してください。")
    
        rt = "\n"
        if cmd.startswith("py"):
            cmd = cmd[5:-3]
        elif cmd.startswith(""):
            cmd = cmd[3:-3]
        elif cmd.startswith("python"):
            cmd = cmd[9:-3]
            
        txt = f'async def evdf(ctx,bot):{rt}{rt.join([f" {i}" for i in cmd.split(rt)])}' 
        try:
            exec(txt)
            rtn = await eval("evdf(ctx,self.bot)")
            await ctx.message.add_reaction("✅")
            if rtn:
                if isinstance(rtn,discord.Embed):
                    await ctx.send(embed=rtn)
                else:
                    await ctx.send(f"{rtn}")
        except:
            await ctx.message.add_reaction("❌")
            await ctx.send(embed=discord.Embed(title="Eval Command Error",description=f"py\n{traceback.format_exc(3)}\n", color=0x2ecc71))
    
    #stop
    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        msg = await ctx.send("> 処理中...")
        
        try:
            await self.bot.close()
        except Exception as exc:
            return await msg.edit(content=f"> エラー\n ```py\n{exc}\n```")
        else:
            return await msg.edit(content=f"> Botを停止します...")

    #ping
    @commands.command()
    async def ping(self, ctx):
        st = time.time()
        
        e = discord.Embed(title="Info - ping", description="Pinging...Please Wait....", color=0x2ecc71, timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=e)
        
        e.description = "ぽんぐっ！🏓"
        e.add_field(name="Ping", value=str(round(time.time()-st, 3) * 1000)+"ms")
        e.add_field(name="WebSocket", value=f"{round(self.bot.latency * 1000, 2)}ms")
        return await msg.edit(embed=e)

def setup(bot):
    bot.add_cog(cmds(bot))
