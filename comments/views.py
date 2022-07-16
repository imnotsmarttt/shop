from django.shortcuts import reverse
from django.views.generic import CreateView
from django.http import HttpResponseRedirect

from .forms import CommentForm
from .models import ProductComment
from catalog.models import Product


# class CreateChildComment(CreateView):
#     model = ProductComment
#     success_url = re


def reply_comment(request, parent_id, product_id):
    prnt = ProductComment.objects.get(id=parent_id)
    prdct = Product.objects.get(id=product_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if request.user.is_authenticated:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.parent = prnt
                new_comment.product = prdct
                new_comment.user = request.user
                new_comment.content = comment_form.cleaned_data.get('content')
                new_comment.save()
                return HttpResponseRedirect(reverse('product_detail', kwargs={'slug': prdct.slug}))
        else:
            comment_form.add_error('__all__', 'Оставлять комментарии могуть только аутентифицированные пользователи')
            return comment_form.form_invalid()