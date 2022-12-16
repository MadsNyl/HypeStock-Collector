def print_progress_bar(iteration: int, total: int, prefix: str = '', suffix:str = '', decimals: int = 1, length: int = 50, fill:str = '█', printEnd:str = "\r")-> None:
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()  

def print_progress_bar_subs(subs: int) -> None:
    print(f"Collecting {subs} subs: ")
    print_progress_bar(0, subs, prefix="Progress: ", suffix="Complete")

def print_progress_bar_tweets(tweets: int) -> None:
    print(f"Collecting {tweets} tweets: ")
    print_progress_bar(0, tweets, prefix="Porgress: ", suffix="Complete")

def print_progress_bar_objects(len: int) -> None:
    print(f"Processing {len} data objects: ")
    print_progress_bar(0, len, prefix="Progress", suffix="Complete")