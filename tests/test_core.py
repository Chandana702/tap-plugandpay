"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_plugandpay.tap import TapPlugandPay

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiODM0NWVhMDYzMTM5MzRlMTNhM2JkYmIzYzRlOWJjMGQxZDQ5YjRlM2RkYWU0Nzg3MGFiOTg2NGNkNTY4ODJiZDRmYzRkMTE1NWZkNjIzOWUiLCJpYXQiOjE3MzkxOTQ0NDcuMzE1Mjg5LCJuYmYiOjE3MzkxOTQ0NDcuMzE1MjkxLCJleHAiOjQ4OTQ4NjgwNDcuMzAxMTk1LCJzdWIiOiIyNDQ1NSIsInNjb3BlcyI6W119.O0mNjrWfpfdgxi3GYgHqu8dhm-W10HcAw8HlRXooIycEX0jVn1u928xY5CfPEwjSnwE2bjEd824B7wsQLGjgEYeRXy1tZOWzKf4Tf1KmjJEH6PGYeWvIEjYYdn8ImlgDKP76b2xYEvFkl27cIJxbKN6E3TsK-W6EJ4Z4On1v3aQBMvFZ1y4Qaak2x_hGaehs7B3iE5uV2bVljuZIDdYPxn51zF5PSKw-culP04GrShN1kw87Kc3RsYqDjAvEFPIrgr0tKV0GgVE6gp9_6ePU7VqkmtN_LgdeJYJajcsQD8O39Dr7HGckEWRjQm977V5TZ9Xj13fQ8Nepmnc69yAInKsdSliVMuc_ep7bwrImB4p6LzmaGmwucI5sEhHXZQidU9WUfnrRjX_RVsUJTKSDOgGIVbKKIbdH3WE1zoHPHLy6g940DsE0W5ByjraliMzqr0FjkFtMkOF-jDqI1nPqXpW3r_AvCO5HtJXfz_ZS6cKm0T7Yn4XFetQRtQDg7jPRyUrNEpZsC6kSlEOZ4VSR95Mz0hyXuJRnONA-ly5aGD9BsirC6lUvvDMxBmYvF5-gjYdFCpokxB74-ASJ8OS1WUxeJVymoSGhZ6nuLp4Exn72HatrndQfEkUtQ5WMePp1F1447M4L9S5QKx2QkUX5ntB0fzID0ceu2BHtYJUKUNs",
    # TODO: Initialize minimal tap config
}


# Run standard built-in tap tests from the SDK:
TestTapPlugandPay = get_tap_test_class(
    tap_class=TapPlugandPay,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
