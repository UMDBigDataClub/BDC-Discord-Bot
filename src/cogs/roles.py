from discord.ext import commands
from discord.utils import get

class Roles(commands.Cog):
    message_id = 'React with an emoji to be assigned a role, choose all that apply.'
    role_channel = "role-assignment"
    role_member = 809832119294492692
    mathematics_role = 812062467198025748
    datascience_role = 812057868743868426
    computerscience_role = 812058129261002792
    business_role = 812058223582117949
    undergraduate_role = 812059883469537290
    graduate_role = 812059646092115989
    colorblind_role = 804467590931808298

    def __init__(self, bot):
        self.bot = bot

    # reaction roles, assigns roles based on emoji used for the reaction of a specific message
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)

        if channel.name == "role-assignment":
            Guild = self.bot.get_guild(payload.guild_id)
            user = payload.member
            # replace this role id with the role id from BDC discord server, I used this other role on my testing server
            # add more roles by copying the role id in discord, for example you could add a data sceince role and copy the id into data_science.

            # each role will need an emoji to go along with it.
            if payload.emoji.name == "🧮":
                math_role = get(Guild.roles, id=self.mathematics_role)
                await user.add_roles(math_role, atomic = True)
            elif payload.emoji.name == '📊':
                data_role = get(Guild.roles, id=self.datascience_role)
                await user.add_roles(data_role, atomic = True)
            elif payload.emoji.name == '🖥️':
                compsci_role = get(Guild.roles, id=self.computerscience_role)
                await user.add_roles(compsci_role, atomic = True)
            elif payload.emoji.name == '👔':
                suits_role = get(Guild.roles, id=self.business_role)
                await user.add_roles(suits_role, atomic = True)
            elif payload.emoji.name == '📚':
                undergrad_role = get(Guild.roles, id=self.undergraduate_role)
                await user.add_roles(undergrad_role, atomic = True)
            elif payload.emoji.name == '👨‍🎓':
                grad_role = get(Guild.roles, id=self.graduate_role)
                await user.add_roles(grad_role, atomic = True)
            elif payload.emoji.name == '🌈':
                color_role = get(Guild.roles, id=self.colorblind_role)
                await user.add_roles(color_role, atomic = True)

def setup(bot):
    bot.add_cog(Roles(bot))