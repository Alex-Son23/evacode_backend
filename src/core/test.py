import unittest
from pycbrf import ExchangeRates
import datetime
from pprint import pprint
from currency_symbols import CurrencySymbols


def curr(krw_kzt, krw_eur, val):
    currencies = [
        "USD",
        "RUB",
        "EUR",
        "KZT",
        "UZS",
        "KGS"
    ]

    currency_data = [
        {
            'value': 'KRW',
            'curr': 1,
            'symbol': '₩',
            'locale': 'ko-KR',
        }
    ]

    return_curr = {}
    c = ExchangeRates(str(datetime.datetime.now())[:10])
    # c = ExchangeRates(str(datetime.datetime.now()))

    for curr in currencies:
        if curr == "RUB":
            rub_kor = 1 / krw_kzt
            return_curr[curr] = rub_kor * val
            currency_data.append(
                {
                    'value': curr,
                    'curr': rub_kor,
                    'symbol': CurrencySymbols.get_symbol(curr),
                    'locale': 'ru',
                }
            )
            continue
        try:
            if curr in ('USD', 'EUR'):
                rub_kor = 1 / krw_eur
            else:
                rub_kor = 1 / krw_kzt
            print(rub_kor, float(c[curr].rate))
            return_curr[curr] = (rub_kor / float(c[curr].rate)) * val
            currency_data.append(
                {
                    'value': curr,
                    'curr': rub_kor / float(c[curr].rate),
                    'symbol': CurrencySymbols.get_symbol(curr),
                    'locale': '',
                }
            )
        except Exception as e:
            print(e)
            currency_data.append(
                {
                    'value': curr,
                    'curr': 0,
                    'symbol': '',
                    'locale': '',
                }
            )
    pprint(return_curr)
    return return_curr


class TestClass(unittest.TestCase):
    def test_curr(self):
        self.assertEqual(curr(12.5, 13, 300000),
                         {"USD": 263.0, "RUB": 24000.0, "EUR": 241.0, "KZT": 129844.0, "UZS": 3312117.0,
                          "KGS": 22389.0})
        # self.assertEqual(curr(12.5, 13, 30000),
        #                  {"USD": 26.0, "RUB": 2400.0, "EUR": 24.0, "KZT": 12987.0, "UZS": 331322.0,
        #                   "KGS": 2240.0})


if __name__ == '__main__':
    unittest.main()
