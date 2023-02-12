string = "test (ticker)"

print(list(filter(lambda x: len(x), string.strip().replace("(", " ").replace(")", " ").split(" "))))