from markupsafe import Markup
from sqlalchemy.orm import RelationshipProperty

from crew_brief.util import model_attributes

class DefinitionKey:

    def __init__(self, key=None, label=None, formatter=None):
        self.key = key
        self.label = label
        if self.key is None and self.label is None:
            raise ValueError(f'key or label must be defined.')
        self.formatter = formatter

    def render_dt(self):
        return Markup(self.label or self.key)

    def render_dd(self, obj):
        if self.key is not None:
            value = getattr(obj, self.key)
        else:
            value = self.label

        if self.formatter:
            value = self.formatter(obj, value)
        return Markup(value)


class DefinitionList:
    """
    HTML <dl> definition list.
    """

    def __init__(self, keys):
        self.keys = keys

    @classmethod
    def from_model(cls, model, include_relationships=True, field_args=None, only=None, sort_key=None):
        keys = []
        for attrname in model_attributes(model, include_relationships=include_relationships):
            if only and attrname not in only:
                continue
            attr = getattr(model, attrname)

            # Construct formatter if attribute is a relationship.
            formatter = None
            if hasattr(attr, 'property'):
                prop = attr.property
                if isinstance(prop, RelationshipProperty):
                    if prop.uselist:
                        def formatter(instance, value):
                            return unordered_list(map(Markup, value))

            kwargs = {'key': attrname}

            label = None
            info = getattr(attr, 'info', {})
            if 'label' in info:
                kwargs['label'] = info['label']

            if 'formatter' in info:
                kwargs['formatter'] = info['formatter']

            if field_args and attrname in field_args:
                kwargs.update(field_args[attrname])

            key_obj = DefinitionKey(**kwargs)
            keys.append(key_obj)

        # Sort the keys if sort key is given.
        if sort_key is not None:
            keys.sort(key=sort_key)

        return cls(keys)
