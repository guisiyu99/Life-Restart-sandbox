---
name: Neo-Sandbox Play
colors:
  surface: '#fef7ff'
  surface-dim: '#ded7e4'
  surface-bright: '#fef7ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f8f1fe'
  surface-container: '#f3ebf8'
  surface-container-high: '#ede5f3'
  surface-container-highest: '#e7e0ed'
  on-surface: '#1d1a23'
  on-surface-variant: '#494454'
  inverse-surface: '#322f39'
  inverse-on-surface: '#f5eefb'
  outline: '#7b7486'
  outline-variant: '#cbc3d7'
  surface-tint: '#6d3bd7'
  primary: '#6b38d4'
  on-primary: '#ffffff'
  primary-container: '#8455ef'
  on-primary-container: '#fffbff'
  inverse-primary: '#d0bcff'
  secondary: '#a43073'
  on-secondary: '#ffffff'
  secondary-container: '#fc79bd'
  on-secondary-container: '#76014e'
  tertiary: '#765700'
  on-tertiary: '#ffffff'
  tertiary-container: '#956e00'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e9ddff'
  primary-fixed-dim: '#d0bcff'
  on-primary-fixed: '#23005c'
  on-primary-fixed-variant: '#5516be'
  secondary-fixed: '#ffd8e7'
  secondary-fixed-dim: '#ffafd3'
  on-secondary-fixed: '#3d0026'
  on-secondary-fixed-variant: '#85145a'
  tertiary-fixed: '#ffdf9f'
  tertiary-fixed-dim: '#f9bd22'
  on-tertiary-fixed: '#261a00'
  on-tertiary-fixed-variant: '#5c4300'
  background: '#fef7ff'
  on-background: '#1d1a23'
  surface-variant: '#e7e0ed'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-md:
    fontFamily: Outfit
    fontSize: 36px
    fontWeight: '800'
    lineHeight: '1.2'
  headline-lg:
    fontFamily: Outfit
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1.3'
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '500'
    lineHeight: '1.6'
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '500'
    lineHeight: '1.6'
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '700'
    lineHeight: '1.2'
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  gutter: 20px
  margin: 32px
---

## Brand & Style
The design system for "重启人生沙盘模拟" is built on the philosophy of **"Stable Grid, Wild Decoration."** It targets a demographic that enjoys simulation, strategy, and self-expression. The UI evokes a sense of tactile play—like a physical board game or a high-end stationery set.

The style is **Playful Geometric**, blending elements of "Neo-Brutalisim" (hard shadows, thick strokes) with a warm, "Pop" aesthetic. The interface is grounded by a rigorous underlying grid to ensure clarity in complex simulation data, while "wild" decorative elements—confetti, dot grids, and dashed lines—inject energy and a sense of chaotic life-possibility into the desktop experience.

## Colors
The palette uses a warm cream base to reduce eye strain during long simulation sessions, contrasting with a high-visibility Slate 800 for legibility.

- **Primary (Vivid Violet):** Represents Career, Ambition, and Status.
- **Secondary (Hot Pink):** Represents Life, Social, and Relationships.
- **Tertiary (Amber):** Represents Wealth and Resources.
- **Quaternary (Emerald):** Represents Health, Energy, and Stamina.

Functional colors (Success/Error) should align with the Emerald and Hot Pink hues respectively to maintain the "Pop" aesthetic.

## Typography
Typography is a mix of high-energy geometric headings and highly readable humanist body text. 

- **Headings:** Use **Outfit** in Bold or ExtraBold. These should feel impactful and "chunky." For Chinese characters, use a matching high-weight sans-serif (e.g., Noto Sans SC Bold) to maintain the visual weight.
- **Body & Data:** Use **Plus Jakarta Sans** in Medium. The increased x-height and open apertures ensure that dense simulation logs and attribute lists remain comfortable to read.
- **Emphasis:** Use the primary/secondary colors for key numbers and life events within the body text.

## Layout & Spacing
The layout follows a **Fixed Grid** philosophy for the main desktop stage, centered at 1280px or 1440px. 

- **Grid:** A 12-column grid with a 20px gutter.
- **Rhythm:** All spacing must be multiples of 4px. Use 16px (md) for standard internal padding and 24px (lg) for section separation.
- **Canvas:** The "Sandbox" area uses a flexible layout where elements are connected by **dashed lines** (2px width, 4px dash/gap) to show life-path progressions.
- **Decoration:** Backgrounds of containers should occasionally feature a "Dot Grid" pattern (1px dots, 12px apart in Slate 800 at 5% opacity).

## Elevation & Depth
This design system rejects traditional soft shadows in favor of **Hard Geometric Shadows**.

- **Shadow Style:** Use a 4px offset (bottom-right) with 0px blur. The shadow color is always the Foreground color (#1E293B). 
- **Borders:** Every interactive or containing element must have a 2px solid border in either the Foreground color or a subtle Border color (#E2E8F0) depending on importance.
- **Layers:** 
    - Base: Background Cream.
    - Level 1 (Cards): White background + 2px Slate border + Hard Shadow.
    - Level 2 (Active/Hover): Card moves -2px -2px with an increased shadow of 6px 6px.

## Shapes
Shapes are intentionally geometric but "softened" to keep the vibe friendly.

- **Main Corners:** Use a radius of 16px (md) for all cards and large buttons. 
- **Small Elements:** Tooltips and tags use 8px (sm).
- **Decorations:** Use primitive geometries (Perfect circles, 45-degree triangles, and squiggles) as background floating elements to represent "life confetti." These should use the primary/secondary colors at 20% opacity.

## Components
### Buttons
- **Primary:** Violet background, White text, 2px Slate border, Hard Shadow. On click, the button shifts +2px down/right and the shadow disappears to simulate a physical press.
- **Ghost:** Transparent background, Slate border, no shadow until hover.

### Cards (Life Events)
- White background, 16px radius, 2px Slate border. 
- Top-right corner often features a "Confetti" decoration or a geometric icon representing the event category (Career, Wealth, etc.).

### Input Fields
- White background, 2px border (#E2E8F0). Focus state changes border to Primary (Violet) with a 2px hard shadow.

### Progress Bars (Attributes)
- Thick (12px) tracks. Use Quaternary (Emerald) for Stamina and Tertiary (Amber) for Money. The track should have a 2px border, and the fill should be a solid, non-gradient color.

### Dashed Connectors
- Used to link "Choice" nodes in the sandbox. Use a 2px stroke width with a rounded cap.