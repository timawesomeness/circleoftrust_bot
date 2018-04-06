import praw, prawcore
import getpass
import webbrowser
import requests
import json
import time
import sys

pw = getpass.getpass()

# Replace wth real values
reddit = praw.Reddit(user_agent="XXX)", client_id="XXX", client_secret="XXX", username="XXX", password=pw)

count = 0
after = 1522792260
print("starting")
while after < 1522872000:
    print("after", after)
    for i in json.loads(requests.get("https://api.pushshift.io/reddit/search/submission/", params=dict(q='-"u/"', subreddit="circleoftrust", size=500, after=after)).text)["data"]: 
        if i["created_utc"] > after:
            after = i["created_utc"]
        try:
            outputs = []
            output = []
            key = ""
            if i["id"] in open("checked_circles.txt").read():
                print(i["id"])
                continue
            else:
                with open("checked_circles.txt", "a") as f:
                    f.write(i["id"] + "\n")
            if not i["title"].startswith("u/") and i.get("link_flair_text") != "Betrayed" and i["author"] != "[deleted]":         # " ".join(i["title"].split()[:2]), 
                for j in [i["title"]]+([i["title"].split()[0], i["title"].split()[-1]] if len(i["title"].split()) > 1 else [])+([" ".join(i["title"].split()[-2:])] if len(i["title"].split()) > 3 else []):
                    if not j:
                        continue
                    try:
                        output = reddit.post("/api/guess_voting_key.json", data=dict(id=f"t3_{i['id']}", raw_json=1, vote_key=j))
                        outputs.append(output)
                        if output.get(j):
                            key = j
                            break
                    except prawcore.exceptions.NotFound:
                        continue
                with open("circles2.txt", "a") as f:
                    f.write(i["title"] + ": " + str(outputs) + "\n")
                if output.get(key):
                    print(f"Got one: {key}")
                    try:
                        with open("joinable_circles.txt", "a") as f:
                            f.write(f"https://www.reddit.com/user/{i['author']}/circle/embed\n")
                        webbrowser.open(f"https://www.reddit.com/user/{i['author']}/circle/embed")
                    except Exception as e:
                        print(f"Error: {str(e)}")
                count += 1
                if count % 25 == 0:
                    print(count)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            if "429" in str(e):
                time.sleep(5)
            print("except:", e)
