# Adminplus

WIP: 20%

Adds a page to the admin, can be used to add some features to the admin.

# Integrate _adminplus in your admin

2 ways:

- override the admin

In the INSTALLED_APPS, just set _adminplus at the very top, a modifyed admin/base.html is included.

- or set this button somewhere

```html
{% if user.is_active and user.is_staff %}
<a href="{% url 'adminplus' %}">
  <h1>Admin +</h1>
</a>
{% endif %}
```
