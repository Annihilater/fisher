from collections import namedtuple

from app.view_models.book import BookViewModel


# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])


class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []

        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list

        self.gifts = self.__parse()

    def __parse(self):
        tem_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            tem_gifts.append(my_gift)
        return tem_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if wish_count['isbn'] == gift.isbn:
                count = wish_count['count']
        r = {
            'id': gift.id,
            'book': BookViewModel(gift.book),
            'wishes_count': count
        }
        return r
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        # return my_gift
