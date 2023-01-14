# import snscrape.modules.twitter as sntwitter

# for i, tweet in enumerate(sntwitter.TwitterSearchScraper("from:jack").get_items()):
#     print(tweet)
#     break


list1 = [
    {
        "name": "test",
        "id": 123
    },
    {
        "name": "test2",
        "id": 123
    },
    {
        "name": "test3",
        "id": 1244
    }
]

list2 = [
    1244
]

def get_id(obj):
    return obj["id"]

comp_list = list(map(get_id, list1))

print(set(comp_list).intersection(list2))