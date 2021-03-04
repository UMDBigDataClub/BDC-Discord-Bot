from discord.ext import commands
from discord.utils import get

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # reaction roles, assigns roles based on emoji used for the reaction of a specific message
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message_id = 'React with an emoji to be assigned a role, choose all that apply.'
        message = reaction.message.content
        channel = reaction.message.channel
        Guild = reaction.message.guild
        role_member = 809832119294492692
        mathematics_role = 812062467198025748
        datascience_role = 812057868743868426
        computerscience_role = 812058129261002792
        business_role = 812058223582117949
        undergraduate_role = 812059883469537290
        graduate_role = 812059646092115989
        colorblind_role = 804467590931808298

        # replace this role id with the role id from BDC discord server, I used this other role on my testing server
        # add more roles by copying the role id in discord, for example you could add a data sceince role and copy the id into data_science.
        member_role = get(Guild.roles, id=role_member)
        math_role = get(Guild.roles, id=mathematics_role)
        data_role = get(Guild.roles, id=datascience_role)
        compsci_role = get(Guild.roles, id=computerscience_role)
        suits_role = get(Guild.roles, id=business_role)
        undergrad_role = get(Guild.roles, id=undergraduate_role)
        grad_role = get(Guild.roles, id=graduate_role)
        color_role = get(Guild.roles, id=colorblind_role)
        # each role will need an emoji to go along with it.
        if message_id == message and reaction.emoji == '👍':
            channel = reaction.message.channel
            await user.add_roles(member_role)
        elif message_id == message and reaction.emoji == '🧮':
            channel = reaction.message.channel
            await user.add_roles(math_role)
        elif message_id == message and reaction.emoji == '📊':
            channel = reaction.message.channel
            await user.add_roles(data_role)
        elif message_id == message and reaction.emoji == '🖥️':
            channel = reaction.message.channel
            await user.add_roles(compsci_role)
        elif message_id == message and reaction.emoji == '👔':
            channel = reaction.message.channel
            await user.add_roles(suits_role)
        elif message_id == message and reaction.emoji == '📚':
            channel = reaction.message.channel
            await user.add_roles(undergrad_role)
        elif message_id == message and reaction.emoji == '👨‍🎓':
            channel = reaction.message.channel
            await user.add_roles(grad_role)
        elif message_id == message and reaction.emoji == '🌈':
            channel = reaction.message.channel
            await user.add_roles(color_role)

def setup(bot):
    bot.add_cog(Roles(bot))