import time
from celery import shared_task


@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    arr = []

    for i in range(50000000):
        i *= i
        arr.append(i)

    time.sleep(5)

    return a + b
