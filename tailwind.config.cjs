/* Tailwind configuration for DiscoverMyUni */
module.exports = {
  darkMode: 'class',
  content: [
    './discovermyuni/templates/**/*.html',
    './discovermyuni/static/js/**/*.js'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50:'#fff6ed',100:'#ffe7d5',200:'#fdc9a8',300:'#fbab7a',400:'#fa8d4d',500:'#ff620e',600:'#e74704',700:'#bc3603',800:'#922802',900:'#5a1600'
        }
      },
      boxShadow: {
        'sm-brand':'0 1px 2px 0 rgba(0,0,0,.05)',
        'brand':'0 1px 3px 0 rgba(0,0,0,.12),0 1px 2px -1px rgba(0,0,0,.1)'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio')
  ]
};
