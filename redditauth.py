import praw

# You'll encounter these steps in many guides on accessing Reddit's API, so I shouldn't have to explain much. 
# Just remember to replace all of the strings here with their respective entries (e.g., YOUR-CLIENT-ID = your bot's Client ID).

reddit = praw.Reddit(client_id='YOUR-CLIENT-ID', \
                     client_secret='YOUR-CLIENT-SECRET', \
                     user_agent='YOUR-USER-AGENT', \
                     username='YOUR-REDDIT-USERNAME', \
                     password='YOUR-REDDIT-PASSWORD')


