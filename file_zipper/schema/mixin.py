import marshmallow as mm

class ValidateMixin:
    """
    Validation common to all schemas.
    """

    @mm.validates_schema
    def validate_airline_iata_fields(self, data, **kwargs):
        """
        Validate that all scraped airline IATA codes are the same.
        """
        airline_iata_values = set(
            val for key, val in data.items() if key.startswith('airline_iata'))
        if len(airline_iata_values) != 1:
            raise ValueError(f'Airline IATA values not equal: {airline_iata_values}')


class OrderMixin:

    _preferred_order = []

    def _reorder_dict(self, data):
        def preferred(key):
            if key in self._preferred_order:
                return self._preferred_order.index(key)
            else:
                return float('inf')

        return {key: data[key] for key in sorted(data, key=preferred)}

    @mm.post_load
    def reorder_dict(self, data, **kwargs):
        """
        Reconstruct the data dict in preferred key order.
        """
        return self._reorder_dict(data)

    @mm.post_dump
    def reorder_dict(self, data, many, **kwargs):
        return self._reorder_dict(data)
