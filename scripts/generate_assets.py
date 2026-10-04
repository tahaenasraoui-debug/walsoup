#!/usr/bin/env python3
"""
generate_assets.py - Generates standalone animated SVG assets for walsoup GitHub profile
"""

import os
import re
import base64
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

DELTAEXT_DIR = "/home/wal/work/deltaext/DELTARUNE Organized Sprite Archive"

SPRITES = {
    "susieb_idle_0": (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADYAAAAtCAYAAADlVJiFAAACo0lEQVRoQ+2WMY4UMRRE"
        "5xZLtpyDgJhsE0RKTs4JSDYkIUNCHIGYjAsQcgZugEiWrj+/rPLf37anh2E8Ykp62mnbbdeb1rZmd80116zn6c1DxUVH"
        "RO5v3lTonK++kCQyGa9vP16Q4KCUUuRUcCrZDVKRVPLs+Qti5OLF4j0mNLNUKRjGI5jHS0SvfcdJEgT4xtOxiEkEsTK+"
        "D/6SMyWRyEpzPKJfhI0tMm9ffTbw2c7YGG6wRjteKsLio/AeSh0qpoWN9x++Pjz/+S3F17TjpTK0OPn17kchziVS3fNt"
        "UUsi4ve0s5TJhAgLq0wkSi27Dp1ti7LiLeSAGF4mk4n0xAD3MzqxYiNPCGv4beEz8T3q+OGZwBpYz/Iq8+nJ9/IZc7i2"
        "/RvpCmUiEeyz386yvw5S8ZpjHOcbD6VZXOVUStfsj6yTipCejIK9CL8IYAcLUUjHo1gpLmDNo/kkVSGQlR7h5d2LSsik"
        "dO+lwJoU5yjGJ6NAgk+NUly/7D8UK4JimUBGlOIe2MyyHK5Sv788q/6SUlQ+86lQinCdn3BQUgkFQiqFe5w6LJEQ5UgU"
        "4xMra47MkJBIteOlWLIqKnOta9/p6FjpKLRJCvGilAI9kXJ9grD4mtDYoV5UpXpih74ctmS7EOOloxglKhHnlE+LMRGR"
        "OixeNIpEVp/eiXOUlJK97imRjflOE8ULkrVXO1AxrptPzMuugcKA/2dFwHn0BZw1WqSBCinZ2n/xVuxnKRC/+YwoxKeH"
        "Of7s4u9GYveeNUuBnlwUoxzmohjGppPTJxGJYhhTKYAxSs0hhrgAaAmSKDWvmEYElExGwZp5pbKIHGhJlXXTh0UDKpQy"
        "bbKyo0ydrDDQZPNg6mSFldE10yUrGhlZN2W8HH+9K1XpkTX/X3a7PyZFUKoLoi3pAAAAAElFTkSuQmCC"
    ),
    "susieb_idle_1": (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADYAAAAtCAYAAADlVJiFAAACo0lEQVRoQ+2WMY4TQRRE"
        "fYslg3MQEJNtgkjJyTkBCSEJ2UqIIxCTcQFCzsANEMnS9f1rVP39p7s9lnFbuKQne3p6euq517Pe3XLLLet5dvdYcdUR"
        "kQ93byv0nM++kiQyGdclOCilzC9Yir15+pCWHwHXzilZymSFt3D1YvEaEyLTREryTzIWj1CiOp4qQYDfFx2LUCrOs7F9"
        "8EoulKxcIXuYHDwkChzHq40VmXevvxh4b/fYGC6wRjteLqLlR+A1lDpWTAsbHz99e3zx63uKz2nHS2VocfL7/c+FeC6R"
        "6t7fJrUkIn5NO6VMJkRYWGUiUaqsOnRvm5QVbyE3WE9HivTEAOWMTqzYyA5hDj8tvCe+Rh0pkElkYC7Lq8znJz+W9ziH"
        "Y1u7ka5QJhLBOvvlLPvjIBSPOabjeI/SLK5yKqVz9resk4qQnoyCtQg/CGA3FjIpoI/wg+Jh3sH5JFUhkJUe4dX9y0rI"
        "pHRtLxaFiIpxZxRIcNcotfyfG4wVQbFMICNKcQ0sZik35y6BP1+fWyG+EpVmae4KpQjn+R2OSiqhQEilcI1ThyUSohyJ"
        "YtyxZc6JGRISqXa8FEtWReVc69hXOjlWOgptkkK8KKVAT2Q5PkNYfE1o7KZeVKV6Ysc+HLZkuxDjpaMYJSoR55y7xZiI"
        "87V4SMNU7SmauR4yJ+ZMm8XlTO3oGVkF3WOBfPclzZzcAzp3cId7msNgdg2C"
        "UqeSzarwHbhHs+Z5SEqdSpTPwm8knoeJpWc3o9KJ0LeM56G48FZx2Sr6lngeCuWLn8a9"
        "2TwPg6LVEeUr6HvN10dSSP0G5t3zcQqnjKh0KvA9zfNSCqdVKh2QzYDcdV5I4ZKMy7UD"
        "qh3yVZJwWUYz11GiOXab9/+07jN81u4M2Gn2j84KXHaAc6XL8J4YDsoyoxxE3wfcxbeY"
        "Dksq0VzzSOBmT9vcD4s6qr0It/92WCiY4fq33XFxBbc3MtxbvZCt4PYq2t07F8IKbq+i"
        "3b1zIazg9ioGu+cAv7NWcHsjk73rozzU8w71Tj2P8ubrAyX84vsAZzWbsegBl/P8AJ3A"
        "PmTcWbuaqYC/D9y8qA1DHa73OX9+/wDi9p805eESMQAAAABJRU5ErkJggg=="
    ),
    "susieb_idle_2": (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADYAAAAtCAYAAADlVJiFAAACpUlEQVRoQ+2WPW4UQRSE"
        "9xYmw+cgICYjQU7JyTkBiUMSMiTEERw74wKEnIEbIBLT1ftqqH77+mdmtWyv2JI+eWa6t7u+bXvk3TXXXFPP7c1TwUVH"
        "RO5v3hXomM2+kAQyEW+ff74gwUEpzyI4pWQqhVOIiq9hPsFUJiq6hbnkNoj5z8wlxFRK6jMPxvXX9yKk9D6Cb8UDsb9y"
        "+EnOlEBM8S8VP45nnJOfJZn3d18zuM57bAwXqNGOlVNQlKcyCsUotVZMC2c+fnp8evnzW4jNqccK1dDi5NeHHwt+LJBq"
        "75+SJ7UkPPaZdlKZSIiwsMp4vFRadWjvPCkq3kI2qKcjRXpigHKZTnKxkRPCHH5buCa2RhwrEYl4MI/lVebLs+/LNcZw"
        "n9dtpCsUiXiwzn65nP09Nk5oaZXQF4a+6VCaxVVOpXTOfssyoQjpyShYi/CLANiYInrt34KR2FLczTsYD1IUAlHpEd68"
        "flUIZSldOxVQwQjK8mQUSPDUKLV8OYPJRVAsEojwUlwDi+WkzVXq98OL4ifRU+Q1T4VShPNsh1UJJRQIqRQ+Y5RhiQAv"
        "R7wYT2yZc2SGhESqHSvFkkVRGWvd20pHJ5f2QpukECtKKdATWe5PEBavCY1takVVqie29uWwJduFGCvtxShRiBinPC0m"
        "i4jUulhRL+Kpnt6Jc5SUEr3uKRE9s5UmihUktVc7UDHOm0/MytZAYcC/s0XAOPgCzhot0kCFlGjuv3gr9pMK+G8+wgvx"
        "9DDGf7sApEj+7FmTCvTkvBjlMObF8Gw6OT0JjxfDM5UCeEapOcQQEwAtQeKl5hXTiIASySiYM69UFJEDLall3vRhUYcK"
        "hUybqOwoUycqDDTROJg6UWFldM50iYp6RuZNGSvH/96VovTInP8vu90fCsVQN7Zp82kAAAAASUVORK5CYII="
    ),
    "susieb_idle_3": (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADYAAAAtCAYAAADlVJiFAAACrUlEQVRoQ+2WPY4TQRSE"
        "fYslY89BQLzZJmhTcnJOQEJIstlKiCMQk3EBQs7ADRDJ0tV+Nap+fv0zYxm3hUv6NJ6Znu763N7R7q655pp6bm+eCy46"
        "IvLx5l2B3rPRF5JApsblCK6QIm9fPpW7SKZJKoOSUfk1FKJTJBWJio4CofmkkA1i/pm5hJCooKHXPbzPn3B+Zqo4gZ4Q"
        "4M+On/WazYojOVMCkVwwgbIsrtcVlczXksz7hy8ZfM5rbAwnqFGPFYpYdmAQPIMjpdaKaeHMp8dvz69/fQ+xMfVYoRpa"
        "nPz+8HPB3wuk2uun5EEtCY89004qEwkRFlYZj5dKsw6tnQdFxVvIAnGsTCTj6YkBzpfpJBcb2SGM4beFz8TmOMygEKEY"
        "j+Tzix/LZ9zDeU+sKxSJeDDPfrqc/TkWTmhpldAXhp6jNIurnErpmP2SZUIR0pNRMBfhFwHywgkvxut634stxQWMObgf"
        "pCgEotIjvLm/K4SylM6dCkRCRIW5MwokuGuUWnZ8MLkIikUCEV6Kc2CynLS4Sv35+qo4Eh2ju4cjpQjH2QqrEkooEFIp"
        "PGOUYYkAL0e8GHdsGXNkhoREqh0rxZJFUbnXOreZjk4u7YU2SSFWlFKgJ7KcnyAsXhMaW9SKqlRPbO3LYUu2CzFW2otR"
        "ohAxTrlbTBYRqXWxol7EU929E+coKSV63VMiumYzTRQrSGqvdqBiHDefmJWtgcKAf2eLgHHwBZw1WqSBCinR2H/xVuwn"
        "FfDffIQX4u7hHv9fBJAi+dmzJhXoyXkxyuGeF8O16eR0JzxeDNdUCuAapeYQQ0wAtASJl5pXTCMCSiSjYMy8UlFEDrSk"
        "lnHTh0UdKhQybaKyo0ydqDDQRPfB1IkKK6NjpktU1DMybspYOf73rhSlR8b8f9nt/gKH01coBKSKLQAAAABJRU5ErkJggg=="
    ),
    "face_susie_alt_2": (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAzCAYAAAADxoFxAAACKUlEQVRoQ8WOAW7DMAwD"
        "9/9Pb01rNgxNybLjdgccFlOUup8Hvzsd4XYWtOHQCNdlGTcvasNQ4GYzAjcraMNO4GZ3"
        "XLxpw4uLh8su3Lfh24WDS07+jg2fTh66LXAz0YbV5e0ybt604WjpKwIz64Ko+FWBmz3s"
        "w6T8URXXafbhYOGjMm7evAaD8tcEbvbwGiTFfxFIfnm4wr8LKOsLmu125TdAe/dDzXaq"
        "9/XtVB5ZX9Bsl3o34CxSeulwm3ovw3kkaOd+qNkO+V6Fe5nUDQfbBG42I92RDssC/j5w"
        "M9dx8gy087V4SMNU7SmauR4yJ+ZMm8XlTO3oGVkF3WOBfPclzZzcAzp3cId7msNgdg2C"
        "UqeSzarwHbhHs+Z5SEqdSpTPwm8knoeJpWc3o9KJ0LeM56G48FZx2Sr6lngeCuWLn8a9"
        "2TwPg6LVEeUr6HvN10dSSP0G5t3zcQqnjKh0KvA9zfNSCqdVKh2QzYDcdV5I4ZKMy7UD"
        "qh3yVZJwWUYz11GiOXab9/+07jN81u4M2Gn2j84KXHaAc6XL8J4YDsoyoxxE3wfcxbeY"
        "Dksq0VzzSOBmT9vcD4s6qr0It/92WCiY4fq33XFxBbc3MtxbvZCt4PYq2t07F8IKbq+i"
        "3b1zIazg9ioGu+cAv7NWcHsjk73rozzU8w71Tj2P8ubrAyX84vsAZzWbsegBl/P8AJ3A"
        "PmTcWbuaqYC/D9y8qA1DHa73OX9+/wDi9p805eESMQAAAABJRU5ErkJggg=="
    ),
    "face_susie_alt_4": (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAzCAYAAAADxoFxAAACI0lEQVRoQ8WOAZLDIAwD"
        "7/+fvmta1ChCNobQ3s7sNMgy9OfB705HuJ0FbTg0wnVZxs2L2jAUuNmMwM0K2rATuNkd"
        "F++04cXFi8su3G/DtwsXLjn5jg2fTl50W+Bmog2ry9tl3Lxpw9HSVwRm1gVR8asCN3vY"
        "h0n5oyqu0+zDwcJHZdy8eQ0G5a8J3OzhNUiK/yKQ/HJwhX8XUNYXNNvtyhugnfuhZjvV"
        "+/XsVB5ZX9Bsl3o34CxSeulwm3ovw3kkaOd+qNkO+V6Fe5nUDQfbBG42I92RDssC/j5w"
        "M9dx8gy087V4SMNU7SmauR4yJ+ZMm8XlTO3oGVkF3WOBfPclzZzcAzp3cId7msNgdg2C"
        "UqeSzarwHbhHs+Z5SEqdSpTPwm8knoeJpWc3o9KJ0LeM56G48FZx2Sr6lngeCuWLn8a9"
        "2TwPg6LVEeUr6HvN10dSSP0G5t3zcQqnjKh0KvA9zfNSCqdVKh2QzYDcdV5I4ZKMy7UD"
        "qh3yVZJwWUYz11GiOXab9/+07jN81u4M2Gn2j84KXHaAc6XL8J4YDsoyoxxE3wfcxbeY"
        "Dksq0VzzSOBmT9vcD4s6qr0It/92WCiY4fq33XFxBbc3MtxbvZCt4PYq2t07F8IKbq+i"
        "3b1zIazg9ioGu+cAv7NWcHsjk73rozzU8w71Tj2P8ubrAyX84vsAZzWbsegBl/P8AJ3A"
        "PmTcWbuaqYC/D9y8qA1DHa73OX9+/wDi9p805eESMQAAAABJRU5ErkJggg=="
    ),
    "dw_susie_plush_0": (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAWCAYAAAAinad/AAAA80lEQVQ4T5WRwQ1CMQxD"
        "/xZwYw+W4c4aXBgCiRmYhCOrIC7wHb6Dk6ZQLD3RJrH7W6YBPTv8JTMdV/sS9jGYpU2jCsgss43K4RHgfUd8FL5G1+B+"
        "uBnn9TXUweJtZE0YYMSeIbrPYQA9BGSFAKL1kbBg0HVFERTDKhPRfn439CxB5IM09cDszzBQmQkO4hxDUiBweRFGhXU1"
        "c621mSA3ZpIp7HOYD/FaWO82J69XaPiMywMAr8YwvaoettCoGnJyGGsy38gN5HHZ2i+MhL10eFduAOldKoYU/i2CvXUH"
        "RQPT+bqfqkw9vgsPTuatm4p6oWl6ATiDM3FLssKXAAAAAElFTkSuQmCC"
    ),
    "dmenu_equip_1": (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAASCAYAAACAa1QyAAAAT0lEQVQ4T+3LyQ0AIAgA"
        "QfpvWg1uPEGN8en8gEWuBQdnH52JxEYz4Vy1Sy0cJBm7LfKK/RJpj5uLbMZdsSo7RhtNF42zSb8SxnP8/cfHRCLsTSbo"
        "WZOjdAAAAABJRU5ErkJggg=="
    ),
    "hpname_0": (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAALCAYAAAB24g05AAAAOklEQVQoU2MAgv8wAGLj"
        "4yMDmBwQk2cACEDliTcAB5+gDVAeJqDIAJgcEGM4CcrDzUfDg8CAIQ0YGABSzkrEaaLCQAAAAABJRU5ErkJggg=="
    ),
}

SPRITE_REL_PATHS = {
    "susieb_idle_0": "Characters/Playable Characters/Susie/Ch1/Dark World/Battle/spr_susieb_idle_0.png",
    "susieb_idle_1": "Characters/Playable Characters/Susie/Ch1/Dark World/Battle/spr_susieb_idle_1.png",
    "susieb_idle_2": "Characters/Playable Characters/Susie/Ch1/Dark World/Battle/spr_susieb_idle_2.png",
    "susieb_idle_3": "Characters/Playable Characters/Susie/Ch1/Dark World/Battle/spr_susieb_idle_3.png",
    "face_susie_alt_2": "Characters/Playable Characters/Susie/Ch1/Portraits/spr_face_susie_alt_2.png",
    "face_susie_alt_4": "Characters/Playable Characters/Susie/Ch1/Portraits/spr_face_susie_alt_4.png",
    "dw_susie_plush_0": "Characters/Playable Characters/Susie/Ch2/Dark World/Misc/spr_dw_susie_plush_0.png",
    "dmenu_equip_1": "UI/HUD/Ch1/spr_dmenu_equip_1.png",
    "hpname_0": "UI/Battle/Text/Ch1/spr_hpname_0.png",
}

def get_sprite_data_uri(key: str) -> str:
    rel_path = SPRITE_REL_PATHS.get(key)
    if rel_path and os.path.isdir(DELTAEXT_DIR):
        full_path = os.path.join(DELTAEXT_DIR, rel_path)
        if os.path.isfile(full_path):
            with open(full_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
                return f"data:image/png;base64,{b64}"
    return SPRITES.get(key, "")

MANE_AX_B64 = "iVBORw0KGgoAAAANSUhEUgAAAA0AAAASCAYAAACAa1QyAAAAT0lEQVQ4T+3LyQ0AIAgAQfpvWg1uPEGN8en8gEWuBQdnH52JxEYz4Vy1Sy0cJBm7LfKK/RJpj5uLbMZdsSo7RhtNF42zSb8SxnP8/cfHRCLsTSboWZOjdAAAAABJRU5ErkJggg=="


def create_pill_website():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="242" height="44" viewBox="0 0 242 44" role="img" aria-label="souphater.page">
  <style>
    .w { font: 600 20px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #ffffff; }
    .m { mix-blend-mode: multiply; }
    @keyframes pill-nudge {
      0%, 100% { transform: translateX(0); }
      50% { transform: translateX(1.5px); }
    }
    .icon {
      animation: pill-nudge 3s ease-in-out infinite alternate;
    }
    @media (prefers-reduced-motion: reduce) {
      .icon { animation: none !important; }
    }
  </style>
  <g style="isolation:isolate">
    <g class="icon">
      <circle class="m" cx="22" cy="22" r="22" fill="#FFB627"/>
    </g>
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
      0%, 100% { transform: translateX(0); }
      50% { transform: translateX(2px); }
    }
    .icon {
      animation: pill-arrow 2.8s ease-in-out infinite alternate;
    }
    @media (prefers-reduced-motion: reduce) {
      .icon { animation: none !important; }
    }
  </style>
  <g style="isolation:isolate">
    <g class="icon">
      <path class="m" transform="scale(1.294)" d="M5 6 L30 17 L5 28 Z" fill="#FFB627" stroke="#FFB627" stroke-width="6" stroke-linejoin="round"/>
    </g>
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
      0%, 100% { transform: translateX(0); }
      50% { transform: translateX(1.5px); }
    }
    .icon {
      animation: pill-diamond 3.2s ease-in-out infinite alternate;
    }
    @media (prefers-reduced-motion: reduce) {
      .icon { animation: none !important; }
    }
  </style>
  <g style="isolation:isolate">
    <g class="icon">
      <rect class="m" x="6.5" y="6.5" width="31" height="31" rx="6.5" transform="rotate(45 22 22)" fill="#FFB627"/>
    </g>
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
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="84" viewBox="0 0 640 84" role="img" aria-label="ditto card">
  <defs>
    <linearGradient id="flagship-border-ditto" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFB627" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#F0542D" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#E64980" stop-opacity="0.9"/>
    </linearGradient>
  </defs>
  <style>
    .bg {{ fill: #FFF3E0; }}
    .t  {{ font: 700 24px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }}
    .sub {{ font: 500 12.5px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #7a6a5c; }}
    .m  {{ mix-blend-mode: multiply; }}
    .card-border {{ stroke-opacity: 0.45; }}
    .rpg-box {{ fill: #24190F; }}
    .rpg-lbl {{ font: 800 11px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #FFB627; letter-spacing: 0.5px; }}
    .rpg-num {{ font: 700 11px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #FFFFFF; }}
    .rpg-stat {{ font: 700 11.5px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #2DA44E; letter-spacing: 0.5px; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #2A2119; }}
      .t  {{ fill: #fff4e6; }}
      .sub {{ fill: #b8a898; }}
      .card-border {{ stroke-opacity: 0.75; }}
      .rpg-box {{ fill: #140E0A; }}
    }}
    @keyframes eq-1 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-3.5px); }} }}
    @keyframes eq-2 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(2.5px); }} }}
    @keyframes eq-3 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
    .bar-1 {{ animation: eq-1 2.2s ease-in-out infinite; }}
    .bar-2 {{ animation: eq-2 1.8s ease-in-out infinite; }}
    .bar-3 {{ animation: eq-3 2.5s ease-in-out infinite; }}
    @keyframes badge-pulse {{
      0%, 100% {{ opacity: 0.88; }}
      50% {{ opacity: 1; }}
    }}
    .badge-anim {{
      animation: badge-pulse 2.8s ease-in-out infinite;
    }}
    @media (prefers-reduced-motion: reduce) {{
      .bar-1, .bar-2, .bar-3, .badge-anim {{ animation: none !important; }}
    }}
  </style>
  <rect class="bg" width="640" height="84" rx="18"/>
  <rect class="card-border" x="1.5" y="1.5" width="637" height="81" rx="16.5" fill="none" stroke="url(#flagship-border-ditto)" stroke-width="1.8"/>
  <g transform="translate(22 14.0) scale(0.875)" style="isolation:isolate">
    <rect class="m bar-1" x="2" y="18" width="22" height="28" rx="11" fill="#FFB627"/>
    <rect class="m bar-2" x="18" y="6" width="22" height="52" rx="11" fill="#F0542D"/>
    <rect class="m bar-3" x="34" y="14" width="22" height="36" rx="11" fill="#E64980"/>
  </g>
  <text class="t" x="88" y="41">ditto</text>
  <text class="sub" x="89" y="60">voice notes into chat · android</text>
  <g transform="translate(442, 24)">
    <g class="badge-anim">
      <rect class="rpg-box" width="178" height="36" rx="9" stroke="#2DA44E" stroke-width="1.5"/>
      <text class="rpg-lbl" x="12" y="23">HP</text>
      <rect x="33" y="14" width="32" height="9" rx="2.5" fill="#1B2E1E" stroke="#2DA44E" stroke-width="1"/>
      <rect x="35" y="16" width="28" height="5" rx="1.5" fill="#2DA44E"/>
      <text class="rpg-num" x="71" y="23">100/100</text>
      <text class="rpg-stat" x="120" y="23">DONE</text>
    </g>
  </g>
</svg>"""

def create_card_fichegen():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="84" viewBox="0 0 640 84" role="img" aria-label="fichegen card">
  <defs>
    <linearGradient id="flagship-border-fichegen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E64980" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#F0542D" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#FFB627" stop-opacity="0.9"/>
    </linearGradient>
  </defs>
  <style>
    .bg {{ fill: #FFF3E0; }}
    .t  {{ font: 700 24px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }}
    .sub {{ font: 500 12.5px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #7a6a5c; }}
    .m  {{ mix-blend-mode: multiply; }}
    .card-border {{ stroke-opacity: 0.45; }}
    .rpg-box {{ fill: #24190F; }}
    .rpg-tag {{ font: 800 10.5px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #FFB627; letter-spacing: 0.5px; }}
    .rpg-equip {{ font: 700 11.5px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #E64980; letter-spacing: 0.5px; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #2A2119; }}
      .t  {{ fill: #fff4e6; }}
      .sub {{ fill: #b8a898; }}
      .card-border {{ stroke-opacity: 0.75; }}
      .rpg-box {{ fill: #140E0A; }}
    }}
    @keyframes sheet-float-1 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
    @keyframes sheet-float-2 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(1.5px); }} }}
    @keyframes sheet-float-3 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-1.5px); }} }}
    .sheet-1 {{ animation: sheet-float-1 3.5s ease-in-out infinite; }}
    .sheet-2 {{ animation: sheet-float-2 3.5s ease-in-out infinite 0.5s; }}
    .sheet-3 {{ animation: sheet-float-3 3.5s ease-in-out infinite 1s; }}
    @keyframes badge-pulse {{
      0%, 100% {{ opacity: 0.88; }}
      50% {{ opacity: 1; }}
    }}
    .badge-anim {{
      animation: badge-pulse 2.8s ease-in-out infinite;
    }}
    .pixelated {{ image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges; }}
    @media (prefers-reduced-motion: reduce) {{
      .sheet-1, .sheet-2, .sheet-3, .badge-anim {{ animation: none !important; }}
    }}
  </style>
  <rect class="bg" width="640" height="84" rx="18"/>
  <rect class="card-border" x="1.5" y="1.5" width="637" height="81" rx="16.5" fill="none" stroke="url(#flagship-border-fichegen)" stroke-width="1.8"/>
  <g transform="translate(22 14.0) scale(0.875)" style="isolation:isolate">
    <rect class="m sheet-1" x="4" y="8" width="36" height="44" rx="8" fill="#FFB627"/>
    <g transform="translate(16 12)">
      <g class="sheet-2">
        <rect class="m" x="0" y="0" width="36" height="44" rx="8" transform="rotate(8 18 22)" fill="#F0542D"/>
      </g>
    </g>
    <g transform="translate(26 6)">
      <g class="sheet-3">
        <rect class="m" x="0" y="0" width="30" height="40" rx="8" transform="rotate(-6 15 20)" fill="#E64980"/>
      </g>
    </g>
  </g>
  <text class="t" x="88" y="41">fichegen (profstudio)</text>
  <text class="sub" x="89" y="60">ai lesson preparation for teachers</text>
  <g transform="translate(438, 24)">
    <g class="badge-anim">
      <rect class="rpg-box" width="182" height="36" rx="9" stroke="#E64980" stroke-width="1.5"/>
      <image class="pixelated" href="data:image/png;base64,{MANE_AX_B64}" x="10" y="9" width="13" height="18"/>
      <text class="rpg-tag" x="30" y="23">[ITEM: AX]</text>
      <text class="rpg-equip" x="94" y="23">MAC · WIN</text>
    </g>
  </g>
</svg>"""

def create_card_gemwallet():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="72" viewBox="0 0 640 72" role="img" aria-label="gemwallet card">
  <style>
    .bg {{ fill: #FFF3E0; }}
    .t  {{ font: 700 22px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }}
    .sub {{ font: 500 12px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #7a6a5c; }}
    .m  {{ mix-blend-mode: multiply; }}
    .card-border {{ stroke-opacity: 0.4; }}
    .rpg-box {{ fill: #24190F; }}
    .rpg-tp {{ font: 800 11px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #FFB627; letter-spacing: 0.5px; }}
    .rpg-val {{ font: 700 11.5px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #E07B00; letter-spacing: 0.5px; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #2A2119; }}
      .t  {{ fill: #fff4e6; }}
      .sub {{ fill: #b8a898; }}
      .card-border {{ stroke-opacity: 0.7; }}
      .rpg-box {{ fill: #140E0A; }}
    }}
    @keyframes gw-float-1 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
    @keyframes gw-float-2 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(2px); }} }}
    @keyframes gw-float-3 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-1.5px); }} }}
    .gw-1 {{ animation: gw-float-1 3.4s ease-in-out infinite; }}
    .gw-2 {{ animation: gw-float-2 3.4s ease-in-out infinite 0.6s; }}
    .gw-3 {{ animation: gw-float-3 3.4s ease-in-out infinite 1.2s; }}
    @keyframes badge-pulse {{
      0%, 100% {{ opacity: 0.86; }}
      50% {{ opacity: 1; }}
    }}
    .badge-anim {{
      animation: badge-pulse 2.2s ease-in-out infinite;
    }}
    @media (prefers-reduced-motion: reduce) {{
      .gw-1, .gw-2, .gw-3, .badge-anim {{ animation: none !important; }}
    }}
  </style>
  <rect class="bg" width="640" height="72" rx="16"/>
  <rect class="card-border" x="1.5" y="1.5" width="637" height="69" rx="14.5" fill="none" stroke="#E07B00" stroke-width="1.3"/>
  <g transform="translate(20 10.0) scale(0.78)" style="isolation:isolate">
    <circle class="m gw-1" cx="26" cy="32" r="22" fill="#FFB627"/>
    <g class="gw-2"><rect class="m" x="22" y="12" width="36" height="36" rx="10" transform="rotate(45 40 30)" fill="#F0542D"/></g>
    <path class="m gw-3" d="M10 54 A22 22 0 0 1 54 54 Z" fill="#E64980"/>
  </g>
  <text class="t" x="84" y="35">gemwallet</text>
  <text class="sub" x="85" y="52">encrypted offline finance · zero telemetry</text>
  <g transform="translate(452, 20)">
    <g class="badge-anim">
      <rect class="rpg-box" width="168" height="32" rx="8" stroke="#E07B00" stroke-width="1.4"/>
      <text class="rpg-tp" x="10" y="21">TP 90%</text>
      <rect x="58" y="12" width="24" height="8" rx="2" fill="#241708" stroke="#E07B00" stroke-width="0.8"/>
      <rect x="59" y="13" width="21" height="6" rx="1.5" fill="#E07B00"/>
      <text class="rpg-val" x="88" y="21">MOSTLY DONE</text>
    </g>
  </g>
</svg>"""

def create_card_bitnet():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="72" viewBox="0 0 640 72" role="img" aria-label="bluenet bitnet card">
  <style>
    .bg {{ fill: #FFF3E0; }}
    .t  {{ font: 700 22px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }}
    .sub {{ font: 500 12px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #7a6a5c; }}
    .m  {{ mix-blend-mode: multiply; }}
    .card-border {{ stroke-opacity: 0.4; }}
    .rpg-box {{ fill: #24190F; }}
    .rpg-tag {{ font: 800 11px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #FFB627; letter-spacing: 0.5px; }}
    .rpg-stat {{ font: 700 11.5px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #F0542D; letter-spacing: 0.5px; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #2A2119; }}
      .t  {{ fill: #fff4e6; }}
      .sub {{ fill: #b8a898; }}
      .card-border {{ stroke-opacity: 0.7; }}
      .rpg-box {{ fill: #140E0A; }}
    }}
    @keyframes mesh-pulse {{
      0%, 100% {{ opacity: 0.8; transform: translateY(0); }}
      50% {{ opacity: 1; transform: translateY(-2px); }}
    }}
    .node-1 {{ animation: mesh-pulse 2.1s ease-in-out infinite; }}
    .node-2 {{ animation: mesh-pulse 2.1s ease-in-out infinite 0.7s; }}
    .node-3 {{ animation: mesh-pulse 2.1s ease-in-out infinite 1.4s; }}
    @keyframes badge-pulse {{
      0%, 100% {{ opacity: 0.86; }}
      50% {{ opacity: 1; }}
    }}
    .badge-anim {{
      animation: badge-pulse 2.2s ease-in-out infinite;
    }}
    @media (prefers-reduced-motion: reduce) {{
      .node-1, .node-2, .node-3, .badge-anim {{ animation: none !important; }}
    }}
  </style>
  <rect class="bg" width="640" height="72" rx="16"/>
  <rect class="card-border" x="1.5" y="1.5" width="637" height="69" rx="14.5" fill="none" stroke="#F0542D" stroke-width="1.3"/>
  <g transform="translate(20 14.0) scale(0.72)" style="isolation:isolate">
    <circle class="m node-1" cx="14" cy="30" r="15" fill="#FFB627"/>
    <circle class="m node-2" cx="32" cy="30" r="15" fill="#F0542D"/>
    <circle class="m node-3" cx="50" cy="30" r="15" fill="#E64980"/>
  </g>
  <text class="t" x="84" y="35">bluenet (bitnet)</text>
  <text class="sub" x="85" y="52">android ble mesh · bluetooth internet</text>
  <g transform="translate(470, 20)">
    <g class="badge-anim">
      <rect class="rpg-box" width="150" height="32" rx="8" stroke="#F0542D" stroke-width="1.4"/>
      <text class="rpg-tag" x="12" y="21">[CAST: 60%]</text>
      <text class="rpg-stat" x="98" y="21">WIP</text>
    </g>
  </g>
</svg>"""

def create_card_agent_base():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="72" viewBox="0 0 640 72" role="img" aria-label="agent base card">
  <style>
    .bg {{ fill: #FFF3E0; }}
    .t  {{ font: 700 22px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }}
    .sub {{ font: 500 12px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #7a6a5c; }}
    .m  {{ mix-blend-mode: multiply; }}
    .card-border {{ stroke-opacity: 0.4; }}
    .rpg-box {{ fill: #24190F; }}
    .rpg-act {{ font: 800 11px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #FFB627; letter-spacing: 0.5px; }}
    .rpg-stat {{ font: 700 11.5px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #E64980; letter-spacing: 0.5px; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #2A2119; }}
      .t  {{ fill: #fff4e6; }}
      .sub {{ fill: #b8a898; }}
      .card-border {{ stroke-opacity: 0.7; }}
      .rpg-box {{ fill: #140E0A; }}
    }}
    @keyframes ag-pulse-1 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2.5px); }} }}
    @keyframes ag-pulse-2 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(2px); }} }}
    .ag-head {{ animation: ag-pulse-1 2.4s ease-in-out infinite; }}
    .ag-base {{ animation: ag-pulse-2 3s ease-in-out infinite 0.5s; }}
    @keyframes badge-pulse {{
      0%, 100% {{ opacity: 0.86; }}
      50% {{ opacity: 1; }}
    }}
    .badge-anim {{
      animation: badge-pulse 2.2s ease-in-out infinite;
    }}
    @media (prefers-reduced-motion: reduce) {{
      .ag-head, .ag-base, .badge-anim {{ animation: none !important; }}
    }}
  </style>
  <rect class="bg" width="640" height="72" rx="16"/>
  <rect class="card-border" x="1.5" y="1.5" width="637" height="69" rx="14.5" fill="none" stroke="#E64980" stroke-width="1.3"/>
  <g transform="translate(20 14.0) scale(0.72)" style="isolation:isolate">
    <circle class="m ag-base" cx="24" cy="34" r="22" fill="#FFB627"/>
    <path class="m ag-body" d="M24 56 V16 A40 40 0 0 1 64 56 Z" fill="#F0542D"/>
    <circle class="m ag-head" cx="48" cy="20" r="12" fill="#E64980"/>
  </g>
  <text class="t" x="84" y="35">agent base</text>
  <text class="sub" x="85" y="52">autonomous agent loop · streaming logs</text>
  <g transform="translate(470, 20)">
    <g class="badge-anim">
      <rect class="rpg-box" width="150" height="32" rx="8" stroke="#E64980" stroke-width="1.4"/>
      <text class="rpg-act" x="12" y="21">[ACT: READY]</text>
      <text class="rpg-stat" x="104" y="21">WIP</text>
    </g>
  </g>
</svg>"""

def create_card_tether_compass():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="60" viewBox="0 0 640 60" role="img" aria-label="tether compass card">
  <style>
    .bg {{ fill: #FFF3E0; }}
    .t  {{ font: 700 20px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }}
    .sub {{ font: 500 11.5px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #7a6a5c; }}
    .m  {{ mix-blend-mode: multiply; }}
    .card-border {{ stroke-opacity: 0.35; }}
    .rpg-box {{ fill: #24190F; }}
    .rpg-item {{ font: 800 10.5px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #FFB627; letter-spacing: 0.5px; }}
    .rpg-ship {{ font: 700 11px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #2DA44E; letter-spacing: 0.5px; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #2A2119; }}
      .t  {{ fill: #fff4e6; }}
      .sub {{ fill: #b8a898; }}
      .card-border {{ stroke-opacity: 0.7; }}
      .rpg-box {{ fill: #140E0A; }}
    }}
    @keyframes arc-sway-1 {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-1.5px); }}
    }}
    @keyframes arc-sway-2 {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(1.5px); }}
    }}
    @keyframes beacon-pulse {{
      0%, 100% {{ opacity: 0.75; }}
      50% {{ opacity: 1; }}
    }}
    .cp-arc1 {{ animation: arc-sway-1 3.5s ease-in-out infinite; }}
    .cp-arc2 {{ animation: arc-sway-2 3.5s ease-in-out infinite 0.6s; }}
    .cp-dot  {{ animation: beacon-pulse 2.2s ease-in-out infinite; }}
    @keyframes badge-pulse {{
      0%, 100% {{ opacity: 0.86; }}
      50% {{ opacity: 1; }}
    }}
    .badge-anim {{
      animation: badge-pulse 2.8s ease-in-out infinite;
    }}
    @media (prefers-reduced-motion: reduce) {{
      .cp-arc1, .cp-arc2, .cp-dot, .badge-anim {{ animation: none !important; }}
    }}
  </style>
  <rect class="bg" width="640" height="60" rx="14"/>
  <rect class="card-border" x="1" y="1" width="638" height="58" rx="13" fill="none" stroke="#2DA44E" stroke-width="1.2"/>
  <g transform="translate(18 10.0) scale(0.62)" style="isolation:isolate">
    <path class="m cp-arc1" d="M30 10 A22 22 0 0 0 30 54 Z" fill="#FFB627"/>
    <g transform="translate(14 0)"><path class="m cp-arc2" d="M22 10 A22 22 0 0 1 22 54 Z" fill="#F0542D"/></g>
    <circle class="m cp-dot" cx="32" cy="32" r="9" fill="#E64980"/>
  </g>
  <text class="t" x="76" y="29">tether compass</text>
  <text class="sub" x="77" y="45">long-distance couples web compass</text>
  <g transform="translate(472, 16)">
    <g class="badge-anim">
      <rect class="rpg-box" width="148" height="28" rx="7" stroke="#2DA44E" stroke-width="1.2"/>
      <text class="rpg-item" x="10" y="19">[KEY ITEM]</text>
      <text class="rpg-ship" x="84" y="19">SHIPPED</text>
    </g>
  </g>
</svg>"""

def create_card_direct_moutamadris():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="60" viewBox="0 0 640 60" role="img" aria-label="direct moutamadris card">
  <style>
    .bg {{ fill: #FFF3E0; }}
    .t  {{ font: 700 20px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -.5px; }}
    .sub {{ font: 500 11.5px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #7a6a5c; }}
    .m  {{ mix-blend-mode: multiply; }}
    .card-border {{ stroke-opacity: 0.35; }}
    .rpg-box {{ fill: #24190F; }}
    .rpg-lv {{ font: 800 10.5px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #FFB627; letter-spacing: 0.5px; }}
    .rpg-ship {{ font: 700 11px ui-monospace, "Cascadia Code", Menlo, monospace; fill: #2DA44E; letter-spacing: 0.5px; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #2A2119; }}
      .t  {{ fill: #fff4e6; }}
      .sub {{ fill: #b8a898; }}
      .card-border {{ stroke-opacity: 0.7; }}
      .rpg-box {{ fill: #140E0A; }}
    }}
    @keyframes dm-float-1 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
    @keyframes dm-float-2 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(2px); }} }}
    @keyframes dm-float-3 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-1.5px); }} }}
    .dm-1 {{ animation: dm-float-1 3.4s ease-in-out infinite; }}
    .dm-2 {{ animation: dm-float-2 3.4s ease-in-out infinite 0.6s; }}
    .dm-3 {{ animation: dm-float-3 3.4s ease-in-out infinite 1.2s; }}
    @keyframes badge-pulse {{
      0%, 100% {{ opacity: 0.86; }}
      50% {{ opacity: 1; }}
    }}
    .badge-anim {{
      animation: badge-pulse 2.8s ease-in-out infinite;
    }}
    @media (prefers-reduced-motion: reduce) {{
      .dm-1, .dm-2, .dm-3, .badge-anim {{ animation: none !important; }}
    }}
  </style>
  <rect class="bg" width="640" height="60" rx="14"/>
  <rect class="card-border" x="1" y="1" width="638" height="58" rx="13" fill="none" stroke="#2DA44E" stroke-width="1.2"/>
  <g transform="translate(18 10.0) scale(0.62)" style="isolation:isolate">
    <rect class="m dm-1" x="4" y="10" width="40" height="40" rx="12" fill="#FFB627"/>
    <circle class="m dm-2" cx="42" cy="40" r="18" fill="#F0542D"/>
    <circle class="m dm-3" cx="50" cy="18" r="10" fill="#E64980"/>
  </g>
  <text class="t" x="76" y="29">direct moutamadris</text>
  <text class="sub" x="77" y="45">lightweight moroccan grade portal client</text>
  <g transform="translate(472, 16)">
    <g class="badge-anim">
      <rect class="rpg-box" width="148" height="28" rx="7" stroke="#2DA44E" stroke-width="1.2"/>
      <text class="rpg-lv" x="12" y="19">[LV 99: FAST]</text>
      <text class="rpg-ship" x="86" y="19">SHIPPED</text>
    </g>
  </g>
</svg>"""

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
    plush_uri = get_sprite_data_uri("dw_susie_plush_0")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="70" viewBox="0 0 640 70" role="img" aria-label="soup is just the best driving force :3">
  <style>
    .t {{ font: 700 20px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; }}
    .m {{ mix-blend-mode: multiply; }}
    .pixelated {{ image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges; }}
    @media (prefers-color-scheme: dark) {{
      .t {{ fill: #fff4e6; }}
    }}
    @keyframes float-l {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2.5px); }} }}
    @keyframes float-r {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(2.5px); }} }}
    @keyframes plush-breathe {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
    .mark-l {{ animation: float-l 4s ease-in-out infinite; }}
    .mark-r {{ animation: float-r 4s ease-in-out infinite; }}
    .plush-cameo, .plush-bob {{ animation: plush-breathe 3.5s ease-in-out infinite; }}
    @media (prefers-reduced-motion: reduce) {{
      .mark-l, .mark-r, .plush-cameo, .plush-bob {{ animation: none !important; }}
    }}
  </style>
  <g transform="translate(14 12.6) scale(0.8)" style="isolation:isolate">
    <g class="mark-l">
      <circle class="m" cx="20" cy="28" r="14" fill="#FFB627"/>
      <rect class="m" x="24" y="14" width="28" height="28" rx="9" fill="#F0542D"/>
      <path class="m" d="M46 42 A14 14 0 0 1 74 42 Z" fill="#E64980"/>
    </g>
  </g>
  <g transform="translate(571 12.6) scale(0.8)" style="isolation:isolate">
    <g class="mark-r">
      <circle class="m" cx="20" cy="28" r="14" fill="#E64980"/>
      <rect class="m" x="24" y="14" width="28" height="28" rx="9" fill="#FFB627"/>
      <path class="m" d="M46 42 A14 14 0 0 1 74 42 Z" fill="#F0542D"/>
    </g>
  </g>
  <text class="t" x="300" y="42" text-anchor="middle">soup is just the best driving force :3</text>
  <!-- Susie Plush Cameo: 2x pixel scale (19x22 -> 38x44) beside soup quote -->
  <g transform="translate(508 13) scale(2)">
    <g class="plush-cameo plush-bob pixelated">
      <image class="pixelated" href="{plush_uri}" width="19" height="22"/>
    </g>
  </g>
</svg>'''

def create_header():
    s0 = get_sprite_data_uri("susieb_idle_0")
    s1 = get_sprite_data_uri("susieb_idle_1")
    s2 = get_sprite_data_uri("susieb_idle_2")
    s3 = get_sprite_data_uri("susieb_idle_3")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="200" viewBox="0 0 880 200" role="img" aria-label="Walid Elonk">
  <style>
    .name {{ font: 700 52px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #24190f; letter-spacing: -1px; }}
    .sub  {{ font: 400 15px ui-sans-serif, -apple-system, "Segoe UI", sans-serif; fill: #7a6a5c; }}
    .m    {{ mix-blend-mode: multiply; }}
    .pixelated {{ image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges; }}
    @media (prefers-color-scheme: dark) {{
      .name {{ fill: #fff4e6; }}
      .sub  {{ fill: #b8a898; }}
    }}
    @keyframes drift-c1 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-3px); }} }}
    @keyframes drift-c2 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(3px); }} }}
    @keyframes drift-c3 {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
    @keyframes cluster-sway {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-3.5px); }} }}
    @keyframes susie-bob    {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-3.5px); }} }}
    @keyframes susie-f0 {{ 0%, 24.99% {{ opacity: 1; }} 25%, 100% {{ opacity: 0; }} }}
    @keyframes susie-f1 {{ 0%, 24.99% {{ opacity: 0; }} 25%, 49.99% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
    @keyframes susie-f2 {{ 0%, 49.99% {{ opacity: 0; }} 50%, 74.99% {{ opacity: 1; }} 75%, 100% {{ opacity: 0; }} }}
    @keyframes susie-f3 {{ 0%, 74.99% {{ opacity: 0; }} 75%, 99.99% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}

    .mark-c1 {{ animation: drift-c1 4.5s ease-in-out infinite; }}
    .mark-c2 {{ animation: drift-c2 4.5s ease-in-out infinite; }}
    .mark-c3 {{ animation: drift-c3 4.5s ease-in-out infinite 0.7s; }}
    .cluster-r {{ animation: cluster-sway 5s ease-in-out infinite alternate; }}
    .susie-mascot, .susie-idle {{ animation: susie-bob 3.2s ease-in-out infinite; }}
    .susie-f0 {{ animation: susie-f0 1.2s infinite; }}
    .susie-f1 {{ animation: susie-f1 1.2s infinite; opacity: 0; }}
    .susie-f2 {{ animation: susie-f2 1.2s infinite; opacity: 0; }}
    .susie-f3 {{ animation: susie-f3 1.2s infinite; opacity: 0; }}

    @media (prefers-reduced-motion: reduce) {{
      .mark-c1, .mark-c2, .mark-c3, .cluster-r, .susie-mascot, .susie-idle, .susie-f0, .susie-f1, .susie-f2, .susie-f3 {{
        animation: none !important;
      }}
      .susie-f0 {{ opacity: 1 !important; }}
      .susie-f1, .susie-f2, .susie-f3 {{ opacity: 0 !important; }}
    }}
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

  <!-- Susie Hero Mascot: 2x pixel scale (54x45 -> 108x90) with bobbing and idle cycle -->
  <g transform="translate(740 55) scale(2)">
    <g class="susie-mascot susie-idle pixelated">
      <image class="pixelated susie-f0" href="{s0}" width="54" height="45"/>
      <image class="pixelated susie-f1" href="{s1}" width="54" height="45"/>
      <image class="pixelated susie-f2" href="{s2}" width="54" height="45"/>
      <image class="pixelated susie-f3" href="{s3}" width="54" height="45"/>
    </g>
  </g>
</svg>'''

def create_dialogue_susie(dialogue_lines=None, animated=True):
    smirk_uri = get_sprite_data_uri("face_susie_alt_2")
    talk_uri = get_sprite_data_uri("face_susie_alt_4")

    if dialogue_lines is None:
        dialogue_lines = [
            ("* ", "Hey! You look like someone who'd spend 40 hours"),
            ("  ", "building an offline mesh instead of studying."),
            ("* ", "...Also, the soup thing is real. Don't ask.")
        ]

    formatted_spans = []
    start_y = 43 if len(dialogue_lines) >= 3 else 54
    line_step = 26 if len(dialogue_lines) >= 3 else 28

    for i, line in enumerate(dialogue_lines):
        if isinstance(line, tuple):
            bullet, text = line
        elif line.startswith("* "):
            bullet, text = "* ", line[2:]
        elif line.startswith("  "):
            bullet, text = "  ", line[2:]
        else:
            bullet, text = "", line

        text_xml = (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("'", "&#8217;")
        )

        y_pos = start_y + i * line_step
        if bullet == "* ":
            content = f'<tspan class="star">* </tspan>{text_xml}'
        elif bullet == "  ":
            content = f'<tspan fill="transparent">* </tspan>{text_xml}'
        else:
            content = text_xml

        formatted_spans.append(f'    <text class="t" x="126" y="{y_pos}">\n      {content}\n    </text>')

    dialogue_svg_text = "\n".join(formatted_spans)

    talking_image = ""
    talking_css = ""
    if animated:
        talking_image = f'    <image class="portrait pixelated mouth-open" href="{talk_uri}" x="20" y="14" width="90" height="102"/>\n'
        talking_css = """    @keyframes susie-talk {
      0%, 6.6%, 13.3%, 20%, 26.6%, 33.3%, 40%, 100% { opacity: 0; }
      3.3%, 10%, 16.7%, 23.3%, 30%, 36.7% { opacity: 1; }
    }
    .mouth-open {
      animation: susie-talk 6s steps(1) infinite;
    }
"""

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="130" viewBox="0 0 640 130" role="img" aria-label="Deltarune Susie Dialogue">
  <style>
    .bg {{ fill: #000000; }}
    .box-outer {{ fill: none; stroke: #FFFFFF; stroke-width: 2.5; }}
    .box-inner {{ fill: none; stroke: #FFFFFF; stroke-width: 1.5; }}
    .pixelated {{ image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges; }}
    .portrait {{ image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges; }}
    .t {{
      font-family: ui-monospace, "Cascadia Code", Menlo, monospace;
      font-size: 15px;
      font-weight: 500;
      fill: #FFFFFF;
      letter-spacing: -0.2px;
    }}
    .star {{ fill: #FFB627; font-weight: 700; }}
    .prompt-arrow {{ fill: #FFB627; animation: blink-arrow 1.2s steps(1) infinite; }}
{talking_css}    @keyframes blink-arrow {{
      0%, 49% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}
    @keyframes arrow-blink {{
      0%, 49% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #000000; }}
      .box-outer {{ stroke: #FFFFFF; }}
      .box-inner {{ stroke: #FFFFFF; }}
      .t {{ fill: #FFFFFF; }}
      .star {{ fill: #FFE800; }}
      .prompt-arrow {{ fill: #FFE800; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .mouth-open, .prompt-arrow {{
        animation: none !important;
      }}
      .mouth-open {{
        opacity: 0 !important;
      }}
      .prompt-arrow {{
        opacity: 1 !important;
      }}
    }}
  </style>
  <rect class="bg" x="0" y="0" width="640" height="130" rx="4"/>
  <rect class="box-outer" x="5" y="5" width="630" height="120" rx="3"/>
  <rect class="box-inner" x="10" y="10" width="620" height="110" rx="2"/>
  <g id="susie-portrait">
    <image class="portrait pixelated" href="{smirk_uri}" x="20" y="14" width="90" height="102"/>
{talking_image}  </g>
  <g id="dialogue-text">
{dialogue_svg_text}
  </g>
  <polygon class="prompt-arrow" points="608,102 618,102 613,109"/>
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
    "header.svg": create_header(),
    "dialogue-susie.svg": create_dialogue_susie()
}

def validate_svg(name, content):
    # 1. XML parsing
    root = ET.fromstring(content)
    assert root.tag.endswith("svg"), f"{name}: root tag is not svg"
    assert "viewBox" in root.attrib, f"{name}: missing viewBox"
    assert "width" in root.attrib, f"{name}: missing width"
    assert "height" in root.attrib, f"{name}: missing height"

    # 2. No transform-box: fill-box (flaky / broken in SVG img contexts across Safari/WebKit)
    assert "transform-box" not in content, f"{name}: contains transform-box which breaks in SVG img contexts"

    # 3. Check for animated transform collision with presentation attributes
    # If a class is animated with transform, verify that elements with that class don't have static transform attributes
    animated_classes = re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{[^}]*animation:[^;]+', content)
    for cls in animated_classes:
        # Check if any element has class="... cls ..." AND transform="..."
        pattern = rf'<[^>]+class="[^"]*\b{cls}\b[^"]*"[^>]+transform="[^"]+"'
        assert not re.search(pattern, content), f"{name}: element with class '{cls}' has both CSS transform animation and static transform attribute"

    # 4. Reduced motion fallback
    if "@keyframes" in content:
        assert "@media (prefers-reduced-motion: reduce)" in content, f"{name}: missing reduced motion fallback"

    # 5. Dark mode support for SVGs with text or backgrounds
    if ".bg" in content or ".t" in content or ".name" in content:
        assert "@media (prefers-color-scheme: dark)" in content, f"{name}: missing dark mode styling"

if __name__ == "__main__":
    for fname, content in files.items():
        fpath = os.path.join(ASSETS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        try:
            validate_svg(fname, content)
            print(f"[OK] {fname}")
        except Exception as e:
            print(f"[FAIL] {fname}: {e}")
            raise
    print(f"\nAll {len(files)} SVG assets generated and validated successfully!")
