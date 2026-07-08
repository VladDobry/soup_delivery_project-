import html
import json
import re
import tempfile
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse

from landing.models import SetPrice, SoupPrice
from landing.views import SOUP_SLUGS


class SoupPageTests(TestCase):
    @staticmethod
    def get_json_script(response, script_id):
        content = response.content.decode()
        match = re.search(
            rf'<script id="{re.escape(script_id)}" type="application/json">(.*?)</script>',
            content,
            flags=re.S,
        )
        if match is None:
            raise AssertionError(f"JSON script {script_id!r} was not found")
        return json.loads(html.unescape(match.group(1)))

    def test_home_page_has_no_initial_soup(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-initial-soup=""')

    def test_soup_modal_has_umami_details_button(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, 'class="soup-umami-info"')
        self.assertContains(response, "data-soup-umami-open")
        self.assertContains(response, "Что за умами")

    def test_soup_modal_has_adjacent_navigation(self):
        response = self.client.get(reverse("index"))
        script = (
            Path(__file__).resolve().parent
            / "static"
            / "landing"
            / "js"
            / "main.js"
        ).read_text()
        styles = (
            Path(__file__).resolve().parent
            / "static"
            / "landing"
            / "css"
            / "styles.css"
        ).read_text()

        self.assertContains(response, "data-soup-prev")
        self.assertContains(response, "data-soup-next")
        self.assertContains(response, 'aria-label="Предыдущий суп"')
        self.assertContains(response, 'aria-label="Следующий суп"')
        content = response.content.decode()
        stage_start = content.index('<div class="soup-bowl-stage">')
        stage_end = content.index('<p class="soup-cook-note"', stage_start)
        bowl_stage = content[stage_start:stage_end]
        self.assertIn("data-soup-prev", bowl_stage)
        self.assertIn("data-soup-next", bowl_stage)
        self.assertIn("const showAdjacentSoup = (direction) => {", script)
        self.assertIn(
            "(currentIndex + direction + soupSequence.length) % soupSequence.length",
            script,
        )
        self.assertIn('window.history.pushState(\n        { soupId: nextOpener.dataset.soupId }', script)
        self.assertIn('event.key === "ArrowLeft"', script)
        self.assertIn('event.key === "ArrowRight"', script)
        self.assertIn('soupDialog?.addEventListener("pointerdown"', script)
        self.assertIn('soupDialog?.addEventListener("pointerup"', script)
        self.assertIn("const closeSoupModalDirectly = () => {", script)
        self.assertIn("closeSoupModalDirectly();", script)
        closer_start = script.index("soupClosers.forEach")
        closer_end = script.index("soupSiteLink?.addEventListener", closer_start)
        closer_script = script[closer_start:closer_end]
        self.assertIn("closeSoupModalDirectly();", closer_script)
        self.assertNotIn("closeSoupWithNavigation();", closer_script)
        self.assertIn(".soup-nav::before", styles)
        self.assertIn(".soup-nav-prev::before", styles)
        self.assertIn(".soup-nav-next::before", styles)
        self.assertIn(".soup-bowl-stage", styles)
        mobile_nav_start = styles.index("    .soup-nav {", styles.index("@media (max-width: 720px)"))
        mobile_nav_end = styles.index("}", mobile_nav_start)
        mobile_nav_styles = styles[mobile_nav_start:mobile_nav_end]
        self.assertNotIn("top: 82px;", mobile_nav_styles)
        self.assertIn(".soup-close:hover", styles)
        close_hover_start = styles.index(".soup-close:hover")
        close_hover_end = styles.index("}", close_hover_start)
        close_hover_styles = styles[close_hover_start:close_hover_end]
        self.assertIn("background: var(--red);", close_hover_styles)
        self.assertIn("rotate(-8deg) scale(1.08)", close_hover_styles)

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
        self.assertEqual(
            self.get_json_script(response, "default-soup-prices"),
            {
                "1l": "2500 ₽",
                "15l": "3750 ₽",
                "2l": "4500 ₽",
            },
        )
        self.assertEqual(
            self.get_json_script(response, "soup-price-overrides"),
            {
                "ukha": {
                    "1l": "3000 ₽",
                    "15l": "4250 ₽",
                    "2l": "5000 ₽",
                },
                "broth": {
                    "2l": "2500 ₽",
                },
            },
        )
        self.assertIn('parseJsonScript("default-soup-prices"', script)
        self.assertIn('parseJsonScript("soup-price-overrides"', script)
        self.assertIn("prices: soupPriceOverrides.ukha", script)
        self.assertIn("prices: soupPriceOverrides.broth", script)
        self.assertIn('const priceRow = item.closest("span");', script)
        self.assertIn("priceRow.hidden = true;", script)
        self.assertIn('priceRow.style.display = "none";', script)
        self.assertIn("priceGrid.style.gridTemplateColumns", script)
        self.assertIn('row.style.borderLeft = "0";', script)
        self.assertNotContains(response, "дегустационных супа")
        self.assertNotContains(response, "0,35 л в подарок")
        self.assertNotContains(response, 'class="feature-gift')
        self.assertNotContains(response, 'class="soup-offer-promo"')
        self.assertContains(response, 'class="btn soup-offer-button"')

    def test_soup_prices_can_be_changed_from_database(self):
        SoupPrice.objects.filter(
            price_group=SoupPrice.PriceGroup.DEFAULT,
            volume=SoupPrice.Volume.ONE_LITER,
        ).update(price_rub=2600)
        SoupPrice.objects.filter(
            price_group=SoupPrice.PriceGroup.UKHA,
            volume=SoupPrice.Volume.TWO_LITERS,
        ).update(price_rub=5200)

        response = self.client.get(reverse("index"))

        self.assertContains(response, "2600 ₽")
        self.assertEqual(
            self.get_json_script(response, "default-soup-prices")["1l"],
            "2600 ₽",
        )
        self.assertEqual(
            self.get_json_script(response, "soup-price-overrides")["ukha"]["2l"],
            "5200 ₽",
        )

    def test_inactive_soup_price_is_omitted_from_modal_data(self):
        SoupPrice.objects.filter(
            price_group=SoupPrice.PriceGroup.BROTH,
            volume=SoupPrice.Volume.TWO_LITERS,
        ).update(is_active=False)

        response = self.client.get(reverse("index"))

        self.assertEqual(
            self.get_json_script(response, "soup-price-overrides")["broth"],
            {},
        )

    def test_soup_set_uses_four_soup_image_and_prices(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, "feature-set-4-soups.png")
        self.assertNotContains(response, "feature-set-transparent.png")
        self.assertContains(response, "Сет из борща, солянки, ухи и тыквенного супа-пюре")
        self.assertContains(response, "350мл")
        self.assertContains(response, "750₽")
        self.assertContains(response, "Уха")
        self.assertContains(response, "850₽")
        self.assertContains(response, "заказ от 4х позиций любого супа")

    def test_soup_set_prices_can_be_changed_from_database(self):
        SetPrice.objects.filter(title="350мл").update(price_rub=790)
        SetPrice.objects.filter(title="Уха").update(price_rub=910)

        response = self.client.get(reverse("index"))

        self.assertContains(response, "790₽")
        self.assertContains(response, "910₽")
        self.assertNotContains(response, "750₽")
        self.assertNotContains(response, "850₽")

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
        styles = (
            Path(__file__).resolve().parent
            / "static"
            / "landing"
            / "css"
            / "styles.css"
        ).read_text()

        self.assertContains(response, "data-order-open", count=6)
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
        content = response.content.decode()
        order_start = content.index('<div class="order-modal"')
        order_end = content.index("</div>", content.index('<a class="btn order-phone"', order_start))
        order_modal = content[order_start:order_end]
        self.assertIn('class="order-telegram-link"', order_modal)
        self.assertIn('href="https://t.me/yaestsup"', order_modal)
        self.assertIn('aria-label="ТГ-канал Я Есть Суп"', order_modal)
        self.assertIn("<svg", order_modal)
        self.assertNotIn(">ТГ</a>", order_modal)
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
        description_start = styles.index(".order-dialog > p {")
        description_end = styles.index("}", description_start)
        description_styles = styles[description_start:description_end]
        self.assertIn("line-height: 34px;", description_styles)
        telegram_start = styles.index(".order-dialog > p .order-telegram-link")
        telegram_end = styles.index("}", telegram_start)
        telegram_styles = styles[telegram_start:telegram_end]
        self.assertIn("width: 34px;", telegram_styles)
        self.assertIn("height: 34px;", telegram_styles)

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

        self.assertIn("<b>готовим<br>суп</b>", passport_benefits)
        self.assertNotIn("<b>варим<br>суп</b>", passport_benefits)

    def test_gallery_is_between_soups_and_features(self):
        response = self.client.get(reverse("index"))
        content = response.content.decode()

        soups_position = content.index('id="soups"')
        gallery_position = content.index('class="section-band gallery-line"')
        features_position = content.index('id="delivery"')

        self.assertLess(soups_position, gallery_position)
        self.assertLess(gallery_position, features_position)

    def test_promo_actions_block_starts_features(self):
        response = self.client.get(reverse("index"))
        content = response.content.decode()

        features_start = content.index('id="delivery"')
        promo_position = content.index('class="promo-actions-panel reveal"', features_start)
        set_position = content.index('class="feature-panel feature-set-panel reveal"', features_start)
        promo = content[promo_position:set_position]

        self.assertLess(promo_position, set_position)
        self.assertNotIn("promo-actions-first-order", promo)
        self.assertNotIn("—", promo)
        self.assertNotIn("–", promo)
        self.assertContains(response, "На первый заказ")
        self.assertContains(response, "вкусные бонусы")
        self.assertContains(response, "1000 гр скидка 5%")
        self.assertContains(response, "1600 гр скидка 10%")
        self.assertContains(response, "2200 гр скидка 15%")
        self.assertContains(response, "+5% за подписку")
        self.assertContains(response, "на ТГ-канал")
        self.assertContains(response, "При заказе от")
        self.assertContains(response, "2 супа в подарок по 250 гр")
        self.assertIn("data-order-open", promo)
        self.assertIn('href="https://t.me/yaestsup"', promo)
        self.assertIn('class="promo-telegram"', promo)

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
