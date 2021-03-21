import discord
from discord.ext import tasks, commands
from scoreboard import Scoreboard

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
        else:
            await ctx.send("Sorry, you are not authorized to use this command")


    @commands.command(name='set_github')
    async def set_github(self, ctx, github, username=None):
        if not username:
            self.sb.update(name=ctx.author.name, github=github)
        elif 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.update(name=username, github=github)
        else:
            await ctx.send("Sorry, you are not authorized to use this command")


    @commands.command(name='set_email')
    async def set_email(self, ctx, email, username=None):
        if not username:
            self.sb.update(name=ctx.author.name, email=email)
        elif 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.update(name=username, email=email)
        else:
            await ctx.send("Sorry, you are not authorized to use this command")


    @commands.command(name='set_participating')
    async def set_participating(self, ctx, participating_true_or_false, username=None):
        if not username:
            self.sb.update(name=ctx.author.name, participating=participating_true_or_false)
        elif 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.update(name=username, participating=participating_true_or_false)
        else:
            await ctx.send("Sorry, you are not authorized to use this command")


    @commands.command(name='add_user')
    async def add_user(self, ctx, name, email=None, github=None):
        if 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.add_user(name, email, github)
        else:
            await ctx.send("Sorry, you are not authorized to use this command")


    @commands.command(name='remove_user')
    async def remove_user(self, ctx, name):
        if 'Administrator' in [role.name for role in ctx.author.roles]:
            self.sb.remove_user(name)
        else:
            await ctx.send("Sorry, you are not authorized to use this command")


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

    @commands.command(name='display_commits')
    async def display_commits(self, ctx, name=None):
        embed = discord.Embed(title="Total Commits",
                              description="This leaderboard lists members with the highest number of total GitHub commits", color=0x3357FF)
        embed.add_field(name="**Top Committers**", value="```" + self.sb.display_commits(name=name) + "```")
        await ctx.send(embed=embed)


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
                self.sb.add_commit(name)
                await message.channel.send(name + " has earned " + str(p) + " points for committing to GitHub!")
        else:
            self.prev_committer = ""


    @commands.Cog.listener()
    async def on_member_join(self, member):
        #Add the user to the scoreboard
        self.sb.add_user(member.name)

        #Find the lobby
        lobby = member.guild.system_channel

        #Define messages that the self.bot sends
        githubMessage = discord.Embed(title="Please type your Github username so we can give you awards for participating in projects.",
                                          description=" If you do not have a Github account, please type 'skip'. This request will timeout after 1 minute.",
                                          color=0x3357FF)

        emailMessage = discord.Embed(title="Please type your Email address to be added to our email list.",
                                     description="If you do not want to enter your email account, please type 'skip'. This request will timeout after 1 minute.",
                                     color=0x3357FF)
        nameMessage = discord.Embed(title="Please type your First and Last name",
                                    description="This will be used as your nickname within the server. This request will timeout after 1 minute.",
                                    color=0x3357FF)
        githubLoggedMessage = discord.Embed(title="Thank you!",
                                            description="Your Github account has been logged!",
                                            color=0x3357FF)
        githubNotLoggedMessage = discord.Embed(title="User does not have a GitHub account",
                                               description="No Github account has been logged.",
                                               color=0x3357FF)
        emailLoggedMessage = discord.Embed(title="Thank you!",
                                           description="Your Email Address has been logged!",
                                           color=0x3357FF)
        emailNotLoggedMessage = discord.Embed(title="User does not have an email account",
                                               description="No email account has been logged.",
                                               color=0x3357FF)
        nameLoggedMessage = discord.Embed(title="Thank You!",
                                          description="Your name has been logged and your Nickname has been changed.",
                                          color=0x3357FF)
        setupCompleteMessage = discord.Embed(title="Setup Complete!",
                                             description="Congratulations! Your account setup is complete! Welcome to the University of Massachusetts Dartmouth Data Science Discord Server! Don't forget to head over to #role-assignment to assign yourself some roles.",
                                             color=0x3357FF)
        if member.name not in self.sb.df.Member.values:
            #Ask for GitHub and collect response
            sent = await lobby.send(embed=githubMessage)
            try:
                github = await self.bot.wait_for("message", timeout=60, check=lambda
                    message: message.author.name == member.name and message.channel.name == lobby.name)


                # users github is stored in githubUsername
                githubUsername = github.content
                ########################################

                if github.content == 'skip':
                    await lobby.send(embed=githubNotLoggedMessage, delete_after=20)
                    await sent.delete()
                    await github.delete()
                else:
                    self.sb.update(member.name,github = githubUsername)
                    await sent.delete()
                    await github.delete()
                    await lobby.send(lobby,embed=githubLoggedMessage, delete_after=20)
                    print("Github username logged")
            except tasks.asyncio.TimeoutError:
                await sent.delete()
            #Collect and store user email
            sent1 = await lobby.send(embed=emailMessage)
            try:
                email = await self.bot.wait_for("message", timeout=60, check=lambda
                    message: message.author.name == member.name and message.channel.name == lobby.name)

                # users email is stored in emailAddress
                emailAddress = email.content
                ########################################
                if email.content == 'skip':
                    await lobby.send(embed=emailNotLoggedMessage, delete_after=20)
                    await sent1.delete()
                    await email.delete()
                else:
                    emailMsg = await lobby.send(embed=emailLoggedMessage, delete_after=20)
                    self.sb.update(member.name,github = emailAddress)
                    await sent1.delete()
                    await email.delete()
                    print("Email Address logged")
            except tasks.asyncio.TimeoutError:
                await sent1.delete()
            #Collect and assign user name
            sent2 = await lobby.send(embed=nameMessage)
            try:
                name = await self.bot.wait_for("message", timeout=60, check=lambda message: message.author.name == member.name and message.channel.name == lobby.name)

                realName = name.content
                await sent2.delete()
                await lobby.send(embed=nameLoggedMessage, delete_after=20)
                print("name logged")
                await name.delete()
                await member.edit(nick=realName)
                await lobby.send(embed=setupCompleteMessage, delete_after=40)
                await lobby.send(":bird: Doot! Doot! :bird:", delete_after=40)
            except tasks.asyncio.TimeoutError:
                await sent2.delete()
        else:
            await lobby.send("Welcome Back, " + member.name + "!", delete_after=20)
def setup(bot):
    bot.add_cog(ScoreboardAwards(bot))
