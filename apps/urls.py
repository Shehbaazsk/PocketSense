from django.urls import include, path

urlpatterns = [
    path("users/", include("apps.accounts.urls")),
    path("groups/", include("apps.groups.urls")),
    path("expenses/", include("apps.expenses.urls")),
]
