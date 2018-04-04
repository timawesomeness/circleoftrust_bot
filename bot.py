import praw, prawcore
import getpass

pw = getpass.getpass()

# Replace with real values
reddit = praw.Reddit(user_agent="XXX", client_id="XXX", client_secret="XXX", username="XXX", password=pw)

count = 0

for i in reddit.subreddit("circleoftrust").stream.submissions():
    if not i.title.startswith("u/"): # People with username circles probably aren't setting the key to that
        try:
            output = reddit.post("/api/guess_voting_key.json", data=dict(id=i.name, raw_json=1, vote_key=i.title))
            key = i.title
            if not output.get(key) and key != key.split()[-1]:
                first_output = output
                output = reddit.post("/api/guess_voting_key.json", data=dict(id=i.name, raw_json=1, vote_key=i.title.split()[-1]))
                key = i.title.split()[-1]
            else:
                first_output = None
        except prawcore.exceptions.NotFound:
            continue
        with open("circles.txt", "a") as f:
            f.write(i.title + ": " + (str(first_output) + ", " if first_output else "") + str(output) + "\n")
        if output.get(key):
            print(f"Got one: {key}")
            try:
                vote = reddit.post("/api/circle_vote.json", data=dict(id=i.name, dir=1, isTrusted=True), params=dict(dir=1, id=i.name))
            except Exception as e:
                print(f"Error: {str(e)}")
        count += 1
        if count % 25 == 0:
            print(count)
