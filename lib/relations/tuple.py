import urecord


class Tuple(urecord.RecordInstance):

    """
    A named tuple type, with helpful methods for manipulating fields.
    """

    def __repr__(self):
        return 'Tuple(%s)' % (
            ', '.join("%s=%r" % (field, self[i])
                      for i, field in enumerate(self._fields)))

    @classmethod
    def _make_projection(cls, *fields):
        return tuple(cls._fields.index(field) for field in fields)

    @classmethod
    def _make_reordering(cls, **new_fields):
        # At this point, new_fields is assumed to be a complete bjiection
        # from new <=> old fields.
        return tuple(cls._fields.index(old_field)
                     for new_field, old_field in sorted(new_fields.items()))

    def _index_restrict(self, *indices):
        return tuple(self[index] for index in indices)
