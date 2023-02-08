import shelve

class Feedback:
    def __init__(self, rating, remarks):
        with shelve.open("counter", writeback=True) as counter:
            if "feedback" not in counter:
                id = 1
            else:
                id = counter["feedback"] + 1
            counter["feedback"] = id

        self.__feedback_id = id
        self.__rating = rating
        self.__remarks = remarks

    def get_feedback_id(self):
        return self.__feedback_id

    def get_rating(self):
        return self.__rating

    def get_remarks(self):
        return self.__remarks

    def set_rating(self, rating):
        self.__rating = rating

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def __str__(self):
        return f"Rating: {self.__rating}\nRemarks: {self.__remarks}"
