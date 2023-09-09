from django import forms
from .models import Reservation
from phonenumber_field.formfields import PhoneNumberField
from intl_tel_input.widgets import IntlTelInputWidget


class DateInput(forms.DateInput):
    input_type = 'date'


class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.include_media = False
        self.fields['phone_number'].widget.attrs['placeholder'] = 'phone number'
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) in (forms.TextInput, forms.DateInput):
                    field.widget = forms.TextInput(attrs={'placeholder': field_name})

    class Meta:
        model = Reservation
        fields = "__all__"
        phone_number = PhoneNumberField(widget=IntlTelInputWidget(attrs={'placeholder': 'phone number'}))

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
            'login_date': DateInput(),
            'logout_date': DateInput(),
            "room_type": forms.Select(attrs={'class': 'form-control form-select', 'placeholder': 'Room Type'}),
            "gender": forms.Select(attrs={'class': 'form-control form-select', 'placeholder': 'Gender'}),
            "details": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Descriptions...'}),
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'number'}),
            'bar': IntlTelInputWidget(),

        }

        # def get_form(self):
        #     form = super().get_form()
        #     form.fields["login_date"].widget = DateTimePickerInput()
        #     return form

    def is_valid(self):
        """
        Returns True if the form has no errors. Otherwise, False. If errors are
        being ignored, returns False.
        """
        return self.is_bound and not self.errors
