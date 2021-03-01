#This class defines the Scoreboard data structure and its associated methods

import pandas as pd
import os
from dotenv import load_dotenv
import boto3


class Scoreboard:

    standard_display = ["Member","Score"]
    all_time_display = ["Member","AllTime"]

    #Load up S3 and create the scoreboard as "df"
    def __init__(self):
        load_dotenv()
        self.s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-2',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

        obj = self.s3.Bucket('bdc-scoreboard').Object("scoreboard.csv").get()
        self.df = pd.read_csv(obj["Body"], index_col=0)
        self.df.to_csv("scoreboard.csv")

        obj = self.s3.Bucket('bdc-scoreboard').Object("awards.csv").get()
        self.awards = pd.read_csv(obj["Body"], index_col=0, dtype={"Award": 'string', 'Description': 'string', 'Point Value': 'Int64'})
        self.awards.to_csv("awards.csv")


    #Add points to the specified user
    def add(self,name,value):
        self.df.at[self.df[self.df.Member == name].index[0], "Score"] += value
        self.df.at[self.df[self.df.Member == name].index[0], "AllTime"] += value
        self.df.sort_values("Score", axis=0, inplace = True, ascending=False)
        self.df.reset_index(drop=True, inplace = True)
        self.df.to_csv("scoreboard.csv")
        self.s3.Bucket('bdc-scoreboard').upload_file(Filename='scoreboard.csv', Key='scoreboard.csv')


    #Display the scoreboard according to specified variables
    def display(self, name = None, all_time = False, non_participating = False):
        #For displaying specific users
        if name:
            temp_df = self.df.sort_values("AllTime", axis=0, ascending=False).reset_index(drop=True)
            temp_df = temp_df[temp_df.Member == name]
            if self.df[self.df.Member == name]["Participating"].values[0]:
                temp_df = self.df[self.df.Participating.values].sort_values("Score", axis=0, ascending=False).reset_index(drop=True)
                temp_df = temp_df[temp_df.Member == name]
            else:
                temp_df = self.df.sort_values("Score", axis=0, ascending=False).reset_index(drop=True)
                temp_df = temp_df[temp_df.Member == name]

            if all_time:
                return temp_df[self.all_time_display].to_string()
            else:
                return temp_df[self.standard_display].to_string()
        #For displaying the entire scoreboard
        else:
            if non_participating and all_time:
                return self.df[self.all_time_display].sort_values("AllTime", axis=0, ascending=False).reset_index(drop=True).to_string()
            elif non_participating:
                return self.df[self.standard_display].sort_values("Score", axis=0, ascending=False).reset_index(drop=True).to_string()
            elif all_time:
                return self.df[self.df.Participating][self.all_time_display].sort_values("AllTime", axis=0, ascending=False).reset_index(drop=True).to_string()
            else:
                return self.df[self.df.Participating][self.standard_display].sort_values("Score", axis=0, ascending=False).reset_index(drop=True).to_string()

    #Add a new user to the scoreboard
    def add_user(self, name, github = None, email = None):
        self.df = self.df.append(pd.DataFrame({"Member": [name], "Score": [0], "AllTime": [0], "GitHub": github, "Email": email, "Participating": True}), ignore_index=True, sort=True)
        self.df.to_csv("scoreboard.csv")
        self.s3.Bucket('bdc-scoreboard').upload_file(Filename='scoreboard.csv', Key='scoreboard.csv')

    #Edit a user's github, email, or participation status
    def update(self, name, github = None, email = None, participating = None):
        if github:
            self.df.at[self.df[self.df.Member == name].index[0], "GitHub"] = github
        if email:
            self.df.at[self.df[self.df.Member == name].index[0], "Email"] = email
        if participating:
            self.df.at[self.df[self.df.Member == name].index[0], "Participating"] = participating == "True"
        self.df.to_csv("scoreboard.csv")
        self.s3.Bucket('bdc-scoreboard').upload_file(Filename='scoreboard.csv', Key='scoreboard.csv')

    def remove_user(self, name):
        self.df = self.df[self.df.Member != name]
        self.df.to_csv("scoreboard.csv")
        self.s3.Bucket('bdc-scoreboard').upload_file(Filename='scoreboard.csv', Key='scoreboard.csv')

    #Add award
    def add_award(self, award, description, points):
        print(points)
        self.awards = self.awards.append(pd.DataFrame({"Award": [award], "Description": [description], "Point Value": [points]}), ignore_index=True, sort=True)
        self.awards.to_csv("awards.csv")
        self.s3.Bucket('bdc-scoreboard').upload_file(Filename='awards.csv', Key='awards.csv')

    #Edit award
    def edit_award(self, award, description = None, points = None):
        if description:
            self.awards.at[self.awards[self.awards.Award == award].index[0], "Description"] = description

        if points:
            self.awards.at[self.awards[self.awards.Award == award].index[0], "Point Value"] = int(points)

        self.awards.to_csv("awards.csv")
        self.s3.Bucket('bdc-scoreboard').upload_file(Filename='awards.csv', Key='awards.csv')

    #Remove an award
    def remove_award(self, award):
        self.awards = self.awards[self.awards.Award != award]
        self.awards.to_csv("awards.csv")
        self.s3.Bucket('bdc-scoreboard').upload_file(Filename='awards.csv', Key='awards.csv')

    #Display awards
    def display_awards(self):
        self.awards.sort_values("Point Value", inplace=True)
        output = ""
        for i in self.awards.index:
            output += "**" + self.awards.loc[i,"Award"].ljust(15) + "(" + str(self.awards.loc[i,"Point Value"]) + ")** : " + self.awards.loc[i,"Description"] + "\n"
        return output

    #Get point value of an award
    def get_award_value(self, award):
        return self.awards[self.awards.Award==award].iloc[0,2]

    def display_award(self, award):
        self.awards = self.awards[self.awards.Award != 'award']
        self.awards.to_csv("awards.csv")
        self.s3.Bucket('bdc-scoreboard').upload_file(Filename='awards.csv', Key='awards.csv')