

def build_url(base_url: str, queries: list[str] = [], params: list[str] = []) -> str:
    url = base_url
    
    if params:
        for param in params:
            url += f"/{param}"
    
    if queries:
        for i, query in enumerate(queries):
            if i == 0:
                url += f"/?{query}"
            else:
                url += f"&{query}"
    
    return url
