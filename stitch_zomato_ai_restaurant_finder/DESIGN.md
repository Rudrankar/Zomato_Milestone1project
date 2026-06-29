---
name: Gourmet Intelligence
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#5b403f'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f1f1f1'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#835500'
  on-secondary: '#ffffff'
  secondary-container: '#feae2c'
  on-secondary-container: '#6b4500'
  tertiary: '#006762'
  on-tertiary: '#ffffff'
  tertiary-container: '#00837c'
  on-tertiary-container: '#f3fffd'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#ffddb4'
  secondary-fixed-dim: '#ffb955'
  on-secondary-fixed: '#291800'
  on-secondary-fixed-variant: '#633f00'
  tertiary-fixed: '#8ef4eb'
  tertiary-fixed-dim: '#71d7cf'
  on-tertiary-fixed: '#00201e'
  on-tertiary-fixed-variant: '#00504c'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-padding-mobile: 16px
  container-padding-desktop: 32px
  gutter: 20px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style

The design system is engineered for a premium AI-driven dining discovery experience. The personality is professional, modern, and highly appetizing, positioning the tool as a discerning digital concierge rather than a simple directory.

The aesthetic blends **Modern Minimalism** with **Glassmorphism**. High-quality food photography is the hero of the interface, supported by a clean, airy layout that utilizes heavy whitespace to reduce cognitive load during the decision-making process. Translucent layers and frosted glass effects are used to create a sense of depth and sophistication, while bold typography ensures a clear information hierarchy.

## Colors

This design system uses a focused palette to drive action and highlight quality.

- **Primary (#E23744):** Reserved for high-priority actions, primary buttons, and critical UI states. It evokes hunger and energy.
- **Secondary/Gold (#F5A623):** Used exclusively for ratings, rewards, and "Elite" status indicators to signify value and excellence.
- **Backgrounds:** The interface utilizes a "layered white" approach. The base background is a clean off-white (#F8F8F8) to reduce glare, while interactive containers and cards use pure white (#FFFFFF) to pop from the surface.
- **System Colors:** Success (Green), Warning (Amber), and Error (Red) should be used sparingly for form validation and status updates.

## Typography

The typography strategy leverages two distinct sans-serifs to balance personality with readability.

- **Outfit** is used for headlines and display text. Its geometric yet friendly curves provide a modern, high-end feel.
- **Inter** is used for all body copy, labels, and data-heavy components. Its high x-height and exceptional legibility ensure that restaurant details and menu items are easily scannable.

**Scalability:**
For mobile viewports, headlines scale down by 15-20% to maintain visual balance. Body text remains at a minimum of 16px for optimal accessibility in varying lighting conditions (e.g., outdoor mobile use).

## Layout & Spacing

This design system employs a **12-column fluid grid** for desktop and a **4-column fluid grid** for mobile. 

- **The 8px Rhythm:** All spacing increments (padding, margin, gaps) are multiples of 4px, with 8px being the baseline "small" unit.
- **Card Layouts:** On desktop, restaurant listings should follow a grid-based card layout. On mobile, these transition to a vertical stack with full-bleed imagery or generous 16px horizontal margins.
- **AI Chat/Recommendations:** Use a centered, max-width container (approx. 800px) for AI-driven conversational interfaces to maintain focus and readability.

## Elevation & Depth

Hierarchy is established through **Glassmorphism** and **Ambient Shadows**.

- **Level 0 (Base):** Off-white background (#F8F8F8).
- **Level 1 (Cards):** Pure white surfaces with a soft, 15% opacity shadow (Blur: 20px, Y: 4px).
- **Level 2 (Overlays/Modals):** Glassmorphism effect. Use a semi-transparent white background (60% opacity) with a 20px backdrop-blur and a subtle 1px white border.
- **Depth:** Avoid heavy, dark shadows. All shadows should use a slight tint of the primary color or a neutral grey to maintain a clean, high-end appearance.

## Shapes

The design system utilizes generous rounding to appear approachable and friendly.

- **Default (rounded-md):** 8px for small components like checkboxes and input fields.
- **Large (rounded-xl):** 12px for standard restaurant cards and action buttons.
- **Extra Large (rounded-2xl):** 24px for prominent feature banners and major UI containers.
- **Interactive Elements:** Buttons should always have at least a 12px radius to match the card language, creating a unified visual flow.

## Components

**Buttons:**
- **Primary:** Filled #E23744 with white text. 12px corner radius. Subtle hover state: slightly darker red.
- **Secondary:** Transparent background with #E23744 border and text.
- **Ghost:** Minimalist text-only buttons for tertiary actions.

**Cards:**
- Restaurant cards are the core component. They must feature a high-aspect-ratio image at the top with a 12px radius. Information is housed in a white container below.
- Use the Gold (#F5A623) color for star icons and numerical ratings.

**AI Interaction:**
- The AI "Thought" or "Typing" indicator should use a soft glassmorphic bubble to distinguish it from static content.
- Use a "Sparkle" icon in the primary color to denote AI-generated suggestions.

**Input Fields:**
- Clean, 1px border (#E0E0E0) that turns Primary Red on focus. 
- Backgrounds should be pure white for maximum contrast against the #F8F8F8 page background.

**Chips/Badges:**
- Used for cuisine types (e.g., "Italian," "Vegan").
- Style: Light grey background (#EEEEEE) with 100px (pill) radius and 12px Inter font.