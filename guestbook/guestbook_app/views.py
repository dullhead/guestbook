from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django import forms
from django.views.generic.edit import FormView

from google.appengine.api import users

from guestbook_app.models import Greeting, Guestbook, DEFAULT_GUESTBOOK_NAME

import urllib
import time


class MainView(TemplateView):
	template_name = "main_page.html"

	def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greetings = Greeting.get_latest(guestbook_name,10)

		if users.get_current_user():
			url = users.create_logout_url(self.request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linktext = 'Login'

		template_values = {
			'greetings': greetings,
			'guestbook_name': guestbook_name,
			'url': url,
			'url_linktext': url_linktext,
		}

		return template_values


class SignForm(forms.Form):
	guestbook_name = forms.CharField(
		label = "Guestbook_name",
		max_length = 10,
		required = True,
		widget = forms.TextInput()
	)
	greeting_message = forms.CharField(
		label = "Greeting Message",
		max_length = 50,
		required = True,
		widget = forms.Textarea()
	)

class SignView(FormView):
	template_name = "greeting.html"
	form_class = SignForm
	def form_valid(self, form):
		time.sleep(0.01)
		return redirect("/?guestbook_name=" + Greeting.put_from_dict(form.cleaned_data))
