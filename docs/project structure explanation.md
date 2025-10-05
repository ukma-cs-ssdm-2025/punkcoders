# Project (/src) structure

The /src/ folder contains the Django project and various files needed to run it using Docker. The only one you may need to touch is **.env.sample**. If you don't have a **.env** file, copy .env.sample and remove .sample. If you need to change the environment variables, make sure these changes are copied over to .env.sample. But try not to mess with the configuration files unless you know what you're doing and/or are that desperate.

## /src/delivery-service

This is the Django project. It contains several Django apps, which separate code by domain (menu, orders...), not functionality (models, controllers...). It also contains manage.py, which is the thing you run to do stuff with the project, and startup.sh, which is what Docker does after it sets the containers up.

### /src/delivery-service/accounts

Django does auth for us, but if we need to add anything on top of it, like fancy HTML, custom user data etc, it goes into this app. If this app gets a lot of data in it, we can create the same folder structure inside as in restaurant/.

### /src/delivery-service/app

This is where the stuff that the entire project uses during its runtime goes. Don't ask me about asgi.py and wsgi.py (and probably don't touch them), but urls.py is where you describe the valid URLs on our site (or import them from other apps), and **settings.py** is for the project's settings (duh). If you don't have settings.py, copy it out of **settings.py.sample**, and if you change it, make sure to also update the sample if you want to confirm the changes.

### /src/delivery-service/restaurant

This is where the rest of the business logic goes for now. If it grows too bulky, we can split it into menu/, orders/, map/ and such.

#### /src/delivery-service/restaurant/forms

These are Django forms used by webpage views to take and validate data from the user. Often tied to models.

#### /src/delivery-service/restaurant/migrations

Migrations are like commits for changes to the DB's structure. Instead of changing the schema manually via SQL don't change the database itself (in a way that can't be synchronized with the rest of the team), you write a migration. Or rather, you let python manage.py makemigrations write them for you based on models. Then everyone can write python manage.py migrate (in the live app container's shell) to update their DB with the changes. If you do need to make a change manually, google the rules for making migrations or ask me.

#### /src/delivery-service/restaurant/models

Models are classes used to interface with the DB without writing SQL.

#### /src/delivery-service/restaurant/serializers

These are used by Django Rest Framework to describe and validate the data accepted and returned by our API. They seem similar to models and forms - I wonder if you can synchronize them in some way?

#### /src/delivery-service/restaurant/services

These interact with models on the views' behalf. This way, the business logic of operating on data can be reused by different views. Kinda similar to controllers of MVC, but apparently, Django views are also kinda controllers, so we don't use that work?

#### /src/delivery-service/restaurant/static

This is where static content, like CSS and JS, goes.

#### /src/delivery-service/restaurant/templates

These are HTML templates that render(...) is going to plug data into to make pretty webpages.

#### /src/delivery-service/restaurant/templatetags

Custom filters for templates go here.

#### /src/delivery-service/restaurant/tests

IDK how to write tests in Django, but it's googleable and hopefully not my problem. Still, it's better to write tests with the code and not as an afterthought if we don't want maintaining them to be a nightmare.

#### /src/delivery-service/restaurant/urls

These describe the main app's URLs in more detail. Obviously, api.py is for API endpoints, and web.py is for webpage URLs. They're included into the global urls.py in different ways, so please don't mix them.

#### /src/delivery-service/restaurant/views

The functions that accept requests, consult services, and return responses. API endpoints go into api/ and use DRF's ApiView/ViewSet and Response, while web/ contains vanilla Django views that return render(...).
