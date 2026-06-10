import tempfile
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse

from landing.views import SOUP_SLUGS


class SoupPageTests(TestCase):
    def test_home_page_has_no_initial_soup(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-initial-soup=""')

    def test_each_soup_url_renders_its_slug(self):
        for slug in SOUP_SLUGS:
            with self.subTest(slug=slug):
                response = self.client.get(
                    reverse("soup-detail", kwargs={"soup_slug": slug})
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(
                    response,
                    f'data-initial-soup="{slug}"',
                )

    def test_unknown_soup_returns_404(self):
        response = self.client.get(
            reverse("soup-detail", kwargs={"soup_slug": "unknown"})
        )

        self.assertEqual(response.status_code, 404)


class GenerateSoupQrTests(TestCase):
    def test_command_requires_public_https_url(self):
        with self.assertRaises(CommandError):
            call_command("generate_soup_qr", base_url="http://example.com")

    def test_command_generates_svg_and_png_for_every_soup(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            call_command(
                "generate_soup_qr",
                base_url="https://example.com",
                output_dir=temp_dir,
                verbosity=0,
            )

            for slug in SOUP_SLUGS:
                self.assertGreater((Path(temp_dir) / f"{slug}.svg").stat().st_size, 0)
                self.assertGreater((Path(temp_dir) / f"{slug}.png").stat().st_size, 0)
