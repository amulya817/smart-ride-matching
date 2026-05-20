/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        rapido: {
          pink: '#F9A8D4', // Tailwind pink-300
          dark: '#EC4899', // Tailwind pink-500
          light: '#FDF2F8' // Tailwind pink-50
        },
        surface: {
          light: '#F3F4F6', // Tailwind gray-100
          dark: '#111827',  // Tailwind gray-900
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
