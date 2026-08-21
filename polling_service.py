# polling_service.py
# Northstar Retail Co. — Original Polling Spec
# Day 3: Poll warehouse API every 5 minutes, cache stock,
# expose query endpoint via GraphQL
# NOTE: This file will be DEPRECATED on Day 4 pivot.
# Kept here clearly marked for Scope Delta Analysis.

import threading
import time
import requests
from datetime import datetime
from flask import Flask
import graphene
from flask_graphql import GraphQLView

# ============================================================
# SIMULATED WAREHOUSE API
# In production: replace WAREHOUSE_API_URL with real endpoint.
# For prototype: we simulate responses locally.
# ============================================================

WAREHOUSE_API_URL = "https://fakestoreapi.com/products"

# In-memory cache — stores latest stock data
# Key: product id, Value: stock data dict
STOCK_CACHE = {}
CACHE_LAST_UPDATED = None

POLL_INTERVAL_SECONDS = 300  # 5 minutes


def fetch_warehouse_stock():
    """
    Polls the warehouse API and updates the local cache.
    Called every POLL_INTERVAL_SECONDS by the background thread.
    Uses retry logic: tries up to 3 times before giving up.
    """
    global STOCK_CACHE, CACHE_LAST_UPDATED

    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            print(
                f"[POLL] Attempt {attempt + 1} — "
                f"fetching warehouse data..."
            )

            response = requests.get(
                WAREHOUSE_API_URL,
                timeout=10
            )

            response.raise_for_status()
            products = response.json()

            # Transform API response into our cache format
            new_cache = {}

            for product in products:
                # FakeStoreAPI does not have stock fields
                # so we simulate stock from product rating
                simulated_stock = int(
                    product.get("rating", {}).get("count", 0)
                ) % 50

                new_cache[str(product["id"])] = {
                    "sku": f"SKU-{product['id']:04d}",
                    "product_name": product["title"][:50],
                    "stock_count": simulated_stock,
                    "in_stock": simulated_stock > 0,
                    "last_polled": datetime.now().isoformat()
                }

            STOCK_CACHE = new_cache
            CACHE_LAST_UPDATED = datetime.now().isoformat()

            print(
                f"[POLL] Success — {len(STOCK_CACHE)} "
                f"products cached at {CACHE_LAST_UPDATED}"
            )

            return

        except requests.exceptions.RequestException as e:
            print(f"[POLL] Attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                print(f"[POLL] Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print("[POLL] All retries failed. Cache not updated.")


def start_polling_thread():
    """
    Starts a background thread that polls every 5 minutes.
    daemon=True means it stops when the main program stops.
    """

    def poll_loop():
        while True:
            fetch_warehouse_stock()
            time.sleep(POLL_INTERVAL_SECONDS)

    thread = threading.Thread(
        target=poll_loop,
        daemon=True
    )

    thread.start()

    print("[POLL] Background polling thread started.")


# ============================================================
# GRAPHQL SCHEMA FOR CACHED STOCK
# ============================================================

class CachedProduct(graphene.ObjectType):
    sku = graphene.String()
    product_name = graphene.String()
    stock_count = graphene.Int()
    in_stock = graphene.Boolean()
    last_polled = graphene.String()


class CacheStatus(graphene.ObjectType):
    total_products = graphene.Int()
    last_updated = graphene.String()
    poll_interval_seconds = graphene.Int()


class Query(graphene.ObjectType):

    product = graphene.Field(
        CachedProduct,
        sku=graphene.String(required=True)
    )

    all_products = graphene.List(CachedProduct)

    cache_status = graphene.Field(CacheStatus)

    def resolve_product(self, info, sku):
        for item in STOCK_CACHE.values():
            if item["sku"] == sku:
                return CachedProduct(**item)

        return None

    def resolve_all_products(self, info):
        return [
            CachedProduct(**item)
            for item in STOCK_CACHE.values()
        ]

    def resolve_cache_status(self, info):
        return CacheStatus(
            total_products=len(STOCK_CACHE),
            last_updated=CACHE_LAST_UPDATED,
            poll_interval_seconds=POLL_INTERVAL_SECONDS
        )


schema = graphene.Schema(query=Query)

app = Flask(__name__)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True
    )
)


@app.route("/health")
def health():
    return {
        "status": "running",
        "cache_size": len(STOCK_CACHE),
        "last_updated": CACHE_LAST_UPDATED
    }


if __name__ == "__main__":

    # Fetch immediately on startup, then every 5 minutes
    fetch_warehouse_stock()
    start_polling_thread()

    print("=" * 50)
    print("Northstar Polling Service Running")
    print("GraphQL: http://localhost:5000/graphql")
    print(f"Poll interval: {POLL_INTERVAL_SECONDS}s")
    print("=" * 50)

    app.run(debug=False, port=5000)