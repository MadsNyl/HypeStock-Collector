from social_media import CNBC

if __name__ == "__main__":
    a = CNBC(
        base_url="https://www.cnbc.com/finance/"
    )
    a.run()