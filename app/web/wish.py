from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app import db
from app.libs.email import send_email
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from . import web


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wish(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyTrades(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        # try:
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
        #     db.session.commit(gift)     # 将数据写入到数据库
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已添加至你的赠送清单或已存在与你的心愿清单,请不要重复添加')

    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(
        uid=current_user.id,
        isbn=wish.isbn).first_or_404()
    if not gift:
        flash('你还没有上传本书，请点击"加入到赠送清单"添加此书.添加前，请确保自己可以赠送此书')
    else:
        send_email(
            wish.user.email,
            '有人想送你一本书',
            'email/satisfy_wish.html',
            gift=gift,
            wish=wish)
        flash('已向他/她发送了一封邮件，如果他/她愿意接收你的赠送，你将收到一个鱼漂。')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, uid=current_user.id).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
