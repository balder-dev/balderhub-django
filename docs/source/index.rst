BalderHub Django
================

**Test Django applications with ready-to-use Balder test scenarios and features.**

This is a BalderHub package for the `Balder<https://docs.balder.dev>`_ test framework. If you are new to Balder check out the
`official documentation <https://docs.balder.dev>`_ first.

``balderhub-django`` is a BalderHub package that provides
**ready-to-use, high-quality test scenarios and building blocks** for comprehensively testing
applications built with the `Django<https://www.djangoproject.com/>`_ web framework.

At the moment, it focuses especially on validating the Django admin interface and data management workflows,
and integrates tightly with ``balderhub-crud`` to deliver reusable CRUD test capabilities tailored
for Django-based systems.

What you will find in this package
----------------------------------

- **Django Admin Page Objects** - Reusable page abstractions for common Django admin views (login, index, change list, change form)
- **CRUD Integration for Django Admin** - Specialized field callbacks and setup features extending ``balderhub-crud`` for Django admin forms (text inputs, textareas, dates, foreign keys, many-to-many)
- **Data Environment Utilities** - Helpers for setting up Django data models in test environments
- **Extensible Foundation** - Clean base classes to implement tests against your own Django applications and custom admin configurations

.. note::
   Please note, this package is still under development. If you would like to contribute, take a look into the
   `project <https://github.com/balder-dev/balderhub-django/>`_.

This is a BalderHub package for the `Balder <https://docs.balder.dev/>`_ test framework. If you are new to Balder check
out the `official documentation <https://docs.balder.dev>`_ first.


.. toctree::
   :maxdepth: 2

   installation.rst
   topic_intro.rst
   scenarios.rst
   features.rst
   examples.rst
   utilities.rst
