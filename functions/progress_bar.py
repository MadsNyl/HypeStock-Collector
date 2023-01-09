def print_progress_bar(iteration: int, total: int)-> None:
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(50 * iteration // total)
    bar = '█' * filledLength + '-' * (50 - filledLength)
    print(f'\r{"Progress: "} |{bar}| {percent}% {"Complete"}', end = "\r")
    # Print New Line on Complete
    if iteration == total: 
        print()  

def print_progress_bar_subs(subs: int) -> None:
    print(f"Collecting {subs} subs: ")
    print_progress_bar(0, subs)

def print_progress_bar_tweets(tweets: int) -> None:
    print(f"Collecting {tweets} tweets: ")
    print_progress_bar(0, tweets)

def print_progress_bar_objects(len: int) -> None:
    print(f"Processing {len} data objects: ")
    print_progress_bar(0, len)