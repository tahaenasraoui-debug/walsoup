# Test Infrastructure & Architecture

## Overview
This document specifies the test architecture, methodology, progressive testability strategy, and verification criteria for Walid's GitHub profile redesign (`walsoup`).

The testing approach is **requirement-driven**, **opaque-box**, and structured across a **4-tier testing hierarchy** that verifies both visual asset integrity and profile integration contracts without depending on internal implementation details.

---

## Testing Principles

1. **Progressive Testability**:
   Tests must be runnable at any point during project development. Features from completed milestones are fully exercised, while features under active implementation (e.g. Milestone 1 Deltarune sprite generation) are conditionally verified or gracefully reported without failing the suite, enabling continuous integration throughout the multi-agent workflow.

2. **Opaque-Box Verification**:
   Tests evaluate only externally observable artifacts: generated SVG files (`assets/*.svg`), profile markup (`README.md`), asset build pipelines (`scripts/generate_assets.py`), and reference sprite archives (`/home/wal/work/deltaext`).

3. **Zero External Dependencies**:
   Tests are written exclusively using Python standard library modules (`unittest`, `xml.etree.ElementTree`, `re`, `struct`, `base64`, `subprocess`, `urllib.parse`, `hashlib`). No external test packages or graphical rendering engines are required.

4. **GitHub Camo Proxy & Security Hardening**:
   Tests actively simulate GitHub Camo's sandboxed image proxy constraints (forbidding external URLs, fragment `#hash` identifiers, `<script>` tags, inline event listeners, and `<foreignObject>` payloads).

---

## 4-Tier Test Taxonomy

```
+-------------------------------------------------------------------------+
|                  Tier 4: Real-World Application Scenarios               |
|  - Camo proxy isolation sandbox simulation                              |
|  - Full profile README rendering & project categorization               |
|  - Bit-for-bit deterministic SVG build reproducibility                  |
|  - Accessibility (role="img", aria-label, semantic <text>) audit        |
|  - Dual-theme (dark/light) visual integrity simulation                  |
+-------------------------------------------------------------------------+
|                  Tier 3: Cross-Feature Combinations                     |
|  - Dark mode with CSS keyframe animations                               |
|  - Prefers-reduced-motion with Susie battle idle bobbing                |
|  - Dialogue box color adaptability in dark & light schemes              |
|  - Project status badge contrast against dark card backgrounds          |
|  - Two-tier container hierarchy (outer transform, inner animation class) |
|  - Responsive image dimensions matching SVG viewBox aspect ratios       |
+-------------------------------------------------------------------------+
|                  Tier 2: Boundary & Corner Cases                        |
|  - Base64 data URI decoding & PNG header validation                     |
|  - Sprite aspect ratio preservation (<= 5% distortion tolerance)        |
|  - Dialogue box text coordinate bounds & overflow guards                |
|  - Double border inset geometry validation                              |
|  - Pixelated image-rendering rules for high-DPI crispness               |
|  - Strict absence of 'transform-box' (WebKit bug prevention)            |
|  - Strict isolation of inline transforms from animated CSS classes      |
|  - Malformed XML error rejection & XML injection safety                 |
|  - Network URL leakage prevention in SVGs                               |
|  - README link validation, HTML tag balance, alt text completeness     |
+-------------------------------------------------------------------------+
|                  Tier 1: Feature Coverage (R1 - R4)                     |
|  - R1: Deltarune Elements & Susie Sprites (Mascot, Dialogue, Cameo)     |
|  - R2: Warm Geometric Cards & Visual Hierarchy (Flagships, WIPs, Small) |
|  - R3: Standalone Animated SVG Pipeline (XML, ViewBox, Camo-safe)       |
|  - R4: README Restructuring & Bio Preservation (Cats, Soup, Projects)   |
+-------------------------------------------------------------------------+
```

---

## Detailed Test Tier Inventory

### Tier 1: Feature Coverage (24 Test Cases)
- **R1: Deltarune Elements & Susie Sprites**
  - `test_tier1_r1_deltaext_sprite_archive_presence_and_format`: Validates availability and PNG headers of source sprites at `/home/wal/work/deltaext`.
  - `test_tier1_r1_header_susie_hero_mascot`: Validates Susie battle idle mascot in `header.svg` with base64 data URI and pixelated scaling.
  - `test_tier1_r1_dialogue_box_structure_and_dimensions`: Validates `dialogue-susie.svg` dimensions (640x130), double borders, and black canvas.
  - `test_tier1_r1_dialogue_box_candid_commentary_content`: Validates retro monospace typography and candid dialogue commentary.
  - `test_tier1_r1_footer_susie_cameo`: Validates Susie plush/relax cameo beside the signature soup quote in `footer.svg`.
  - `test_tier1_r1_themed_rpg_badges`: Validates Deltarune RPG-style badges on project cards.
- **R2: Warm Geometric Cards & Visual Hierarchy**
  - `test_tier1_r2_warm_palette_in_all_cards`: Confirms signature palette (`#FFB627`, `#F0542D`, `#E64980`) in all 7 project cards.
  - `test_tier1_r2_dual_theme_dark_light_palette`: Confirms `#2A2119` dark and `#FFF3E0` light background support.
  - `test_tier1_r2_flagship_cards_visual_prominence`: Confirms flagship cards (`ditto`, `fichegen`) have height >= 84 and prominent badges.
  - `test_tier1_r2_wip_cards_status_indication`: Confirms WIP cards (`gemwallet`, `bitnet`, `agent-base`) display status indicators.
  - `test_tier1_r2_smaller_stuff_cards_compact_dimensions`: Confirms smaller cards (`tether-compass`, `direct-moutamadris`) have height <= 64.
  - `test_tier1_r2_typography_and_geometry_hierarchy`: Confirms card corner radii `rx >= 12` and typography weight hierarchy.
- **R3: Standalone Animated SVG Pipeline & Camo Proxy Safety**
  - `test_tier1_r3_xml_wellformedness_and_namespaces`: Validates well-formed XML across all SVG assets.
  - `test_tier1_r3_explicit_dimensions_and_viewbox`: Validates positive numeric `width`, `height`, and `viewBox`.
  - `test_tier1_r3_camo_proxy_standalone_architecture`: Validates zero `#hash` fragment identifiers and zero external network URLs.
  - `test_tier1_r3_nested_g_container_animation_isolation`: Validates no element with animated class has inline `transform`.
  - `test_tier1_r3_accessibility_prefers_reduced_motion`: Validates `@media (prefers-reduced-motion: reduce)` disables animations with `!important`.
  - `test_tier1_r3_deterministic_asset_pipeline_execution`: Validates `scripts/generate_assets.py` executes cleanly with code 0.
- **R4: README Restructuring & Bio Preservation**
  - `test_tier1_r4_bio_and_personality_retention`: Validates 100% retention of bio details (cats, cat facts, soup clarification, quotes).
  - `test_tier1_r4_all_seven_project_showcases_present`: Validates presence of all 7 project cards in README.
  - `test_tier1_r4_project_repository_urls`: Validates exact official GitHub URLs for all 7 projects.
  - `test_tier1_r4_section_ordering_and_visual_flow`: Validates strict section sequence from header to footer.
  - `test_tier1_r4_contact_pills_and_links`: Validates presence and links of contact pills (`souphater.page`, `walidelonk@gmail.com`, `fsr`).
  - `test_tier1_r4_tech_stack_and_stats_integration`: Validates `stack.svg` and GitHub stats cards in README.

### Tier 2: Boundary & Corner Cases (24 Test Cases)
- **R1 Boundaries**:
  - `test_tier2_r1_base64_data_uri_validity_and_payload`: Decodes embedded base64 strings and asserts valid PNG signature.
  - `test_tier2_r1_sprite_aspect_ratio_consistency`: Asserts SVG `<image>` aspect ratios match native sprite aspect ratios within 5%.
  - `test_tier2_r1_dialogue_box_text_bounds_and_overflow`: Confirms dialogue text coordinates fit strictly within viewBox bounds.
  - `test_tier2_r1_dialogue_box_double_border_geometry`: Confirms non-negative coordinates and positive dimensions on border rects.
  - `test_tier2_r1_pixel_art_rendering_properties`: Enforces `image-rendering: pixelated;` or `crisp-edges` on pixel art.
  - `test_tier2_r1_empty_or_corrupt_sprite_source_handling`: Verifies exception handling when invalid sprite data is supplied.
- **R2 Boundaries**:
  - `test_tier2_r2_zero_and_negative_dimension_absence`: Asserts no SVG visual element has zero or negative dimension.
  - `test_tier2_r2_card_viewbox_coordinate_bounds`: Asserts card viewBoxes originate at `(0, 0)` with width `640` and height in `[60, 100]`.
  - `test_tier2_r2_badge_text_centering_and_anchors`: Verifies status badge text midpoint aligns with badge rect center.
  - `test_tier2_r2_card_contrast_ratio_validation`: Validates WCAG AAA contrast (> 7:1) for text on background in dark and light modes.
  - `test_tier2_r2_extreme_text_length_tolerance`: Verifies card title and badge maintain minimum layout buffer against collisions.
  - `test_tier2_r2_corner_radius_bounds`: Asserts card background corner radius `rx` is between 12 and 22.
- **R3 Boundaries**:
  - `test_tier2_r3_transform_box_strict_absence`: Asserts `transform-box` does not appear anywhere in SVG assets.
  - `test_tier2_r3_inline_transform_collision_strict_isolation`: Strictly disallows inline `transform` on animated classes.
  - `test_tier2_r3_malformed_xml_rejection`: Asserts XML parser catches unclosed or mismatched tags with `ET.ParseError`.
  - `test_tier2_r3_external_network_resource_prohibition`: Rejects any `http://` or `https://` references in SVG markup.
  - `test_tier2_r3_xml_injection_and_escaping_safety`: Asserts text nodes do not contain unescaped XML delimiters.
  - `test_tier2_r3_reduced_motion_override_completeness`: Ensures every `@keyframes` animation has a corresponding override.
- **R4 Boundaries**:
  - `test_tier2_r4_readme_broken_link_detection`: Verifies all local assets referenced in README exist on disk.
  - `test_tier2_r4_url_scheme_validation`: Verifies all README links use strictly `https://` or `mailto:`.
  - `test_tier2_r4_empty_section_header_guard`: Prevents empty or orphaned section headers in README.
  - `test_tier2_r4_html_tag_pairing_and_nesting`: Verifies HTML tags (`<div>`, `<a>`) in README are balanced.
  - `test_tier2_r4_duplicate_image_or_link_guard`: Ensures no project card image is duplicated in README.
  - `test_tier2_r4_alt_text_completeness`: Verifies every `<img>` in README declares a non-empty `alt` attribute.

### Tier 3: Cross-Feature Combinations (6 Test Cases)
- `test_tier3_dark_mode_with_css_keyframe_animations`: Validates dark mode rules do not disable or collide with keyframe animations.
- `test_tier3_reduced_motion_with_susie_bobbing`: Validates reduced-motion disables Susie idle bobbing while preserving static sprite visibility.
- `test_tier3_dialogue_box_dark_light_color_adaptability`: Validates dialogue box contrast in dark and light viewing modes.
- `test_tier3_project_card_badges_with_dark_background`: Validates badge text contrast against card backgrounds.
- `test_tier3_nested_containers_with_static_transforms_and_animated_classes`: Validates two-tier container hierarchy in animated assets.
- `test_tier3_responsive_card_scaling_and_viewbox_aspect_ratios`: Validates README declared image dimensions match SVG viewBox ratios within 1%.

### Tier 4: Real-World Application Scenarios (5 Test Cases)
- `test_tier4_camo_proxy_document_isolation_simulation`: Emulates GitHub Camo proxy sandbox, verifying complete document isolation.
- `test_tier4_full_profile_readme_rendering_simulation`: Simulates complete README profile load and project categorization.
- `test_tier4_asset_pipeline_deterministic_e2e_rebuild`: Runs generator twice and verifies 100% bit-for-bit SHA-256 reproducibility.
- `test_tier4_accessibility_and_screen_reader_audit`: Audits `role="img"`, `aria-label`, and `alt` attributes across profile.
- `test_tier4_dual_theme_visual_integrity_simulation`: Simulates theme switching and validates dark/light rules across all headers and cards.

---

## Requirement Traceability Matrix

| Requirement | PROJECT.md Feature | Tier 1 Tests | Tier 2 Tests | Tier 3 Tests | Tier 4 Tests |
|---|---|---|---|---|---|
| **R1** Deltarune & Susie | #1, #2, #3, #4 | 6 tests | 6 tests | 2 tests | 1 test |
| **R2** Geometric Cards | #5, #6 | 6 tests | 6 tests | 2 tests | 1 test |
| **R3** Standalone SVG Pipeline | #7, #9, #11 | 6 tests | 6 tests | 1 test | 2 tests |
| **R4** README Restructuring | #8, #10 | 6 tests | 6 tests | 1 test | 1 test |
| **Total** | All Features | **24** | **24** | **6** | **5** |

---

## Test Execution

### Running All Tests
```bash
python3 -m unittest discover tests -v
```

### Running E2E Suite Specifically
```bash
python3 -m unittest tests/test_e2e_comprehensive.py -v
```

### Running Core Unit Suite
```bash
python3 -m unittest tests/test_profile_assets.py -v
```

---

## Quality & Exit Criteria
- **Pass Threshold**: 0 failures, 0 errors.
- **Coverage**: 100% of features in `PROJECT.md` Feature Inventory covered across all 4 tiers.
- **Progressive Testability**: Zero false failures during active milestone implementation.
