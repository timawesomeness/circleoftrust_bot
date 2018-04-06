import praw, prawcore
import getpass
import webbrowser

pw = getpass.getpass()

# Replace with real values
reddit = praw.Reddit(user_agent="XXX", client_id="XXX", client_secret="XXX", username="XXX", password=pw)

count = 0
while True:
    try:
        for i in reddit.subreddit("circleoftrust").stream.submissions():
            outputs = []
            output = []
            key = ""
            if not i.title.startswith("u/") and i.link_flair_text != "Betrayed":                                   # " ".join(i.title.split()[:2]), 
                for j in [i.title]+([i.title.split()[0], i.title.split()[-1]] if len(i.title.split()) > 1 else [])+([" ".join(i.title.split()[-2:])] if len(i.title.split()) > 3 else []):
                    if not j:
                        continue
                    try:
                        output = reddit.post("/api/guess_voting_key.json", data=dict(id=i.name, raw_json=1, vote_key=j))
                        outputs.append(output)
                        if output.get(j):
                            key = j
                            break
                    except prawcore.exceptions.NotFound:
                        continue
                with open("circles.txt", "a") as f:
                    f.write(i.title + ": " + str(outputs) + "\n")
                if output.get(key):
                    print(f"Got one: {key}")
                    try:
                        with open("joinable_circles.txt", "a") as f:
                            f.write(f"https://www.reddit.com/user/{i.author}/circle/embed\n")
                        webbrowser.open(f"https://www.reddit.com/user/{i.author}/circle/embed")
                    except Exception as e:
                        print(f"Error: {str(e)}")
                count += 1
                if count % 25 == 0:
                    print(count)
    except KeyboardInterrupt:
        break
    except:
        pass
