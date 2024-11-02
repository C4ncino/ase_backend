from celery import Celery, Task


def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()

    celery_app.conf.task_queues = app.config["CELERY"]["task_queues"]
    app.extensions["celery"] = celery_app

    return celery_app
