#This class defines the Scoreboard data structure and its associated methods

import pandas as pd
import os
from dotenv import load_dotenv
import boto3


class Scoreboard:

    standard_display = ["Member","Score"]
    all_time_display = ["Member","AllTime"]
    commits_display = ["Member","Commits"]

    #Load up S3 and create the scoreboard as "df"
    def __init__(self):
        load_dotenv()
        self.s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-2',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

        obj = self.s3.Bucket('bdc-scoreboard').Object("Big-Data-Club/scoreboard.csv").get()
        self.df = pd.read_csv(obj["Body"], index_col=0)
        self.df.to_csv("scoreboard.csv")

        obj = self.s3.Bucket('bdc-scoreboard').Object("Big-Data-Club/awards.csv").get()
        self.awards = pd.read_csv(obj["Body"], index_col=0, dtype={"Award": 'string', 'Description': 'string', 'Point Value': 'Int64'})
        self.awards.to_csv("awards.csv")

    def update_S3(self, table):
        if table == "scoreboard":
            self.df.to_csv("scoreboard.csv")
            self.s3.Bucket('bdc-scoreboard').upload_file(Filename='scoreboard.csv', Key='Big-Data-Club/scoreboard.csv')
        elif table == "awards":
            self.awards.to_csv("awards.csv")
            self.s3.Bucket('bdc-scoreboard').upload_file(Filename='awards.csv', Key='Big-Data-Club/awards.csv')

    #Add points to the specified user
    def add(self,name,value):
        if name in self.df.Member.values:
            self.df.at[self.df[self.df.Member == name].index[0], "Score"] += value
            self.df.at[self.df[self.df.Member == name].index[0], "AllTime"] += value
            self.df.sort_values("Score", axis=0, inplace = True, ascending=False)
            self.df.reset_index(drop=True, inplace = True)
            self.update_S3("scoreboard")



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
        if name not in self.df.Member.values:
            self.df = self.df.append(pd.DataFrame({"Member": [name], "Score": [0], "AllTime": [0], "GitHub": github, "Email": email, "Participating": True}), ignore_index=True, sort=True)
            self.update_S3("scoreboard")


    #Edit a user's github, email, or participation status
    def update(self, name, github = None, email = None, participating = None):
        if github:
            self.df.at[self.df[self.df.Member == name].index[0], "GitHub"] = github
        if email:
            self.df.at[self.df[self.df.Member == name].index[0], "Email"] = email
        if participating:
            self.df.at[self.df[self.df.Member == name].index[0], "Participating"] = participating == "True"
        self.update_S3("scoreboard")

    def remove_user(self, name):
        self.df = self.df[self.df.Member != name]
        self.update_S3("scoreboard")

    #Add award
    def add_award(self, award, description, points):
        print(points)
        self.awards = self.awards.append(pd.DataFrame({"Award": [award], "Description": [description], "Point Value": [points]}), ignore_index=True, sort=True)
        self.update_S3("awards")

    #Edit award
    def edit_award(self, award, description = None, points = None):
        if description:
            self.awards.at[self.awards[self.awards.Award == award].index[0], "Description"] = description
        if points:
            self.awards.at[self.awards[self.awards.Award == award].index[0], "Point Value"] = int(points)
        self.update_S3("awards")

    #Remove an award
    def remove_award(self, award):
        self.awards = self.awards[self.awards.Award != award]
        self.update_S3("awards")

    #Display awards
    def display_awards(self):
        self.awards.sort_values("Point Value", inplace=True)
        output = ""
        for i in self.awards.index:
            output += "**" + self.awards.loc[i,"Award"].ljust(15) + "(" + str(self.awards.loc[i,"Point Value"]) + ")** : " + self.awards.loc[i,"Description"] + "\n"
        return output

    def display_award(self, award):
        self.awards = self.awards[self.awards.Award != 'award']
        self.awards.to_csv("awards.csv")
        self.s3.Bucket('bdc-scoreboard').upload_file(Filename='awards.csv', Key='awards.csv')

    #Get point value of an award
    def get_award_value(self, award):
        return self.awards[self.awards.Award == award].iloc[0,2]

    #Record a commit
    def add_commit(self, name):
        self.df.at[self.df[self.df.Member == name].index[0], "Commits"] += 1
        self.update_S3("scoreboard")

    #Display total commits
    def display_commits(self, name = None):
        if name:
            temp_df = self.df[self.commits_display].sort_values("Commits", axis=0, ascending=False).reset_index(drop=True)
            return temp_df[temp_df.Member == name].to_string()
        else:
            return self.df[self.commits_display].sort_values("Commits", axis=0, ascending=False).reset_index(drop=True).to_string()
