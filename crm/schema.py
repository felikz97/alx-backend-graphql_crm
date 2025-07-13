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
class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_orders(self, info):
        return Order.objects.all()