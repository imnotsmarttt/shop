from datetime import datetime

from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .forms import CouponForm
from .models import Coupon


@require_POST
def coupon_apply(request):
    now = datetime.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, is_active=True, valid_from__lte=now, valid_to__gte=now)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            form.add_error('__all__', 'Купон не действителен')
            request.session['coupon_id'] = None
    return redirect('cart_detail')

