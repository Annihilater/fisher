from app.libs.enums import PendingStatus


# 处理一组鱼漂数据
class DriftConnection:
    def __init__(self, drifts, current_user_id):
        self.data = []

        self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)


# 处理单个鱼漂数据
class DriftViewModel:
    def __init__(self, drift, current_user_id):
        self.data = {}

        self.data = self.__parse(drift, current_user_id)

    def __parse(self, drift, current_user_id):
        # 确定当前用户是请求者还是赠送者
        you_are = self.requester_or_gifter(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)

        r = {
            # 当前用户信息
            'you_are': you_are,
            'operator': drift.requester_nickname if you_are != 'requester' else drift.gifter_nickname,
            'status_str': pending_status,

            # 鱼漂信息
            'drift_id': drift.id,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),

            # 书籍信息
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,

            # 收件人信息
            'recipient_name': drift.requester_nickname,
            'mobile': drift.mobile,
            'address': drift.address,
            'message': drift.message,

            # 交易信息
            'status': drift.pending
        }
        return r

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are
