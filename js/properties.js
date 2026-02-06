/**
 * ROLA REAL ESTATE - Property Data
 * Locations: Dar es Salaam, Tanzania | Currency: TZS
 * Structured for easy replacement with API/database later
 */

var PROPERTIES = [
  {
    id: 1,
    title: "Modern Villa with Pool in Oyster Bay",
    status: "sale",
    price: 1850000000,
    rentPrice: null,
    location: "Oyster Bay, Dar es Salaam",
    description: "Stunning modern villa featuring an open-plan living area, premium finishes, and a private pool. Perfect for families seeking luxury and comfort. The property includes a spacious garden, covered parking, and smart home features. Located in one of Dar es Salaam's most exclusive neighborhoods.",
    bedrooms: 4,
    bathrooms: 3,
    size: 280,
    images: [
      { url: "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800", label: "Exterior" },
      { url: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800", label: "Living Room" },
      { url: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800", label: "Kitchen" },
      { url: "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800", label: "Pool & Garden" }
    ],
    featured: true
  },
  {
    id: 2,
    title: "Cozy 2-Bedroom Apartment in City Centre",
    status: "rent",
    price: null,
    rentPrice: 2500000,
    location: "City Centre, Dar es Salaam",
    description: "Bright and welcoming apartment in the heart of Dar es Salaam. Walking distance to shops, restaurants, banks, and public transport. Includes fitted kitchen, built-in wardrobes, and balcony with city views.",
    bedrooms: 2,
    bathrooms: 2,
    size: 95,
    images: [
      { url: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800", label: "Exterior" },
      { url: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800", label: "Living Area" },
      { url: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800", label: "Bedroom" }
    ],
    featured: true
  },
  {
    id: 3,
    title: "Luxury Penthouse with Sea Views",
    status: "sale",
    price: 3200000000,
    rentPrice: null,
    location: "Masaki, Dar es Salaam",
    description: "Exceptional penthouse with panoramic sea views. Features floor-to-ceiling windows, private terrace, premium appliances, and 24/7 security. A rare opportunity for discerning buyers in Dar es Salaam's prime waterfront.",
    bedrooms: 3,
    bathrooms: 3,
    size: 220,
    images: [
      { url: "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800", label: "Exterior" },
      { url: "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800", label: "Sea View Terrace" },
      { url: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800", label: "Interior" }
    ],
    featured: true
  },
  {
    id: 4,
    title: "Family House with Garden in Mikocheni",
    status: "rent",
    price: null,
    rentPrice: 4200000,
    location: "Mikocheni, Dar es Salaam",
    description: "Spacious family home with a large garden, ideal for children and pets. Features a separate dining room, study, and garage. Quiet neighborhood with excellent schools and amenities nearby.",
    bedrooms: 4,
    bathrooms: 2,
    size: 180,
    images: [
      { url: "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800", label: "Exterior" },
      { url: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800", label: "Living Room" }
    ],
    featured: true
  },
  {
    id: 5,
    title: "Contemporary Townhouse in Msasani",
    status: "sale",
    price: 980000000,
    rentPrice: null,
    location: "Msasani, Dar es Salaam",
    description: "Elegant townhouse with modern design. Three floors of living space, rooftop terrace, and underground parking. Low maintenance, high quality finishes throughout.",
    bedrooms: 3,
    bathrooms: 2,
    size: 150,
    images: [
      { url: "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800", label: "Exterior" },
      { url: "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800", label: "Interior" }
    ],
    featured: false
  },
  {
    id: 6,
    title: "Studio Apartment Near University",
    status: "rent",
    price: null,
    rentPrice: 950000,
    location: "Sinza, Dar es Salaam",
    description: "Compact studio perfect for students or young professionals. Fully furnished, includes utilities. Walking distance to university and public transport.",
    bedrooms: 1,
    bathrooms: 1,
    size: 45,
    images: [
      { url: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800", label: "Interior" }
    ],
    featured: false
  },
  {
    id: 7,
    title: "Executive Apartment with Parking",
    status: "sale",
    price: 650000000,
    rentPrice: null,
    location: "Upanga, Dar es Salaam",
    description: "Move-in ready executive apartment. Features high-end finishes, secure parking, and building amenities including gym. Ideal for professionals.",
    bedrooms: 2,
    bathrooms: 2,
    size: 110,
    images: [
      { url: "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800", label: "Exterior" },
      { url: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800", label: "Interior" }
    ],
    featured: false
  },
  {
    id: 8,
    title: "Charming Duplex in Kawe",
    status: "rent",
    price: null,
    rentPrice: 3500000,
    location: "Kawe, Dar es Salaam",
    description: "Character duplex with modern features. Spacious layout, private courtyard, and garden. Perfect blend of comfort and convenience.",
    bedrooms: 3,
    bathrooms: 2,
    size: 130,
    images: [
      { url: "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800", label: "Exterior" },
      { url: "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800", label: "Living Room" }
    ],
    featured: false
  }
];
