from django.db.models.query import QuerySet


def add_sorting_if_exists(request, query_set: QuerySet, fields: list[str]) -> QuerySet:
    to_sort = []

    for field in fields:
        if sort_by := request.GET.get(field, '').lower():
            if sort_by == 'asc':
                to_sort.append(field)
            elif sort_by == 'desc':
                to_sort.append(f'-{field}')

    query_set = query_set.order_by(*to_sort)

    return query_set
