import enum

class AttributeSort(enum.Enum):

    none = ''
    ascending = 'a'
    descending = 'd'

    def order_by_clause(self, attr):
        if self == AttributeSort.none:
            return None
        elif self == AttributeSort.ascending:
            return attr.asc()
        elif self == AttributeSort.descending:
            return attr.desc()


AttributeSort.none.label = '(None)'
AttributeSort.ascending.label = 'Ascending'
AttributeSort.descending.label = 'Descending'

for member in AttributeSort:
    member.choice_item = (member.value, member.label)
