import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
		extend: {
			colors: {
				main: '#88aaee',
				mainAccent: '#4d80e6', // not needed for shadcn components
				overlay: 'rgba(0,0,0,0.8)', // background color overlay for alert dialogs, modals, etc.
	
				// light mode
				bg: '#dfe5f2',
				text: '#000',
				border: '#000',
	
				// dark mode
				darkBg: '#272933',
				darkText: '#eeefe9',
				darkBorder: '#000',
				secondaryBlack: '#1b1b1b', // opposite of plain white, not used pitch black because borders and box-shadows are that color 
			},
			borderRadius: {
				base: '2px'
			},
			boxShadow: {
				light: '-1px 0px 0px 0px #000',
				dark: '-1px 0px 0px 0px #000',
			},
			translate: {
				boxShadowX: '-1px',
				boxShadowY: '0px',
				reverseBoxShadowX: '1px',
				reverseBoxShadowY: '0px',
			},
			fontWeight: {
				base: '500',
				heading: '700',
			},
      fontFamily: {
        sans: ['Work Sans', 'sans-serif'], // Update with your font
      },
		},
	},
  plugins: [require("tailwindcss-animate")],
};

export default config;
