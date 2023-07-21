import masterhackerbot
import praw
import os
import re
import time

print("Connecting to Reddit, please wait...")
# Create the Reddit instance
reddit = praw.Reddit('masterhack') #set login information in the praw.ini file

footer = "\n\n---\n\n^^I&#32;am&#32;a&#32;bot&#32;created&#32;by&#32;[u/drewman301](https://www.youtube.com/watch?v=dQw4w9WgXcQ)&#32;and&#32;this&#32;action&#32;was&#32;performed&#32;automatically.&#32;AI&#32;is&#32;involved&#32;so&#32;please&#32;DM&#32;drewman301&#32;if&#32;it&#32;produces&#32;anything&#32;offensive&#32;and&#32;I&#32;will&#32;delete&#32;it.&#32;Original&#32;idea&#32;by&#32;[u/circuit10](https://www.youtube.com/watch?v=dQw4w9WgXcQ).&#32;Jargon&#32;from&#32;[http://shinytoylabs.com/jargon/](https://www.youtube.com/watch?v=dQw4w9WgXcQ)."
home_subreddit = 'masterhacker'
account_name = "masterhackerbot"
admin_users = ['drewman301', 'circuit10', 'snorlaxmaster65'] # not implemented yet
wait_time = 10 # how many minutes to wait between comments (to avoid spamming)

subreddit = reddit.subreddit(home_subreddit)

def re_results(target, message):
    print("Replying to u/"+str(target.author)+"'s comment...")
    target.reply(message + footer)

def check_mentions():
    print("Checking mentions...")
    repeat = False
    for mention in reddit.inbox.mentions(limit=100):
        text = 'Sample text, sample text. This is a placeholder'
        generated_text = 'Sample text, sample text. This is also a placeholder'
        print("<"+str(mention.author)+"> ("+mention.id+") "+str(mention.body))
        if mention.id not in comments_replied_to:#If comment has not alreay been replied to
            mention_message = mention.body.replace(('u/'+account_name+' '), '')#Message without the username
            if ("u/"+str(account_name)) in mention.body:
                parent_id = mention.parent_id
                if 't1' in parent_id:#if it's a comment
                    parent_id = parent_id.replace('t1_', '')
                    parent = reddit.comment(parent_id)
                    print("Parent comment: " + parent.body)
                    text = parent.body
                elif 't3' in parent_id:#if it's a post
                    parent = mention.submission
                    try:
                        print("Parent post: " + parent.title)
                    except:
                        print("Parent post: Printing error :(")
                    text = parent.title
                print("*********************************")
                generated_text = masterhackerbot.generate_jargon(text)
                print(generated_text)
                if repeat:
                    print("\nWaiting "+str(wait_time)+" minute(s) until next comment...")
                    time.sleep(wait_time * 60)
                re_results(mention, generated_text)
                comments_replied_to.append(mention.id)
                print("\n")
                repeat = True
            else:
                print("Mention uses wrong format. Skipping...")
                comments_replied_to.append(mention.id)

if not os.path.isfile("comments_replied_to.txt"): #if reply file no exist, make new empty list.
    comments_replied_to = []
else:
    #load the file
    with open("comments_replied_to.txt", "r") as f:
       comments_replied_to = f.read()
       comments_replied_to = comments_replied_to.split("\n")
       comments_replied_to = list(filter(None, comments_replied_to))
check_mentions()
with open("comments_replied_to.txt", "w") as f:
    #save the file
    for post_id in comments_replied_to:
        f.write(post_id + "\n")
