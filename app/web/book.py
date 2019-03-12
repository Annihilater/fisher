# import json

from flask import request, render_template, flash
from flask_login import current_user

from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import TradeInfo
from app.web import web
from app.forms.book import SearchForm
from app.view_models.book import BookCollection, BookViewModel
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook


# @web.route('/test')
# def test():
#     r = {
#         'name': '',
#         'age': 18
#     }
#     r1 = {
#         'name': '八月',
#         'age': 25
#     }
#     flash('你好，这里是消息闪现!', category='errors')
#     flash('Hello, this is messaging flash!', category='warning')
#     flash('你好，这里是消息闪现!')
#     return render_template('test.html', data=r, data1=r1)


# @web.route('/test')
# def test1():
#     from flask import request
#     from app.libs.none_local import n
#     print(n.v)
#     n.v = 2
#     print('-----------------------------')
#     print(getattr(request, 'v', None))
#     setattr(request, 'v', 2)
#     print('-----------------------------')
#     return ''


@web.route("/book/search")
def search():
    # q = request.args['q']
    # page = request.args['page']
    # a = request.args.to_dict()  # 将不可边的字典 immutablemultidict 转化为可变字典 dict
    args = request.args
    form = SearchForm(args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == "isbn":
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        flash("搜索的关键字不符合要求，请重新输入关键字")
        # return jsonify(form.errors)

    return render_template("search_result.html", books=books, form=form)


@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍的详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    if current_user.is_authenticated:
        if Gift.query.filter_by(isbn=isbn, launched=False, uid=current_user.id).first():
            has_in_gifts = True
        if Wish.query.filter_by(isbn=isbn, launched=False, uid=current_user.id).first():
            has_in_wishes = True

    return render_template(
        "book_detail.html",
        book=book,
        gifts=trade_gifts_model,
        wishes=trade_wishes_model,
        has_in_gifts=has_in_gifts,
        has_in_wishes=has_in_wishes,
    )
