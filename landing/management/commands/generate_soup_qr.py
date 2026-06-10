import os
from pathlib import Path
from urllib.parse import urljoin, urlparse

import segno
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from landing.views import SOUP_SLUGS


class Command(BaseCommand):
    help = "Generate SVG and PNG QR codes for the soup composition pages."

    def add_arguments(self, parser):
        parser.add_argument(
            "--base-url",
            default=os.environ.get("SITE_URL"),
            help="Public HTTPS site URL. Falls back to the SITE_URL environment variable.",
        )
        parser.add_argument(
            "--output-dir",
            default=str(settings.BASE_DIR / "qr_codes"),
            help="Directory for generated SVG and PNG files.",
        )

    def handle(self, *args, **options):
        base_url = (options["base_url"] or "").strip().rstrip("/") + "/"
        parsed_url = urlparse(base_url)

        if parsed_url.scheme != "https" or not parsed_url.netloc:
            raise CommandError(
                "Provide a public HTTPS URL with --base-url or SITE_URL."
            )

        output_dir = Path(options["output_dir"]).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        for slug in SOUP_SLUGS:
            soup_url = urljoin(base_url, f"soup/{slug}/")
            qr = segno.make(soup_url, error="m")
            qr.save(
                output_dir / f"{slug}.svg",
                scale=10,
                border=4,
                dark="#000000",
                light="#ffffff",
            )
            qr.save(
                output_dir / f"{slug}.png",
                scale=16,
                border=4,
                dark="#000000",
                light="#ffffff",
                dpi=300,
            )
            self.stdout.write(f"{slug}: {soup_url}")

        self.stdout.write(
            self.style.SUCCESS(f"QR codes saved to {output_dir}")
        )
