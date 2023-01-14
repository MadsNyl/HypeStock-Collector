def validate_reddit_comment(db: object, data: list[dict]):
    """
        Check if comments already have been visited.
    """
    comparison_list = list(map(get_comment_url, data))

    comments = db.reddit_comments_seen(comparison_list)

    if not comments: return data
    comments = list(map(map_comment, comments))
    
    return filter_list(data, comments)


def get_comment_url(obj: dict): return obj["comment_url"]

def map_comment(comment): return comment[0]

def filter_list(data: list[dict], comments: list[tuple]): 
    new_list = []
    for obj in data:
        if obj["comment_url"] not in comments:
            new_list.append(obj)

    return new_list

