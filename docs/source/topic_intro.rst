Introduction into Django
************************

What is Django?
===============

Django is a high-level Python web framework that comes with most of the tools you need to build web applications right
out of the box. It includes an ORM, template system, form handling, authentication, and a lot more. The idea is to let
developers focus on their application logic instead of writing the same plumbing code over and over
again.

This BalderHub closes the loop and provides ready-to-use features and test scenarios for writing integration/e2e tests
with the same speed.

One of Django's most practical features is the admin interface. It automatically creates a web-based management area
for your data models. You get list views where you can browse, search, filter and sort records, plus dedicated forms
for adding or editing single entries. The admin knows how to deal with relationships like foreign keys and many-to-many
fields, supports custom actions, and comes with a permission system so you can control who is allowed to do what.

About this BalderHub package
============================

This BalderHub package provides different features for testing django applications, specially the admin area and the
data management flows around it. The page objects and CRUD helpers are written to match how the admin actually renders
its forms and processes input.

Ready to use Page Objects
-------------------------

This package comes with ready-made page objects that map directly to the mostly used Django admin pages:

* the login page
* the main admin index
* change-list views for browsing multiple records
* change-form views for editing single entries

Find examples :ref:`here <Use Django Admin Page Objects>`.

Ready to use CRUD features for the admin area
---------------------------------------------

On top of that it integrates tightly with ``balderhub-crud``. A set of setup features and field callbacks make the
common admin form elements (text fields, text areas, dates, foreign keys, many-to-many relations) work out of the box
so you do not need to write CRUD features by yourself.

Find examples :ref:`here <Use the CRUD Feature Factories for testing Django Admin Operations>`.

Data Environment from Django Fixtures
-------------------------------------

The package also offers small utilities that load Django fixture files into the test database. This gives you a fast
way to seed realistic data for your scenarios without writing repetitive setup code.

Find an example :ref:`here <Use the Django Mixin>`.

