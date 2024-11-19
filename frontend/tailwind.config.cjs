/** @type {import('tailwindcss').Config}*/
const config = {
  content: ["./src/**/*.{html,js,svelte,ts}"],

  theme: {
    extend: {
      fontFamily: {
        int: ["Inter", "sans-serif"],
      },
      gap: {
        "form-field": "8px",
      },
      maxWidth: {
        "form-field": "350px",
      },
      minWidth: {
        "form-field": "350px",
      },
      colors: {
        primary: {
          25: "#FCFCFD",
          50: "#F9FAFB",
          100: "#F2F4F7",
          200: "#EAECF0",
          300: "#D0D5DD",
          400: "#98A2B3",
          500: "#667085",
          600: "#475467",
          700: "#344054",
          800: "#1D2939",
          900: "#101828",
          950: "#030712",
        },
        gray: {
          25: "#FCFCFD",
          50: "#F9FAFB",
          100: "#F2F4F7",
          200: "#EAECF0",
          300: "#D0D5DD",
          400: "#98A2B3",
          500: "#667085",
          600: "#475467",
          700: "#344054",
          800: "#1D2939",
          900: "#101828",
        },
        brand: {
          '50': '#fdf4ff',
          '100': '#fbe8ff',
          '200': '#f6d0fe',
          '300': '#edabfc',
          '400': '#e279f9',
          '500': '#d046ef',
          '600': '#b426d3',
          '700': '#941caf',
          '800': '#7a198f',
          '900': '#641a75',
          '950': '#41044e',
        },
        error: {
          50: "#FEF3F2",
          100: "#FEE4E2",
          200: "#ABEFC6",
          700: "#B42318",
        },
        success: {
          50: "#ECFDF3",
          200: "#ABEFC6",
          700: "#067647",
        },
      },
    },

    fontSize: {
      xs: [
        "0.75rem",
        {
          lineHeight: "1.125rem",
        },
      ],
      sm: [
        "0.875rem",
        {
          lineHeight: "1.25rem",
        },
      ],
      md: [
        "1rem",
        {
          lineHeight: "1.5rem",
        },
      ],
      lg: [
        "1.125rem",
        {
          lineHeight: "1.75rem",
        },
      ],
      xl: [
        "1.25rem",
        {
          lineHeight: "1.875rem",
        },
      ],
      "2xl": [
        "1.5rem",
        {
          lineHeight: "2rem",
        },
      ],
      "3xl": [
        "1.875rem",
        {
          lineHeight: "2.375rem",
        },
      ],
      "4xl": [
        "2.25rem",
        {
          lineHeight: "2.75rem",
          letterSpacing: "-0.045rem",
        },
      ],
      "5xl": [
        "3rem",
        {
          lineHeight: "3.75rem",
          letterSpacing: "-0.06rem",
        },
      ],
      "6xl": [
        "3.75rem",
        {
          lineHeight: "4.5rem",
          letterSpacing: "-0.075rem",
        },
      ],
      "7xl": [
        "4.5rem",
        {
          lineHeight: "5.625rem",
          letterSpacing: "-0.09rem",
        },
      ],
    },
    boxShadow: {
      none: "none",
      xs: "0px 1px 2px rgba(16, 24, 40, 0.05)",
      sm: "0px 1px 3px rgba(16, 24, 40, 0.1), 0px 1px 2px rgba(16, 24, 40, 0.06)",
      md: "0px 4px 8px -2px rgba(16, 24, 40, 0.1), 0px 2px 4px -2px rgba(16, 24, 40, 0.06)",
      lg: "0px 12px 16px -4px rgba(16, 24, 40, 0.08), 0px 4px 6px -2px rgba(16, 24, 40, 0.03)",
      xl: "0px 20px 24px rgba(16, 24, 40, 0.08), 0px 8px 8px rgba(16, 24, 40, 0.03)",
      "2xl": "0px 24px 48px -12px rgba(16, 24, 40, 0.18)",
      "3xl": "0px 32px 64px -12px rgba(16, 24, 40, 0.14)",
      "table-container":
        "0px 1px 2px 0px rgba(16, 24, 40, 0.06),0px 1px 3px 0px rgba(16, 24, 40, 0.1);",
      "input-focus": "0px 0px 0px 4px #58585914",
      "input-blur": "0px 1px 2px 0px rgba(16, 24, 40, 0.05);",
      modal:
        "0px 1px 2px 0px rgba(16, 24, 40, 0.06),0px 1px 3px 0px rgba(16, 24, 40, 0.1)",
      error: "0px 0px 0px 4px #FEE4E2",
    },
    container: {
      center: true,
      padding: "2rem",
    },
    screens: {
      xs: "480px",
      sm: "640px",
      md: "768px",
      lg: "1024px",
      xl: "1280px",
      "2xl": "1536px",
    },
    keyframes: {
      fadeUp: {
        "0%": { opacity: 0, transform: "translateY(20px)" },
        "100%": { opacity: 1, transform: "translateY(0)" },
      },
    },
    animation: {
      fadeUp: "fadeUp 0.8s ease-out",
    },
  },
  plugins: [require("tailwind-scrollbar")],
};

module.exports = config;
