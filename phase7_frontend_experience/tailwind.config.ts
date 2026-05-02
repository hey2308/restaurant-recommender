import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Zomato-inspired color palette
        primary: {
          DEFAULT: '#CB202D',
          dark: '#A61B24',
          light: '#E85D68',
        },
        secondary: {
          DEFAULT: '#2D2D2D',
          dark: '#1C1C1C',
          light: '#686B78',
        },
        accent: {
          DEFAULT: '#F4F4F4',
          dark: '#E8E8E8',
          light: '#FAFAFA',
        },
        success: '#4CAF50',
        warning: '#FF9800',
        rating: {
          high: '#4CAF50',
          medium: '#FF9800',
          low: '#F44336',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        card: '0 2px 8px rgba(0, 0, 0, 0.08)',
        'card-hover': '0 4px 16px rgba(0, 0, 0, 0.12)',
      },
    },
  },
  plugins: [],
};

export default config;
