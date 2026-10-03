#!/usr/bin/env python3
"""
test_profile_assets.py - Comprehensive verification suite for walsoup GitHub profile assets
"""

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

if __name__ == "__main__":
    unittest.main()
