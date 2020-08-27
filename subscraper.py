import praw
import time
import requests
import pandas as pd 
import prawcore
import sys

print(time.time())

# Opens and executes the script to authenticate your account to access the API
exec(open("redditauth.py").read())

# Enter the path to the subreddit list. Make sure the subreddit names don't contain "/r/" (e.g., Politics instead of /r/Politics)
subreddit_names = 'top250subs.txt'

# Enter the path you want your scraper to store the data.
csvfile = 'subreddit_data.csv'

# Read in each string from the subreddit list through this loop and write out to the csv.

with open(subreddit_names,'r') as sub_names_list:
    with open(csvfile, 'w') as csv_file:
 # Data frame structure       
        sub_dict_empty = { "input_name": [],
                            "status": [],
                            "display_name": [],
                            "id": [],
                            "created": [],
                            "description_html": [],
                            "subscribers": [],
                            "accounts_active":[],
                            "active_user_count": [],
                            "mod_count": [],
                            "mod_list": [],
                            "advertiser_cat":[]}
# These aren't the only things you can get from PRAW, so check out its documentation if this isn't what you're looking for.

        pd.DataFrame(sub_dict_empty).to_csv(csvfile, mode="w", header=True, index=False)

        for name in sub_names_list:
            name = name.rstrip()
            if name == "":
                break

            print("starting: ", name)

            sub_dict = sub_dict_empty.copy()
            sub_dict["input_name"] = [name]

            try:
                # Variable to store the subreddit name from each string in the sub_names_list list.
                subreddit = reddit.subreddit(name) 
                # Variable to store the ListingGenerator from prawcore for moderators needed for this study.
                mods = [m for m in subreddit.moderator()]
                mod_list = ",".join([m.id for m in subreddit.moderator()])
                mod_count =  len(mods)
        
 # The dictionary to use in building our data frame
                sub_dict["display_name"] = [name]
                sub_dict["id"] = [subreddit.id]
                sub_dict["created"] = [subreddit.created]
                sub_dict["description_html"] = [subreddit.description_html]
                sub_dict["subscribers"] = [subreddit.subscribers]
                sub_dict["accounts_active"] = [subreddit.accounts_active]
                sub_dict["active_user_count"] = [subreddit.active_user_count]
                sub_dict["mod_count"] = mod_count
                sub_dict["mod_list"] = mod_list
                sub_dict["advertiser_cat"] = [subreddit.advertiser_category]

# Catch exceptions that might break the script, like when the subreddit can't be accessed through the API.
            except prawcore.PrawcoreException as err: 
                sub_dict["status"] = [str(err)]
                sub_dict["display_name"] = [None]
                sub_dict["id"] = [None]
                sub_dict["created"] = None
                sub_dict["description_html"] = [None]
                sub_dict["subscribers"] = [None]
                sub_dict["accounts_active"] = [None]
                sub_dict["active_user_count"] = [None]
                sub_dict["mod_count"] = [None]
                sub_dict["mod_list"] = [None]
                sub_dict["advertiser_cat"] = [None]
            else:
                sub_dict["status"] = ["OK"]
# Write out to csv with Pandas.DatFrame.to_csv.
            reds = pd.DataFrame(sub_dict)
            reds.to_csv(csvfile, index=False, header=False, mode='a')
            
            time.sleep(1)
print(time.time())
