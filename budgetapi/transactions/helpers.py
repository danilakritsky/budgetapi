import datetime

from django.db.models import F, Sum


def get_balance(queryset):
    return queryset.values("amount").aggregate(current_balance=Sum("amount"))


def get_categories_summary(queryset):
    result = (
        queryset.values("category__category_name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
        # rename category field
        .annotate(category=F("category__category_name"))
        .values("category", "total")
    )
    return {category["category"]: category["total"] for category in result}


def get_companies_summary(queryset) -> dict:
    result = (
        queryset.values("company")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    return {company["company"]: company["total"] for company in result}


def get_monthly_summary(queryset) -> dict:
    result = (
        queryset.values("datetime__year", "datetime__month")
        .annotate(total=Sum("amount"))
        .order_by("datetime")
        # rename category field
        .annotate(year=F("datetime__year"), month=F("datetime__month"))
        .values("year", "month", "total")
    )
    return {
        f"{month['year']}-{month['month']:02d}": month["total"]
        for month in result
    }


def get_summary(queryset) -> dict:
    return {
        "current_balance": get_balance(queryset)["current_balance"],
        "monthly_balance": get_monthly_summary(queryset),
        "categories": get_categories_summary(queryset),
        "companies": get_companies_summary(queryset),
    }


def get_current_week_data(queryset):
    start_of_week = datetime.date.today() - datetime.timedelta(
        days=datetime.date.today().weekday()
    )
    this_week = queryset.filter(datetime__date__gte=start_of_week)
    return this_week


def get_current_week_summary(queryset) -> dict:
    this_week = get_current_week_data(queryset)
    return {
        "current_week_balance": (
            f"{get_balance(this_week)['current_balance'] or 0}"
        ),
        "balance_per_category": (get_categories_summary(this_week)),
        "balance_per_company": (get_companies_summary(this_week)),
    }


def get_current_week_text_summary(queryset) -> str:
    start_of_week = datetime.date.today() - datetime.timedelta(
        days=datetime.date.today().weekday()
    )
    this_week = queryset.filter(datetime__date__gte=start_of_week)
    return (
        "BUDGET SUMMARY\n"
        + "-----------------------\n"
        + f"CURRENT_BALANCE: {get_balance(queryset)['current_balance']}\n"
        + "\nTHIS WEEK'S STATS\n"
        + "-----------------------\n"
        + f"Balance: {get_balance(this_week)['current_balance'] or 0}\n"
        + "Balance per category:\n"
        + (
            "\n".join(
                [
                    f"- {category}: {total}"
                    for category, total in get_categories_summary(
                        this_week
                    ).items()
                ]
            )
            or "0"
        )
        + "\n"
        + "Balance per company:\n"
        + (
            "\n".join(
                [
                    f"- {company}: {total}"
                    for company, total in get_companies_summary(
                        this_week
                    ).items()
                ]
            )
            or "0"
        )
    )
