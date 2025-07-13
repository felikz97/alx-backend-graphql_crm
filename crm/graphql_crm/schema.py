# graphql_crm/schema.py
import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
class UpdateLowStockProducts(graphene.Mutation):
    class Output:
        products = graphene.List(ProductType)
        message = graphene.String()

    def mutate(self, info):
        low_stock = Product.objects.filter(stock__lt=10)
        for p in low_stock:
            p.stock += 10
            p.save()
        return UpdateLowStockProducts(products=low_stock, message="Stock levels updated for low-stock products")

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()
    