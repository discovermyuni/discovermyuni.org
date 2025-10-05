# Frontend Build Instructions

## Quick Start

### Option 1: Python Build Script (Recommended)
```bash
python build.py
```

### Option 2: Manual Tailwind Compilation
```bash
# If npm works on your system:
npm run build

# Or use npx directly:
npx tailwindcss -i .\discovermyuni\static\css\tailwind.css -o .\discovermyuni\static\css\tailwind.build.css --minify
```

### Option 3: Development Mode (Auto-rebuild)
```bash
npx tailwindcss -i .\discovermyuni\static\css\tailwind.css -o .\discovermyuni\static\css\tailwind.build.css --watch
```

## Frontend Features Completed

### ✅ Modern Design System
- **Tailwind CSS** integration with custom brand colors
- **Dark/Light theme** with persistent localStorage
- **Component layer** with reusable button and card styles
- **Professional navbar** with profile integration and search
- **Responsive layout** with desktop sidebar and mobile drawer

### ✅ Navigation & Layout
- **3-column layout**: Left sidebar, main content, optional right sidebar
- **Sticky navigation** with proper z-index and positioning
- **Mobile-first responsive** design with AlpineJS interactions
- **Active state highlighting** for current page/section

### ✅ Pages Redesigned
- **Home page**: Modern hero section with gradients and feature grid
- **Post cards**: Vote columns, metadata display, responsive images
- **Post composer**: Clean form with proper styling
- **Organization pages**: Community management and browsing
- **Dashboard**: User management interface
- **User profiles**: Profile forms and detail views
- **Error pages**: Professional 404/500 pages with helpful actions

### ✅ Interactive Elements
- **Theme toggle** with sun/moon SVG icons
- **User dropdown** with profile picture and menu
- **Mobile drawer** with smooth slide animations
- **Post voting** interface (UI ready)
- **Search bar** (UI ready for backend integration)

### ✅ Technical Implementation
- **AlpineJS** for lightweight interactions
- **CSS Grid & Flexbox** for modern layouts
- **PostCSS** processing pipeline
- **Build optimization** with minified output
- **Accessibility** considerations with proper ARIA labels

## File Structure

```
discovermyuni/
├── static/css/
│   ├── tailwind.css         # Source CSS with @tailwind directives
│   ├── tailwind.build.css   # Compiled output (generated)
│   └── project.css          # Legacy CSS (minimal)
├── templates/
│   ├── base.html           # Master layout with Tailwind
│   ├── partials/navbar.html # Modern navbar component
│   ├── pages/home.html     # Landing page
│   ├── posts/              # Post-related templates
│   ├── dashboard/          # User dashboard
│   └── users/              # User profile templates
└── static/js/
    └── reddit.js           # Enhanced interactions
```

## Theme System

The application supports automatic dark/light mode switching:

- **System preference detection**: Respects `prefers-color-scheme`
- **Manual toggle**: Sun/moon button in navbar
- **Persistent storage**: Choice saved in localStorage
- **Dual class system**: Both `theme-dark` and `dark` classes for compatibility

## Mobile Experience

- **Responsive breakpoints**: Mobile, tablet, desktop optimization
- **Touch-friendly**: Proper button sizes and touch targets
- **Slide drawer**: Native mobile navigation pattern
- **Performance**: Optimized animations and transitions

## Next Steps

1. **Search functionality**: Connect search bar to backend
2. **Comment system**: Add comment threads to posts
3. **Real-time features**: WebSocket integration for live updates
4. **PWA features**: Service worker and offline support
5. **Performance**: Image optimization and lazy loading

## Browser Support

- **Modern browsers**: Chrome, Firefox, Safari, Edge (latest 2 versions)
- **CSS Grid/Flexbox**: Full support required
- **JavaScript ES6+**: For AlpineJS functionality
- **CSS Custom Properties**: For theming system