
class Vouchers:

    count_id = 0

    def __init__(self, code, discount, expiry_date):
        Vouchers.count_id += 1
        self.__id = Vouchers.count_id
        self.__code = code
        self.__discount = discount
        self.__expiry_date = expiry_date

    def get_code(self):
        return self.__code

    def set_code(self, code):
        self.__code = code

    def get_discount(self):
        return self.__discount

    def set_discount(self, discount):
        self.__discount = discount

    def get_expiry_date(self):
        return self.__expiry_date

    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id
