"""PlugandPay tap class."""

from __future__ import annotations

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_plugandpay.streams import *

STREAM_TYPES = [
    ProductsStream,
    PricesStream,
    OrdersStream,
    SubscriptionsStream,
    SubscriptionCommentsStream,
    TaxRatesStream,
    CheckoutsStream,
]


class TapPlugandPay(Tap):
    """PlugandPay tap class."""

    name = "tap-plugandpay"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=False,
            secret=True,  # Flag config as protected.
            title="Auth Token",
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapPlugandPay.cli()
