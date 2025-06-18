from rest_framework.routers import DefaultRouter

from .views import BooksViewSet

router = DefaultRouter()
router.register(r'books', BooksViewSet, basename='books')

urlpatterns = router.urls
