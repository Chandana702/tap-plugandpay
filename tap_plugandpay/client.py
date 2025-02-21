"""REST client handling, including PlugandPayStream base class."""

from __future__ import annotations

import decimal
import typing as t
from typing import Optional
from importlib import resources
from urllib.parse import parse_qsl, urlparse, ParseResult
from datetime import datetime

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseHATEOASPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"


class MyPaginator(BaseHATEOASPaginator):
    def get_next_url(self, response):
        data = response.json()
        next_url = data.get("links", {}).get("next")
        return next_url


class PlugandPayStream(RESTStream):
    """PlugandPay stream class."""

    # Update this value if necessary or override `parse_response`.
    # records_jsonpath = "$[*]"

    # Update this value if necessary or override `get_new_paginator`.
    # next_page_token_jsonpath = "$.links.next"  # noqa: S105

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: hardcode a value here, or retrieve it from self.config
        return "https://api.plugandpay.nl/v2"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("auth_token", ""),
            # token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiODM0NWVhMDYzMTM5MzRlMTNhM2JkYmIzYzRlOWJjMGQxZDQ5YjRlM2RkYWU0Nzg3MGFiOTg2NGNkNTY4ODJiZDRmYzRkMTE1NWZkNjIzOWUiLCJpYXQiOjE3MzkxOTQ0NDcuMzE1Mjg5LCJuYmYiOjE3MzkxOTQ0NDcuMzE1MjkxLCJleHAiOjQ4OTQ4NjgwNDcuMzAxMTk1LCJzdWIiOiIyNDQ1NSIsInNjb3BlcyI6W119.O0mNjrWfpfdgxi3GYgHqu8dhm-W10HcAw8HlRXooIycEX0jVn1u928xY5CfPEwjSnwE2bjEd824B7wsQLGjgEYeRXy1tZOWzKf4Tf1KmjJEH6PGYeWvIEjYYdn8ImlgDKP76b2xYEvFkl27cIJxbKN6E3TsK-W6EJ4Z4On1v3aQBMvFZ1y4Qaak2x_hGaehs7B3iE5uV2bVljuZIDdYPxn51zF5PSKw-culP04GrShN1kw87Kc3RsYqDjAvEFPIrgr0tKV0GgVE6gp9_6ePU7VqkmtN_LgdeJYJajcsQD8O39Dr7HGckEWRjQm977V5TZ9Xj13fQ8Nepmnc69yAInKsdSliVMuc_ep7bwrImB4p6LzmaGmwucI5sEhHXZQidU9WUfnrRjX_RVsUJTKSDOgGIVbKKIbdH3WE1zoHPHLy6g940DsE0W5ByjraliMzqr0FjkFtMkOF-jDqI1nPqXpW3r_AvCO5HtJXfz_ZS6cKm0T7Yn4XFetQRtQDg7jPRyUrNEpZsC6kSlEOZ4VSR95Mz0hyXuJRnONA-ly5aGD9BsirC6lUvvDMxBmYvF5-gjYdFCpokxB74-ASJ8OS1WUxeJVymoSGhZ6nuLp4Exn72HatrndQfEkUtQ5WMePp1F1447M4L9S5QKx2QkUX5ntB0fzID0ceu2BHtYJUKUNs",
        )

    # @property
    # def http_headers(self) -> dict:
    #     """Return the http headers needed.

    #     Returns:
    #         A dictionary of HTTP headers.
    #     """
    #     # If not using an authenticator, you may also provide inline auth headers:
    #     # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
    #     headers = {}
    #     return headers

    def get_new_paginator(self):
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance.
        """
        return MyPaginator()

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            # Check if next_page_token is already parsed
            if isinstance(next_page_token, ParseResult):
                parsed_url = next_page_token  # Already parsed
            else:
                parsed_url = urlparse(next_page_token)  # Parse if it's a string

            params.update(parse_qsl(parsed_url.query))

        return params

    # def prepare_request_payload(
    #     self,
    #     context: Context | None,  # noqa: ARG002
    #     next_page_token: t.Any | None,  # noqa: ARG002, ANN401
    # ) -> dict | None:
    #     """Prepare the data payload for the REST API request.

    #     By default, no payload will be sent (return None).

    #     Args:
    #         context: The stream context.
    #         next_page_token: The next page index or value.

    #     Returns:
    #         A dictionary with the JSON body for a POST requests.
    #     """
    #     # TODO: Delete this method if no payload is required. (Most REST APIs.)
    #     return None

    # def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
    #     """Parse the response and return an iterator of result records.

    #     Args:
    #         response: The HTTP ``requests.Response`` object.

    #     Yields:
    #         Each record from the source.
    #     """
    #     # TODO: Parse response body and return a set of records.
    #     yield from extract_jsonpath(
    #         self.records_jsonpath,
    #         input=response.json(parse_float=decimal.Decimal),
    #     )

    def post_process(
        self,
        row: dict,
        context: Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.

        start_date = self.config.get("start_date")

        if not start_date:
            return row

        updated_at_str = row.get("updated_at")
        if not updated_at_str:
            return row

        # Append time part to start_date
        start_date_str = f"{start_date}T00:00:00.000000Z"

        # Convert start_date and updated_at to datetime objects
        start_date_dt = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        updated_at_dt = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        return row if updated_at_dt >= start_date_dt else None
