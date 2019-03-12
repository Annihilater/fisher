from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id"))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    # 默认值False表示书籍未赠送出去

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        recent_gift = []

        # 从 gift 表中先按 isbn 分组取出最近上传的 [gift.id, gift.isbn]，限量 30 条
        recent_gift_id_isbn_list = sorted(
            db.session.query(func.max(Gift.id), Gift.isbn)
            .filter_by(launched=False, status=1)
            .group_by(Gift.isbn)
            .limit(current_app.config["RECENT_BOOK_COUNT"])
            .all()
        )
        recent_gift_id_isbn_list.reverse()  # 倒序排序

        for recent_gift_id_isbn in recent_gift_id_isbn_list:  # 根据 gift.id 取 gift
            gift = Gift.query.filter_by(
                id=recent_gift_id_isbn[0]
            ).first_or_404()  # 遍历列表，按照列表的isbn编号查询出对应的gift
            recent_gift.append(gift)  # 将查询出的gift添加到recent_gift

        # 下面这段代码是七月给的代码，但是会报错，原因未知
        # recent_gift = Gift.query.filter_by(
        #     launched=False).group_by(
        #     Gift.isbn).order_by(
        #     desc(Gift.create_time)).limit(
        #     current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift

    @classmethod
    def get_user_gift(cls, uid):
        gifts = (
            Gift.query.filter_by(launched=False, uid=uid)
            .order_by(desc(Gift.create_time))
            .all()
        )
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish

        # 根据传入的一组isbn，到Wish表中计算出某个礼物Wish的心愿数量
        # filter要求传入条件表达式
        count_list = (
            db.session.query(func.count(Wish.id), Wish.isbn)
            .filter(Wish.launched == False, Wish.isbn.in_(isbn_list), Wish.status == 1)
            .group_by(Wish.isbn)
            .all()
        )
        count_list = [{"count": w[0], "isbn": w[1]} for w in count_list]
        return count_list

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False
