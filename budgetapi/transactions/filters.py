from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from .models import Transaction


class TransactionFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            "datetime": [
                "time__exact",
                "time__lt",
                "time__gt",
                "date__exact",
                "date__lt",
                "date__gt",
            ],
            "amount": ["exact", "lt", "gt"],
        }


class CustomOrderingFilter(OrderingFilter):
    def remove_invalid_fields(self, queryset, fields, view, request):
        valid_fields = [
            item[0]
            for item in self.get_valid_fields(
                queryset, view, {"request": request}
            )
        ]

        def term_valid(term):
            if term.startswith("-"):
                term = term[1:]
            return term in valid_fields

        result = [term for term in fields if term_valid(term)]
        return result

    def filter_queryset(self, request, queryset, view):
        """
        Filter query set by requested ordering.
        Allows filtering datetime fields by specifying 'date' or 'time'
        as an ordering term.
        """
        ordering = self.get_ordering(request, queryset, view)

        if ordering:

            def get_ordering_tuple(term: str) -> tuple[str, str]:
                if term.startswith("-"):
                    return ("-", term[1:])
                else:
                    return ("", term)

            def make_datetime_term(date_or_time_term: str) -> str:
                modifier, term = get_ordering_tuple(date_or_time_term)
                return modifier + "datetime__" + term

            def is_datepart_term(term: str) -> bool:
                return term in ("date", "-date", "time", "-time")

            ordering = [
                make_datetime_term(term) if is_datepart_term(term) else term
                for term in ordering
            ]
            return queryset.order_by(*ordering)

        return queryset
