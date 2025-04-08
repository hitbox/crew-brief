import sqlalchemy as sa

class ModelAttrs:
    """
    Convenience for template rendering links to objects from relationships.
    """

    def __init__(
        self,
        inspector,
        instance_endpoint = None,
        list_endpoint = None,
        exclude_pk = True,
        exclude_fk = True,
    ):
        self.inspector = inspector
        self.instance_endpoint = instance_endpoint
        self.list_endpoint = list_endpoint
        self.exclude_pk = exclude_pk
        self.exclude_fk = exclude_fk
        self.relationships = {relationship.key for relationship in self.inspector.relationships}
        self.primary_keys = {col.name for col in self.inspector.primary_key}
        self.foreign_keys = {col.name for col in self.inspector.columns if col.foreign_keys}

    def __iter__(self):
        for attr in self.inspector.attrs:
            # Exclude primary keys
            if self.exclude_pk and attr.key in self.primary_keys:
                continue

            # Exclude foreign keys
            if self.exclude_fk and attr.key in self.foreign_keys:
                continue

            if attr in self.inspector.relationships:
                breakpoint()
                pass

            yield attr


class InstanceAttrs:

    def __init__(
        self,
        inspector,
        instance_endpoint = None,
        list_endpoint = None,
        exclude_pk = True,
        exclude_fk = True,
    ):
        if not isinstance(inspector, sa.orm.InstanceState):
            raise ValueError(f'inspector must be sqlalchemy.orm.InstanceState.')

        self.inspector = inspector
        self.mapper = self.inspector.mapper
        self.instance_endpoint = instance_endpoint
        self.list_endpoint = list_endpoint
        self.exclude_pk = exclude_pk
        self.exclude_fk = exclude_fk
        self.relationships = {relationship.key for relationship in self.mapper.relationships}
        self.primary_keys = {col.name for col in self.mapper.primary_key}
        self.foreign_keys = {col.name for col in self.mapper.columns if col.foreign_keys}

    def __iter__(self):

        ordering = getattr(self.mapper.class_, '__display_order__', [])

        def display_order(attr):
            if attr.key in ordering:
                return ordering.index(attr.key)
            else:
                return float('inf')

        attrs = sorted(self.mapper.attrs, key=display_order)

        for attr in attrs:
            # Exclude primary keys
            if self.exclude_pk and attr.key in self.primary_keys:
                continue

            # Exclude foreign keys
            if self.exclude_fk and attr.key in self.foreign_keys:
                continue

            instance = self.inspector.obj()
            value = getattr(instance, attr.key)

            attrdata = {
                'key': attr.key,
                'value': value,
                'url': None,
            }

            if (
                value is not None
                and attr.key in self.mapper.relationships
            ):
                # An endpoint builder exists and this is a relationship attribute.
                if isinstance(value, list):
                    if self.list_endpoint:
                        other_class = attr.mapper.class_
                        attrdata['url'] = self.list_endpoint(other_class)
                        attrdata['value'] = f'{attr.mapper.class_.__name__} objects...'
                elif self.instance_endpoint:
                    attrdata['url'] = self.instance_endpoint(value)
                    if hasattr(value, 'name'):
                        attrdata['value'] = value.name

            yield attrdata
