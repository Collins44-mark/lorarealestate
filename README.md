# Lora Real Estate

A modern, professional real estate website for buying and renting properties.

## Features

- **Home page** – Hero, quick filter, featured properties, Why Choose Us
- **Buy** – Grid of properties for sale
- **Rent** – Grid of rental properties
- **Property details** – Full listing with WhatsApp inquiry and call buttons
- **About** – Company overview, mission, and values
- **Contact** – Contact form, phone, WhatsApp, email, office address

## Tech Stack

- HTML5
- CSS3 (Flexbox + Grid)
- Vanilla JavaScript
- No frameworks

## Setup

1. Open `frontend/index.html` in a browser, or serve the `frontend/` folder with a local server:
   ```bash
   npx serve frontend
   ```

2. Update the WhatsApp number in `frontend/js/script.js` and in each HTML file (search for `1234567890`).

3. Add your logo: place `logo.png` in `frontend/images/`. The header and footer will display it; if missing, text "Lora Real Estate" shows instead.

4. Replace property images in `frontend/js/properties.js` with your own URLs, or add images to `frontend/images/` and reference them.

## File Structure

```
/
├── frontend/
│   ├── index.html
│   ├── buy.html
│   ├── rent.html
│   ├── property.html
│   ├── about.html
│   ├── contact.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── script.js
│   │   └── properties.js
│   └── images/
├── backend/
└── README.md
```

## Future-Ready

- Property data in `js/properties.js` can be replaced with API calls
- Clean structure for adding an admin panel or backend
- Commented code for easy maintenance
