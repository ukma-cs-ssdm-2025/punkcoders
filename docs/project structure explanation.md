Currently, we have the accounts app, which will have anything we might want to glue on top of Django's auth system, and the restaurant app, which is for the rest of the business logic. If the restaurant app grows too big to work with, we can replace it with smaller apps like menu and orders. Note that Django apps are meant to be separated by their domain (menu, orders), not their internal function (models, controllers, views).

URLs for the API endpoints are going to look like api/vX/whatever, while webpage enpoints will look like /whatever. There may be webpages for the exact same things as the API endpoints, like "show all dishes", or for things there is no API endpoint for, like a form for creating a dish.

