# Theme Switching Guide

This documentation site features a dynamic theme switching system that allows you to choose between different visual styles.

## Available Themes

### 🏛️ NPS Classic
- **Style**: Professional Naval Postgraduate School branding
- **Colors**: Navy blue and gold color scheme
- **Features**: Clean, academic appearance with NPS-specific styling
- **Best for**: Official documentation, academic presentations

### ✨ Modern
- **Style**: Contemporary glassmorphism design
- **Colors**: Purple gradients with modern aesthetics
- **Features**: Backdrop blur effects, smooth animations, gradient text
- **Best for**: Modern web applications, creative projects

## How to Switch Themes

### Using the Theme Switcher Widget
1. Look for the floating **🎨 Theme** widget on the right side of your screen
2. Click on either:
   - **🏛️ NPS Classic** for the professional theme
   - **✨ Modern** for the contemporary theme
3. The theme will switch immediately and your preference will be saved

### Keyboard Shortcut
- Press **Ctrl + Shift + T** to cycle between themes quickly

## Features

### Persistent Preferences
- Your theme choice is automatically saved in your browser
- The selected theme will be remembered when you return to the site
- Theme preference persists across all pages of the documentation

### Responsive Design
- Both themes are fully responsive and work on all device sizes
- On mobile devices, the theme switcher adapts to a more compact layout
- Theme icons remain visible even on smaller screens

### Dark Mode Compatibility
- Both themes support the built-in Material theme dark/light mode toggle
- The theme switcher widget adapts its appearance based on the current color scheme
- Themes work seamlessly with both light and dark modes

## Technical Details

### Implementation
- Built with vanilla JavaScript for maximum compatibility
- Uses CSS custom properties for efficient theme switching
- Leverages modern CSS features like backdrop-filter and CSS Grid
- Fully accessible with proper focus management and keyboard navigation

### Browser Support
- Works in all modern browsers that support CSS custom properties
- Gracefully degrades in older browsers
- No external dependencies required

## Customization

The theme system is designed to be easily extensible. Additional themes can be added by:

1. Creating new CSS files in the `docs/stylesheets/` directory
2. Adding theme configurations to the JavaScript theme switcher
3. Following the established naming conventions and structure

## Accessibility

- All theme controls are keyboard accessible
- Proper ARIA labels and focus management
- High contrast ratios maintained in both themes
- Screen reader compatible
