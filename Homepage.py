import shelve


class DailyDish:
    def __init__(self, daily_dish, daily_price, weekly_store, weekly_description):
        with shelve.open("counter", writeback=True) as counter:
            if "daily_dishes" not in counter:
                id = 1
            else:
                id = counter["daily_dishes"] + 1

            counter["daily_dishes"] = id
        self.__daily_dish_id = id
        self.__daily_dish = daily_dish
        self.__daily_price = daily_price
        self.__daily_image = ''
        self.__weekly_store = weekly_store
        self.__weekly_description = weekly_description
        # self.__weekly_image = ''

    def get_daily_dish_id(self):
        return self.__daily_dish_id

    def get_daily_dish(self):
        return self.__daily_dish

    def get_daily_price(self):
        return self.__daily_price

    def get_daily_image(self):
        return self.__daily_image

    def get_weekly_store(self):
        return self.__weekly_store

    def get_weekly_description(self):
        return self.__weekly_description


    def set_daily_dish_id(self, daily_dish_id):
        self.__daily_dish_id = daily_dish_id

    def set_daily_dish(self, daily_dish):
        self.__daily_dish = daily_dish

    def set_daily_price(self, daily_price):
        self.__daily_price = daily_price

    def set_daily_image(self, daily_image):
        self.__daily_image = daily_image

    def set_weekly_store(self, weekly_store):
        self.__weekly_store = weekly_store

    def set_weekly_description(self, weekly_description):
        self.__weekly_description = weekly_description



