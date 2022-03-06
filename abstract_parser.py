from abc import abstractmethod, ABC


class ABCParser(ABC):

    @abstractmethod
    def get_low_price(self):
        """
        Returns low price
        """

    @abstractmethod
    def get_high_price(self):
        """
        Return price
        :return:
        """


class SingleOptionParser(ABCParser):
    def __init__(self):
        super().__init__()

    def get_low_price(self):
        pass

    def get_high_price(self):
        pass


class MultipleOptionsParser(ABCParser):
    def __init__(self):
        super().__init__()

    def get_low_price(self):
        pass

    def get_high_price(self):
        pass


