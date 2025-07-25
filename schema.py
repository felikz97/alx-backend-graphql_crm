# crm/schema.py
import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter
from django.core.exceptions import ValidationError
from django.db import transaction
import re

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (graphene.relay.Node, )

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (graphene.relay.Node, )

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (graphene.relay.Node, )

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")

        if phone and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', phone):
            raise Exception("Invalid phone format")

        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(graphene.JSONString, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created = []
        errors = []

        with transaction.atomic():
            for i, data in enumerate(input):
                try:
                    if Customer.objects.filter(email=data['email']).exists():
                        raise Exception(f"Email {data['email']} already exists")
                    if 'phone' in data and data['phone'] and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', data['phone']):
                        raise Exception(f"Invalid phone format: {data['phone']}")
                    c = Customer(name=data['name'], email=data['email'], phone=data.get('phone'))
                    c.save()
                    created.append(c)
                except Exception as e:
                    errors.append(f"Record {i}: {str(e)}")

        return BulkCreateCustomers(customers=created, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(default_value=0)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        if not product_ids:
            raise Exception("At least one product must be selected")

        products = Product.objects.filter(id__in=product_ids)
        if len(products) != len(product_ids):
            raise Exception("Some product IDs are invalid")

        total = sum(p.price for p in products)
        order = Order(customer=customer, total_amount=total)
        order.save()
        order.products.set(products)
        return CreateOrder(order=order)

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
    customer = graphene.relay.Node.Field(CustomerType)
    customers = DjangoFilterConnectionField(CustomerType, filterset_class=CustomerFilter)

    product = graphene.relay.Node.Field(ProductType)
    products = DjangoFilterConnectionField(ProductType, filterset_class=ProductFilter)

    order = graphene.relay.Node.Field(OrderType)
    orders = DjangoFilterConnectionField(OrderType, filterset_class=OrderFilter)