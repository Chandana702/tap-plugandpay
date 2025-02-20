"""Stream type classes for tap-plugandpay."""

from __future__ import annotations

import typing as t
from importlib import resources
from pathlib import Path

import requests
from typing import Iterable
from urllib.parse import parse_qsl, urlparse, ParseResult

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_plugandpay.client import PlugandPayStream

# TODO: Delete this is if not using json files for schema definition
# SCHEMAS_DIR = resources.files(__package__) / "schemas"
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class CheckoutsStream(PlugandPayStream):
    """Checkout stream"""

    name = "checkouts"
    path = "/checkouts"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "updated_at"
    schema_filepath = SCHEMAS_DIR / "checkouts.json"

    def get_url_params(self, context, next_page_token):

        params: dict = {
            "include": "confirmation,custom_fields,order_bumps,popups,product,product_pricing,settings,statistics,template,upsells,video"
        }

        if next_page_token:
            # Check if next_page_token is already parsed
            if isinstance(next_page_token, ParseResult):
                parsed_url = next_page_token  # Already parsed
            else:
                parsed_url = urlparse(next_page_token)  # Parse if it's a string

            params.update(parse_qsl(parsed_url.query))

        return params


class ProductsStream(PlugandPayStream):
    """Product stream"""

    name = "products"
    path = "/products"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "products.json"

    def get_url_params(self, context, next_page_token):

        params: dict = {
            "include": "custom_fields,pricing,statistics,tax_rates",
        }

        if next_page_token:
            # Check if next_page_token is already parsed
            if isinstance(next_page_token, ParseResult):
                parsed_url = next_page_token  # Already parsed
            else:
                parsed_url = urlparse(next_page_token)  # Parse if it's a string

            params.update(parse_qsl(parsed_url.query))

        return params

    def get_child_context(self, record, context):
        """Pass product_id to child stream"""
        return {"product_id": record["id"]}


class PricesStream(PlugandPayStream):
    """Price stream"""

    name = "prices"
    path = "/products/{product_id}/prices"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "prices.json"

    parent_stream_type = ProductsStream

    def get_child_context(self, record, context):
        return super().get_child_context(record, context)


class OrdersStream(PlugandPayStream):
    """Order stream"""

    name = "orders"
    path = "/orders"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "updated_at"
    schema_filepath = SCHEMAS_DIR / "orders.json"

    def get_url_params(self, context, next_page_token):
        params: dict = {
            "include": "billing,checkout,collection_costs,commissions,custom_fields,discounts,is_collectible,items,note,related_orders,payment,products,subscriptions,shipping,tags,taxes"
        }

        if next_page_token:
            # Check if next_page_token is already parsed
            if isinstance(next_page_token, ParseResult):
                parsed_url = next_page_token  # Already parsed
            else:
                parsed_url = urlparse(next_page_token)  # Parse if it's a string

            params.update(parse_qsl(parsed_url.query))

        return params

    def get_child_context(self, record: dict, context: dict) -> dict:
        """Pass order_id to child stream"""
        return {"order_id": record["id"]}


class OrderPaymentsStream(PlugandPayStream):
    """OrderPayment stream"""

    name = "order_payments"
    path = "/orders/{order_id}/payment"
    records_jsonpath = "$.data[*]"
    primary_keys = ["transaction_id"]
    replication_key = "transaction_id"
    schema_filepath = SCHEMAS_DIR / "order_payments.json"

    parent_stream_type = OrdersStream
    ignore_parent_replication_key = True

    def get_child_context(self, record, context):
        return super().get_child_context(record, context)


class OrderCommentsStream(PlugandPayStream):
    """OrderComment stream"""

    name = "order_comments"
    path = "/orders/{order_id}/comments"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "updated_at"
    schema_filepath = SCHEMAS_DIR / "order_comments.json"

    parent_stream_type = OrdersStream
    ignore_parent_replication_key = True

    def get_child_context(self, record, context):
        return super().get_child_context(record, context)


class SubscriptionsStream(PlugandPayStream):
    """Subscription stream"""

    name = "subscriptions"
    path = "/subscriptions"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "updated_at"
    schema_filepath = SCHEMAS_DIR / "subscriptions.json"

    def get_url_params(self, context, next_page_token):
        params: dict = {
            "include": "billing,cancellation_reason,commissions,events,history,meta,pricing,product,product_images,tags,trial"
        }

        if next_page_token:
            # Check if next_page_token is already parsed
            if isinstance(next_page_token, ParseResult):
                parsed_url = next_page_token  # Already parsed
            else:
                parsed_url = urlparse(next_page_token)  # Parse if it's a string

            params.update(parse_qsl(parsed_url.query))

        return params

    def get_child_context(self, record, context):
        """Pass subscription_id to child stream"""
        return {"subscription_id": record["id"]}


class SubscriptionCommentsStream(PlugandPayStream):
    """SubscriptionComment stream"""

    name = "subscription_comments"
    path = "/subscriptions/{subscription_id}/comments"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "updated_at"
    schema_filepath = SCHEMAS_DIR / "subscription_comments.json"

    parent_stream_type = SubscriptionsStream
    ignore_parent_replication_key = True

    def get_child_context(self, record, context):
        return super().get_child_context(record, context)


class TaxRatesStream(PlugandPayStream):
    """TaxRate stream"""

    name = "tax_rates"
    path = "/tax-rates"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "tax_rates.json"
