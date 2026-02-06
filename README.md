# Rola Real Estate

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

1. Open `index.html` in a browser, or serve the folder with a local server:
   ```bash
   npx serve .
   ```

2. Update the WhatsApp number in `js/script.js` and in each HTML file (search for `1234567890`).

3. Replace property images in `js/properties.js` with your own URLs, or add images to `/images/` and reference them.

## File Structure

```
/
├── index.html
├── buy.html
├── rent.html
├── property.html
├── about.html
├── contact.html
├── css/
│   └── style.css
├── js/
│   ├── script.js
│   └── properties.js
├── images/
└── README.md
```

## Future-Ready

- Property data in `js/properties.js` can be replaced with API calls
- Clean structure for adding an admin panel or backend
- Commented code for easy maintenance
