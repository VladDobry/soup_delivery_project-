import re
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

    def test_home_page_has_no_umami_teaser(self):
        response = self.client.get(reverse("index"))

        self.assertNotContains(response, 'id="umami"')
        self.assertNotContains(response, 'class="umami-teaser')
        self.assertNotContains(response, "data-umami-open")
        self.assertContains(response, 'class="umami-modal"')
        self.assertContains(response, 'id="umami-modal-title"')

    def test_header_navigation_has_no_delivery_link(self):
        response = self.client.get(reverse("index"))
        content = response.content.decode()

        nav_start = content.index('<nav class="main-nav">')
        nav_end = content.index("</nav>", nav_start)
        nav = content[nav_start:nav_end]

        self.assertIn("Супы", nav)
        self.assertIn("О нас", nav)
        self.assertIn("Контакты", nav)
        self.assertNotIn("Доставка", nav)
        self.assertNotIn('href="#delivery"', nav)
        self.assertIn('id="delivery"', content)

    def test_umami_modal_header_has_no_navigation(self):
        response = self.client.get(reverse("index"))
        content = response.content.decode()

        header_start = content.index('<header class="umami-modal-header">')
        header_end = content.index("</header>", header_start)
        header = content[header_start:header_end]

        self.assertNotIn("<nav", header)
        self.assertNotIn("Наши супы", header)
        self.assertNotIn("Супотерапия", header)
        self.assertIn("data-order-open", header)
        self.assertIn("data-umami-close", header)

    def test_soup_modal_header_has_no_navigation(self):
        response = self.client.get(reverse("index"))
        content = response.content.decode()

        header_start = content.index('<header class="soup-passport-header">')
        header_end = content.index("</header>", header_start)
        header = content[header_start:header_end]

        self.assertNotIn("<nav", header)
        self.assertNotIn("passport-nav", header)
        self.assertNotIn("Супотерапия", header)
        self.assertNotIn("Доставка и оплата", header)
        self.assertNotIn("Контакты", header)
        self.assertIn("passport-logo", header)
        self.assertIn("data-order-open", header)
        self.assertIn("data-soup-close", header)

    def test_soup_modal_has_prices_promotion_and_order_link(self):
        response = self.client.get(reverse("index"))
        script = (
            Path(__file__).resolve().parent
            / "static"
            / "landing"
            / "js"
            / "main.js"
        ).read_text()

        self.assertContains(response, "Цены")
        self.assertContains(response, "2500 ₽")
        self.assertContains(response, "3750 ₽")
        self.assertContains(response, "4500 ₽")
        self.assertContains(response, "1000гр")
        self.assertContains(response, "1600гр")
        self.assertContains(response, "2200гр")
        self.assertNotContains(response, "1950 ₽")
        self.assertNotContains(response, "2850 ₽")
        self.assertNotContains(response, "При покупке любого супа от 1 литра")
        self.assertContains(response, 'data-soup-price="1l"')
        self.assertContains(response, 'data-soup-price="15l"')
        self.assertContains(response, 'data-soup-price="2l"')
        self.assertIn('"1l": "3000 ₽"', script)
        self.assertIn('"15l": "4250 ₽"', script)
        self.assertIn('"2l": "5000 ₽"', script)
        self.assertNotContains(response, "дегустационных супа")
        self.assertNotContains(response, "0,35 л в подарок")
        self.assertNotContains(response, 'class="feature-gift')
        self.assertNotContains(response, 'class="soup-offer-promo"')
        self.assertContains(response, 'class="btn soup-offer-button"')

    def test_broth_modal_uses_special_passport(self):
        response = self.client.get(reverse("index"))
        script = (
            Path(__file__).resolve().parent
            / "static"
            / "landing"
            / "js"
            / "main.js"
        ).read_text()

        self.assertContains(response, "data-broth-passport")
        self.assertIn('types: ["Говяжий", "Петух", "Сёмга"]', script)
        self.assertIn('water: "Горная кристально чистая"', script)
        self.assertIn("Гвоздика, корень сельдерея, лук-порей", script)
        self.assertIn("renderBrothPassport(detail.passport)", script)
        self.assertIn("renderSoupGroups(detail.groups || [])", script)

    def test_order_buttons_open_phone_modal(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, "data-order-open", count=5)
        self.assertContains(response, 'class="order-modal"')
        self.assertContains(response, 'id="order-modal-title"')
        self.assertContains(
            response,
            'aria-describedby="order-modal-description order-delivery-info"',
        )
        self.assertContains(response, 'id="order-delivery-info"')
        self.assertContains(response, "Дорогие друзья!")
        self.assertContains(response, "ПО-НАСТОЯЩЕМУ ДОМАШНЯЯ")
        self.assertContains(response, "А ещё можно сделать предзаказ!")
        self.assertContains(
            response,
            '<a href="https://t.me/yaestsup" target="_blank" rel="noopener noreferrer">ТГ</a>',
            html=True,
        )
        self.assertContains(response, "Адлер, Сириус — бесплатно")
        self.assertContains(response, "Сочи, Красная Поляна — бесплатно от 2200гр")
        self.assertRegex(
            response.content.decode(),
            r"landing/img/hero-logo(?:\.[0-9a-f]+)?\.png",
        )
        self.assertRegex(
            response.content.decode(),
            r"landing/img/hero-mascot(?:\.[0-9a-f]+)?\.png",
        )
        self.assertContains(response, "+7 (928) 851-2525")
        self.assertContains(response, 'href="tel:+79288512525"')
        self.assertContains(response, "data-order-close", count=2)

    def test_footer_has_no_store_links(self):
        response = self.client.get(reverse("index"))

        self.assertNotContains(response, "Где купить")
        self.assertNotContains(response, "Показать магазины")
        self.assertContains(response, '<footer class="footer section-band"')
        self.assertContains(response, "+7 (928) 851-2525")
        self.assertContains(response, "Мы в соцсетях")
        self.assertContains(response, "Суп спасёт")
        self.assertContains(response, 'class="footer-mascot"')
        self.assertRegex(
            response.content.decode(),
            r"landing/img/hero-mascot(?:\.[0-9a-f]+)?\.png",
        )

    def test_benefit_icons_have_consistent_order(self):
        response = self.client.get(reverse("index"))
        content = response.content.decode()
        expected_images = [
            "benefit-25h.png",
            "benefit-broth.png",
            "benefit-no-pork.png",
            "benefit-water.png",
            "benefit-farm.png",
        ]

        hero_start = content.index('<div class="benefits"')
        hero_end = content.index('<section class="section-band soup-line"', hero_start)
        hero_benefits = content[hero_start:hero_end]

        passport_start = content.index('<div class="soup-passport-benefits"')
        passport_end = content.index("</section>", passport_start)
        passport_benefits = content[passport_start:passport_end]

        for benefits in (hero_benefits, passport_benefits):
            positions = []
            for image in expected_images:
                stem = image.removesuffix(".png")
                match = re.search(rf"{re.escape(stem)}(?:\.[0-9a-f]+)?\.png", benefits)
                self.assertIsNotNone(match)
                positions.append(match.start())
            self.assertEqual(positions, sorted(positions))

    def test_gallery_is_between_soups_and_features(self):
        response = self.client.get(reverse("index"))
        content = response.content.decode()

        soups_position = content.index('id="soups"')
        gallery_position = content.index('class="section-band gallery-line"')
        features_position = content.index('id="delivery"')

        self.assertLess(soups_position, gallery_position)
        self.assertLess(gallery_position, features_position)

    def test_volume_cards_use_branded_jar_images(self):
        response = self.client.get(reverse("index"))
        content = response.content.decode()

        self.assertRegex(content, r"feature-jar-solyanka-1000g(?:\.[0-9a-f]+)?\.png")
        self.assertRegex(content, r"feature-jar-pumpkin-1600g(?:\.[0-9a-f]+)?\.png")
        self.assertRegex(content, r"feature-jar-borsch-2200g(?:\.[0-9a-f]+)?\.png")
        self.assertNotContains(response, "feature-jar-solyanka-1l.png")
        self.assertNotContains(response, "feature-jar-pumpkin-15l.png")
        self.assertNotContains(response, "feature-jar-borsch-2l.png")
        self.assertContains(response, "Банка тыквенного супа-пюре весом 1600гр")
        self.assertContains(response, "На троих")
        self.assertContains(response, "На пятерых")
        self.assertContains(response, "На семерых")
        self.assertIn("<small>На троих</small>\n                                            <b>1000гр</b>", content)
        self.assertIn("<small>На пятерых</small>\n                                            <b>1600гр</b>", content)
        self.assertIn("<small>На семерых</small>\n                                            <b>2200гр</b>", content)
        self.assertNotContains(response, "feature-jar-ukha-15l.png")
        self.assertNotContains(response, "feature-jars-volumes-pumpkin.png")
        self.assertNotContains(response, "3350 ₽")
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
                self.assertContains(response, "Цены")
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
