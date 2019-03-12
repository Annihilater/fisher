from sqlalchemy import Column, Integer, String, SmallInteger

from app.libs.enums import PendingStatus
from app.models.base import Base


class Drift(Base):
    id = Column(Integer, primary_key=True)
    gift_id = Column(Integer)

    # 索要者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gifter_nickname = Column(String(20))

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(50))
    book_img = Column(String(50))

    # 邮寄信息
    recipient_name = Column(String(20), nullable=True)
    address = Column(String(100), nullable=True)
    mobile = Column(String(20), nullable=True)
    message = Column(String(200))

    _pending = Column("pending", SmallInteger, default=1)
    # 第一个字符串将该字段的名字强制定为pending，改名前面的变量名不改变数据库里字段的名称

    @property
    def pending(self):
        return PendingStatus(self._pending)

    # 将数字类型转换成枚举类型返回，调用drift.pending的时候返回的是枚举类型了

    @pending.setter
    def pending(self, status):
        self._pending = status.value

    # 将枚举类型转换成数字类型，
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')
