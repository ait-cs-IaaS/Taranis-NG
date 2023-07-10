from celery import shared_task


@shared_task
def task1(msg: str):
    print(f"MESSAGE {msg}")


@shared_task
def task2():
    print("task2")
