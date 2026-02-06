/**
 * LORA REAL ESTATE - Main JavaScript
 * Handles navigation, property filtering, WhatsApp, and shared UI
 */

// WhatsApp configuration - update with your business number (include country code, no + or spaces)
const WHATSAPP_NUMBER = "255788275367";
const DEFAULT_MESSAGE = "Hello, I am interested in this property from Lora Real Estate. Please share more details.";

/**
 * Initialize mobile navigation toggle
 */
function initNavToggle() {
  const toggle = document.querySelector('.nav-toggle');
  const menu = document.querySelector('.nav-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('open');
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });
    // Close menu when clicking a link
    menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        menu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
    // Close menu when clicking backdrop (outside menu)
    document.addEventListener('click', (e) => {
      if (menu.classList.contains('open') && !menu.contains(e.target) && !toggle.contains(e.target)) {
        menu.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }
}

/**
 * Set active nav link based on current page
 */
function setActiveNav() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-menu a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

/**
 * Format price for display (TZS - Tanzanian Shilling)
 */
function formatPrice(price) {
  if (price >= 1000000000) {
    return (price / 1000000000).toFixed(1).replace(/\.0$/, '') + 'B TZS';
  }
  if (price >= 1000000) {
    return (price / 1000000).toFixed(1).replace(/\.0$/, '') + 'M TZS';
  }
  if (price >= 1000) {
    return (price / 1000).toFixed(0) + 'K TZS';
  }
  return price.toLocaleString('en-TZ') + ' TZS';
}

/**
 * Get WhatsApp link with pre-filled message
 */
function getWhatsAppLink(message = DEFAULT_MESSAGE) {
  const encoded = encodeURIComponent(message);
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encoded}`;
}

/**
 * Open WhatsApp with property inquiry
 */
function openWhatsAppInquiry(property) {
  const message = property
    ? `Hello, I am interested in this property from Lora Real Estate: ${property.title}. Please share more details.`
    : DEFAULT_MESSAGE;
  window.open(getWhatsAppLink(message), '_blank');
}

/**
 * Create property card HTML
 */
function createPropertyCard(property) {
  const price = property.status === 'sale'
    ? formatPrice(property.price)
    : `${formatPrice(property.rentPrice)}/mo`;
  const badgeClass = property.status === 'sale' ? 'badge-sale' : 'badge-rent';
  const badgeText = property.status === 'sale' ? 'For Sale' : 'For Rent';
  const features = property.bedrooms && property.size
    ? `<div class="property-features">
         <span>🛏️ ${property.bedrooms} Beds</span>
         <span>🛁 ${property.bathrooms} Baths</span>
         <span>📐 ${property.size} m²</span>
       </div>`
    : '';

  return `
    <article class="property-card">
      <div class="property-card-image">
        <img src="${getImageUrl(property.images[0])}" alt="${property.title}" loading="lazy">
        <span class="property-badge ${badgeClass}">${badgeText}</span>
      </div>
      <div class="property-card-body">
        <div class="property-price">${price}</div>
        <div class="property-location">${property.location}</div>
        ${features}
        <a href="property.html#${property.id}" class="btn btn-primary">View Details</a>
      </div>
    </article>
  `;
}

/**
 * Render property grid
 */
function renderPropertyGrid(containerId, properties) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (!properties || properties.length === 0) {
    container.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1;">
        <h3>No properties found</h3>
        <p>Check back soon for new listings, or contact us to discuss your requirements.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = properties.map(p => createPropertyCard(p)).join('');
}

/**
 * Filter properties by status
 */
function getPropertiesByStatus(status) {
  return PROPERTIES.filter(p => p.status === status);
}

/**
 * Filter properties by URL params (location, min, max price)
 */
function filterByParams(properties, params) {
  let result = properties;
  const location = params.get('location');
  const min = params.get('min') ? parseInt(params.get('min'), 10) : null;
  const max = params.get('max') ? parseInt(params.get('max'), 10) : null;

  if (location) {
    const locLower = location.toLowerCase();
    result = result.filter(p => p.location.toLowerCase().includes(locLower));
  }
  if (min != null) {
    result = result.filter(p => {
      const price = p.status === 'sale' ? p.price : p.rentPrice;
      return price && price >= min;
    });
  }
  if (max != null) {
    result = result.filter(p => {
      const price = p.status === 'sale' ? p.price : p.rentPrice;
      return price && price <= max;
    });
  }
  return result;
}

/**
 * Get featured properties
 */
function getFeaturedProperties(limit = 4) {
  return PROPERTIES.filter(p => p.featured).slice(0, limit);
}

/**
 * Get single property by ID
 */
function getPropertyById(id) {
  return PROPERTIES.find(p => p.id === parseInt(id, 10));
}

/**
 * Get image URL from property image (supports string or {url, label})
 */
function getImageUrl(img) {
  return typeof img === 'string' ? img : img?.url || '';
}

/**
 * Get image label from property image
 */
function getImageLabel(img) {
  return typeof img === 'object' && img?.label ? img.label : '';
}

/**
 * Initialize quick filter form (home page)
 */
function initQuickFilter() {
  const form = document.getElementById('quickFilterForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const type = form.querySelector('[name="type"]')?.value;
    const page = type === 'rent' ? 'rent.html' : 'buy.html';
    const params = new URLSearchParams();
    const location = form.querySelector('[name="location"]')?.value;
    const minPrice = form.querySelector('[name="minPrice"]')?.value;
    const maxPrice = form.querySelector('[name="maxPrice"]')?.value;
    if (location) params.set('location', location);
    if (minPrice) params.set('min', minPrice);
    if (maxPrice) params.set('max', maxPrice);
    window.location.href = page + (params.toString() ? '?' + params.toString() : '');
  });
}

/**
 * Initialize contact form (no backend - just feedback)
 */
function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you for your message! We will get back to you soon. For urgent inquiries, please call or WhatsApp us.');
    form.reset();
  });
}

/**
 * Initialize on DOM ready
 */
document.addEventListener('DOMContentLoaded', () => {
  initNavToggle();
  setActiveNav();
  initQuickFilter();
  initContactForm();
});
