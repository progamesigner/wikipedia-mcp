from html.parser import HTMLParser


class WikipediaHTMLParser(HTMLParser):
    texts: list[str]

    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.texts = []

    def handle_data(self, data: str) -> None:
        self.texts.append(data)


def html_to_text(html: str) -> str:
    parser = WikipediaHTMLParser()
    parser.feed(html)
    return ''.join(parser.texts)
