# Template Guide
Last updated: 1 March 2025

Templating is done using django-templates, read about the syntax [here](https://docs.djangoproject.com/en/5.1/ref/templates/language/).

Each file has specific context attached to it, i.e. variables you can refer to with information, like if the user is authenticated, different kinds of models, locales, etc.

You may refer to this file to quickly refer to what the context is.

## URL Reversing
Often, you might see `{% url "posts:home" %} or `{% url "posts:detail" post.pk %}

## Global Context
All templates can access these variables:
- request (can be used to access the current user session, including auth) via
  - request.is_authenticated

- settings (the current loaded settings.py file, refer to this carefully as you can expose secrets)


## Models
`posts` is a common context variable that is filled with `Post` models. These are the attributes of a directly provided (not serialized into JSON) and `users` refers to `User`. Each field also has a `pk` variable that refers to the primary key.

Post
- id: int {pk}
- title: str
- description: str
- author: User object
- start_date: datetime object
- end_date: datetime object
- created_at: datetime object
- location: PostLocation (__str__ refers to PostLocation.name)
- tags: _TaggableManager
- image: Image {optional}

PostLocation
- name: str {pk}

_TaggableManager: [simplified]
- all: list[str] (all the avaliable tags)

User: [simplified]
- id: int {pk}
- name: str
- email: str
- is_author: bool
- is_staff: bool

datetime objects when printed, default to a format of "Feb. 27, 2025, 10:50 p.m.".
You can change this by changing the `date` kwarg, i.e.:

<p>{{ post.created_at|date:"j F, Y, g:i a" }}</p>
27 February, 2025, 10:50 p.m.

You can read more about the date formats [here](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date).




## Templates
`base.html`
Everything inherits from this file, defines all the meta files, loads static, navbar, etc.
Extendable blocks include:
- title (<title/>)
- css (add file-specific stylesheets, remember to {{ block.super }})
- java (add file-specific script files, remember to {{ block.super }})
- body (to override all content)
- main/content (main file elements)
- modal (add any pop-ups here)
- inline_javascript (minor functions that don't deserve to be in a js file)

The navbar active links are auto set by a custom templatetag (the class called is `.nav-active`), see pre-made example in file.



`posts/home.html`
The primary page users will view, starts with an initial set of posts based on the URL filters (see `static/js/home.js` for more info -- same filters).

Initial set of posts can be referred with `posts` and the filter params by `params`. Filter params come in a dictionary (key: value). Latest filters are:
- page (p): int
- posts_per_page (c): int
- sort_type (s): "newest" | "oldest" | "start_date"
- author_ids (a): list[str]
- tags (t): list[str]

`home.js` comes with a basic function, `refreshPosts` that outlines how to dynamically query and refresh posts when filters are changed.


`posts/compact_posts.html`
When refreshing posts dynamically, it must be rendered first by the server to avoid code repetition. This is where a set of `posts` are rendered.

For standarization, `home.html` {% include %}s this file.


`posts/detail.html`
When a post is clicked, this is the URL that the browser should forward to see all the 'details' of the post.

To the user, the URL should be like: `domain.com/post/<int>`. To you, it should be `{% url "posts:detail" post.pk}`.


`dashboard/home.html`
docs WIP

`dashboard/post_form.html`
docs WIP


Accounts and logging in is done via abstraction and inheritance mostly.

Since there are 9,483,234 templates that need to be made for auth like forgot password, sign up, social auth, email confirmation which all really share the same stuff:
`django-allauth` has nicely provided an abstraction using `crispy_forms` which also does all the relevant field validation (like checking the email is an email).

The `allauth/elements` directory consists of the main elements, like the buttons, fields, etc.

There are two main files in `allauth/layouts`: `entrance.html` and `manage.html`.

`manage.html` should not be changed unless necessary, adding stuff to ALL the auth pages (like adding an app-wide css file) should be done in `entrance.html`.


## URLs
There should be examples of URLs in the templates already, if you would like to take a look at all the currently added URLs, follow `config/urls.py`.

That should `include()` urls from apps, defined in `discoverutm/<app_name>/urls.py`. Each app url points to a view that points to the template (and defines context)
and most have a `name` kwarg, this is the reverse kwarg if you would like to access this url.

Example:
`discoverutm/posts/detail.py`
The name for one url is `post-detail`, so you can reverse to it by doing {% url "post-detail" %}.

Some url files have an app_name at the top,
`discoverutm/dashboard/urls.py`

```python
app_name = "dashboard"
urlpatterns = [
    path("", views.dashboard_page_view, name="home"),
    path("new/", views.post_form_view, name="new-post"),
]
```

In this case, to refer to the first url, {% url "dashboard:home" %} (prefix by app_name).

If quotes, just use " in the html tag and ' in the template tag. Like "{% url 'dashboard:home' %}"
