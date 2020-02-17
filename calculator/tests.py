from django.test import SimpleTestCase
from django.urls import reverse

from calculator.forms import TomForm
from calculator.utils import get_discount_by_price, get_price_with_tax, get_price_with_discount
from tom.settings import STATE_TAXES


class TomTestCase(SimpleTestCase):
    BAD_FORM_DATA = dict(
        empty=dict(),
        bad_key=dict(foo='bar'),
        price_only_1=dict(price=-1),
        price_only_2=dict(price='1'),
        number_only_1=dict(number=-1),
        number_only_2=dict(number='1'),
        state_only_1=dict(state=-1),
        state_only_2=dict(state='1'),
        bad_price_number_1=dict(price=-1, number=-1),
        bad_price_number_2=dict(price=1, number=-1),
        bad_price_number_3=dict(price='', number=1),
        good_price_number=dict(price=1,  number=1),
        bad_price_number_state_1=dict(price=-1, number=-1, state=list(STATE_TAXES.keys())[0]),
        bad_price_number_state_2=dict(price=-1, number=1, state=list(STATE_TAXES.keys())[0]),
        bad_price_number_state_3=dict(price=1, number=-1, state=list(STATE_TAXES.keys())[0]),
        bad_price_number_state_4=dict(price=1, number=1, state=1),
        bad_price_number_state_5=dict(price=1, number=1, state='foo'),
    )
    GOOD_FORM_DATA = dict(
        first=dict(price=1, number=1, state=list(STATE_TAXES.keys())[0]),
        second=dict(price=1, number=42, state=list(STATE_TAXES.keys())[0]),
        third=dict(price=100000, number=1, state=list(STATE_TAXES.keys())[0]),
    )

    def test_get_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIsNone(response.context.get('price_with_discount'))
        self.assertIsNone(response.context.get('price_with_tax'))

    def test_empty_post_index(self):
        response = self.client.post(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIsNone(response.context.get('price_with_discount'))
        self.assertIsNone(response.context.get('price_with_tax'))

    def test_form_invalid(self):
        for case, data in self.BAD_FORM_DATA.items():
            with self.subTest(case):
                self.assertFalse(TomForm(data=data).is_valid())

    def test_form_valid(self):
        for case, data in self.GOOD_FORM_DATA.items():
            with self.subTest(case):
                self.assertTrue(TomForm(data=data).is_valid())

    def test_result(self):
        for case, data in self.GOOD_FORM_DATA.items():
            with self.subTest(case):
                response = self.client.post(reverse('index'), data)
                self.assertIsNotNone(response.context['price_with_discount'])
                self.assertIsNotNone(response.context['price_with_tax'])


class UtilsTestCase(SimpleTestCase):
    GET_DISCOUNT_BY_PRICE = dict(
        one=dict(price=-1, result=0),
        two=dict(price=0, result=0),
        three=dict(price=42, result=0),
        four=dict(price=1500, result=0),
        five=dict(price={}, result=0),
        six=dict(price=42, result=0),
        seven=dict(price=1000., result=3),
        eight=dict(price=5000., result=5),
        nine=dict(price=7000., result=7),
        ten=dict(price=10000., result=10),
        eleven=dict(price=50000., result=15),
        twelve=dict(price=49999., result=10),
        thirteen=dict(price=9999., result=7),
        fourteen=dict(price=6999., result=5),
        fifteen=dict(price=4999., result=3),
        sixteen=dict(price=999., result=0),
        seventeen=dict(price=100000, result=0),
    )

    GET_PRICE_WITH_TAX = dict(
        one=dict(price=-1, tax=1, result=-1),
        two=dict(price='', tax=1, result=''),
        three=dict(price={}, tax=1, result={}),
        four=dict(price=1., tax=0, result=1.),
        five=dict(price=100., tax=6., result=106.),
        six=dict(price=100., tax=10., result=110.),
        seven=dict(price=42.42, tax=2.35, result=43.41687),
        eight=dict(price=100., tax=-10., result=100.),
        nine=dict(price=100, tax=-10., result=100),
        ten=dict(price=100., tax=10, result=100.),
    )

    GET_PRICE_WITH_DISCOUNT = dict(
        one=dict(price=-1, discount=1, result=-1),
        two=dict(price='', discount=1, result=''),
        three=dict(price={}, discount=1, result={}),
        four=dict(price=1., discount=0, result=1.),
        five=dict(price=100., discount=6, result=94.),
        six=dict(price=100., discount=10, result=90.),
        seven=dict(price=42.42, discount=2, result=41.571600000000004),
        eight=dict(price=100., discount=-10., result=100.),
        nine=dict(price=100, discount=6, result=100),
        ten=dict(price=100., discount=6., result=100.),
    )

    def test_get_discount_by_price(self):
        for case, data in self.GET_DISCOUNT_BY_PRICE.items():
            with self.subTest(case):
                self.assertEqual(get_discount_by_price(data['price']), data['result'])

    def test_get_price_with_tax(self):
        for case, data in self.GET_PRICE_WITH_TAX.items():
            with self.subTest(case):
                self.assertEqual(get_price_with_tax(data['price'], data['tax']), data['result'])

    def test_get_price_with_discount(self):
        for case, data in self.GET_PRICE_WITH_DISCOUNT.items():
            with self.subTest(case):
                self.assertEqual(get_price_with_discount(data['price'], data['discount']), data['result'])
