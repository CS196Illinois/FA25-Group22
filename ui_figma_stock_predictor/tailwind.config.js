/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand gradient (from Figma)
        brand: {
          start: '#3C24B3',
          end: '#502D69',
        },
        // Accents and status
        primary: '#1F6FEB',
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
        // Neutrals
        ink: {
          900: '#070606',
          800: '#170808',
          700: '#080404',
        },
        paper: {
          50: '#FFFFFF',
          100: '#F9FAFB',
          200: '#F3F4F6',
        },
      },
      fontFamily: {
        // Map Figma fonts to available web-safe fallbacks
        display: ['Jockey One', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
        heading: ['Mukta', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        condensed: ['Khand', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        icon: ['Jua', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
