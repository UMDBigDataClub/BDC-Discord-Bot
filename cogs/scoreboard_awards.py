import discord
from discord.ext import commands
from cogs.scoreboard import Scoreboard

class ScoreboardAwards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sb = Scoreboard()
        self.prev_author = ""
        self.cur_author = ""
        self.prev_committer = ""


    @commands.command(name='scoreboard')
    async def scoreboard(self, ctx):
        embed = discord.Embed(title="Big Data Club Scoreboard", description="Check out who's leading the pack in points this semester!", color=0x3357FF)
        embed.add_field(name="**Top Scorers**", value="```" + self.sb.display() + "```")
        await ctx.send(embed=embed)
        # Prints the score of everyone in the scoreboard.csv file


    @commands.command(name='scoreboard_everyone')
    async def scoreboard_everyone(self, ctx):
        embed = discord.Embed(title="Big Data Club Scoreboard - All Users", description="This scoreboard includes admins as well as the users eligible for prizes.", color=0x3357FF)
        embed.add_field(name="**Top Scorers**", value="```" + self.sb.display(non_participating=True) + "```")
        await ctx.send(embed=embed)


    @commands.command(name='scoreboard_all_time')
    async def scoreboard_all_time(self, ctx):
        embed = discord.Embed(title="Big Data Club Scoreboard - All Time", description="This shows the total scores attained by all BDC members since time immemorial", color=0x3357FF)
        embed.add_field(name="**Top Scorers**", value="```" + self.sb.display(all_time=True, non_participating=True) + "```")
        await ctx.send(embed=embed)


    @commands.command(name='score_all_time')
    async def scoreboard_all_time(self, ctx, username):
        await ctx.send(self.sb.display(name=username, all_time=True))


    @commands.command(name='score')
    async def scoreboard_all_time(self, ctx, username):
        await ctx.send(self.sb.display(name=username))


    @commands.command(name='add')
    async def add(self, ctx, username, value):
        if 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.add(username, int(value))


    @commands.command(name='set_github')
    async def set_github(self, ctx, github, username=None):
        if not username:
            self.sb.update(name=ctx.author.name, github=github)
        elif 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.update(name=username, github=github)


    @commands.command(name='set_email')
    async def set_email(self, ctx, email, username=None):
        if not username:
            self.sb.update(name=ctx.author.name, email=email)
        elif 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.update(name=username, email=email)


    @commands.command(name='set_participating')
    async def set_participating(self, ctx, participating_true_or_false, username=None):
        if not username:
            self.sb.update(name=ctx.author.name, participating=participating_true_or_false)
        elif 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.update(name=username, participating=participating_true_or_false)


    @commands.command(name='add_user')
    async def add_user(self, ctx, name, email=None, github=None):
        if 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.add_user(name, email, github)


    @commands.command(name='remove_user')
    async def remove_user(self, ctx, name):
        if 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.remove_user(name)


    @commands.command(name='add_award')
    async def add_award(self, ctx, award, description, points):
        print(points)
        self.sb.add_award(award, description, points)


    @commands.command(name='set_award_desc')
    async def set_award_desc(self, ctx, award, description=None):
        self.sb.edit_award(award, description=description)


    @commands.command(name='set_award_points')
    async def set_award_points(self, ctx, award, points=None):
        self.sb.edit_award(award, points=points)


    @commands.command(name='remove_award')
    async def remove_award(self, ctx, award):
        self.sb.remove_award(award)


    @commands.command(name='awards')
    async def awards(self, ctx):
        embed = discord.Embed(title="Scoreboard Awards",
                              description="List of potential tasks to win points on the scoreboard.",
                              color=0x3357FF)
        embed.add_field(name="*Points Available*", value="" + self.sb.display_awards() + "")
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.sb.add_user(member.name)


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        if message.author != "BDC-Bot" and message.author != "GitHub" and not message.content.startswith("!"):
            self.prev_author = self.cur_author
            self.cur_author = message.author.name

        # Give members one point for each message, but only if they are not posting multiple times in a row
        if self.cur_author != self.prev_author and self.prev_author != "" and not message.content.startswith(
                '/') and not message.content.startswith('\'') and not message.content.startswith('!'):
            self.sb.add(self.cur_author, self.sb.get_award_value("Posting"))

        # Give members 20 points for each GitHub commit, but only if they are nonconsecutive
        if message.author.name == "GitHub":
            committer = message.embeds[0].to_dict()["author"]["name"]
            # Test for previous committer
            if committer in self.sb.df.GitHub.values and (committer != self.prev_committer or committer != self.prev_author):
                self.prev_committer = committer
                name = self.sb.df[self.sb.df.GitHub == committer].Member.iloc[0]
                p = self.sb.get_award_value("Code Commit")
                self.sb.add(name, p)
                await message.channel.send(name + " has earned " + p + " points for committing to GitHub!")
        else:
            self.prev_committer = ""

def setup(bot):
    bot.add_cog(ScoreboardAwards(bot))
