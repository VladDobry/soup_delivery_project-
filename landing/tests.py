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

    def test_soup_modal_has_umami_details_button(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, 'class="soup-umami-info"')
        self.assertContains(response, "data-soup-umami-open")
        self.assertContains(response, "Что за умами")

    def test_soup_modal_has_prices_promotion_and_order_link(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, "Цены на банки")
        self.assertContains(response, "1950 ₽")
        self.assertContains(response, "2850 ₽")
        self.assertContains(response, "3750 ₽")
        self.assertContains(
            response,
            "2 дегустационных супа по 0,35 л в подарок!",
        )
        self.assertContains(response, 'class="btn soup-offer-button"')

    def test_order_buttons_open_phone_modal(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, "data-order-open", count=5)
        self.assertContains(response, 'class="order-modal"')
        self.assertContains(response, 'id="order-modal-title"')
        self.assertContains(response, 'aria-describedby="order-modal-description"')
        self.assertContains(response, "+7 (928) 851-2525")
        self.assertContains(response, 'href="tel:+79288512525"')
        self.assertContains(response, "data-order-close", count=2)

    def test_gallery_is_between_soups_and_umami(self):
        response = self.client.get(reverse("index"))
        content = response.content.decode()

        soups_position = content.index('id="soups"')
        gallery_position = content.index('class="section-band gallery-line"')
        umami_position = content.index('id="umami"')

        self.assertLess(soups_position, gallery_position)
        self.assertLess(gallery_position, umami_position)

    def test_volume_cards_use_branded_jar_images(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, "feature-jar-solyanka-1l.png")
        self.assertContains(response, "feature-jar-ukha-15l.png")
        self.assertContains(response, "feature-jar-borsch-2l.png")
        self.assertNotContains(response, "<h4>1 л</h4>", html=True)
        self.assertNotContains(response, "<h4>1,5 л</h4>", html=True)
        self.assertNotContains(response, "<h4>2 л</h4>", html=True)

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
                self.assertContains(response, "data-soup-umami-open")
                self.assertContains(response, "Цены на банки")
                self.assertContains(response, "data-order-open")

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
