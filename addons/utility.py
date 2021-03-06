import discord
from discord.ext import commands
import os
import sys

class Utility:
    """Utility bot commands."""
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))  
    
    @commands.command()
    async def test(self):
        """A test command."""
        embed = discord.Embed(title="testing", description="Testing")
        embed.add_field(name="Notes", value="Testing!", inline=False)
        embed.colour = discord.Colour(0x00FFFF)            
        await self.bot.say("", embed=embed)

    @commands.has_permissions(ban_members=True)    
    @commands.command()
    async def restart(self):
        """Restarts the bot."""
        await self.bot.say("Restarting...")
        sys.exit(0)

    @commands.command(pass_context=True)
    async def support(self, ctx):
        """Use to access the support channel"""
        await self.bot.delete_message(ctx.message)
        found_member = ctx.message.author
        member_roles = found_member.roles
        await self.bot.add_roles(found_member, self.bot.support_role)
        embed = discord.Embed(description="<@{1.id}> | {0.name}#{0.discriminator} accessed <#336761748159987713>".format(ctx.message.author, found_member))
        await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
        try:
            await self.bot.send_message(found_member, "You now have access to <#336761748159987713>")
        except discord.errors.Forbidden:
            pass
            
    @commands.command(pass_context=True)
    async def unsupport(self, ctx):
        """Use to remove access to the support channel"""
        await self.bot.delete_message(ctx.message)
        found_member = ctx.message.author
        member_roles = found_member.roles
        await self.bot.remove_roles(found_member, self.bot.support_role)
        embed = discord.Embed(description="<@{1.id}> | {0.name}#{0.discriminator} left <#336761748159987713>".format(ctx.message.author, found_member))
        await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
        try:
            await self.bot.send_message(found_member, "You have left <#336761748159987713>")
        except discord.errors.Forbidden:
            pass
            
    @commands.command(pass_context=True)
    async def about(self, ctx):
        """Information about Goku"""
        await self.bot.delete_message(ctx.message)
        embed = discord.Embed(description="Goku is a shitty bot created by <@175456582098878464> and <@177939404243992578> for use on the Nintendo Homebrew Idiot Log server. \nYou can view the source code [here](https://github.com/LyricLy/Goku/)")
        await self.bot.say(embed=embed)
            
    @commands.command(pass_context=True)
    async def derek(self, ctx):
        """Get your Daily Derek today!"""
        await self.bot.delete_message(ctx.message)
        found_member = ctx.message.author
        member_roles = found_member.roles
        await self.bot.add_roles(found_member, self.bot.derek_role)
        embed = discord.Embed(description="<@{1.id}> | {0.name}#{0.discriminator} has chosen to meme about <#357720803988733952>".format(ctx.message.author, found_member))
        await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
        try:
            await self.bot.send_message(found_member, "You can now meme about derek in <#357720803988733952>!")
        except discord.errors.Forbidden:
            pass
            
    @commands.command(pass_context=True)
    async def underek(self, ctx):
        """No more daily derek"""
        await self.bot.delete_message(ctx.message)
        found_member = ctx.message.author
        member_roles = found_member.roles
        await self.bot.remove_roles(found_member, self.bot.derek_role)
        embed = discord.Embed(description="<@{1.id}> | {0.name}#{0.discriminator} has chosen to leave <#357720803988733952>".format(ctx.message.author, found_member))
        await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
        try:
            await self.bot.send_message(found_member, "You don't want to derek meme anymore?")
        except discord.errors.Forbidden:
            pass
            
def setup(bot):
    bot.add_cog(Utility(bot))
