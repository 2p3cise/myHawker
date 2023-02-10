#Nicholas
import User
import shelve


class Customer(User.User):
    def __init__(self, first_name, last_name, gender, membership, remarks, email, date_joined, address, password):
        super().__init__(first_name, last_name, gender, membership, remarks)
        with shelve.open("counter", writeback=True) as counter:
            if "customer" not in counter:
                id = 1
            else:
                id = counter["customer"] + 1
            counter["customer"] = id
        self.__customer_id = id
        self.__email = email
        self.__date_joined = date_joined
        self.__address = address
        self.__password = password

    # accessor methods
    def get_customer_id(self):
        return self.__customer_id

    def get_email(self):
        return self.__email

    def get_date_joined(self):
        return self.__date_joined

    def get_address(self):
        return self.__address

    def get_password(self):
        return self.__password

    # mutator methods
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def set_password(self, password):
        self.__password = password
