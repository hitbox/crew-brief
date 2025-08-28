from enum import Enum

class AttributeSort(Enum):

    none = ''
    ascending = 'a'
    descending = 'd'

    @property
    def label(self):
        if self is AttributeSort.none:
            return '(None)'
        elif self is AttributeSort.ascending:
            return 'Ascending'
        elif self is AttributeSort.descending:
            return 'Descending'

    @property
    def choice_item(self):
        return (self.value, self.label)
