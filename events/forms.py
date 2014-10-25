from django import forms as django_forms
import bleach


class EventForm(django_forms.Form):
    title = django_forms.CharField(
        max_length=500,
        widget=django_forms.TextInput(attrs={'placeholder': 'Title'}))
    cover_image_link = django_forms.CharField(max_length=256, required=False)
    time = django_forms.DateField(widget=django_forms.SplitDateTimeWidget)
    location = django_forms.CharField(max_length=256)
    description = django_forms.CharField(widget=django_forms.Textarea)
    coordinator1 = django_forms.CharField(max_length=256)
    coordinator2 = django_forms.CharField(max_length=256)

    def clean(self):
        cleaned_data = super(EventForm, self).clean()

        body = cleaned_data.get("body")

        # clean with python bleach
        white_list_tags = [u'h2', u'p', u'a', u'img', u'ol', u'ul', u'li',
                           u'strong', u'em', u'blockquote', u'sub', u'sup',
                           u'iframe']
        white_list_attrs = {
            'a': ['href', 'title'],
            'img': ['src', 'title'],
            '*':    ['style', 'class'],
            'iframe': ['src', 'width', 'height',
                       'frameborder', 'allowfullscreen']
        }
        white_list_styles = ['padding', 'padding-left']
        body = bleach.clean(
            body, white_list_tags, white_list_attrs, white_list_styles)
        cleaned_data['body'] = body

        return cleaned_data
