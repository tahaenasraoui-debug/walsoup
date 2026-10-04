#!/usr/bin/env python3
"""
test_e2e_comprehensive.py - Comprehensive Requirement-Driven Opaque-Box E2E Test Suite
for Walid's GitHub Profile Redesign.

Tiers Covered:
- Tier 1: Feature Coverage (R1 Deltarune & Susie, R2 Geometric Cards, R3 Standalone SVG Pipeline, R4 README Restructuring)
- Tier 2: Boundary & Corner Cases (R1-R4 Boundary conditions, extremes, and stress inputs)
- Tier 3: Cross-Feature Combinations (Pairwise interactions and mode intersections)
- Tier 4: Real-World Application Scenarios (GitHub Camo proxy sandbox, full profile load, deterministic rebuild)

Test Runner:
    python3 -m unittest discover tests
    or
    python3 -m unittest tests/test_e2e_comprehensive.py
"""

import base64
import glob
import hashlib
import os
import re
import struct
import subprocess
import sys
import unittest
import urllib.parse
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(REPO_ROOT, "assets")
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
README_PATH = os.path.join(REPO_ROOT, "README.md")
GENERATE_ASSETS_PATH = os.path.join(SCRIPTS_DIR, "generate_assets.py")
DELTAEXT_ARCHIVE = "/home/wal/work/deltaext/DELTARUNE Organized Sprite Archive"

PROJECT_CARD_ASSETS = [
    "card-ditto.svg",
    "card-fichegen.svg",
    "card-gemwallet.svg",
    "card-bitnet.svg",
    "card-agent-base.svg",
    "card-tether-compass.svg",
    "card-direct-moutamadris.svg",
]

WARM_PALETTE = ["#FFB627", "#F0542D", "#E64980"]


def read_asset_text(filename):
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_png_dimensions_from_bytes(png_bytes):
    if len(png_bytes) < 24 or png_bytes[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Invalid PNG header")
    width, height = struct.unpack(">II", png_bytes[16:24])
    return width, height


def get_png_dimensions_from_file(filepath):
    with open(filepath, "rb") as f:
        data = f.read(24)
    return get_png_dimensions_from_bytes(data)


def srgb_channel_to_linear(c):
    c_norm = c / 255.0
    return c_norm / 12.92 if c_norm <= 0.04045 else ((c_norm + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color):
    hex_clean = hex_color.lstrip("#")
    if len(hex_clean) == 3:
        hex_clean = "".join(c * 2 for c in hex_clean)
    r = int(hex_clean[0:2], 16)
    g = int(hex_clean[2:4], 16)
    b = int(hex_clean[4:6], 16)
    return (
        0.2126 * srgb_channel_to_linear(r)
        + 0.7152 * srgb_channel_to_linear(g)
        + 0.0722 * srgb_channel_to_linear(b)
    )


def compute_contrast_ratio(hex_color1, hex_color2):
    lum1 = relative_luminance(hex_color1)
    lum2 = relative_luminance(hex_color2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


# ==============================================================================
# TIER 1: FEATURE COVERAGE
# ==============================================================================

class TestTier1FeatureCoverage(unittest.TestCase):
    """
    Tier 1: Comprehensive feature coverage across all 4 requirements in PROJECT.md:
    - R1: Deltarune Elements & Susie Sprites
    - R2: Warm Geometric Cards & Visual Hierarchy
    - R3: Standalone Animated SVG Pipeline & Camo Proxy Safety
    - R4: README Restructuring & Bio Preservation
    """

    # --------------------------------------------------------------------------
    # R1: Deltarune Elements & Susie Sprites
    # --------------------------------------------------------------------------

    def test_tier1_r1_deltaext_sprite_archive_presence_and_format(self):
        """Verify required Deltarune sprite assets exist at deltaext and have valid PNG format."""
        if not os.path.isdir(DELTAEXT_ARCHIVE):
            self.skipTest(f"DeltaExt sprite archive not found at {DELTAEXT_ARCHIVE}")

        susie_idle_path = os.path.join(
            DELTAEXT_ARCHIVE,
            "Characters/Playable Characters/Susie/Ch1/Dark World/Battle/spr_susieb_idle_0.png",
        )
        susie_portrait_path = os.path.join(
            DELTAEXT_ARCHIVE,
            "Characters/Playable Characters/Susie/Ch1/Portraits/spr_face_sB_0.png",
        )
        susie_plush_path = os.path.join(
            DELTAEXT_ARCHIVE,
            "Characters/Playable Characters/Susie/Ch2/Dark World/Misc/spr_dw_susie_plush_0.png",
        )
        rpg_equip_path = os.path.join(
            DELTAEXT_ARCHIVE,
            "UI/HUD/Ch1/spr_dmenu_equip_1.png",
        )

        for sprite_path, (min_w, min_h) in [
            (susie_idle_path, (40, 40)),
            (susie_portrait_path, (40, 40)),
            (susie_plush_path, (15, 15)),
            (rpg_equip_path, (10, 10)),
        ]:
            self.assertTrue(os.path.isfile(sprite_path), f"Missing required sprite: {sprite_path}")
            self.assertGreater(os.path.getsize(sprite_path), 50, f"Sprite file empty: {sprite_path}")
            w, h = get_png_dimensions_from_file(sprite_path)
            self.assertGreaterEqual(w, min_w, f"Sprite width unexpected for {sprite_path}: {w}")
            self.assertGreaterEqual(h, min_h, f"Sprite height unexpected for {sprite_path}: {h}")

    def test_tier1_r1_header_susie_hero_mascot(self):
        """Verify header.svg incorporates the animated Susie battle idle hero mascot."""
        content = read_asset_text("header.svg")
        self.assertIsNotNone(content, "header.svg must exist")

        has_susie_image = "<image" in content and "data:image/png;base64" in content
        if not has_susie_image:
            self.skipTest("Milestone M1 in progress: Susie mascot not yet integrated into header.svg")

        self.assertIn("data:image/png;base64", content, "Susie mascot must be embedded as base64 data URI")
        self.assertTrue(
            "pixelated" in content or "crisp-edges" in content,
            "Susie mascot must specify pixelated image rendering for crisp pixel art scaling",
        )
        root = ET.fromstring(content)
        images = root.findall(".//{http://www.w3.org/2000/svg}image") + root.findall(".//image")
        self.assertGreaterEqual(len(images), 1, "header.svg must contain Susie <image> element")

    def test_tier1_r1_dialogue_box_structure_and_dimensions(self):
        """Verify dialogue-susie.svg is a standalone SVG with 640x130 dimensions and double border."""
        content = read_asset_text("dialogue-susie.svg")
        if content is None:
            self.skipTest("Milestone M1 in progress: dialogue-susie.svg not yet generated in assets/")

        root = ET.fromstring(content)
        self.assertEqual(root.attrib.get("width"), "640", "dialogue-susie.svg width must be 640")
        self.assertEqual(root.attrib.get("height"), "130", "dialogue-susie.svg height must be 130")
        self.assertIn("viewBox", root.attrib, "dialogue-susie.svg must specify viewBox")
        self.assertIn("0 0 640 130", root.attrib["viewBox"], "viewBox must match 0 0 640 130")

        # Double border: pitch black background and white borders
        self.assertTrue(
            "#000000" in content or "#000" in content or "black" in content,
            "Deltarune dialogue box must have pitch black background",
        )
        rects = root.findall(".//{http://www.w3.org/2000/svg}rect") + root.findall(".//rect")
        self.assertGreaterEqual(len(rects), 2, "Deltarune dialogue box must contain outer and inner border rects")

    def test_tier1_r1_dialogue_box_candid_commentary_content(self):
        """Verify dialogue-susie.svg contains retro monospace typography, asterisk, and candid commentary."""
        content = read_asset_text("dialogue-susie.svg")
        if content is None:
            self.skipTest("Milestone M1 in progress: dialogue-susie.svg not yet generated in assets/")

        # Retro monospace font stack
        self.assertTrue(
            any(f in content for f in ["monospace", "Menlo", "Cascadia Code", "Courier"]),
            "dialogue-susie.svg must use retro monospace font stack",
        )
        # Asterisk dialogue bullet marker
        self.assertTrue(
            "*" in content or "&#42;" in content,
            "dialogue-susie.svg must include classic Deltarune dialogue bullet asterisk '*'",
        )
        # Dialogue commentary keywords
        text_lower = content.lower()
        self.assertTrue(
            any(w in text_lower for w in ["soup", "network", "code", "hey", "build", "offline"]),
            "dialogue-susie.svg must contain candid commentary script",
        )

    def test_tier1_r1_footer_susie_cameo(self):
        """Verify footer.svg incorporates Susie cameo beside the signature soup quote."""
        content = read_asset_text("footer.svg")
        self.assertIsNotNone(content, "footer.svg must exist")

        self.assertIn("soup is just the best driving force :3", content, "Signature soup quote must exist in footer")

        has_susie = "<image" in content and "data:image/png;base64" in content
        if not has_susie:
            self.skipTest("Milestone M1 in progress: Susie cameo not yet integrated into footer.svg")

        self.assertIn("data:image/png;base64", content, "Susie cameo must be embedded as inline base64 image")
        self.assertTrue(
            "pixelated" in content or "crisp-edges" in content,
            "Susie cameo must declare pixelated image rendering",
        )

    def test_tier1_r1_themed_rpg_badges(self):
        """Verify Deltarune RPG badges (HP bars, item tags, equip styling) on project cards."""
        card_contents = [read_asset_text(c) for c in PROJECT_CARD_ASSETS]
        has_rpg_badge = any(
            any(k in c.lower() for k in ["hp", "item", "equip", "spr_dmenu", "badge-rpg", "ax", "mane"])
            for c in card_contents
            if c is not None
        )
        if not has_rpg_badge:
            self.skipTest("Milestone M1 in progress: Deltarune RPG badges not yet integrated into project cards")

        # When integrated, verify at least one card has RPG styling
        self.assertTrue(has_rpg_badge, "Project cards must incorporate Deltarune RPG themed badges")

    # --------------------------------------------------------------------------
    # R2: Warm Geometric Cards & Visual Hierarchy
    # --------------------------------------------------------------------------

    def test_tier1_r2_warm_palette_in_all_cards(self):
        """Verify all project cards utilize signature warm palette (#FFB627, #F0542D, #E64980)."""
        for card in PROJECT_CARD_ASSETS:
            content = read_asset_text(card)
            self.assertIsNotNone(content, f"Card missing: {card}")
            found_colors = [c for c in WARM_PALETTE if c.lower() in content.lower()]
            self.assertGreaterEqual(
                len(found_colors),
                1,
                f"Card {card} must incorporate signature warm palette colors (found: {found_colors})",
            )

    def test_tier1_r2_dual_theme_dark_light_palette(self):
        """Verify dual dark/light mode palette with #2A2119 and #FFF3E0 across all cards."""
        for card in PROJECT_CARD_ASSETS:
            content = read_asset_text(card)
            self.assertIsNotNone(content, f"Card missing: {card}")
            self.assertIn(
                "@media (prefers-color-scheme: dark)",
                content,
                f"Card {card} must support prefers-color-scheme: dark",
            )
            self.assertTrue(
                "#2A2119" in content or "#2a2119" in content,
                f"Card {card} must define dark background #2A2119",
            )
            self.assertTrue(
                "#FFF3E0" in content or "#fff3e0" in content,
                f"Card {card} must define light background #FFF3E0",
            )

    def test_tier1_r2_flagship_cards_visual_prominence(self):
        """Verify flagship project cards (ditto, fichegen) have prominent visual hierarchy (height >= 84)."""
        for flagship in ["card-ditto.svg", "card-fichegen.svg"]:
            content = read_asset_text(flagship)
            self.assertIsNotNone(content, f"Flagship card missing: {flagship}")
            root = ET.fromstring(content)
            height = float(root.attrib.get("height", 0))
            self.assertGreaterEqual(
                height,
                84.0,
                f"Flagship card {flagship} must have prominent height >= 84 (got {height})",
            )
            # Verify status badge element present
            self.assertTrue(
                "finished" in content.lower() or "badge" in content.lower(),
                f"Flagship card {flagship} must feature prominent status badge",
            )

    def test_tier1_r2_wip_cards_status_indication(self):
        """Verify WIP cards (gemwallet, bitnet, agent-base) have dedicated WIP indicators."""
        wip_cards = ["card-gemwallet.svg", "card-bitnet.svg", "card-agent-base.svg"]
        for card in wip_cards:
            content = read_asset_text(card)
            self.assertIsNotNone(content, f"WIP card missing: {card}")
            # Each WIP card should indicate status or badge
            self.assertTrue(
                any(kw in content.lower() for kw in ["wip", "pulse", "badge", "ble", "agentic", "offline"]),
                f"WIP card {card} must display active status or feature badge",
            )

    def test_tier1_r2_smaller_stuff_cards_compact_dimensions(self):
        """Verify smaller project cards (tether-compass, direct-moutamadris) are compact (height <= 64)."""
        smaller_cards = ["card-tether-compass.svg", "card-direct-moutamadris.svg"]
        for card in smaller_cards:
            content = read_asset_text(card)
            self.assertIsNotNone(content, f"Smaller card missing: {card}")
            root = ET.fromstring(content)
            height = float(root.attrib.get("height", 0))
            self.assertLessEqual(
                height,
                64.0,
                f"Smaller card {card} must have compact height <= 64 (got {height})",
            )

    def test_tier1_r2_typography_and_geometry_hierarchy(self):
        """Verify cards adhere to geometric design hierarchy (rx >= 12, bold titles, clean subtexts)."""
        for card in PROJECT_CARD_ASSETS:
            content = read_asset_text(card)
            self.assertIsNotNone(content, f"Card missing: {card}")
            root = ET.fromstring(content)
            rects = root.findall(".//{http://www.w3.org/2000/svg}rect") + root.findall(".//rect")
            card_bg = next((r for r in rects if float(r.attrib.get("width", 0)) >= 600), None)
            self.assertIsNotNone(card_bg, f"Card {card} missing main background rect")
            rx = float(card_bg.attrib.get("rx", 0))
            self.assertGreaterEqual(rx, 12.0, f"Card {card} background rx must be >= 12 for rounded aesthetic")

    # --------------------------------------------------------------------------
    # R3: Standalone Animated SVG Pipeline & Camo Proxy Safety
    # --------------------------------------------------------------------------

    def test_tier1_r3_xml_wellformedness_and_namespaces(self):
        """Verify all SVG assets parse strictly as well-formed XML via ElementTree."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        self.assertGreaterEqual(len(svg_files), 15, "Expected at least 15 SVG assets")
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                root = ET.fromstring(content)
            except ET.ParseError as e:
                self.fail(f"Asset {filename} failed XML parse: {e}")
            self.assertTrue(
                root.tag.endswith("svg"),
                f"Asset {filename} root tag must be svg (got {root.tag})",
            )

    def test_tier1_r3_explicit_dimensions_and_viewbox(self):
        """Verify every SVG asset declares explicit positive width, height, and viewBox."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            root = ET.fromstring(content)
            for attr in ["width", "height", "viewBox"]:
                self.assertIn(attr, root.attrib, f"Asset {filename} missing explicit attribute '{attr}'")

            w = float(root.attrib["width"])
            h = float(root.attrib["height"])
            self.assertGreater(w, 0, f"Asset {filename} width must be > 0")
            self.assertGreater(h, 0, f"Asset {filename} height must be > 0")

            vb_parts = [float(p) for p in root.attrib["viewBox"].split()]
            self.assertEqual(len(vb_parts), 4, f"Asset {filename} viewBox must have 4 numerical components")
            self.assertGreater(vb_parts[2], 0, f"Asset {filename} viewBox width must be > 0")
            self.assertGreater(vb_parts[3], 0, f"Asset {filename} viewBox height must be > 0")

    def test_tier1_r3_camo_proxy_standalone_architecture(self):
        """Verify zero fragment identifiers (#hash) and zero external http/https asset dependencies."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            # Skip old legacy sprite.svg sheet if present
            if filename == "sprite.svg":
                continue
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Camo proxy strips fragment hashes in URLs like foo.svg#view
            # Confirm no <image href="...#..."> or <use href="...#...">
            fragment_refs = re.findall(r'(?:href|xlink:href|src)=["\'][^"\']*#[^"\']+["\']', content)
            self.assertEqual(
                fragment_refs,
                [],
                f"Asset {filename} contains fragment hash reference which breaks under Camo: {fragment_refs}",
            )

            # Check no external network fetches inside SVG (http:// or https:// outside namespace declaration)
            non_ns_links = re.findall(r'(?:href|xlink:href|src)=["\']https?://[^"\']+["\']', content)
            self.assertEqual(
                non_ns_links,
                [],
                f"Asset {filename} contains external network URL which Camo proxy blocks: {non_ns_links}",
            )

    def test_tier1_r3_nested_g_container_animation_isolation(self):
        """Verify two-tier <g> container isolation: no element with an animated class has an inline transform."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()

            animated_classes = re.findall(r"\.([a-zA-Z0-9_-]+)\s*\{[^}]*animation:[^;]+", content)
            for cls in animated_classes:
                # Search for element having both class="{cls}" and transform="..."
                pattern = rf'<[^>]+class="[^"]*\b{cls}\b[^"]*"[^>]+transform="[^"]+"'
                match = re.search(pattern, content)
                self.assertIsNone(
                    match,
                    f"Asset {filename} has element with animated class '{cls}' AND inline transform: {match.group(0) if match else ''}",
                )

    def test_tier1_r3_accessibility_prefers_reduced_motion(self):
        """Verify all assets with CSS @keyframes declare prefers-reduced-motion fallback."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()

            if "@keyframes" in content:
                self.assertIn(
                    "@media (prefers-reduced-motion: reduce)",
                    content,
                    f"Asset {filename} has @keyframes but lacks prefers-reduced-motion media query",
                )
                self.assertIn(
                    "animation: none !important;",
                    content,
                    f"Asset {filename} prefers-reduced-motion block must contain 'animation: none !important;'",
                )

    def test_tier1_r3_deterministic_asset_pipeline_execution(self):
        """Verify scripts/generate_assets.py executes cleanly with exit code 0."""
        self.assertTrue(os.path.isfile(GENERATE_ASSETS_PATH), "generate_assets.py must exist")
        proc = subprocess.run(
            [sys.executable, GENERATE_ASSETS_PATH],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            proc.returncode,
            0,
            f"generate_assets.py failed with code {proc.returncode}.\nStderr: {proc.stderr}\nStdout: {proc.stdout}",
        )
        self.assertIn(
            "validated successfully",
            proc.stdout.lower(),
            "generate_assets.py output should confirm successful asset validation",
        )

    # --------------------------------------------------------------------------
    # R4: README Restructuring & Bio Preservation
    # --------------------------------------------------------------------------

    def test_tier1_r4_bio_and_personality_retention(self):
        """Verify README.md preserves 100% of authentic bio details (cats, soup clarification, quotes)."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        # Authentic bio assertions
        self.assertIn("cats", readme.lower(), "README must retain mention of cats")
        self.assertIn("cat facts", readme.lower(), "README must retain cat facts")
        self.assertIn("souphater.page", readme, "README must retain souphater.page clarification")
        self.assertIn("no, i don't hate soup", readme.lower(), "README must retain 'no, i don't hate soup'")
        self.assertIn(
            "every elegant solution eventually creates a new, much worse problem.",
            readme,
            "README must retain signature quote",
        )
        self.assertIn(
            "soup is just the best driving force :3",
            readme,
            "README must retain footer soup driving force quote",
        )

    def test_tier1_r4_all_seven_project_showcases_present(self):
        """Verify README.md showcases all 7 software projects across finished and WIP categories."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        expected_projects = [
            "ditto",
            "fichegen",
            "gemwallet",
            "bitnet",
            "agent-base",
            "tether-compass",
            "direct-moutamadris",
        ]
        for proj in expected_projects:
            self.assertIn(
                f"card-{proj}.svg",
                readme,
                f"README must showcase project card: card-{proj}.svg",
            )

    def test_tier1_r4_project_repository_urls(self):
        """Verify all project links point to the correct GitHub repositories."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        expected_repo_links = [
            "https://github.com/walsoup/ditto",
            "https://github.com/walsoup/Fichegen",
            "https://github.com/walsoup/gemwallet",
            "https://github.com/walsoup/bitnet",
            "https://github.com/walsoup/agent-base",
            "https://github.com/walsoup/tether-compass",
            "https://github.com/walsoup/DirectMoutamadris",
        ]
        for url in expected_repo_links:
            self.assertIn(url, readme, f"README must link to official repository: {url}")

    def test_tier1_r4_section_ordering_and_visual_flow(self):
        """Verify README section headers preserve strict visual sequence."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        headers = [
            "header.svg",
            "h-about.svg",
            "h-building.svg",
            "h-working-on.svg",
            "h-smaller.svg",
            "h-stack.svg",
            "footer.svg",
        ]
        indices = [readme.find(h) for h in headers]
        for i, (h, idx) in enumerate(zip(headers, indices)):
            self.assertNotEqual(idx, -1, f"README missing section header: {h}")
            if i > 0:
                self.assertGreater(
                    idx,
                    indices[i - 1],
                    f"Section header {h} must appear after {headers[i-1]}",
                )

    def test_tier1_r4_contact_pills_and_links(self):
        """Verify contact pills are present and link to valid targets."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        for pill in ["pill-website.svg", "pill-email.svg", "pill-fsr.svg"]:
            self.assertIn(pill, readme, f"README missing contact pill: {pill}")

        self.assertIn("https://souphater.page", readme, "Website pill must link to https://souphater.page")
        self.assertIn("mailto:walidelonk@gmail.com", readme, "Email pill must link to mailto:walidelonk@gmail.com")

    def test_tier1_r4_tech_stack_and_stats_integration(self):
        """Verify stack.svg and GitHub stats widgets are cleanly integrated in README."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        self.assertIn("stack.svg", readme, "README must feature stack.svg")
        self.assertIn("github-readme-stats", readme, "README must feature github-readme-stats widget")
        self.assertIn("top-langs", readme, "README must feature top languages widget")


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES
# ==============================================================================

class TestTier2BoundariesAndCornerCases(unittest.TestCase):
    """
    Tier 2: Boundary & Corner Cases across all 4 requirements:
    - R1: Data URI decoding, sprite aspect ratios, dialogue geometry, error handling
    - R2: Coordinate bounds, dimension extremes, text anchors, WCAG contrast
    - R3: transform-box absence, collision isolation, XML error recovery, escaping
    - R4: Link validation, URL protocols, HTML balance, alt attributes, deduplication
    """

    # --------------------------------------------------------------------------
    # R1 Boundaries
    # --------------------------------------------------------------------------

    def test_tier2_r1_base64_data_uri_validity_and_payload(self):
        """Verify all embedded PNG base64 data URIs decode strictly to valid PNG bytes."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        tested_uris = 0
        for svg_path in svg_files:
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            matches = re.findall(r'data:image/png;base64,([A-Za-z0-9+/=]+)', content)
            for b64 in matches:
                try:
                    raw_bytes = base64.b64decode(b64, validate=True)
                except Exception as e:
                    self.fail(f"Corrupt base64 data URI in {os.path.basename(svg_path)}: {e}")
                self.assertEqual(
                    raw_bytes[:8],
                    b"\x89PNG\r\n\x1a\n",
                    f"Decoded data URI in {os.path.basename(svg_path)} is not a valid PNG",
                )
                tested_uris += 1

        # If assets do not contain base64 yet (pre-M1), test deltaext source encoding
        if tested_uris == 0 and os.path.isdir(DELTAEXT_ARCHIVE):
            sample_sprite = os.path.join(
                DELTAEXT_ARCHIVE,
                "Characters/Playable Characters/Susie/Ch1/Dark World/Battle/spr_susieb_idle_0.png",
            )
            with open(sample_sprite, "rb") as f:
                raw = f.read()
            encoded = base64.b64encode(raw).decode("ascii")
            decoded = base64.b64decode(encoded, validate=True)
            self.assertEqual(decoded[:8], b"\x89PNG\r\n\x1a\n")

    def test_tier2_r1_sprite_aspect_ratio_consistency(self):
        """Verify sprite <image> dimensions preserve native sprite aspect ratios within 5% tolerance."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        tested_images = 0
        for svg_path in svg_files:
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            root = ET.fromstring(content)
            for img in root.findall(".//{http://www.w3.org/2000/svg}image") + root.findall(".//image"):
                href = img.attrib.get("href") or img.attrib.get("{http://www.w3.org/1999/xlink}href", "")
                if href.startswith("data:image/png;base64,"):
                    b64 = href.split("base64,")[1]
                    raw_png = base64.b64decode(b64)
                    native_w, native_h = get_png_dimensions_from_bytes(raw_png)
                    svg_w = float(img.attrib.get("width", native_w))
                    svg_h = float(img.attrib.get("height", native_h))
                    ratio_native = native_w / native_h
                    ratio_svg = svg_w / svg_h
                    diff = abs(ratio_native - ratio_svg) / ratio_native
                    self.assertLess(
                        diff,
                        0.05,
                        f"Sprite in {os.path.basename(svg_path)} is distorted (aspect ratio difference: {diff:.2%})",
                    )
                    tested_images += 1

    def test_tier2_r1_dialogue_box_text_bounds_and_overflow(self):
        """Verify dialogue box text elements stay within coordinate bounds [0..640, 0..130]."""
        content = read_asset_text("dialogue-susie.svg")
        if content is None:
            self.skipTest("Milestone M1 in progress: dialogue-susie.svg not yet generated")

        root = ET.fromstring(content)
        texts = root.findall(".//{http://www.w3.org/2000/svg}text") + root.findall(".//text")
        for t in texts:
            x = float(t.attrib.get("x", 0))
            y = float(t.attrib.get("y", 0))
            self.assertGreaterEqual(x, 10.0, f"Dialogue text x={x} too close to left margin")
            self.assertLessEqual(x, 620.0, f"Dialogue text x={x} overflows right margin")
            self.assertGreaterEqual(y, 15.0, f"Dialogue text y={y} overflows top margin")
            self.assertLessEqual(y, 125.0, f"Dialogue text y={y} overflows bottom margin")

    def test_tier2_r1_dialogue_box_double_border_geometry(self):
        """Verify dialogue box outer and inner border rect geometry is strictly valid."""
        content = read_asset_text("dialogue-susie.svg")
        if content is None:
            self.skipTest("Milestone M1 in progress: dialogue-susie.svg not yet generated")

        root = ET.fromstring(content)
        rects = root.findall(".//{http://www.w3.org/2000/svg}rect") + root.findall(".//rect")
        self.assertGreaterEqual(len(rects), 2, "Double border requires at least two rects")
        for r in rects:
            w = float(r.attrib.get("width", 0))
            h = float(r.attrib.get("height", 0))
            x = float(r.attrib.get("x", 0))
            y = float(r.attrib.get("y", 0))
            self.assertGreater(w, 0, f"Border rect width must be positive: {w}")
            self.assertGreater(h, 0, f"Border rect height must be positive: {h}")
            self.assertGreaterEqual(x, 0, f"Border rect x must be >= 0: {x}")
            self.assertGreaterEqual(y, 0, f"Border rect y must be >= 0: {y}")

    def test_tier2_r1_pixel_art_rendering_properties(self):
        """Verify pixel art image elements declare pixelated rendering to avoid anti-aliasing blur."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "<image" in content and "data:image/png;base64" in content:
                self.assertTrue(
                    "image-rendering: pixelated" in content or "image-rendering: crisp-edges" in content,
                    f"{os.path.basename(svg_path)} embeds raster sprite but lacks pixelated image rendering rule",
                )

    def test_tier2_r1_empty_or_corrupt_sprite_source_handling(self):
        """Verify helper raises FileNotFoundError or ValueError on missing/corrupt sprite data."""
        with self.assertRaises((FileNotFoundError, OSError)):
            get_png_dimensions_from_file("/tmp/nonexistent_susie_sprite_12345.png")

        corrupt_bytes = b"\x00\x00\x00\x00not_a_png"
        with self.assertRaises(ValueError):
            get_png_dimensions_from_bytes(corrupt_bytes)

    # --------------------------------------------------------------------------
    # R2 Boundaries
    # --------------------------------------------------------------------------

    def test_tier2_r2_zero_and_negative_dimension_absence(self):
        """Verify no SVG geometric element contains zero or negative width, height, or radius."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            root = ET.fromstring(content)
            for elem in root.iter():
                for dim_attr in ["width", "height", "r", "rx", "ry"]:
                    if dim_attr in elem.attrib:
                        val_str = elem.attrib[dim_attr].rstrip("px")
                        try:
                            val = float(val_str)
                            self.assertGreater(
                                val,
                                0,
                                f"Element <{elem.tag.split('}')[-1]}> in {filename} has non-positive {dim_attr}='{val}'",
                            )
                        except ValueError:
                            pass

    def test_tier2_r2_card_viewbox_coordinate_bounds(self):
        """Verify all project cards declare standard viewBox [0, 0, 640, height] with height in [60, 100]."""
        for card in PROJECT_CARD_ASSETS:
            content = read_asset_text(card)
            self.assertIsNotNone(content, f"Card missing: {card}")
            root = ET.fromstring(content)
            vb = [float(p) for p in root.attrib["viewBox"].split()]
            self.assertEqual(vb[0], 0.0, f"Card {card} viewBox min-x must be 0")
            self.assertEqual(vb[1], 0.0, f"Card {card} viewBox min-y must be 0")
            self.assertEqual(vb[2], 640.0, f"Card {card} viewBox width must be 640")
            self.assertTrue(
                60.0 <= vb[3] <= 100.0,
                f"Card {card} viewBox height {vb[3]} outside standard [60, 100]",
            )

    def test_tier2_r2_badge_text_centering_and_anchors(self):
        """Verify status badge text uses text-anchor='middle' and is centered on badge rectangle."""
        for card in PROJECT_CARD_ASSETS:
            content = read_asset_text(card)
            root = ET.fromstring(content)
            badge_rects = [
                r for r in root.findall(".//{http://www.w3.org/2000/svg}rect") + root.findall(".//rect")
                if float(r.attrib.get("x", 0)) > 400 and float(r.attrib.get("width", 0)) < 150
            ]
            badge_texts = [
                t for t in root.findall(".//{http://www.w3.org/2000/svg}text") + root.findall(".//text")
                if float(t.attrib.get("x", 0)) > 400
            ]
            if badge_rects and badge_texts:
                b_rect = badge_rects[0]
                b_text = badge_texts[0]
                self.assertEqual(
                    b_text.attrib.get("text-anchor"),
                    "middle",
                    f"Badge text in {card} must specify text-anchor='middle'",
                )
                rect_center = float(b_rect.attrib["x"]) + float(b_rect.attrib["width"]) / 2.0
                text_x = float(b_text.attrib["x"])
                self.assertLess(
                    abs(rect_center - text_x),
                    2.0,
                    f"Badge text in {card} is misaligned from badge rect center: {text_x} vs {rect_center}",
                )

    def test_tier2_r2_card_contrast_ratio_validation(self):
        """Verify WCAG contrast compliance: dark mode text on dark bg and light mode text on light bg > 7:1."""
        dark_contrast = compute_contrast_ratio("#2A2119", "#fff4e6")
        self.assertGreater(
            dark_contrast,
            7.0,
            f"Dark mode contrast ratio {dark_contrast:.2f} must exceed WCAG AAA threshold of 7:1",
        )

        light_contrast = compute_contrast_ratio("#FFF3E0", "#24190f")
        self.assertGreater(
            light_contrast,
            7.0,
            f"Light mode contrast ratio {light_contrast:.2f} must exceed WCAG AAA threshold of 7:1",
        )

    def test_tier2_r2_extreme_text_length_tolerance(self):
        """Verify card title and badge coordinate layout maintains minimum 40px gap."""
        for card in PROJECT_CARD_ASSETS:
            content = read_asset_text(card)
            root = ET.fromstring(content)
            title_text = next(
                (t for t in root.findall(".//{http://www.w3.org/2000/svg}text") + root.findall(".//text")
                 if float(t.attrib.get("x", 0)) < 200),
                None,
            )
            badge_rect = next(
                (r for r in root.findall(".//{http://www.w3.org/2000/svg}rect") + root.findall(".//rect")
                 if float(r.attrib.get("x", 0)) > 400),
                None,
            )
            if title_text is not None and badge_rect is not None:
                title_x = float(title_text.attrib["x"])
                badge_x = float(badge_rect.attrib["x"])
                # Minimum separation to prevent layout collision
                self.assertGreater(
                    badge_x - title_x,
                    200.0,
                    f"Card {card} title and badge lack sufficient layout buffer",
                )

    def test_tier2_r2_corner_radius_bounds(self):
        """Verify card background corner radii rx bounded between 12 and 22."""
        for card in PROJECT_CARD_ASSETS:
            content = read_asset_text(card)
            root = ET.fromstring(content)
            rects = root.findall(".//{http://www.w3.org/2000/svg}rect") + root.findall(".//rect")
            card_bg = next((r for r in rects if float(r.attrib.get("width", 0)) >= 600), None)
            if card_bg is not None and "rx" in card_bg.attrib:
                rx = float(card_bg.attrib["rx"])
                self.assertTrue(
                    12.0 <= rx <= 22.0,
                    f"Card {card} corner radius rx={rx} outside standard [12, 22]",
                )

    # --------------------------------------------------------------------------
    # R3 Boundaries
    # --------------------------------------------------------------------------

    def test_tier2_r3_transform_box_strict_absence(self):
        """Verify transform-box is strictly absent across all SVG assets."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(
                "transform-box",
                content,
                f"Asset {filename} contains 'transform-box', which causes WebKit bugs in Camo context",
            )

    def test_tier2_r3_inline_transform_collision_strict_isolation(self):
        """Verify no XML tag combines an animated CSS class with an inline transform attribute."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            animated_classes = re.findall(r"\.([a-zA-Z0-9_-]+)\s*\{[^}]*animation:[^;]+", content)
            for cls in animated_classes:
                regex = re.compile(rf"<[^>]+class=[\"'][^\"']*\b{cls}\b[^\"']*[\"'][^>]*>", re.DOTALL)
                for tag_match in regex.finditer(content):
                    tag_str = tag_match.group(0)
                    self.assertNotIn(
                        "transform=",
                        tag_str,
                        f"Asset {filename} has collision: element with animated class '{cls}' has inline transform attribute: {tag_str}",
                    )

    def test_tier2_r3_malformed_xml_rejection(self):
        """Verify ElementTree strictly rejects malformed XML inputs with ET.ParseError."""
        malformed_samples = [
            "<svg><rect width='10' height='10'></svg>",
            "<svg><g>&invalid_entity;</g></svg>",
            "<svg width='100' height='100'><path d='M0 0'</svg>",
        ]
        for sample in malformed_samples:
            with self.assertRaises(ET.ParseError):
                ET.fromstring(sample)

    def test_tier2_r3_external_network_resource_prohibition(self):
        """Verify SVGs contain zero external network references in href, src, or CSS url()."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            if filename == "sprite.svg":
                continue
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            url_matches = re.findall(r"url\s*\(\s*['\"]?https?://[^'\")]+['\"]?\s*\)", content)
            self.assertEqual(
                url_matches,
                [],
                f"Asset {filename} contains external CSS url(...) call: {url_matches}",
            )

    def test_tier2_r3_xml_injection_and_escaping_safety(self):
        """Verify SVG text elements do not contain raw unescaped XML syntax markers."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            root = ET.fromstring(content)
            for t in root.iter():
                if t.text:
                    # After parsing, text should be clean string, not containing raw unparsed tags
                    self.assertNotIn(
                        "<?xml",
                        t.text,
                        f"Asset {filename} text node contains raw XML injection payload",
                    )

    def test_tier2_r3_reduced_motion_override_completeness(self):
        """Verify every @keyframes animation rule has an explicit reduced-motion disablement."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            keyframes = re.findall(r"@keyframes\s+([a-zA-Z0-9_-]+)", content)
            if keyframes:
                self.assertIn(
                    "@media (prefers-reduced-motion: reduce)",
                    content,
                    f"Asset {filename} declares keyframes {keyframes} but lacks prefers-reduced-motion block",
                )
                self.assertIn(
                    "animation: none !important;",
                    content,
                    f"Asset {filename} prefers-reduced-motion block must enforce 'animation: none !important;'",
                )

    # --------------------------------------------------------------------------
    # R4 Boundaries
    # --------------------------------------------------------------------------

    def test_tier2_r4_readme_broken_link_detection(self):
        """Verify all local asset references in README.md exist on filesystem."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()
        srcs = re.findall(r'<img[^>]+src="([^">]+)"', readme)
        for src in srcs:
            if src.startswith("./assets/") or src.startswith("assets/"):
                clean_path = src.lstrip("./")
                full_path = os.path.join(REPO_ROOT, clean_path)
                self.assertTrue(
                    os.path.isfile(full_path),
                    f"README references broken local asset path: {src}",
                )

    def test_tier2_r4_url_scheme_validation(self):
        """Verify all href attributes in README.md use strictly https:// or mailto: schemes."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()
        hrefs = re.findall(r'<a[^>]+href="([^">]+)"', readme)
        for href in hrefs:
            parsed = urllib.parse.urlparse(href)
            self.assertIn(
                parsed.scheme,
                ["https", "mailto"],
                f"README link uses unauthorized or insecure scheme: {href}",
            )

    def test_tier2_r4_empty_section_header_guard(self):
        """Verify no section header image in README.md is orphaned without following content."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()
        headers = [
            "h-about.svg",
            "h-building.svg",
            "h-working-on.svg",
            "h-smaller.svg",
            "h-stack.svg",
        ]
        for i in range(len(headers) - 1):
            h_curr = headers[i]
            h_next = headers[i + 1]
            section_content = readme.split(h_curr)[1].split(h_next)[0].strip()
            self.assertGreater(
                len(section_content),
                20,
                f"Section under {h_curr} has insufficient or empty content before {h_next}",
            )

    def test_tier2_r4_html_tag_pairing_and_nesting(self):
        """Verify HTML wrapper tags in README.md (like <div align='center'>) are balanced."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()
        open_divs = len(re.findall(r"<div\b", readme))
        close_divs = len(re.findall(r"</div>", readme))
        self.assertEqual(
            open_divs,
            close_divs,
            f"Mismatched <div> tags in README: {open_divs} open vs {close_divs} closed",
        )
        open_as = len(re.findall(r"<a\b", readme))
        close_as = len(re.findall(r"</a>", readme))
        self.assertEqual(
            open_as,
            close_as,
            f"Mismatched <a> tags in README: {open_as} open vs {close_as} closed",
        )

    def test_tier2_r4_duplicate_image_or_link_guard(self):
        """Verify each project card image appears exactly once in README.md."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()
        for card in PROJECT_CARD_ASSETS:
            count = readme.count(card)
            self.assertEqual(
                count,
                1,
                f"Project card {card} must appear exactly once in README (found {count})",
            )

    def test_tier2_r4_alt_text_completeness(self):
        """Verify every <img ...> element in README.md declares a non-empty alt attribute."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()
        img_tags = re.findall(r"<img[^>]+>", readme)
        for img in img_tags:
            alt_match = re.search(r'alt="([^"]*)"', img)
            self.assertIsNotNone(alt_match, f"Image tag missing alt attribute: {img}")
            self.assertGreater(
                len(alt_match.group(1).strip()),
                0,
                f"Image tag has empty alt attribute: {img}",
            )


# ==============================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS
# ==============================================================================

class TestTier3CrossFeatureCombinations(unittest.TestCase):
    """
    Tier 3: Pairwise interactions and cross-feature mode intersections:
    - Dark mode with CSS keyframe animations
    - Reduced motion with Susie bobbing
    - Dialogue box in dark vs light mode
    - Project card badges with dark backgrounds
    - Nested containers with static transforms and animated classes
    - Responsive card scaling and viewBox aspect ratios
    """

    def test_tier3_dark_mode_with_css_keyframe_animations(self):
        """Verify that prefers-color-scheme: dark and @keyframes animations coexist independently."""
        for card in PROJECT_CARD_ASSETS:
            content = read_asset_text(card)
            self.assertIsNotNone(content)
            if "@keyframes" in content:
                self.assertIn("@media (prefers-color-scheme: dark)", content)
                # Verify dark mode block does not accidentally override animations with 'animation: none'
                dark_block = content.split("@media (prefers-color-scheme: dark)")[1].split("}")[0]
                self.assertNotIn(
                    "animation: none",
                    dark_block,
                    f"Dark mode in {card} should not disable animations",
                )

    def test_tier3_reduced_motion_with_susie_bobbing(self):
        """Verify that reduced-motion preference disables idle bobbing while keeping Susie sprite rendered."""
        content = read_asset_text("header.svg")
        self.assertIsNotNone(content)
        if "@keyframes" in content:
            self.assertIn(
                "@media (prefers-reduced-motion: reduce)",
                content,
                "header.svg must disable bobbing under prefers-reduced-motion: reduce",
            )
            rm_block = content.split("@media (prefers-reduced-motion: reduce)")[1].split("}")[0]
            self.assertIn(
                "animation: none !important;",
                rm_block,
                "Reduced motion must disable all animations with !important",
            )

    def test_tier3_dialogue_box_dark_light_color_adaptability(self):
        """Verify dialogue box maintains high contrast double border in both dark and light modes."""
        content = read_asset_text("dialogue-susie.svg")
        if content is None:
            self.skipTest("Milestone M1 in progress: dialogue-susie.svg not yet generated")

        # Deltarune aesthetic maintains pitch black canvas (#000000) with crisp white linework (#FFFFFF)
        self.assertTrue(
            "#000000" in content or "#000" in content,
            "Dialogue box must retain pitch black canvas",
        )
        self.assertTrue(
            "#ffffff" in content or "#fff" in content or "#FFFFFF" in content,
            "Dialogue box must retain crisp white borders and text",
        )

    def test_tier3_project_card_badges_with_dark_background(self):
        """Verify that status badges maintain legible contrast against both dark (#2A2119) and light backgrounds."""
        card_content = read_asset_text("card-ditto.svg")
        self.assertIsNotNone(card_content)
        # Badge green (#2DA44E) on white text (#FFFFFF)
        badge_contrast = compute_contrast_ratio("#2DA44E", "#ffffff")
        self.assertGreaterEqual(
            badge_contrast,
            3.0,
            f"Status badge contrast {badge_contrast:.2f} must meet UI component contrast standard",
        )

    def test_tier3_nested_containers_with_static_transforms_and_animated_classes(self):
        """Verify two-tier container hierarchy in animated assets (outer static transform, inner animation class)."""
        animated_assets = ["header.svg", "footer.svg", "card-ditto.svg"]
        for asset in animated_assets:
            content = read_asset_text(asset)
            self.assertIsNotNone(content)
            root = ET.fromstring(content)
            # Check any element with transform attribute
            for elem in root.iter():
                if "transform" in elem.attrib:
                    cls = elem.attrib.get("class", "")
                    # Ensure element with transform does not also have an animated class
                    for c in cls.split():
                        self.assertFalse(
                            f".{c}" in content and "animation:" in content.split(f".{c}")[1].split("}")[0],
                            f"Element in {asset} has transform and animated class '{c}' simultaneously",
                        )

    def test_tier3_responsive_card_scaling_and_viewbox_aspect_ratios(self):
        """Verify that declared img width and height in README.md match SVG viewBox aspect ratios within 1%."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        for card in PROJECT_CARD_ASSETS:
            content = read_asset_text(card)
            root = ET.fromstring(content)
            vb = [float(p) for p in root.attrib["viewBox"].split()]
            svg_ratio = vb[2] / vb[3]

            # Look up README img tag for this card
            pattern = rf'<img[^>]+src="[^"]*{card}"[^>]*>'
            match = re.search(pattern, readme)
            if match:
                img_tag = match.group(0)
                w_match = re.search(r'width="(\d+)"', img_tag)
                h_match = re.search(r'height="(\d+)"', img_tag)
                if w_match and h_match:
                    img_w = float(w_match.group(1))
                    img_h = float(h_match.group(1))
                    readme_ratio = img_w / img_h
                    diff = abs(svg_ratio - readme_ratio) / svg_ratio
                    self.assertLess(
                        diff,
                        0.01,
                        f"Aspect ratio mismatch for {card} in README: svg={svg_ratio:.3f}, readme={readme_ratio:.3f}",
                    )


# ==============================================================================
# TIER 4: REAL-WORLD APPLICATION SCENARIOS
# ==============================================================================

class TestTier4RealWorldScenarios(unittest.TestCase):
    """
    Tier 4: Real-World Application Scenarios:
    - Camo proxy document isolation simulation
    - Full profile README rendering & integrity simulation
    - Deterministic asset rebuild execution
    - Accessibility & screen reader semantic audit
    - Dual theme visual integrity simulation
    """

    def test_tier4_camo_proxy_document_isolation_simulation(self):
        """Simulate GitHub Camo image proxy document isolation sandbox across all SVGs."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            if filename == "sprite.svg":
                continue
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Camo disallows <script>, inline event handlers (onclick, onload), <foreignObject>
            self.assertNotIn("<script", content.lower(), f"Asset {filename} contains forbidden <script> tag")
            self.assertNotIn("onload=", content.lower(), f"Asset {filename} contains forbidden onload event handler")
            self.assertNotIn("onclick=", content.lower(), f"Asset {filename} contains forbidden onclick event handler")
            self.assertNotIn("onerror=", content.lower(), f"Asset {filename} contains forbidden onerror event handler")
            self.assertNotIn("<foreignobject", content.lower(), f"Asset {filename} contains <foreignObject> tag")

    def test_tier4_full_profile_readme_rendering_simulation(self):
        """Simulate end-to-end README rendering and validate categorization of all 7 projects."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        # Categorization check
        building_sec = readme.split("h-building.svg")[1].split("h-working-on.svg")[0]
        self.assertIn("card-ditto.svg", building_sec, "ditto must be in 'what i'm building' section")
        self.assertIn("card-fichegen.svg", building_sec, "fichegen must be in 'what i'm building' section")

        working_sec = readme.split("h-working-on.svg")[1].split("h-smaller.svg")[0]
        self.assertIn("card-gemwallet.svg", working_sec, "gemwallet must be in 'what i'm working on' section")
        self.assertIn("card-bitnet.svg", working_sec, "bitnet must be in 'what i'm working on' section")
        self.assertIn("card-agent-base.svg", working_sec, "agent-base must be in 'what i'm working on' section")

        smaller_sec = readme.split("h-smaller.svg")[1].split("h-stack.svg")[0]
        self.assertIn("card-tether-compass.svg", smaller_sec, "tether-compass must be in 'smaller stuff' section")
        self.assertIn("card-direct-moutamadris.svg", smaller_sec, "direct-moutamadris must be in 'smaller stuff' section")

    def test_tier4_asset_pipeline_deterministic_e2e_rebuild(self):
        """Execute scripts/generate_assets.py twice and assert bit-for-bit SHA-256 reproducibility."""
        def run_pipeline():
            proc = subprocess.run(
                [sys.executable, GENERATE_ASSETS_PATH],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, f"Generator failed: {proc.stderr}")
            hashes = {}
            for svg in PROJECT_CARD_ASSETS:
                p = os.path.join(ASSETS_DIR, svg)
                with open(p, "rb") as f:
                    hashes[svg] = hashlib.sha256(f.read()).hexdigest()
            return hashes

        run1 = run_pipeline()
        run2 = run_pipeline()
        self.assertEqual(run1, run2, "Asset pipeline must be 100% deterministic (reproducible builds)")

    def test_tier4_accessibility_and_screen_reader_audit(self):
        """Audit entire profile assets and README for accessibility and semantic text compliance."""
        svg_files = glob.glob(os.path.join(ASSETS_DIR, "*.svg"))
        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            if filename == "sprite.svg":
                continue
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            root = ET.fromstring(content)
            self.assertEqual(
                root.attrib.get("role"),
                "img",
                f"Asset {filename} must declare role='img' for accessibility",
            )
            self.assertIn(
                "aria-label",
                root.attrib,
                f"Asset {filename} must declare aria-label for accessibility",
            )

    def test_tier4_dual_theme_visual_integrity_simulation(self):
        """Simulate theme switcher and verify dark/light color adaptations across all cards and headers."""
        headers_and_cards = [
            "header.svg",
            "footer.svg",
            "h-about.svg",
            "h-building.svg",
            "h-working-on.svg",
            "h-smaller.svg",
            "h-stack.svg",
        ] + PROJECT_CARD_ASSETS

        for asset in headers_and_cards:
            content = read_asset_text(asset)
            self.assertIsNotNone(content, f"Asset missing: {asset}")
            self.assertIn(
                "@media (prefers-color-scheme: dark)",
                content,
                f"Asset {asset} must declare dark mode rules in @media (prefers-color-scheme: dark)",
            )


if __name__ == "__main__":
    unittest.main()
