import re

from flask import current_app

from app import db
from app.libs.httper import HTTP
from app.models.book import Book


class YuShuBook:
    """
    对鱼书的API进行封装，所有的书籍信息都从这里获取
    """

    isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        self.total = 0
        self.books = []

    @property
    def first(self):
        # if self.total:
        #     return self.books[0]
        # else:
        #     print('鱼书API异常')
        #     return None
        return self.books[0] if self.total >= 1 else None

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data.get("total", None)
        self.books = data.get("books", [])

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(
            keyword, current_app.config["PER_PAGE"], self.calculate_start(page)
        )
        result = HTTP.get(url)
        self.__fill_collection(result)

    @staticmethod
    def calculate_start(page):
        return (page - 1) * current_app.config["PER_PAGE"]


def save_to_mysql(q, page=1):
    yushu_book.search_by_keyword(q, page)
    books = yushu_book.books
    for item in books:
        if not Book.query.filter_by(isbn=item["isbn"]).first():
            del item["id"]
            item["author"] = "、".join(item["author"])
            item["translator"] = "、".join(item["translator"])
            print(item["title"])
            with db.auto_commit():
                db.session.add(Book(**item))
                print(q, item["title"] + "-----------入库成功 ok...")
        else:
            print(q, item["title"] + " ------------已存在")


if __name__ == "__main__":
    q_list = [
        "c",
        "go",
        "c++",
        "c#",
        "java",
        "mysql",
        "数据库",
        "算法",
        "sql",
        "架构",
        "黑客",
        "编程",
        "鲁迅",
        "老舍",
        "flask",
        "django",
        "web",
        "scrapy",
        "爬虫",
    ]
    for j in range(4, len(q_list)):
        q = q_list[j]
        yushu_book = YuShuBook()
        from fisher import app

        with app.app_context():
            yushu_book.search_by_keyword(q)
            total = yushu_book.total
            if (total % 15) == 0:
                search_page = int(total / 15)
            else:
                search_page = int(total / 15) + 1
            for i in range(1, search_page + 1):
                save_to_mysql(q, i)
