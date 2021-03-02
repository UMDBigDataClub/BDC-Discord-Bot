from discord.ext import commands
from discord.utils import get

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


	@bot.command(name='setup')
	async def setup(ctx):
		githubMessage = discord.Embed(title="Please type your Github username", 
									description=" If you do not have a Github account, please type 'skip'. This request will timeout after 1 minute.",
									color = 0x3357FF)
		emailMessage = discord.Embed(title="Please type your Email address", 
									description="This request will timeout after 1 minute.",
									color = 0x3357FF)
		nameMessage = discord.Embed(title="Please type your First and Last name", 
									description="This will be used as your nickname within the server. This request will timeout after 1 minute.",
									color = 0x3357FF)
		githubLoggedMessage = discord.Embed(title="Thank you!", 
									description="Your Github account has been logged!",
									color = 0x3357FF)
		githubNotLoggedMessage = discord.Embed(title="User does not have a github account", 
									description="No Github account has been logged.",
									color = 0x3357FF)
		emailLoggedMessage = discord.Embed(title="Thank you!", 
									description="Your Email Address has been Logged.",
									color = 0x3357FF)
		nameLoggedMessage = discord.Embed(title="Thank You!", 
									description="Your name has been logged and your Nickname has been changed.",
									color = 0x3357FF)
		setupCompleteMessage = discord.Embed(title="Setup Complete!", 
									description="Congratualations! Your account setup is complete! Welcome to the University of Massachusetts Dartmouth data science discord server! Don't forget to head over to #role-assingment to assign yourself some roles.",
									color = 0x3357FF)
		sent = await ctx.send(embed = githubMessage)
		#non embed message below
		#sent = await ctx.send("`Please Enter Your Github Username. If you do not have a GitHub, Please type 'skip'.`")
		member = ctx.author
		try:
			github = await bot.wait_for("message",timeout = 60,check = lambda message: message.author == ctx.author and message.channel == ctx.channel)
			
			#users github is stored in githubUsername
			githubUsername = github.content
			########################################

			if github.content == 'skip':
				await ctx.send(embed = githubNotLoggedMessage,delete_after= 20)
				await sent.delete()
				await github.delete()
			else:
				await sent.delete()
				await github.delete()
				await ctx.send(embed = githubLoggedMessage,delete_after = 20)
				print("Github username logged")
		except asyncio.TimeoutError:
			await sent.delete()
		sent1 = await ctx.send(embed = emailMessage)
		try:
			email = await bot.wait_for("message",timeout = 60,check = lambda message: message.author == ctx.author and message.channel == ctx.channel)


			#users email is stored in emailAddress
			emailAddress = email.content
			########################################

			emailMsg = await ctx.send(embed = emailLoggedMessage,delete_after = 20)
			await sent1.delete()
			await email.delete()
			print("Email Address logged")
		except asyncio.TimeoutError:
			await sent1.delete()
		sent2 = await ctx.send(embed = nameMessage)
		try:
			name = await bot.wait_for("message",timeout = 60,check = lambda message: message.author == ctx.author
																					and message.channel == ctx.channel)

			realName = name.content
			await sent2.delete()
			await ctx.send(embed = nameLoggedMessage,delete_after = 20)
			print("name logged")
			await name.delete()
			await member.edit(nick = realName)
			await ctx.send(embed = setupCompleteMessage,delete_after= 40)
			await ctx.send(":bird: Doot! Doot! :bird:", delete_after =40)
		except asyncio.TimeoutError:
			await sent2.delete()
def setup(bot):
    bot.add_cog(Setup(bot))


			 




