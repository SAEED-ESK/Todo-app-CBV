{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello kia
{% endblock %}

{% block html %}
Hello {{user.username}}
{% endblock %}