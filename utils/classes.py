class Bookmark:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __str__(self):
        return self.title

class BookmarkFolder: 
    def __init__(self, title):
        self.title = title
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return self.title
