# app.py
# Northstar Retail Co. — GraphQL Stock Query Mini-Prototype
# Assignment 1: Days 1-2 Solo Recon
# Tool: GraphQL (genuinely unfamiliar tool)

from flask import Flask
import graphene
from flask_graphql import GraphQLView

# ============================================================
# STEP 1: FAKE WAREHOUSE DATA
# In production this would come from a real database.
# For the prototype we use hardcoded data so we can
# focus entirely on learning GraphQL without database complexity.
# ============================================================

WAREHOUSE_STOCK = {
    "SKU-4421": {
        "sku": "SKU-4421",
        "product_name": "Winter Coat - Blue",
        "stock_count": 14,
        "warehouse_location": "Lagos-A3",
        "last_updated": "2026-06-04T09:00:00"
    },
    "SKU-8834": {
        "sku": "SKU-8834",
        "product_name": "Red Sneaker - Size 42",
        "stock_count": 0,
        "warehouse_location": "Lagos-B1",
        "last_updated": "2026-06-04T08:30:00"
    },
    "SKU-2291": {
        "sku": "SKU-2291",
        "product_name": "Black Hoodie - Size M",
        "stock_count": 7,
        "warehouse_location": "Accra-C2",
        "last_updated": "2026-06-04T10:15:00"
    },
    "SKU-5512": {
        "sku": "SKU-5512",
        "product_name": "Blue Backpack",
        "stock_count": 3,
        "warehouse_location": "Nairobi-D4",
        "last_updated": "2026-06-04T07:45:00"
    }
}

# ============================================================
# STEP 2: DEFINE THE SCHEMA
# This tells GraphQL what a Product looks like.
# graphene.ObjectType is how you define a data structure.
# Each field has a type: String, Int, Boolean.
# ============================================================

class Product(graphene.ObjectType):
    """
    Represents one product in the Northstar warehouse.
    GraphQL will only return the fields the client asks for.
    """
    sku = graphene.String(
        description="Unique product identifier"
    )
    product_name = graphene.String(
        description="Human-readable product name"
    )
    stock_count = graphene.Int(
        description="Current units available in warehouse"
    )
    warehouse_location = graphene.String(
        description="Physical warehouse bin location"
    )
    last_updated = graphene.String(
        description="ISO timestamp of last stock update"
    )
    in_stock = graphene.Boolean(
        description="True if stock_count is greater than zero"
    )

    def resolve_in_stock(self, info):
        """
        Resolver for the in_stock field.
        This runs automatically when in_stock is requested.
        Notice: stock_count is accessed via self.stock_count
        because self refers to this Product instance.
        """
        return self.stock_count > 0


# ============================================================
# STEP 3: DEFINE THE QUERIES
# Query is what clients can ask for.
# Think of each method as one question the API can answer.
# ============================================================

class Query(graphene.ObjectType):
    """
    All available GraphQL queries for Northstar stock data.
    """

    # Query 1: Get one product by SKU
    product = graphene.Field(
        Product,
        sku=graphene.String(required=True),
        description="Look up a single product by its SKU"
    )

    # Query 2: Get all products
    all_products = graphene.List(
        Product,
        description="Return all products in the warehouse"
    )

    # Query 3: Get only out-of-stock products
    out_of_stock = graphene.List(
        Product,
        description="Return all products with zero stock"
    )

    def resolve_product(self, info, sku):
        """
        Resolver for the 'product' query.
        'sku' is the argument the client passes in.
        We look it up in our warehouse dictionary.
        If not found, return None.
        """
        data = WAREHOUSE_STOCK.get(sku)
        if not data:
            return None
        return Product(**data)

    def resolve_all_products(self, info):
        """
        Resolver for 'all_products'.
        Convert every item in our dictionary to a Product object.
        The ** unpacks the dictionary as keyword arguments.
        """
        return [Product(**item) for item in WAREHOUSE_STOCK.values()]

    def resolve_out_of_stock(self, info):
        """
        Resolver for 'out_of_stock'.
        Filter to only products where stock_count is zero.
        """
        return [
            Product(**item)
            for item in WAREHOUSE_STOCK.values()
            if item["stock_count"] == 0
        ]


# ============================================================
# STEP 4: CREATE THE SCHEMA AND FLASK APP
# schema combines Query with GraphQL's engine.
# Flask serves it as a web endpoint.
# ============================================================

schema = graphene.Schema(query=Query)

app = Flask(__name__)

# This creates the /graphql endpoint.
# graphiql=True enables the browser-based query playground.
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True  # Set to False in production
    )
)

@app.route("/health")
def health():
    """Simple health check endpoint."""
    return {
        "status": "running",
        "service": "Northstar GraphQL Stock API",
        "version": "1.0.0-prototype"
    }

if __name__ == "__main__":
    print("=" * 50)
    print("Northstar GraphQL Mini-Prototype Running")
    print("Open: http://localhost:5000/graphql")
    print("Use the playground to test your queries")
    print("=" * 50)
    app.run(debug=True, port=5000)