# BalderHub Package ``balderhub-django``

**Test Django applications with ready-to-use Balder test scenarios and features.**

This is a BalderHub package for the [Balder](https://docs.balder.dev) test framework. If you are new to Balder check out the
[official documentation](https://docs.balder.dev) first.

``balderhub-django`` is a BalderHub package that provides 
**ready-to-use, high-quality test scenarios and building blocks** for comprehensively testing 
applications built with the [Django](https://www.djangoproject.com/) web framework.

At the moment, it focuses especially on validating the Django admin interface and data management workflows, 
and integrates tightly with ``balderhub-crud`` to deliver reusable CRUD test capabilities tailored 
for Django-based systems.

## What you will find in this package

- **Django Admin Page Objects** - Reusable page abstractions for common Django admin views (login, index, change list, change form)
- **CRUD Integration for Django Admin** - Specialized field callbacks and setup features extending ``balderhub-crud`` for Django admin forms (text inputs, textareas, dates, foreign keys, many-to-many)
- **Data Environment Utilities** - Helpers for setting up Django data models in test environments
- **Extensible Foundation** - Clean base classes to implement tests against your own Django applications and custom admin configurations

## Installation

You can install the latest release with pip:

```
python -m pip install balderhub-django
```

For the full CRUD functionality you may want to install the optional extra:

```
python -m pip install "balderhub-django[crud]"
```

# Check out the documentation

If you need more information, 
[checkout the ``balderhub-django`` documentation](https://hub.balder.dev/projects/django).

# License

This BalderHub package is free and Open-Source

Copyright (c) 2026 Max Stahlschmidt

Distributed under the terms of the MIT license