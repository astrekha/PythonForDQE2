from abc import ABC, abstractmethod
from datetime import datetime, date



class BaseHandler(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def add(self, *args, **kwargs):
        pass


class ConcreteFileHandler(BaseHandler):

    def __init__(self, file_name: str):
        self.file_name = file_name

    def add(self, text: str):
        with open(self.file_name, "a") as file:
            file.write(text)


# class ConcreteDBHandler(BaseHandler):
#
#     def __init__(self, url: str, credentials: dict):
#         self.url = url
#         self.credentials = credentials

    # def add(self, text: str):
    #     pass


class BaseFeedProvider(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_text(self) -> str:
        pass


class NewsFeedProvider(BaseFeedProvider):

    def __init__(self, pub_name: str, city: str, text: str):
        self.city = city
        self.text = text
        self.pub_name = pub_name

    def get_text(self) -> str:
        # final_news = self.city + '\n' + self.text
        # return final_news
        put_here_minus_n_times = lambda x: "-" * x
        title = self.pub_name.title()
        s1 = f"{title} {put_here_minus_n_times(25)}"
        s2 = self.text
        s3 = f'{self.city}, {self.calculate_publish_date()}'
        s4 = put_here_minus_n_times(30)
        s5 = "\n\n"
        publication_formatted = "\n".join((s1, s2, s3, s4, s5))
        return publication_formatted

    def calculate_publish_date(self):
        return datetime.now().strftime("%d/%m/%Y %H.%M")


class AdvFeedProvider(BaseFeedProvider):

    def __init__(self, pub_name: str, text: str, exp_date: str):
        self.pub_name = pub_name
        self.text = text
        self.exp_date = exp_date

    def get_text(self) -> str:
        # final_news = self.city + '\n' + self.text
        # return final_news
        put_here_minus_n_times = lambda x: "-" * x
        title = self.pub_name.title()
        s1 = f"{title} {put_here_minus_n_times(20)}"
        s2 = self.text
        s3 = f'Actual until: {self.format_exp_date(self.exp_date)}, {self.calculate_day_left(self.exp_date)} day(s) left'
        s4 = put_here_minus_n_times(30)
        s5 = "\n\n"
        publication_formatted = "\n".join((s1, s2, s3, s4, s5))
        return publication_formatted

    def calculate_day_left(self, exp_date):
        try:
            exp_date = datetime.strptime(exp_date, '%Y-%m-%d').date()
            date_diff = str((exp_date - date.today()).days)
        except TypeError:
            # print(f"Incorrect input date format: {exp_date}")
            date_diff = None
        return date_diff

    def format_exp_date(self, exp_date):
        try:
            date_formatted = datetime.strptime(exp_date, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            print(f"Incorrect input date format: {exp_date}")
            date_formatted = ''
        except TypeError:
            # print(f"Incorrect input date format: {exp_date}")
            date_formatted = ''
        return date_formatted


class DiscountFeedProvider(AdvFeedProvider, NewsFeedProvider):

    def __init__(self, pub_name: str, city: str, text: str, exp_date: str, discount: float):
        self.pub_name = pub_name
        self.city = city
        self.text = text
        self.exp_date = exp_date
        self.discount = discount

    def get_text(self) -> str:
        put_here_minus_n_times = lambda x: "-" * x
        title = self.pub_name.title()
        s1 = f"{title} {put_here_minus_n_times(14)}"
        s2 = self.text
        s3 = f'{self.city}, {self.calculate_publish_date()}'
        s4 = f'Discount: {self.discount} %'
        s5 = f'Actual until: {self.format_exp_date(self.exp_date)}, {self.calculate_day_left(self.exp_date)} day(s) left'
        s6 = put_here_minus_n_times(30)
        s7 = "\n\n"
        publication_formatted = "\n".join((s1, s2, s3, s4, s5,s6, s7))
        return publication_formatted

    # def calculate_publish_date(self):
    #     return datetime.now().strftime("%d/%m/%Y %H.%M")

    # def calculate_day_left(self, exp_date):
    #     try:
    #         exp_date = datetime.strptime(exp_date, '%Y-%m-%d').date()
    #         date_diff = str((exp_date - date.today()).days)
    #     except TypeError:
    #         # print(f"Incorrect input date format: {exp_date}")
    #         date_diff = None
    #     return date_diff
    #
    # def format_exp_date(self, exp_date):
    #     try:
    #         date_formatted = datetime.strptime(exp_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    #     except ValueError:
    #         print(f"Incorrect input date format: {exp_date}")
    #         date_formatted = ''
    #     except TypeError:
    #         # print(f"Incorrect input date format: {exp_date}")
    #         date_formatted = ''
    #     return date_formatted


class Publication:

    def __init__(self, handler: BaseHandler, provider: BaseFeedProvider):
        self.handler = handler
        self.provider = provider

    def publish(self):
        text = self.provider.get_text()
        self.handler.add(text)


class InputBaseHandler(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_pub_type(self, *args, **kwargs):
        pass


class InputManualHandler(InputBaseHandler):

    def __init__(self, input_value: str):
        self.input_value = input_value

    def get_pub_type(self):
        publication_type_in = input(f'Select publication type you want to publish:'
                                    f'\n1 - News\n2 - Private Ad\n3 - Discount Coupon\n')
        return publication_type_in

    def get_pub_name(self, publication_type_in):
        publication_types = {'1': "News", '2': "Private Ad", '3': "Discount Coupon"}
        pub_name = publication_types[publication_type_in]
        return pub_name

    def get_city(self):
        publication_city_in = input("Add city: ")
        return publication_city_in

    def get_text(self):
        publication_text_in = input("Add text: ")
        return publication_text_in

    def get_exp_date(self):
        publication_exp_date_in = input("Add expiration date in YYYY-MM-DD format: ")
        try:
            datetime.strptime(publication_exp_date_in, '%Y-%m-%d')
            return publication_exp_date_in
        except ValueError:
            print(f'Incorrect date format "{publication_exp_date_in}". Should be a YYYY-MM-DD.')
            return None

    def get_discount(self):
        publication_discount_in = input("Add discount in %: ")
        try:
            return float(publication_discount_in)
        except ValueError:
            print(f'Incorrect discount size "{publication_discount_in}". Should be a number.')