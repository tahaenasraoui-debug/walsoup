#!/usr/bin/env python3
"""
generate_assets.py - Generates standalone animated SVG assets for walsoup GitHub profile
"""

import os
import xml.etree.ElementTree as ET

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
os.makedirs(ASSETS_DIR, exist_ok=True)

# Common SVG elements and palettes
# Primary Yellow: #FFB627
# Primary Orange: #F0542D
# Primary Pink:   #E64980
# Amber:          #E07B00
# Green:          #2DA44E
# Dark bg:        #2A2119
# Light bg:       #FFF3E0
# Text Dark:      #fff4e6
# Text Light:     #24190f
# Sub Dark:       #b8a898
# Sub Light:      #7a6a5c

def create_pill_website():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="242" height="44" viewBox="0 0 242 44" role="img" aria-label="souphater.page">
  <style>
    .w { font: 600 20px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m { mix-blend-mode: multiply; }
    @keyframes pill-float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-1.5px); }
    }
    .icon {
      animation: pill-float 3s ease-in-out infinite alternate;
    }
    @media (prefers-reduced-motion: reduce) {
      .icon { animation: none !important; }
    }
  </style>
  <g style="isolation:isolate">
    <circle class="m icon" cx="22" cy="22" r="22" fill="#FFB627"/>
    <rect class="m" x="16" y="0" width="226" height="44" rx="22" fill="#F0542D"/>
  </g>
  <text class="w" x="60" y="29">souphater.page</text>
</svg>'''

def create_pill_email():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="310" height="44" viewBox="0 0 310 44" role="img" aria-label="walidelonk@gmail.com">
  <style>
    .w { font: 600 20px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m { mix-blend-mode: multiply; }
    @keyframes pill-arrow {
      0%, 100% { transform: scale(1.294) translateX(0); }
      50% { transform: scale(1.294) translateX(1px); }
    }
    .icon {
      animation: pill-arrow 2.8s ease-in-out infinite alternate;
    }
    @media (prefers-reduced-motion: reduce) {
      .icon { animation: none !important; }
    }
  </style>
  <g style="isolation:isolate">
    <path class="m icon" transform="scale(1.294)" d="M5 6 L30 17 L5 28 Z" fill="#FFB627" stroke="#FFB627" stroke-width="6" stroke-linejoin="round"/>
    <rect class="m" x="16" y="0" width="294" height="44" rx="22" fill="#E64980"/>
  </g>
  <text class="w" x="60" y="29">walidelonk@gmail.com</text>
</svg>'''

def create_pill_fsr():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="264" height="44" viewBox="0 0 264 44" role="img" aria-label="cs student · fsr">
  <style>
    .w { font: 600 20px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m { mix-blend-mode: multiply; }
    @keyframes pill-diamond {
      0%, 100% { transform: rotate(45deg) scale(1); }
      50% { transform: rotate(45deg) scale(1.06); }
    }
    .icon {
      transform-box: fill-box;
      transform-origin: center;
      animation: pill-diamond 3.2s ease-in-out infinite alternate;
    }
    @media (prefers-reduced-motion: reduce) {
      .icon { animation: none !important; }
    }
  </style>
  <g style="isolation:isolate">
    <rect class="m icon" x="6.5" y="6.5" width="31" height="31" rx="6.5" transform="rotate(45 22 22)" fill="#FFB627"/>
    <rect class="m" x="16" y="0" width="248" height="44" rx="22" fill="#E07B00"/>
  </g>
  <text class="w" x="60" y="29">cs student · fsr</text>
</svg>'''

def create_section_header(title, c1, c2, c3):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="56" viewBox="0 0 640 56" role="img" aria-label="{title}">
  <style>
    .t {{ font: 700 30px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }}
    .m {{ mix-blend-mode: multiply; }}
    @media (prefers-color-scheme: dark) {{
      .t {{ fill: #fff4e6; }}
    }}
    @keyframes float-c1 {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-2.5px); }}
    }}
    @keyframes float-c2 {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(2px); }}
    }}
    @keyframes float-c3 {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-1.5px); }}
    }}
    .shape-1 {{ animation: float-c1 3.6s ease-in-out infinite alternate; }}
    .shape-2 {{ animation: float-c2 3.6s ease-in-out infinite alternate -1.2s; }}
    .shape-3 {{ animation: float-c3 3.6s ease-in-out infinite alternate -2.4s; }}
    @media (prefers-reduced-motion: reduce) {{
      .shape-1, .shape-2, .shape-3 {{ animation: none !important; }}
    }}
  </style>
  <g style="isolation:isolate">
    <circle class="m shape-1" cx="20" cy="28" r="14" fill="{c1}"/>
    <rect class="m shape-2" x="24" y="14" width="28" height="28" rx="9" fill="{c2}"/>
    <path class="m shape-3" d="M46 42 A14 14 0 0 1 74 42 Z" fill="{c3}"/>
  </g>
  <text class="t" x="92" y="39">{title}</text>
</svg>'''

def create_card_ditto():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="84" viewBox="0 0 640 84" role="img" aria-label="ditto card">
  <style>
    .bg { fill: #FFF3E0; }
    .t  { font: 700 26px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }
    .w  { font: 600 17px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m  { mix-blend-mode: multiply; }
    @media (prefers-color-scheme: dark) {
      .bg { fill: #2A2119; }
      .t  { fill: #fff4e6; }
    }
    @keyframes eq-1 { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3.5px); } }
    @keyframes eq-2 { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(2.5px); } }
    @keyframes eq-3 { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-2px); } }
    .bar-1 { animation: eq-1 2.2s ease-in-out infinite; }
    .bar-2 { animation: eq-2 1.8s ease-in-out infinite; }
    .bar-3 { animation: eq-3 2.5s ease-in-out infinite; }
    @keyframes badge-glow {
      0%, 100% { opacity: 0.94; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.025); }
    }
    .badge-pill {
      transform-box: fill-box;
      transform-origin: center;
      animation: badge-glow 3s ease-in-out infinite;
    }
    @media (prefers-reduced-motion: reduce) {
      .bar-1, .bar-2, .bar-3, .badge-pill { animation: none !important; }
    }
  </style>
  <rect class="bg" width="640" height="84" rx="18"/>
  <g transform="translate(22 14.0) scale(0.875)" style="isolation:isolate">
    <rect class="m bar-1" x="2" y="18" width="22" height="28" rx="11" fill="#FFB627"/>
    <rect class="m bar-2" x="18" y="6" width="22" height="52" rx="11" fill="#F0542D"/>
    <rect class="m bar-3" x="34" y="14" width="22" height="36" rx="11" fill="#E64980"/>
  </g>
  <text class="t" x="96" y="51.1">ditto</text>
  <g class="badge-pill">
    <rect x="511" y="26.0" width="107" height="32" rx="16.0" fill="#2DA44E"/>
    <text class="w" x="564.5" y="48.0" text-anchor="middle">finished</text>
  </g>
</svg>'''

def create_card_gemwallet():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="84" viewBox="0 0 640 84" role="img" aria-label="gemwallet card">
  <style>
    .bg { fill: #FFF3E0; }
    .t  { font: 700 26px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }
    .w  { font: 600 17px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m  { mix-blend-mode: multiply; }
    @media (prefers-color-scheme: dark) {
      .bg { fill: #2A2119; }
      .t  { fill: #fff4e6; }
    }
    @keyframes gw-float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-2px); }
    }
    @keyframes gw-gem {
      0%, 100% { transform: rotate(45deg); }
      50% { transform: rotate(48deg) translateY(-1.5px); }
    }
    .gw-1 { animation: gw-float 3.4s ease-in-out infinite; }
    .gw-2 {
      transform-box: fill-box;
      transform-origin: center;
      animation: gw-gem 4s ease-in-out infinite;
    }
    .gw-3 { animation: gw-float 3.4s ease-in-out infinite 0.6s; }
    @keyframes wip-pulse {
      0%, 100% { opacity: 0.90; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.03); }
    }
    .badge-pill {
      transform-box: fill-box;
      transform-origin: center;
      animation: wip-pulse 2.2s ease-in-out infinite;
    }
    @media (prefers-reduced-motion: reduce) {
      .gw-1, .gw-2, .gw-3, .badge-pill { animation: none !important; }
    }
  </style>
  <rect class="bg" width="640" height="84" rx="18"/>
  <g transform="translate(22 14.0) scale(0.875)" style="isolation:isolate">
    <circle class="m gw-1" cx="26" cy="32" r="22" fill="#FFB627"/>
    <rect class="m gw-2" x="22" y="12" width="36" height="36" rx="10" transform="rotate(45 40 30)" fill="#F0542D"/>
    <path class="m gw-3" d="M10 54 A22 22 0 0 1 54 54 Z" fill="#E64980"/>
  </g>
  <text class="t" x="96" y="51.1">gemwallet</text>
  <g class="badge-pill">
    <rect x="482" y="26.0" width="136" height="32" rx="16.0" fill="#E07B00"/>
    <text class="w" x="550.0" y="48.0" text-anchor="middle">mostly done</text>
  </g>
</svg>'''

def create_card_fichegen():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="84" viewBox="0 0 640 84" role="img" aria-label="fichegen card">
  <style>
    .bg { fill: #FFF3E0; }
    .t  { font: 700 26px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }
    .w  { font: 600 17px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m  { mix-blend-mode: multiply; }
    @media (prefers-color-scheme: dark) {
      .bg { fill: #2A2119; }
      .t  { fill: #fff4e6; }
    }
    @keyframes sheet-sway-1 { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-2px); } }
    @keyframes sheet-sway-2 { 0%, 100% { transform: rotate(8deg); } 50% { transform: rotate(10deg) translateY(-1px); } }
    @keyframes sheet-sway-3 { 0%, 100% { transform: rotate(-6deg); } 50% { transform: rotate(-4deg) translateY(1px); } }
    .sheet-1 { animation: sheet-sway-1 3.5s ease-in-out infinite; }
    .sheet-2 { transform-box: fill-box; transform-origin: center; animation: sheet-sway-2 3.5s ease-in-out infinite 0.3s; }
    .sheet-3 { transform-box: fill-box; transform-origin: center; animation: sheet-sway-3 3.5s ease-in-out infinite 0.6s; }
    @keyframes badge-glow {
      0%, 100% { opacity: 0.94; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.025); }
    }
    .badge-pill {
      transform-box: fill-box;
      transform-origin: center;
      animation: badge-glow 3s ease-in-out infinite;
    }
    @media (prefers-reduced-motion: reduce) {
      .sheet-1, .sheet-2, .sheet-3, .badge-pill { animation: none !important; }
    }
  </style>
  <rect class="bg" width="640" height="84" rx="18"/>
  <g transform="translate(22 14.0) scale(0.875)" style="isolation:isolate">
    <rect class="m sheet-1" x="4" y="8" width="36" height="44" rx="8" fill="#FFB627"/>
    <rect class="m sheet-2" x="16" y="12" width="36" height="44" rx="8" transform="rotate(8 34 34)" fill="#F0542D"/>
    <rect class="m sheet-3" x="26" y="6" width="30" height="40" rx="8" transform="rotate(-6 41 26)" fill="#E64980"/>
  </g>
  <text class="t" x="96" y="51.1">fichegen (profstudio)</text>
  <g class="badge-pill">
    <rect x="442" y="26.0" width="176" height="32" rx="16.0" fill="#E64980"/>
    <text class="w" x="530.0" y="48.0" text-anchor="middle">macos · windows</text>
  </g>
</svg>'''

def create_card_bitnet():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="64" viewBox="0 0 640 64" role="img" aria-label="bluenet bitnet card">
  <style>
    .bg { fill: #FFF3E0; }
    .t  { font: 700 22px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }
    .w  { font: 600 17px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m  { mix-blend-mode: multiply; }
    @media (prefers-color-scheme: dark) {
      .bg { fill: #2A2119; }
      .t  { fill: #fff4e6; }
    }
    @keyframes mesh-ping {
      0%, 100% { transform: scale(1); opacity: 0.85; }
      50% { transform: scale(1.12); opacity: 1; }
    }
    .node-1 { transform-box: fill-box; transform-origin: center; animation: mesh-ping 2.1s ease-in-out infinite; }
    .node-2 { transform-box: fill-box; transform-origin: center; animation: mesh-ping 2.1s ease-in-out infinite 0.7s; }
    .node-3 { transform-box: fill-box; transform-origin: center; animation: mesh-ping 2.1s ease-in-out infinite 1.4s; }
    @keyframes wip-pulse {
      0%, 100% { opacity: 0.90; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.03); }
    }
    .badge-pill {
      transform-box: fill-box;
      transform-origin: center;
      animation: wip-pulse 2.2s ease-in-out infinite;
    }
    @media (prefers-reduced-motion: reduce) {
      .node-1, .node-2, .node-3, .badge-pill { animation: none !important; }
    }
  </style>
  <rect class="bg" width="640" height="64" rx="16"/>
  <g transform="translate(20 10.88) scale(0.66)" style="isolation:isolate">
    <circle class="m node-1" cx="14" cy="32" r="16" fill="#FFB627"/>
    <circle class="m node-2" cx="32" cy="32" r="16" fill="#F0542D"/>
    <circle class="m node-3" cx="50" cy="32" r="16" fill="#E64980"/>
  </g>
  <text class="t" x="78" y="39.7">bluenet (bitnet)</text>
  <g class="badge-pill">
    <rect x="563" y="17.0" width="57" height="30" rx="15.0" fill="#E07B00"/>
    <text class="w" x="591.5" y="38.0" text-anchor="middle">wip</text>
  </g>
</svg>'''

def create_card_agent_base():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="64" viewBox="0 0 640 64" role="img" aria-label="agent base card">
  <style>
    .bg { fill: #FFF3E0; }
    .t  { font: 700 22px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }
    .w  { font: 600 17px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m  { mix-blend-mode: multiply; }
    @media (prefers-color-scheme: dark) {
      .bg { fill: #2A2119; }
      .t  { fill: #fff4e6; }
    }
    @keyframes ag-pulse {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-2.5px); }
    }
    .ag-head { animation: ag-pulse 2.4s ease-in-out infinite; }
    .ag-base { animation: ag-pulse 3s ease-in-out infinite 0.5s; }
    @keyframes wip-pulse {
      0%, 100% { opacity: 0.90; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.03); }
    }
    .badge-pill {
      transform-box: fill-box;
      transform-origin: center;
      animation: wip-pulse 2.2s ease-in-out infinite;
    }
    @media (prefers-reduced-motion: reduce) {
      .ag-head, .ag-base, .badge-pill { animation: none !important; }
    }
  </style>
  <rect class="bg" width="640" height="64" rx="16"/>
  <g transform="translate(20 10.88) scale(0.66)" style="isolation:isolate">
    <circle class="m ag-base" cx="24" cy="34" r="22" fill="#FFB627"/>
    <path class="m ag-body" d="M24 56 V16 A40 40 0 0 1 64 56 Z" fill="#F0542D"/>
    <circle class="m ag-head" cx="48" cy="20" r="12" fill="#E64980"/>
  </g>
  <text class="t" x="78" y="39.7">agent base</text>
  <g class="badge-pill">
    <rect x="563" y="17.0" width="57" height="30" rx="15.0" fill="#E07B00"/>
    <text class="w" x="591.5" y="38.0" text-anchor="middle">wip</text>
  </g>
</svg>'''

def create_card_tether_compass():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="64" viewBox="0 0 640 64" role="img" aria-label="tether compass card">
  <style>
    .bg { fill: #FFF3E0; }
    .t  { font: 700 22px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }
    .w  { font: 600 17px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m  { mix-blend-mode: multiply; }
    @media (prefers-color-scheme: dark) {
      .bg { fill: #2A2119; }
      .t  { fill: #fff4e6; }
    }
    @keyframes cp-sway {
      0%, 100% { transform: rotate(-5deg); }
      50% { transform: rotate(5deg); }
    }
    @keyframes cp-beacon {
      0%, 100% { transform: scale(1); opacity: 0.9; }
      50% { transform: scale(1.15); opacity: 1; }
    }
    .cp-arc1, .cp-arc2 {
      transform-box: fill-box;
      transform-origin: center;
      animation: cp-sway 4s ease-in-out infinite alternate;
    }
    .cp-dot {
      transform-box: fill-box;
      transform-origin: center;
      animation: cp-beacon 2.2s ease-in-out infinite;
    }
    @keyframes badge-glow {
      0%, 100% { opacity: 0.94; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.025); }
    }
    .badge-pill {
      transform-box: fill-box;
      transform-origin: center;
      animation: badge-glow 3s ease-in-out infinite;
    }
    @media (prefers-reduced-motion: reduce) {
      .cp-arc1, .cp-arc2, .cp-dot, .badge-pill { animation: none !important; }
    }
  </style>
  <rect class="bg" width="640" height="64" rx="16"/>
  <g transform="translate(20 10.88) scale(0.66)" style="isolation:isolate">
    <path class="m cp-arc1" d="M30 10 A22 22 0 0 0 30 54 Z" fill="#FFB627"/>
    <path class="m cp-arc2" d="M22 10 A22 22 0 0 1 22 54 Z" transform="translate(14 0)" fill="#F0542D"/>
    <circle class="m cp-dot" cx="32" cy="32" r="9" fill="#E64980"/>
  </g>
  <text class="t" x="78" y="39.7">tether compass</text>
  <g class="badge-pill">
    <rect x="523" y="17.0" width="97" height="30" rx="15.0" fill="#2DA44E"/>
    <text class="w" x="571.5" y="38.0" text-anchor="middle">shipped</text>
  </g>
</svg>'''

def create_card_direct_moutamadris():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="64" viewBox="0 0 640 64" role="img" aria-label="direct moutamadris card">
  <style>
    .bg { fill: #FFF3E0; }
    .t  { font: 700 22px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }
    .w  { font: 600 17px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m  { mix-blend-mode: multiply; }
    @media (prefers-color-scheme: dark) {
      .bg { fill: #2A2119; }
      .t  { fill: #fff4e6; }
    }
    @keyframes dm-float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-2px); }
    }
    .dm-1 { animation: dm-float 3.4s ease-in-out infinite; }
    .dm-2 { animation: dm-float 3.4s ease-in-out infinite 0.6s; }
    .dm-3 { animation: dm-float 3.4s ease-in-out infinite 1.2s; }
    @keyframes badge-glow {
      0%, 100% { opacity: 0.94; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.025); }
    }
    .badge-pill {
      transform-box: fill-box;
      transform-origin: center;
      animation: badge-glow 3s ease-in-out infinite;
    }
    @media (prefers-reduced-motion: reduce) {
      .dm-1, .dm-2, .dm-3, .badge-pill { animation: none !important; }
    }
  </style>
  <rect class="bg" width="640" height="64" rx="16"/>
  <g transform="translate(20 10.88) scale(0.66)" style="isolation:isolate">
    <rect class="m dm-1" x="4" y="10" width="40" height="40" rx="12" fill="#FFB627"/>
    <circle class="m dm-2" cx="42" cy="40" r="18" fill="#F0542D"/>
    <circle class="m dm-3" cx="50" cy="18" r="10" fill="#E64980"/>
  </g>
  <text class="t" x="78" y="39.7">direct moutamadris</text>
  <g class="badge-pill">
    <rect x="523" y="17.0" width="97" height="30" rx="15.0" fill="#2DA44E"/>
    <text class="w" x="571.5" y="38.0" text-anchor="middle">shipped</text>
  </g>
</svg>'''

def create_stack():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="344" viewBox="0 0 640 344" role="img" aria-label="technologies and tools">
  <style>
    .c { font: 600 19px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; }
    .l { font: 600 18px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #7a6a5c; }
    .m { mix-blend-mode: multiply; }
    @media (prefers-color-scheme: dark) {
      .c { fill: #fff4e6; }
      .l { fill: #b8a898; }
      .pill-bg { fill-opacity: .45; }
    }
    @keyframes icon-bob {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-1.5px); }
    }
    .sec-icon-1 { animation: icon-bob 3.6s ease-in-out infinite; }
    .sec-icon-2 { animation: icon-bob 3.6s ease-in-out infinite 0.8s; }
    .sec-icon-3 { animation: icon-bob 3.6s ease-in-out infinite 1.6s; }
    @media (prefers-reduced-motion: reduce) {
      .sec-icon-1, .sec-icon-2, .sec-icon-3 { animation: none !important; }
    }
  </style>

  <!-- Languages -->
  <g class="sec-icon-1" style="isolation:isolate">
    <circle class="m" cx="14" cy="19" r="12" fill="#FFB627"/>
    <circle class="m" cx="28" cy="19" r="12" fill="#F0542D"/>
  </g>
  <text class="l" x="48" y="25">languages</text>
  <g style="isolation:isolate">
    <rect class="m pill-bg" x="0" y="44" width="104" height="40" rx="20" fill="#FFB627" fill-opacity=".6"/>
    <rect class="m pill-bg" x="94" y="44" width="104" height="40" rx="20" fill="#F0542D" fill-opacity=".6"/>
    <rect class="m pill-bg" x="188" y="44" width="148" height="40" rx="20" fill="#E64980" fill-opacity=".6"/>
    <rect class="m pill-bg" x="326" y="44" width="148" height="40" rx="20" fill="#FFB627" fill-opacity=".6"/>
    <rect class="m pill-bg" x="464" y="44" width="71" height="40" rx="20" fill="#F0542D" fill-opacity=".6"/>
    <rect class="m pill-bg" x="525" y="44" width="82" height="40" rx="20" fill="#E64980" fill-opacity=".6"/>
  </g>
  <text class="c" x="52.0" y="70.5" text-anchor="middle">kotlin</text>
  <text class="c" x="146.0" y="70.5" text-anchor="middle">python</text>
  <text class="c" x="262.0" y="70.5" text-anchor="middle">typescript</text>
  <text class="c" x="400.0" y="70.5" text-anchor="middle">javascript</text>
  <text class="c" x="499.5" y="70.5" text-anchor="middle">c++</text>
  <text class="c" x="566.0" y="70.5" text-anchor="middle">rust</text>

  <!-- Environments -->
  <g class="sec-icon-2" style="isolation:isolate">
    <rect class="m" x="2" y="110" width="22" height="22" rx="7" fill="#FFB627"/>
    <rect class="m" x="13" y="114" width="22" height="22" rx="7" fill="#F0542D"/>
  </g>
  <text class="l" x="48" y="129">environments</text>
  <g style="isolation:isolate">
    <rect class="m pill-bg" x="0" y="148" width="115" height="40" rx="20" fill="#F0542D" fill-opacity=".6"/>
    <rect class="m pill-bg" x="105" y="148" width="115" height="40" rx="20" fill="#E64980" fill-opacity=".6"/>
    <rect class="m pill-bg" x="210" y="148" width="93" height="40" rx="20" fill="#FFB627" fill-opacity=".6"/>
    <rect class="m pill-bg" x="293" y="148" width="93" height="40" rx="20" fill="#F0542D" fill-opacity=".6"/>
    <rect class="m pill-bg" x="376" y="148" width="115" height="40" rx="20" fill="#E64980" fill-opacity=".6"/>
  </g>
  <text class="c" x="57.5" y="174.5" text-anchor="middle">android</text>
  <text class="c" x="162.5" y="174.5" text-anchor="middle">windows</text>
  <text class="c" x="256.5" y="174.5" text-anchor="middle">macos</text>
  <text class="c" x="339.5" y="174.5" text-anchor="middle">linux</text>
  <text class="c" x="433.5" y="174.5" text-anchor="middle">node.js</text>

  <!-- Focus -->
  <g class="sec-icon-3" style="isolation:isolate">
    <circle class="m" cx="20" cy="227" r="14" fill="#FFB627"/>
    <circle class="m" cx="20" cy="227" r="7" fill="#E64980"/>
  </g>
  <text class="l" x="48" y="233">focus</text>
  <g style="isolation:isolate">
    <rect class="m pill-bg" x="0" y="252" width="225" height="40" rx="20" fill="#E64980" fill-opacity=".6"/>
    <rect class="m pill-bg" x="215" y="252" width="137" height="40" rx="20" fill="#FFB627" fill-opacity=".6"/>
    <rect class="m pill-bg" x="342" y="252" width="203" height="40" rx="20" fill="#F0542D" fill-opacity=".6"/>
    <rect class="m pill-bg" x="0" y="300" width="137" height="40" rx="20" fill="#E64980" fill-opacity=".6"/>
  </g>
  <text class="c" x="112.5" y="278.5" text-anchor="middle">offline protocols</text>
  <text class="c" x="283.5" y="278.5" text-anchor="middle">audio dsp</text>
  <text class="c" x="443.5" y="278.5" text-anchor="middle">agentic tooling</text>
  <text class="c" x="68.5" y="326.5" text-anchor="middle">mobile ux</text>
</svg>'''

def create_footer():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="70" viewBox="0 0 640 70" role="img" aria-label="soup is just the best driving force :3">
  <style>
    .t { font: 700 20px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; }
    .m { mix-blend-mode: multiply; }
    @media (prefers-color-scheme: dark) {
      .t { fill: #fff4e6; }
    }
    @keyframes float-l { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-2.5px); } }
    @keyframes float-r { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(2.5px); } }
    .mark-left  { animation: float-l 4s ease-in-out infinite; }
    .mark-right { animation: float-r 4s ease-in-out infinite; }
    @media (prefers-reduced-motion: reduce) {
      .mark-left, .mark-right { animation: none !important; }
    }
  </style>
  <g class="mark-left" transform="translate(14 12.6) scale(0.8)" style="isolation:isolate">
    <circle class="m" cx="20" cy="28" r="14" fill="#FFB627"/>
    <rect class="m" x="24" y="14" width="28" height="28" rx="9" fill="#F0542D"/>
    <path class="m" d="M46 42 A14 14 0 0 1 74 42 Z" fill="#E64980"/>
  </g>
  <g class="mark-right" transform="translate(571 12.6) scale(0.8)" style="isolation:isolate">
    <circle class="m" cx="20" cy="28" r="14" fill="#E64980"/>
    <rect class="m" x="24" y="14" width="28" height="28" rx="9" fill="#FFB627"/>
    <path class="m" d="M46 42 A14 14 0 0 1 74 42 Z" fill="#F0542D"/>
  </g>
  <text class="t" x="320" y="42" text-anchor="middle">soup is just the best driving force :3</text>
</svg>'''

def create_header():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="200" viewBox="0 0 880 200" role="img" aria-label="Walid Elonk">
  <style>
    .name { font: 700 52px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -1px; }
    .sub  { font: 400 15px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #7a6a5c; }
    .m    { mix-blend-mode: multiply; }
    @media (prefers-color-scheme: dark) {
      .name { fill: #fff4e6; }
      .sub  { fill: #b8a898; }
    }
    @keyframes drift-c1 { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
    @keyframes drift-c2 { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(3px); } }
    @keyframes drift-c3 { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-2px); } }
    @keyframes cluster-sway { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3.5px); } }
    .mark-c1 { animation: drift-c1 4.5s ease-in-out infinite; }
    .mark-c2 { animation: drift-c2 4.5s ease-in-out infinite; }
    .mark-c3 { animation: drift-c3 4.5s ease-in-out infinite 0.7s; }
    .cluster-r { animation: cluster-sway 5s ease-in-out infinite alternate; }
    @media (prefers-reduced-motion: reduce) {
      .mark-c1, .mark-c2, .mark-c3, .cluster-r { animation: none !important; }
    }
  </style>

  <!-- mark: three overlapping circles, colors blend where they cross -->
  <g style="isolation:isolate">
    <circle class="m mark-c1" cx="90"  cy="88"  r="40" fill="#FFB627"/>
    <circle class="m mark-c2" cx="128" cy="88"  r="40" fill="#F0542D"/>
    <circle class="m mark-c3" cx="109" cy="122" r="40" fill="#E64980"/>
  </g>

  <!-- name -->
  <text class="name" x="196" y="104">Walid Elonk</text>
  <text class="sub"  x="198" y="138">@walsoup</text>

  <!-- shape cluster, same blend -->
  <g class="cluster-r" style="isolation:isolate">
    <circle class="m" cx="660" cy="100" r="44" fill="#FFB627"/>
    <rect   class="m" x="680" y="62" width="76" height="76" rx="22" fill="#F0542D"/>
    <path   class="m" d="M726 140 A44 44 0 0 1 814 140 Z" fill="#E64980"/>
  </g>
</svg>'''

files = {
    "pill-website.svg": create_pill_website(),
    "pill-email.svg": create_pill_email(),
    "pill-fsr.svg": create_pill_fsr(),
    "h-about.svg": create_section_header("about me", "#FFB627", "#F0542D", "#E64980"),
    "h-building.svg": create_section_header("what i&#8217;m building", "#F0542D", "#E64980", "#FFB627"),
    "h-working-on.svg": create_section_header("what i&#8217;m working on", "#F0542D", "#FFB627", "#E64980"),
    "h-smaller.svg": create_section_header("smaller stuff", "#E64980", "#FFB627", "#F0542D"),
    "h-stack.svg": create_section_header("what i write in", "#FFB627", "#E64980", "#F0542D"),
    "card-ditto.svg": create_card_ditto(),
    "card-gemwallet.svg": create_card_gemwallet(),
    "card-fichegen.svg": create_card_fichegen(),
    "card-bitnet.svg": create_card_bitnet(),
    "card-bluenet.svg": create_card_bitnet(),
    "card-agent-base.svg": create_card_agent_base(),
    "card-tether-compass.svg": create_card_tether_compass(),
    "card-direct-moutamadris.svg": create_card_direct_moutamadris(),
    "stack.svg": create_stack(),
    "footer.svg": create_footer(),
    "header.svg": create_header()
}

if __name__ == "__main__":
    for fname, content in files.items():
        fpath = os.path.join(ASSETS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        # Validate XML
        try:
            ET.fromstring(content)
            print(f"[OK] {fname}")
        except Exception as e:
            print(f"[FAIL] {fname}: {e}")
            raise
    print(f"\nAll {len(files)} SVG assets generated and validated successfully!")
