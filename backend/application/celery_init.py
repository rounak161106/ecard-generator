from celery import Celery, Task
import os
import sys

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    try:
        import celery_config
        celery_app.config_from_object(celery_config)
    except Exception as e:
        print("[Celery init] Could not load celery_config:", e)

    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app