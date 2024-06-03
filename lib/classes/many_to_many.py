import weakref

class Article:
    all = []

    def __init__(self, author, magazine, title):
        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)
        magazine._articles.append(weakref.ref(self))
        author._articles.append(weakref.ref(self))

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        raise AttributeError("Title is immutable")

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value
        else:
            raise ValueError("Author must be an instance of Author")

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value
        else:
            raise ValueError("Magazine must be an instance of Magazine")


class Author:
    def __init__(self, name):
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Name is immutable")

    def add_article(self, magazine, title):
        article = Article(self, magazine, title)
        return article

    def articles(self):
        return [ref() for ref in self._articles if ref()]

    def magazines(self):
        return list(set(article.magazine for article in self.articles()))

    def topic_areas(self):
        if not self._articles:
            return None
        return list(set(article.magazine.category for article in self.articles()))


class Magazine:
    def __init__(self, name, category):
        if isinstance(name, str) and 2 <= len(name) <= 16:
            self._name = name
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")
        
        if isinstance(category, str) and category:
            self._category = category
        else:
            raise ValueError("Category must be a non-empty string")
        
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and value:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string")

    def articles(self):
        return [ref() for ref in self._articles if ref()]

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self.articles()]

    def contributors(self):
        return list(set(article.author for article in self.articles()))

    def contributing_authors(self):
        if not self._articles:
            return None
        return [author for author in self.contributors() if sum(1 for article in self.articles() if article.author == author) > 2]

