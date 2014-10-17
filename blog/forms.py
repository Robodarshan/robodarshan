from django import forms as django_forms
import bleach

class BlogEditForm(django_forms.Form):
	title = django_forms.CharField(max_length=500, widget=django_forms.TextInput(attrs={'placeholder': 'Title'}))
	body = django_forms.CharField(widget=django_forms.Textarea)

	def clean(self):
		cleaned_data = super(BlogEditForm, self).clean()

		body = cleaned_data.get("body")

		# clean with python bleach
		white_list_tags = [u'h2', u'p', u'a', u'img', u'ol', u'ul', u'li',
						 u'strong', u'em', u'blockquote', u'sub', u'sup', u'iframe']
		white_list_attrs = {
				'img': ['src', 'title'],
				'*':	['style', 'class'],
				'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen']
				}
		white_list_styles = ['padding', 'padding-left']
		body = bleach.clean(body, white_list_tags, white_list_attrs, white_list_styles)
		cleaned_data['body'] = body

		return cleaned_data