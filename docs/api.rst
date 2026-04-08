:tocdepth: 2
API
===

This part of the documentation lists the full API reference of all classes and functions.

WSGI
----

.. autoclass:: my_fastapi_project.wsgi.ApplicationLoader
   :members:
   :show-inheritance:

Config
------

.. automodule:: my_fastapi_project.config

.. autoclass:: my_fastapi_project.config.application.Application
   :members:
   :show-inheritance:

.. autoclass:: my_fastapi_project.config.redis.Redis
   :members:
   :show-inheritance:

.. automodule:: my_fastapi_project.config.gunicorn

CLI
---

.. automodule:: my_fastapi_project.cli

.. autofunction:: my_fastapi_project.cli.cli.cli

.. autofunction:: my_fastapi_project.cli.utils.validate_directory

.. autofunction:: my_fastapi_project.cli.serve.serve

App
---

.. automodule:: my_fastapi_project.app

.. autofunction:: my_fastapi_project.app.asgi.on_startup

.. autofunction:: my_fastapi_project.app.asgi.on_shutdown

.. autofunction:: my_fastapi_project.app.asgi.get_application

.. automodule:: my_fastapi_project.app.router

Controllers
~~~~~~~~~~~

.. automodule:: my_fastapi_project.app.controllers

.. autofunction:: my_fastapi_project.app.controllers.ready.readiness_check

Models
~~~~~~

.. automodule:: my_fastapi_project.app.models

Views
~~~~~

.. automodule:: my_fastapi_project.app.views

.. autoclass:: my_fastapi_project.app.views.error.ErrorModel
   :members:
   :show-inheritance:

.. autoclass:: my_fastapi_project.app.views.error.ErrorResponse
   :members:
   :show-inheritance:

Exceptions
~~~~~~~~~~

.. automodule:: my_fastapi_project.app.exceptions

.. autoclass:: my_fastapi_project.app.exceptions.http.HTTPException
   :members:
   :show-inheritance:

.. autofunction:: my_fastapi_project.app.exceptions.http.http_exception_handler

Utils
~~~~~

.. automodule:: my_fastapi_project.app.utils

.. autoclass:: my_fastapi_project.app.utils.aiohttp_client.AiohttpClient
   :members:
   :show-inheritance:

.. autoclass:: my_fastapi_project.app.utils.redis.RedisClient
   :members:
   :show-inheritance:
