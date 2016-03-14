from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import colander as cl

class RegisterSchema(cl.MappingSchema):
    username = cl.SchemaNode(
        cl.String(),
        validator=cl.All(cl.Length(max=25, min=5)),
    )
    password = cl.SchemaNode(cl.String())
    app_key = cl.SchemaNode(cl.String())

class LoginSchema(cl.MappingSchema):
    # app_key = cl.SchemaNode(
    #     cl.String(),
    #     validator=cl.All(cl.Length(max=40, min=40)),
    # )
    username = cl.SchemaNode(
        cl.String(),
        validator=cl.All(cl.Length(max=25, min=5)),
    )
    password = cl.SchemaNode(cl.String())
    