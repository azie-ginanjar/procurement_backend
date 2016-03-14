from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import colander as cl


class PaginationSchema(cl.MappingSchema):
    page = cl.SchemaNode(cl.Integer(), default=1, missing=1)
    per_page = cl.SchemaNode(cl.Integer(), default=20, missing=20)
