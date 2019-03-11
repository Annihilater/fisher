from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app import db
from app.forms.book import DriftForm
from app.libs.email import send_email
from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftConnection
from . import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_gift.id):
        flash('这本书是你自己的，不能向自己索要书籍')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    can = current_user.can_send_drift()

    if not can:
        return render_template(
            'not_enough_beans.html',
            beans=current_user.beans)

    form = DriftForm(request.form)

    if request.method == 'POST':
        if form.validate():
            save_drift(form, current_gift)
            send_email(
                current_gift.user.email,
                '有人想要一本书',
                'email/get_gift.html',
                wisher=current_user,
                gift=current_gift)
            wish = Wish.query.filter_by(
                uid=current_user.id,
                isbn=current_gift.isbn).first()
            if not wish:
                with db.auto_commit():
                    wish = Wish()
                    wish.isbn = current_gift.isbn
                    wish.uid = current_user.id
                    db.session.add(wish)
            return redirect(url_for('web.pending'))

    gifter = current_gift.user.summary
    return render_template(
        'drift.html',
        gifter=gifter,
        user_beans=current_user.beans,
        form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(or_(
        Drift.requester_id == current_user.id,
        Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()

    views = DriftConnection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(
            Gift.uid == current_user.id,
            id == did).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit():
        # 超权
        # uid：1     did：1       1号用户发送了一个鱼漂，鱼漂did是1
        # uid：2     did：2       2号用户也发送了也一个鱼漂，鱼漂did是2
        # 假设1号用户在访问redraw_drift的时候将did改成了2，同样是可以访问执行下去的
        drift = Drift.query.filter_by(
            requester_id=current_user.id,
            id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))
    # 这里最好是写成ajax的，来回重定向消耗服务器资源


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id=current_user.id,
            id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1

        gift = Gift.query.filter_by(
            id=drift.gift_id,
            launched=False).first_or_404()
        gift.launched = True

        wish = Wish.query.filter_by(
            uid=drift.requester_id,
            isbn=drift.isbn,
            launched=False).first_or_404()
        wish.launched = True

        # Wish.query.filter_by(uid=drift.requester_id, isbn=drift.isbn, launched=False).update({Wish.launched: True})
        # 第二种写法
        # 建议在实际开发中保持一种写法，两种写法效果相等

    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # drift.message = drift_form.message.data
        drift_form.populate_obj(drift)

        # 确定鱼漂
        drift.gift_id = current_gift.id

        # 索要者信息
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname

        # 赠送者信息
        drift.gifter_id = current_gift.user.id
        drift.gifter_nickname = current_gift.user.nickname

        # 书籍信息
        book = BookViewModel(current_gift.book)
        drift.isbn = book.isbn
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image

        # # 书籍信息的另一种写法
        # # 此时的book是一个字典
        # book = current_gift.book.first
        #
        # # 用字典取值的方式取值
        # drift.isbn = book['isbn']
        # drift.book_title = book['title']
        # drift.book_author = book['author']
        # drift.book_img = book['image']

        # 鱼豆消耗1个
        current_user.beans -= 1

        db.session.add(drift)
