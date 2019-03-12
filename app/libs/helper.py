def is_isbn_or_key(word):
    """
    isbn13: 由13个0-9的数字组成
    isbn10: 由10个0-9的数字组成，包含'-'
    判断传入的isbn是否符合isbn规范
    :param word:
    :return:
    """
    isbn_or_key = "key"
    if len(word) == 13 and word.isdigit():
        isbn_or_key = "isbn"
    short_word = word.replace("-", "")
    if "-" in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = "isbn"
    return isbn_or_key
