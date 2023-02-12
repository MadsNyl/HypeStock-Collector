def progressbar(iteration: int, total: int, text: str)-> None:
    if text: print(text)
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(50 * iteration // total)
    bar = '█' * filledLength + '-' * (50 - filledLength)
    print(f'\r{"Progress: "} |{bar}| {percent}% {"Complete"}', end = "\r")
    # Print New Line on Complete
    if iteration == total: 
        print()  