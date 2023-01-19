from datetime import datetime

class Comment():

    @staticmethod
    def create(comment: object, symbol: str, post_url: str) -> dict:
        obj = {}
        obj["symbol"] = symbol
        obj["author"] = Comment.get_author(comment)
        obj["post_url"] = post_url
        obj["comment_url"] = comment.permalink
        obj["comment_body"] = comment.body
        obj["created_date"] = Comment.format_time(comment)

        return obj
    
    @staticmethod
    def get_author(comment: object) -> str:
        if comment.author: return comment.author.name
        return comment.author
    
    @staticmethod
    def format_time(comment: object) -> datetime:
        time = comment.created
        return datetime.fromtimestamp(time)
    
