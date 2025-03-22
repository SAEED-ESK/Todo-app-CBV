{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reset Password Link
{% endblock %}

{% block html %}
http://127.0.0.1:8000/accounts/api/v1/reset_password_confirm/{{token}}/
{% endblock %}