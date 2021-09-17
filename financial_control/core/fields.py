from django import forms


def DateField(*args, **kwargs):
    attrs = {'type': 'date'}

    for arg in args:
        attrs[arg] = True

    for item, value in kwargs.items():
        attrs[item] = value

    return forms.DateField(widget=forms.DateInput(attrs=attrs))


def CharField(*args, **kwargs):
    attrs = {}

    for arg in args:
        attrs[arg] = True

    for item, value in kwargs.items():
        attrs[item] = value

    return forms.CharField(widget=forms.TextInput(attrs=attrs))


def TimeField(*args, **kwargs):
    attrs = {'type': 'time'}

    for arg in args:
        attrs[arg] = True

    for item, value in kwargs.items():
        attrs[item] = value

    return forms.TimeField(
        widget=forms.TimeInput(attrs=attrs)
    )
