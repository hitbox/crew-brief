from wtforms import SelectField

class DynamicSelectField(SelectField):

    def __init__(
        self,
        label = None,
        validators = None,
        query_factory = None,
        get_label = None,
        allow_blank = False,
        blank_text = '',
        **kwargs,
    ):
        super().__init__(label, validators, **kwargs)
        self.query_factory = query_factory
        self.get_label = get_label
        self.allow_blank = allow_blank
        self.blank_text = blank_text
        self.choices = []
        self._refresh_choices()

    def _refresh_choices(self):
        items = self.query_factory()
        choices = []
        if self.allow_blank:
            choices.append(('', self.blank_text or ''))
        for item in items:
            if self.get_label is None:
                # item assumed to be scalar or (value, label) tuple
                if isinstance(item, tuple) and len(item) == 2:
                    choices.append(item)
                else:
                    choices.append((str(item), str(item)))
            elif callable(self.get_label):
                choices.append((str(item), self.get_label(item)))
            else:
                # get_label is attribute name
                label = getattr(item, self.get_label, str(item))
                choices.append((str(item), str(label)))
        self.choices = choices

    def pre_validate(self, form):
        # refresh choices before validating
        self._refresh_choices()
        super().pre_validate(form)
