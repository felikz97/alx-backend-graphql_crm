import graphene
from crm.mutations import (
    CreateCustomer,
    BulkCreateCustomers,
    CreateProduct,
    CreateOrder,
)

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

schema = graphene.Schema(query=Query)
