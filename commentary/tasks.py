from celery import shared_task
from django.db.models import Avg

from books.models import Books
from .models import Review


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def recalculate_book_rating(self, book_id: int):
    try:
        average = Review.objects.filter(
            book_id=book_id, rating__isnull=False).aggregate(avg=Avg("rating"))["avg"]

        Books.objects.filter(id=book_id).update(rating=round(average or 0, 2))

    except Exception as exc:
        raise self.retry(exc=exc)


