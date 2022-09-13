from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import ProductComment
from catalog.models import Product


@login_required
def comment_post(request):
    try:
        parent = ProductComment.objects.get(id=int(request.POST.get('parentid')))
    except:
        parent = None
    product = Product.objects.get(id=request.POST.get('product_id'))
    content = request.POST.get('comment')
    if content:
        comment = ProductComment(user=request.user, product=product, content=content, parent=parent)
        comment.save()
        return JsonResponse({
            'user': comment.user.username,
            'content': comment.content,
            'created': comment.created,
            'id': comment.id
        })
    else:
        return JsonResponse({'error': True})