insertstocks:
	python stocks.py

reddit:
	python reddit.py ${args}

crawl:
	python app/crawler/main.py ${args}

pushshift:
	python pushshift.py ${args}

update_tracking:
	python update_trackings.py

article:
	python article_crawl.py

tracking:
	python tracking.py

legacy_tracking:
	python download_legacy.py