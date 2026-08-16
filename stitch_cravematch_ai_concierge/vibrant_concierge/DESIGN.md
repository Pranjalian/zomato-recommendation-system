---
name: Vibrant Concierge
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1c1b1b'
  on-surface-variant: '#5c403a'
  inverse-surface: '#313030'
  inverse-on-surface: '#f3f0ef'
  outline: '#916f69'
  outline-variant: '#e5bdb6'
  surface-tint: '#ba1c00'
  primary: '#b51c00'
  on-primary: '#ffffff'
  primary-container: '#dc3214'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb4a5'
  secondary: '#b90040'
  on-secondary: '#ffffff'
  secondary-container: '#de2656'
  on-secondary-container: '#fffbff'
  tertiary: '#725c00'
  on-tertiary: '#ffffff'
  tertiary-container: '#cca700'
  on-tertiary-container: '#4d3e00'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad3'
  primary-fixed-dim: '#ffb4a5'
  on-primary-fixed: '#3e0400'
  on-primary-fixed-variant: '#8e1300'
  secondary-fixed: '#ffd9dc'
  secondary-fixed-dim: '#ffb2ba'
  on-secondary-fixed: '#400011'
  on-secondary-fixed-variant: '#910031'
  tertiary-fixed: '#ffe07c'
  tertiary-fixed-dim: '#ecc200'
  on-tertiary-fixed: '#231b00'
  on-tertiary-fixed-variant: '#564500'
  background: '#fcf9f8'
  on-background: '#1c1b1b'
  surface-variant: '#e5e2e1'
typography:
  headline-xl:
    fontFamily: Montserrat
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Montserrat
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  2xl: 64px
  container-margin: 20px
  gutter: 16px
---

## Brand & Style

The brand personality is that of an expert, high-energy digital concierge—knowledgeable, fast, and visually appetizing. The target audience consists of urban foodies and travelers seeking immediate, high-quality dining recommendations. 

The design style is **Modern Corporate with a Tactile Edge**, leaning heavily into high-chroma colors and soft, organic shapes to evoke the warmth of hospitality. It utilizes subtle "AI Sparkle" accents—fine-grained gradients and shimmering borders—to signal the intelligence behind the platform without feeling overly "techy" or cold. The emotional goal is to make the user feel hungry and excited, providing a premium experience that feels both human and cutting-edge.

## Colors

The palette is anchored by a high-energy "Zest" gradient. **Primary (#FF4B2B)** provides the appetizing foundation, while **Secondary (#FF416C)** adds depth and a premium, berry-like warmth. 

- **Primary:** Used for main actions and brand identity.
- **Secondary:** Used for accents, heart icons, and secondary highlights.
- **AI Sparkle:** A three-stop gradient used exclusively for AI-generated insights, magic-search bars, and recommendation badges.
- **Neutral:** A deep charcoal (#1A1A1A) is used for text to ensure high legibility against the vibrant accents, avoiding pure black to maintain a softer, premium feel.
- **Semantic Colors:** Success (Green), Warning (Amber), and Error (Red) should be desaturated slightly to avoid clashing with the high-vibrancy primary palette.

## Typography

This design system uses a pairing of **Montserrat** for personality and **Inter** for utility.

- **Headlines:** Montserrat is set with tight letter-spacing and heavy weights to create a confident, bold presence.
- **Body:** Inter provides maximum readability for restaurant descriptions, reviews, and ingredient lists.
- **Labels:** Used for categories (e.g., "ITALIAN", "OPEN NOW"). These should be set in Inter SemiBold with slight tracking to provide a clean, organized look in small spaces.
- **Mobile Scaling:** Headlines above 32px should scale down on mobile devices to ensure the vibrant UI remains tight and readable without excessive scrolling.

## Layout & Spacing

The layout follows a **Fluid Mobile-First** model. 

- **Grid:** On mobile, use a single-column layout with 20px side margins. On desktop, transition to a 12-column grid with a max-width of 1200px.
- **Rhythm:** Use a 4px baseline shift. Most vertical gaps between related elements should be `md` (16px), while sections should be separated by `xl` (40px) to provide breathable whitespace.
- **Safe Areas:** Ensure that primary action buttons (like "Get Directions") are placed within the thumb-zone on mobile, utilizing a sticky bottom-bar with a backdrop-blur.

## Elevation & Depth

To achieve the "Concierge" feel, the system uses **Ambient Shadows** and **Tonal Layering**.

- **Level 1 (Cards):** Low-offset, highly diffused shadows using a hint of the primary color (e.g., `0px 4px 20px rgba(255, 75, 43, 0.08)`).
- **Level 2 (Modals/Overlays):** Increased blur and spread to lift the element significantly off the background.
- **Level 3 (Floating Actions):** Use a subtle glow effect rather than a traditional grey shadow to emphasize the "AI Sparkle" narrative.
- **Glassmorphism:** Use `backdrop-filter: blur(12px)` on top navigation bars and bottom action sheets to maintain context of the vibrant imagery behind the UI.

## Shapes

The design system uses a **Rounded (2xl)** language to feel approachable and friendly. 

- **Cards:** Use a generous 24px radius to soften the edges of high-density food photography.
- **Buttons:** Large buttons use a 16px radius, while secondary buttons and chips use a fully pill-shaped (100px) radius.
- **Interactive Elements:** Inputs and selection states should maintain a consistent 12px-16px radius to ensure the UI feels unified and soft to the touch.

## Components

- **AI Recommendation Cards:** Features the `primary-vibrant` gradient border (2px) and an "AI Sparkle" badge in the top right corner. Use high-quality imagery with a subtle dark overlay at the bottom for white text legibility.
- **Primary Buttons:** High-contrast `primary-vibrant` gradient backgrounds with white text. Apply a subtle lift effect on hover/active states.
- **Action Chips:** Used for filters like "Price," "Distance," and "Cuisine." Default state is a light grey stroke; active state is a solid `primary-color` fill with white text.
- **Search Bar:** A "Magic" search bar utilizing a subtle shimmering gradient border to indicate AI-assisted input.
- **Rating Component:** Instead of standard stars, use a customized "Flame" or "Plate" icon in the `tertiary_color_hex` (Yellow) to match the appetizing theme.
- **Lists:** Clean, borderless list items with `md` (16px) padding and subtle `surface-warm` background tints for alternating rows or categories.