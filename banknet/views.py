from .models import Rating
from .services import Method
from django.shortcuts import render
from .libraries.KohonenNet import KohonenNet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def about(request):
    return render(request, 'banknet/about.html')

def rating_list(request, method = 'byEuclid'):
    rows = 25
    count = Rating.objects.count()
    page = request.GET.get('page')
    end = rows * int(page if page else 1)
    start = end - rows
    ratings_list = Method.make_retings(Rating.objects.all().order_by('id').reverse()[start:end], method)
    try:
        paginator = Paginator(list(range(0, start)) + list(ratings_list) + list(range(end, count)), rows)
        ratings = paginator.page(page)
    except PageNotAnInteger:
        ratings = paginator.page(1)
    except EmptyPage:
        ratings = paginator.page(paginator.num_pages)
    except Exception:
        ratings = None
    return render(request, 'banknet/rating_list.html', {'ratings': ratings})

def correct_weight(request):
    success = None
    max_samples_count = Rating.objects.count()
    if request.method == 'POST':
        success = Method.save(
            Rating.objects.all(),
            request.POST.get('samples-count', '20'),
            request.POST.get('ratio-upper-limit', '0.3'),
            request.POST.get('ratio-lower-limit', '0.0'),
            request.POST.get('ratio-step', '0.5'),
            request.POST.get('method', 'byEuclid')
        )
    return render(request, 'banknet/correct_weight.html', {
        'max_samples_count': max_samples_count,
        'success': success
    })