/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        blue: "#00b2ff",
        secondary: "#C0BDBD",
        green: "#9BD491",
        red: "#FFD2DE",
        yellow: "FFCF87",
      },
    },
  },
  plugins: [],
};
