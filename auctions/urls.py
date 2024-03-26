from django.urls import path, re_path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("activelisting", views.active, name="active"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting/", views.create_listing, name="create-listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("addtowatchlist/<int:listing_id>", views.add_to_watchlist, name="addtowatchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.category, name="category"),
    path("bid/<int:listing_id>", views.bidding, name="bidding"),
    path("categories/<str:category_name>", views.listing_by_category, name="listcategory")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
