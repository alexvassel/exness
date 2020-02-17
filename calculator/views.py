from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from calculator.utils import get_discount_by_price, get_price_with_discount, get_price_with_tax
from tom.settings import STATE_TAXES
from .forms import TomForm


def index(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TomForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            number = form.cleaned_data['number']
            full_price = float(price * number)
            discount = get_discount_by_price(full_price)
            price_with_discount = get_price_with_discount(full_price, discount)
            price_with_tax = get_price_with_tax(price_with_discount, float(STATE_TAXES[form.cleaned_data['state']]))
            return render(request, 'index.html', {'form': form, 'price_with_discount': price_with_discount,
                                                  'price_with_tax': price_with_tax, 'taxes': STATE_TAXES,
                                                  'full_order_price': full_price})
    else:
        form = TomForm()
    return render(request, 'index.html', {'form': form, 'taxes': STATE_TAXES})
