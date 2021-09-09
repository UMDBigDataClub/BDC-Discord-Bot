import discord
from discord.ext import tasks, commands
import pandas as pd
import os
from dotenv import load_dotenv
import boto3

class DataCollection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #Load the S3 research bucket data into memory
        load_dotenv()
        self.s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-2',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

        obj = self.s3.Bucket('bdc-research').Object("Big-Data-Club/data.tsv").get()
        self.df = pd.read_csv(obj["Body"], index_col=0, sep = "\t")
        self.df.to_csv("data.csv", sep = "\t")

    #Function to update data in S3
    def update_S3(self):
        self.df.to_csv("data.tsv", sep = "\t")
        self.s3.Bucket('bdc-research').upload_file(Filename='data.tsv', Key='Big-Data-Club/data.tsv')


    #Listen for any messages that users send and record them in the dataframe
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.channel == "question-and-answer":
            self.df.append({"Time": message.created_at, "User": message.author, "Message": message.clean_content, "Pos_Rating": 0, "Neg_Rating": 0, "Question": False}, ignore_index = True, inplace = True)
            self.update_S3()

    #Listen for any reactions that affect a message's rating
    #NOTE: message must be in internal message cache for reaction to be recorded

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        if reaction.emoji.name == "positive":
            self.df.loc[self.df.index[self.df.Message == msg.clean_content], "Pos_Rating"] += 1
        if reaction.emoji.name == "negative":
            self.df.loc[self.df.index[self.df.Message == msg.clean_content], "Neg_Rating"] += 1
        if reaction.emoji.name == "question":
            self.df.loc[self.df.index[self.df.Message == msg.clean_content], "Question"] = True
        if reaction.emoji.name

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        msg = reaction.message
        if reaction.emoji.name == "positive":
            self.df.loc[self.df.index[self.df.Message == msg.clean_content], "Pos_Rating"] -= 1
        if reaction.emoji.name == "negative":
            self.df.loc[self.df.index[self.df.Message == msg.clean_content], "Neg_Rating"] -= 1
        if reaction.emoji.name == "question":
            self.df.loc[self.df.index[self.df.Message == msg.clean_content], "Question"] = False


def setup(bot):
    bot.add_cog(DataCollection(bot))