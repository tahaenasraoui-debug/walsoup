#!/usr/bin/env python3
"""
test_profile_assets.py - Comprehensive verification suite for walsoup GitHub profile assets
"""

import base64
import os
import re
import unittest
import urllib.parse
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(REPO_ROOT, "assets")
README_PATH = os.path.join(REPO_ROOT, "README.md")

EXPECTED_ASSETS = [
    "pill-website.svg",
    "pill-email.svg",
    "pill-fsr.svg",
    "h-about.svg",
    "h-building.svg",
    "h-working-on.svg",
    "h-smaller.svg",
    "h-stack.svg",
    "card-ditto.svg",
    "card-gemwallet.svg",
    "card-fichegen.svg",
    "card-bitnet.svg",
    "card-bluenet.svg",
    "card-agent-base.svg",
    "card-tether-compass.svg",
    "card-direct-moutamadris.svg",
    "stack.svg",
    "footer.svg",
    "header.svg",
    "dialogue-susie.svg",
]

class TestProfileAssets(unittest.TestCase):

    def test_all_assets_exist(self):
        for asset in EXPECTED_ASSETS:
            path = os.path.join(ASSETS_DIR, asset)
            self.assertTrue(os.path.isfile(path), f"Asset missing: {asset}")

    def test_svg_xml_validity(self):
        for asset in EXPECTED_ASSETS:
            path = os.path.join(ASSETS_DIR, asset)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            root = ET.fromstring(content)
            self.assertTrue(root.tag.endswith("svg"), f"{asset}: root tag is not svg ({root.tag})")
            self.assertIn("viewBox", root.attrib, f"{asset}: missing viewBox attribute")
            self.assertIn("width", root.attrib, f"{asset}: missing width attribute")
            self.assertIn("height", root.attrib, f"{asset}: missing height attribute")

    def test_no_flaky_transform_box(self):
        for asset in EXPECTED_ASSETS:
            path = os.path.join(ASSETS_DIR, asset)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("transform-box", content, (
                f"{asset}: contains 'transform-box' which has cross-browser bugs in SVG <img> context"
            ))

    def test_no_animated_transform_collisions(self):
        for asset in EXPECTED_ASSETS:
            path = os.path.join(ASSETS_DIR, asset)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            animated_classes = re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{[^}]*animation:[^;]+', content)
            for cls in animated_classes:
                pattern = rf'<[^>]+class="[^"]*\b{cls}\b[^"]*"[^>]+transform="[^"]+"'
                match = re.search(pattern, content)
                self.assertIsNone(match, (
                    f"{asset}: element has class '{cls}' with CSS animation and static transform attribute: "
                    f"{match.group(0) if match else ''}"
                ))

    def test_accessibility_reduced_motion(self):
        for asset in EXPECTED_ASSETS:
            path = os.path.join(ASSETS_DIR, asset)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if "@keyframes" in content:
                self.assertIn("@media (prefers-reduced-motion: reduce)", content, (
                    f"{asset}: contains keyframes but lacks prefers-reduced-motion block"
                ))
                self.assertIn("animation: none !important;", content, (
                    f"{asset}: prefers-reduced-motion does not disable animations"
                ))

    def test_dark_mode_support(self):
        for asset in EXPECTED_ASSETS:
            path = os.path.join(ASSETS_DIR, asset)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if any(cls in content for cls in [".bg", ".t ", ".t{", ".t\n", ".name"]):
                self.assertIn("@media (prefers-color-scheme: dark)", content, (
                    f"{asset}: contains theme-dependent classes but lacks dark mode media query"
                ))

    def test_readme_integrity(self):
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        # Verify images
        img_srcs = re.findall(r'<img[^>]+src="([^">]+)"', readme)
        self.assertGreaterEqual(len(img_srcs), 15, f"Too few images in README: {len(img_srcs)}")
        for src in img_srcs:
            if src.startswith("./assets/") or src.startswith("assets/"):
                clean_path = src.lstrip("./")
                full_path = os.path.join(REPO_ROOT, clean_path)
                self.assertTrue(os.path.isfile(full_path), f"README references non-existent local image: {src}")
            elif src.startswith("http://") or src.startswith("https://"):
                parsed = urllib.parse.urlparse(src)
                self.assertTrue(parsed.netloc, f"Invalid URL: {src}")
            else:
                self.fail(f"Unexpected image src in README: {src}")

        # Verify links
        links = re.findall(r'<a[^>]+href="([^">]+)"', readme)
        self.assertGreaterEqual(len(links), 8, f"Too few links in README: {len(links)}")
        for href in links:
            self.assertTrue(href.startswith("https://") or href.startswith("mailto:"), f"Invalid link: {href}")

        # Verify key sections
        self.assertIn("h-about.svg", readme, "README missing about section")
        self.assertIn("h-building.svg", readme, "README missing what i'm building section")
        self.assertIn("h-working-on.svg", readme, "README missing what i'm working on section")
        self.assertIn("h-smaller.svg", readme, "README missing smaller stuff section")
        self.assertIn("h-stack.svg", readme, "README missing stack section")
        self.assertIn("footer.svg", readme, "README missing footer")

        # Verify categorization of projects
        building_section = readme.split("h-building.svg")[1].split("h-working-on.svg")[0]
        self.assertIn("card-ditto.svg", building_section, "ditto should be in building section")
        self.assertIn("card-fichegen.svg", building_section, "fichegen should be in building section")

        working_on_section = readme.split("h-working-on.svg")[1].split("h-smaller.svg")[0]
        self.assertIn("card-gemwallet.svg", working_on_section, "gemwallet should be in working-on section")
        self.assertIn("card-bitnet.svg", working_on_section, "bitnet should be in working-on section")
        self.assertIn("card-agent-base.svg", working_on_section, "agent-base should be in working-on section")

        smaller_section = readme.split("h-smaller.svg")[1].split("h-stack.svg")[0]
        self.assertIn("card-tether-compass.svg", smaller_section, "tether-compass should be in smaller section")
        self.assertIn("card-direct-moutamadris.svg", smaller_section, "direct-moutamadris should be in smaller section")

    def test_camo_proxy_embedded_images(self):
        """Verify embedded sprites use valid data URIs and zero external network fetches."""
        data_uri_pattern = re.compile(r"^data:image/png;base64,([A-Za-z0-9+/=]+)$")
        image_count = 0
        for asset in EXPECTED_ASSETS:
            path = os.path.join(ASSETS_DIR, asset)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            root = ET.fromstring(content)
            for elem in root.iter():
                if elem.tag.endswith("image"):
                    image_count += 1
                    href = elem.attrib.get("href") or elem.attrib.get("{http://www.w3.org/1999/xlink}href")
                    self.assertIsNotNone(href, f"{asset}: <image> tag missing href")
                    self.assertFalse(href.startswith("http://") or href.startswith("https://"),
                                    f"{asset}: <image> uses external network URL: {href}")
                    match = data_uri_pattern.match(href)
                    self.assertTrue(match, f"{asset}: <image> href is not a valid base64 PNG data URI")
                    payload = match.group(1)
                    decoded = base64.b64decode(payload)
                    self.assertTrue(decoded.startswith(b"\x89PNG\r\n\x1a\n"),
                                    f"{asset}: Decoded image does not start with PNG header")
        self.assertGreater(image_count, 0, "No embedded images found across assets")

    def test_pixelated_rendering_for_sprites(self):
        """Verify .pixelated CSS class with crisp-edges / pixelated image-rendering."""
        for asset in EXPECTED_ASSETS:
            path = os.path.join(ASSETS_DIR, asset)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if "<image" in content:
                self.assertIn("image-rendering: pixelated", content,
                              f"{asset}: contains <image> but lacks 'image-rendering: pixelated'")
                self.assertIn(".pixelated", content,
                              f"{asset}: contains <image> but lacks '.pixelated' CSS rule")
                root = ET.fromstring(content)
                for elem in root.iter():
                    if elem.tag.endswith("image"):
                        cls = elem.attrib.get("class", "")
                        self.assertIn("pixelated", cls, f"{asset}: <image> missing 'pixelated' class")

    def test_header_susie_mascot(self):
        """Verify Susie battle idle mascot in header.svg with collision-free bobbing."""
        path = os.path.join(ASSETS_DIR, "header.svg")
        self.assertTrue(os.path.isfile(path), "header.svg missing")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<image", content, "header.svg missing sprite <image> element")
        self.assertIn("data:image/png;base64,", content, "header.svg missing embedded base64 sprite")
        self.assertIn("@keyframes susie-bob", content, "header.svg missing @keyframes susie-bob animation")
        self.assertIn(".susie-idle", content, "header.svg missing .susie-idle class")
        match = re.search(r'<[^>]+class="[^"]*\bsusie-idle\b[^"]*"[^>]+transform="[^"]+"', content)
        self.assertIsNone(match, "header.svg has conflicting transform on .susie-idle element")

    def test_footer_susie_cameo(self):
        """Verify Susie plush cameo in footer.svg beside soup quote."""
        path = os.path.join(ASSETS_DIR, "footer.svg")
        self.assertTrue(os.path.isfile(path), "footer.svg missing")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<image", content, "footer.svg missing sprite <image> element")
        self.assertIn("data:image/png;base64,", content, "footer.svg missing embedded plush sprite")
        self.assertIn("soup is just the best driving force :3", content, "footer.svg missing soup quote")
        self.assertIn(".plush-bob", content, "footer.svg missing .plush-bob idle animation")

    def test_dialogue_susie_asset(self):
        """Verify dialogue-susie.svg dimensions, double border, Susie portrait, prompt arrow, and accessibility."""
        path = os.path.join(ASSETS_DIR, "dialogue-susie.svg")
        self.assertTrue(os.path.isfile(path), "dialogue-susie.svg missing")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        root = ET.fromstring(content)
        self.assertEqual(root.attrib.get("width"), "640", "dialogue-susie.svg width should be 640")
        self.assertEqual(root.attrib.get("height"), "130", "dialogue-susie.svg height should be 130")
        self.assertEqual(root.attrib.get("viewBox"), "0 0 640 130", "dialogue-susie.svg viewBox should be '0 0 640 130'")
        rects = [elem for elem in root.iter() if elem.tag.endswith("rect")]
        self.assertGreaterEqual(len(rects), 2, "dialogue-susie.svg should have at least 2 rects for double border")
        images = [elem for elem in root.iter() if elem.tag.endswith("image")]
        self.assertGreaterEqual(len(images), 1, "dialogue-susie.svg missing portrait image")
        self.assertIn("arrow-blink", content, "dialogue-susie.svg missing arrow-blink animation")
        self.assertIn("@media (prefers-reduced-motion: reduce)", content, "dialogue-susie.svg missing reduced motion support")
        self.assertIn("@media (prefers-color-scheme: dark)", content, "dialogue-susie.svg missing dark mode support")

if __name__ == "__main__":
    unittest.main()
