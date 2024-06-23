from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def Paginate(request, queryset, results):
    page = request.GET.get("page")
    paginator = Paginator(queryset, results)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        data = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages()
        data = paginator.page(page)

    leftIndex = int(page) - 2

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 3

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return data, custom_range
