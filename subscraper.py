import praw
import time
import requests
import pandas as pd 
import prawcore
import sys

print(time.time())

# Reads in and execute the source of the redditauth.py file.
exec(open("redditauth.py").read())

# Enter the path with the list you want the scraper to read from. This is using the txt file of randomized subreddit names used in the study.
inputs = 'top250subs.txt'

# Enter the path you want your scraper to store the data.
outputs = 'output.csv'

# Below is the loop that will read from each line of the inputs file and scrape the subreddit for that line.

with open(inputs,'r') as intr:
    with open(outputs, 'w') as outr:
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
# Note: You can add or remove these parameters depending on what you want to include in your scrape. 
# Refer to the PRAW documentation and the Reddit API references / documentation for how to get the data you want.

        pd.DataFrame(sub_dict_empty).to_csv(outputs, mode="w", header=True, index=False)

        for line in intr:
            line = line.rstrip()
            if line == "":
                break

            print("starting: ", line)

            sub_dict = sub_dict_empty.copy()
            sub_dict["input_name"] = [line]

            try:
                # Variable to store the subreddit name from each line in the text file
                linesub = reddit.subreddit(line) 
                # Variable to store the ListingGenerator from prawcore for moderators needed for this study.
                mods = [m for m in linesub.moderator()]
                mod_list = ",".join([m.id for m in linesub.moderator()])
                mod_count =  len(mods)
        
 # Data frame column functions
                sub_dict["display_name"] = [line]
                sub_dict["id"] = [linesub.id]
                sub_dict["created"] = [linesub.created]
                sub_dict["description_html"] = [linesub.description_html]
                #sub_dict["praw_pickle"] = pickle.dumps(linesub)
                sub_dict["subscribers"] = [linesub.subscribers]
                sub_dict["accounts_active"] = [linesub.accounts_active]
                sub_dict["active_user_count"] = [linesub.active_user_count]
                sub_dict["mod_count"] = mod_count
                sub_dict["mod_list"] = mod_list
                sub_dict["advertiser_cat"] = [linesub.advertiser_category]

# This line and the following code will prevent the script from breaking if your scrape involves subreddits that don't exist.
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
# This stores the scraped data into a data frame using Python.
            reds = pd.DataFrame(sub_dict)
            reds.to_csv(outputs, index=False, header=False, mode='a')
            
            time.sleep(1)
print(time.time())
