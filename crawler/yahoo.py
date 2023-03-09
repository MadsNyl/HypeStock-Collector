from .article import ArticleCrawler

class YahooCrawler(ArticleCrawler):

    FILTER_URL: str = "https://finance.yahoo.com"

    def run(self):
        anchors = super()._get_anchor_tags(self.BASE_URL)
        # anchors = super()._filter_links(anchors, self.FILTER_URL)
        anchors = super()._filter_news(anchors)
        print(len(anchors))