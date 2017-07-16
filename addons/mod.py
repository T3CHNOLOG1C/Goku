import discord
from discord.ext import commands
import os
import sys
import json

class Moderation:
    """Bot commands for moderation."""
    def __init__(self, bot):
        self.bot = bot
        with open('saves/warns.json', 'r+') as f:
            self.warns = json.load(f)
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        
    def find_user(self, user, ctx):
        found_member = self.bot.server.get_member(user)
        if not found_member:
            found_member = self.bot.server.get_member_named(user)
        if not found_member:
            try:
                found_member = ctx.message.mentions[0]
            except IndexError:
                pass
        if not found_member:
            return None
        else:
            return found_member
    
    @commands.has_permissions(kick_members=True)    
    @commands.command(pass_context=True)
    async def kick(self, ctx, member, *, reason=""):
        """Kick a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if reason:
                reason_msg = "The given reason was: {}".format(reason)
            else:
                reason_msg = "No reason was given."
            await self.bot.send_message(found_member, "You have been kicked by user {0.name}#{0.discriminator}.\n{2}\nYou can rejoin the server with this link: https://discord.gg/hHHKPFz".format(ctx.message.author, self.bot.rules_channel.mention, reason_msg))
            await self.bot.kick(found_member)
            await self.bot.say("Successfully kicked user {0.name}#{0.discriminator}!".format(found_member))
            embed = discord.Embed(description="<@{0.id}> | {0.name}#{0.discriminator} kicked user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
    
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def ban(self, ctx, member, *, reason=""):
        """Ban a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if reason:
                reason_msg = "The given reason was: {}".format(reason)
            else:
                reason_msg = "No reason was given."
            await self.bot.send_message(found_member, "You have been banned by user {0.name}#{0.discriminator}.\n{2}\nIf you feel that you did not deserve this ban, send a direct message to one of the staff on the Server Admins list in {1}.\nIn the rare scenario that you do not have the entire staff list memorized, YourLocalLyric#5752 and Griffin#2329 are two choices you could use.".format(ctx.message.author, self.bot.rules_channel.mention, reason_msg))
            await self.bot.ban(found_member)
            await self.bot.say("Successfully banned user {0.name}#{0.discriminator}!".format(found_member))
            embed = discord.Embed(description="<@{0.id}> | {0.name}#{0.discriminator} banned user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def mute(self, ctx, member, *, reason=""):
        """Mute a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.add_roles(found_member, self.bot.muted_role)
            if reason:
                reason_msg = "The given reason was: {}".format(reason)
            else:
                reason_msg = "No reason was given."
            await self.bot.say("Successfully muted user {0.name}#{0.discriminator}!".format(found_member))
            embed = discord.Embed(description="<@{0.id}> | {0.name}#{0.discriminator} muted user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            await self.bot.send_message(found_member, "You have been muted by user {0.name}#{0.discriminator}.\n{2}\nIf you feel that you did not deserve this mute, send a direct message to one of the staff on the Server Admins list in {1}.".format(ctx.message.author, self.bot.rules_channel.mention, reason_msg))
            
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def unmute(self, ctx, *, member):
        """Unmute a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if self.bot.muted_role in found_member.roles:
                await self.bot.remove_roles(found_member, self.bot.muted_role)
                embed = discord.Embed(description="{0.name}#{0.discriminator} unmuted user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
                await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
                await self.bot.send_message(found_member, "You have been unmuted by user {0.name}#{0.discriminator}. Don't do it again!".format(ctx.message.author))
                await self.bot.say("Successfully unmuted user {0.name}#{0.discriminator}!".format(found_member))
            else:
                await self.bot.say("That user isn't muted!")
                
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def warn(self, ctx, member, *, reason):
        """Warn a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            owner = server.owner
            
            if self.bot.server_admin_role in found_member.roles and not found_member == owner:
                return await self.bot.say("You cannot warn a staff member!")
            try:
                self.warns[found_member.id]
            except KeyError:
                self.warns[found_member.id] = []
            self.warns[found_member.id].append(reason)
            reply_msg = "Warned user {}#{}. This is warn {}.".format(found_member.name, found_member.discriminator, len(self.warns[found_member.id]))
            private_message = "You have been warned by user {}#{}. The given reason was: `{}`\nThis is warn {}.".format(ctx.message.author.name, ctx.message.author.discriminator, reason, len(self.warns[found_member.id]))
            
            if len(self.warns[found_member.id]) >= 5:
                private_message += "\nYou were banned due to this warn. \nIf you feel that you did not deserve this ban, send a direct message to one of the staff on the Server Admins list in {1}.\nIn the rare scenario that you do not have the entire staff list memorized, YourLocalLyric#5752 and Griffin#2329 are two choices you could use."
                await self.bot.send_message(found_member, private_message)
                await self.bot.ban(found_member)
                reply_msg += " As a result of this warn, the user was banned."
                
            elif len(self.warns[found_member.id]) == 4:
                private_message += "\nYou were kicked due to this warn. You can rejoin the server with this link: https://discord.gg/hHHKPFz\nYour next warn will automatically ban you."
                await self.bot.send_message(found_member, private_message)
                await self.bot.kick(found_member)
                reply_msg += " As a result of this warn, the user was kicked. The next warn will automatically ban the user."
                
            elif len(self.warns[found_member.id]) == 3:
                private_message += "\nYou were kicked due to this warn. \nYou can rejoin the server with this link: https://discord.gg/hHHKPFz\nYour next warn will automatically kick you."
                await self.bot.send_message(found_member, private_message)
                await self.bot.kick(found_member)
                reply_msg += " As a result of this warn, the user was kicked. The next warn will automatically kick the user."
                
            elif len(self.warns[found_member.id]) == 2:
                private_message += "\nYour next warn will automatically kick you."
                await self.bot.send_message(found_member, private_message)
                reply_msg += " The next warn will automatically kick the user."
                
            elif len(self.warns[found_member.id]) == 1:
                await self.bot.send_message(found_member, private_message)
                
            await self.bot.say(reply_msg)
            embed = discord.Embed(description="{0.name}#{0.discriminator} warned user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            with open("saves/warns.json", "w+") as f:
                json.dump(self.warns, f)
                
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def listwarns(self, ctx, *, member):
        """List a member's warns."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            try:
                user_warns = self.warns[found_member.id]
                if user_warns:
                    embed = discord.Embed(title="Warns for user {}#{}".format(found_member.name, found_member.discriminator), description="")
                    for warn in user_warns:
                        embed.description += "• {}\n".format(warn)
                    embed.set_footer(text="There are {} warns in total.".format(len(user_warns)))
                    await self.bot.say("", embed=embed)
                else:
                    await self.bot.say("That user has no warns!")
            except KeyError:
                await self.bot.say("That user has no warns!")
                
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def clearwarns(self, ctx, *, member):
        """Clear a member's warns."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:            
            try:
                if self.warns[found_member.id]:
                    self.warns[found_member.id] = []
                    with open("saves/warns.json", "w+") as f:
                        json.dump(self.warns, f)
                    await self.bot.say("Cleared the warns of user {}#{}.".format(found_member.name, found_member.discriminator))
                    embed = discord.Embed(description="{0.name}#{0.discriminator} cleared warns of user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
                    await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
                    await self.bot.send_message(found_member, "All your warns have been cleared.")
                else:
                    await self.bot.say("That user has no warns!")
            except KeyError:
                await self.bot.say("That user has no warns!")
                
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def unwarn(self, ctx, member, *, reason):
        """Take a specific warn off a user."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:            
            try:
                if self.warns[found_member.id]:
                    try:
                        self.warns[found_member.id].remove(reason)
                        with open("saves/warns.json", "w+") as f:
                            json.dump(self.warns, f)
                        await self.bot.say("Removed `{}` warn of user {}#{}.".format(reason, found_member.name, found_member.discriminator))
                        embed = discord.Embed(description="{0.name}#{0.discriminator} took a warn off of user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
                        embed.add_field(name="Removed Warn", value="• " + reason)
                        await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
                    except ValueError:
                        await self.bot.say("{}#{} was never warned for the reason `{}`!".format(found_member.name, found_member.discriminator, reason))
                else:
                    await self.bot.say("That user has no warns!")
            except KeyError:
                await self.bot.say("That user has no warns!")
                
    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def uncontain(self, ctx, member):
        """Remove a member from #containment."""
        await self.bot.delete_message(ctx.message)
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.replace_roles(found_member, self.bot.unhelpful_jerks_role)
            embed = discord.Embed(description="{0.name}#{0.discriminator} moved user <@{1.id}> | {1.name}#{1.discriminator} out of <#335599294553915392>".format(ctx.message.author, found_member))
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            await self.bot.send_message(found_member, "Enjoy the server!")
            
    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def promote(self, ctx, member):
        """Upgrade to Neutron Stars."""
        await self.bot.delete_message(ctx.message)
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.replace_roles(found_member, self.bot.neutron_stars_role)
            embed = discord.Embed(description="{0.name}#{0.discriminator} promoted user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            await self.bot.send_message(found_member, "You now have the Neutron Stars role!")
            
def setup(bot):
    bot.add_cog(Moderation(bot))
