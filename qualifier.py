"""
Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""
import datetime
import itertools
import string
import typing
from collections import Counter
from functools import total_ordering


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: typing.Type[typing.Any]):
        self.field_type = field_type

    def __get__(self, obj, objtype):
        return obj.__dict__['attribute']

    def __set__(self, obj, value):
        if isinstance(value, self.field_type):
            obj.__dict__['attribute'] = value
        else:
            raise TypeError(
                f"expected an instance of type '{self.field_type.__name__}' for attribute 'attribute', got '{type(value).__name__}' instead")


@total_ordering
class Article:
    """The `Article` class you need to write for the qualifier."""

    article_ids = itertools.count()

    def __init__(self, title: str, author: str, publication_date: datetime.datetime, content: str):
        self.id = next(self.article_ids)
        self.title = title
        self.author = author
        self.content = content
        self.publication_date = publication_date
        self.last_edited = None

    def __repr__(self):
        cls_name = self.__class__.__name__
        publication_date = self.publication_date.isoformat()
        return f"<{cls_name} title={self.title!r} author={self.author!r} publication_date={publication_date!r}>"

    def __len__(self):
        return len(self.content)

    def __lt__(self, value):
        return self.publication_date < value.publication_date

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value: str):
        self._content = value
        self.last_edited = datetime.datetime.now()

    def short_introduction(self, n_characters: int):
        short_content = self.content[:n_characters+1]
        rightmost_space = short_content.rfind(' ')
        rightmost_newline = short_content.rfind('\n')
        rightmost_seperator = max((rightmost_space, rightmost_newline))
        return short_content[:rightmost_seperator]

    def most_common_words(self, n_words: int):
        translator = str.maketrans(
            string.punctuation, ' ' * len(string.punctuation))
        clean_content = self.content.translate(translator).lower()
        words = clean_content.split()
        word_counts = Counter(words)
        most_commmon_words = dict(word_counts.most_common(n_words))
        return most_commmon_words
