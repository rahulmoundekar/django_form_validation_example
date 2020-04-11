from django import forms
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import date


class StudentForm(forms.Form):
    name = forms.CharField(max_length=30, required=False)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    age = forms.IntegerField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format: '+9999999999'. Up to 10 digits allowed.")
    mobile = forms.CharField(validators=[phone_regex], max_length=10)

    GENDER_CHOICES = (
        ('NA', '--Select--'),
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, initial='--Select--')

    COURSE_CHOICES = (
        ('NA', '--Select--'),
        ('Java', 'Java'),
        ('Python', 'Python'),
    )
    course = forms.ChoiceField(choices=COURSE_CHOICES, initial='--Select--')
    date_of_birth = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # Validation
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4:
            raise forms.ValidationError("password is too short")
        return password

    # Validation
    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to Admit")
        return age

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("You must be enter Valid Mail Id")
        return email

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender == 'NA':
            raise forms.ValidationError("You must be Select Gender")
        return gender

    def clean_course(self):
        course = self.cleaned_data['course']
        if course == 'NA':
            raise forms.ValidationError("You must be Select Course")
        return course

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        if not (20 < age < 30):
            raise forms.ValidationError("You are no eligible for the Admission")
        return date_of_birth
