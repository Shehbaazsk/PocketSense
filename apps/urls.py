from django.urls import include, path

urlpatterns = [
    path(r"users/", include("apps.accounts.urls")),
    path(r"groups/", include("apps.groups.urls")),
    path(r"expenses/", include("apps.expenses.urls")),
    path(r"settlements/", include("apps.settlements.urls")),
]
