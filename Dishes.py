import random
import shelve 
class Dish:
    count_id = None

    def __init__(self, dish_name, price, description, cuisine):
        with shelve.open("counter", writeback=True) as counter:
            if "dishes" not in counter:
                id = 1
            else:
                id = counter["dishes"] + 1

            counter["dishes"] = id
        self.__dish_id = id
        self.__dish_name = dish_name
        self.__price = price
        self.__description = description
        self.__cuisine = cuisine
        self.__image = ''

    def get_dish_id(self):
        return self.__dish_id

    def get_dish_name(self):
        return self.__dish_name

    def get_price(self):
        return self.__price

    def get_description(self):
        return self.__description

    def get_cuisine(self):
        return self.__cuisine

    def get_image(self):
        return self.__image

    def set_dish_id(self, dish_id):
        self.__dish_id = dish_id

    def set_dish_name(self, dish_name):
        self.__dish_name = dish_name

    def set_price(self, price):
        self.__price = price

    def set_description(self, description):
        self.__description = description

    def set_cuisine(self, cuisine):
        self.__cuisine = cuisine

    def set_image(self, image):
        self.__image = image
