from unittest import TestCase
from unittest.mock import patch

from bs4 import BeautifulSoup

from backend.celery_tasks import get_info_about_product


class TestParser(TestCase):

    def test_parser_with_specification_available(self):
        mock_get_patcher = patch('backend.celery_tasks.get_product_html')
        mock_get = mock_get_patcher.start()

        html_str = BeautifulSoup(str(open("mock_files/test_parser_with_specification_available.txt", encoding="utf8").readlines()))
        result = ["MAKE UP FOR EVER HD SKIN UNDETECTABLE STAY-TRUE FOUNDATION Тональный крем 397291",
                  4300, 2500, 2500]

        mock_get.return_value = html_str

        url = 'https://ephora.ru/make-up/tint/cream/make-up-for-ever-hd-skin-prod8l06/397291'
        response = get_info_about_product(url=url)

        mock_get_patcher.stop()

        self.assertEqual(response, result)

    def test_parser_with_specification_not_available(self):
        mock_get_patcher = patch('backend.celery_tasks.get_product_html')
        mock_get = mock_get_patcher.start()

        html_str = BeautifulSoup(
            str(open("mock_files/test_parser_with_specification_not_available.txt", encoding="utf8").readlines()))

        result = ["MAKE UP FOR EVER HD SKIN UNDETECTABLE STAY-TRUE FOUNDATION Тональный крем 397291",
                  4300, 4300, 4300]

        mock_get.return_value = html_str

        url = 'https://ephora.ru/make-up/tint/cream/make-up-for-ever-hd-skin-prod8l06/397291'
        response = get_info_about_product(url=url)

        mock_get_patcher.stop()

        self.assertEqual(response, result)

    def test_parser_without_specification_available_sale(self):
        mock_get_patcher = patch('backend.celery_tasks.get_product_html')
        mock_get = mock_get_patcher.start()

        html_str = BeautifulSoup(str(
            open("mock_files/test_parser_without_specification_available.txt", encoding="utf8"
                 ).readlines()))
        result = ["MAKE UP FOR EVER HD SKIN UNDETECTABLE STAY-TRUE FOUNDATION Тональный крем",
                  8200, 0, 1200]

        mock_get.return_value = html_str
        url = 'https://ephora.ru/make-up/tint/cream/make-up-for-ever-hd-skin-prod8l0'
        response = get_info_about_product(url=url)

        mock_get_patcher.stop()

        self.assertEqual(response, result)

    def test_parser_without_specification_available_card(self):
        mock_get_patcher = patch('backend.celery_tasks.get_product_html')
        mock_get = mock_get_patcher.start()

        html_str = BeautifulSoup(str(
            open("mock_files/test_parser_without_specification_available_card.txt", encoding="utf8"
                 ).readlines()))
        result = ["MAKE UP FOR EVER HD SKIN UNDETECTABLE STAY-TRUE FOUNDATION Тональный крем",
                  8200, 1200, 0]

        mock_get.return_value = html_str
        url = 'https://ephora.ru/make-up/tint/cream/make-up-for-ever-hd-skin-prod8l0'
        response = get_info_about_product(url=url)

        mock_get_patcher.stop()

        self.assertEqual(response, result)

    def test_parser_without_specification_not_available(self):
        mock_get_patcher = patch('backend.celery_tasks.get_product_html')
        mock_get = mock_get_patcher.start()

        html_str = BeautifulSoup(
            str(open("mock_files/test_parser_without_specification_not_available.txt", encoding="utf8").readlines()))

        result = ["MAKE UP FOR EVER HD SKIN UNDETECTABLE STAY-TRUE FOUNDATION Тональный крем",
                  2500, 0, 0]

        mock_get.return_value = html_str

        url = 'https://ephora.ru/make-up/tint/cream/make-up-for-ever-hd-skin-prod8l06/'
        response = get_info_about_product(url=url)

        mock_get_patcher.stop()

        self.assertEqual(response, result)
