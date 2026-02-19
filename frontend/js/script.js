/**
 * LORA REAL ESTATE - Frontend JS (DB-driven)
 * Loads all property content from the backend API (Render).
 */

// Configure API base URL (can be overridden by setting window.LORA_API_BASE_URL before this script loads)
const API_BASE_URL = window.LORA_API_BASE_URL || (
  (location.hostname === 'localhost' || location.hostname === '127.0.0.1')
    ? 'http://127.0.0.1:8000'
    : 'https://lorarealestate.onrender.com'
);

async function apiGet(path, params) {
  const url = new URL(path, API_BASE_URL);
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      if (v === undefined || v === null || v === '') return;
      url.searchParams.set(k, String(v));
    });
  }
  const res = await fetch(url.toString(), { headers: { 'Accept': 'application/json' } });
  if (!res.ok) throw new Error(`API GET failed (${res.status})`);
  return await res.json();
}

async function apiPost(path, body) {
  const url = new URL(path, API_BASE_URL);
  const res = await fetch(url.toString(), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(body || {})
  });
  if (!res.ok) {
    let errText = '';
    try { errText = JSON.stringify(await res.json()); } catch { errText = await res.text(); }
    throw new Error(`API POST failed (${res.status}): ${errText}`);
  }
  return await res.json();
}

/**
 * Initialize mobile navigation toggle
 */
function initNavToggle() {
  const toggle = document.querySelector('.nav-toggle');
  const menu = document.querySelector('.nav-menu');
  if (!toggle || !menu) return;

  // Create backdrop and close button for mobile
  let backdrop = document.querySelector('.nav-backdrop');
  if (!backdrop) {
    backdrop = document.createElement('div');
    backdrop.className = 'nav-backdrop';
    backdrop.setAttribute('aria-hidden', 'true');
    menu.parentNode.insertBefore(backdrop, menu);
  }

  const closeBtn = document.createElement('button');
  closeBtn.className = 'nav-close';
  closeBtn.setAttribute('aria-label', 'Close menu');
  closeBtn.innerHTML = '&times;';
  closeBtn.type = 'button';
  menu.insertBefore(closeBtn, menu.firstChild);

  function closeMenu() {
    menu.classList.remove('open');
    backdrop.classList.remove('open');
    document.body.style.overflow = '';
  }

  function openMenu() {
    menu.classList.add('open');
    backdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  toggle.addEventListener('click', () => {
    if (menu.classList.contains('open')) closeMenu();
    else openMenu();
  });

  closeBtn.addEventListener('click', closeMenu);
  backdrop.addEventListener('click', closeMenu);

  menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });
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
 * Format price for display. currency: 'USD' or 'TZS' (default TZS)
 */
function formatPrice(price, currency) {
  const n = typeof price === 'string' ? Number(price) : price;
  if (!Number.isFinite(n)) return '';
  const c = (currency || 'TZS').toUpperCase();
  if (c === 'USD') {
    return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
  }
  if (n >= 1000000000) {
    return (n / 1000000000).toFixed(1).replace(/\.0$/, '') + 'B TZS';
  }
  if (n >= 1000000) {
    return (n / 1000000).toFixed(1).replace(/\.0$/, '') + 'M TZS';
  }
  if (n >= 1000) {
    return (n / 1000).toFixed(0) + 'K TZS';
  }
  return n.toLocaleString('en-TZ') + ' TZS';
}

function formatLocation(location) {
  if (!location) return '';
  const name = location.name || '';
  const city = location.city || '';
  return [name, city].filter(Boolean).join(', ');
}

function normalizeApiList(data) {
  // DRF pagination returns {count,next,previous,results}
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data.results)) return data.results;
  return [];
}

/**
 * Create property card HTML
 */
function createPropertyCard(property) {
  const currency = property.currency || 'TZS';
  const price = property.listing_type === 'sale'
    ? formatPrice(property.price, currency)
    : `${formatPrice(property.price, currency)}/month`;
  const badgeClass = property.listing_type === 'sale' ? 'badge-sale' : 'badge-rent';
  const badgeText = property.listing_type === 'sale' ? 'For Sale' : 'For Rent';
  const isOccupied = property.availability === 'occupied' || property.availability === 'booked';
  const featureParts = [];
  if (property.bedrooms != null && property.bedrooms !== '') featureParts.push(`<span>${property.bedrooms} Beds</span>`);
  if (property.bathrooms != null && property.bathrooms !== '') featureParts.push(`<span>${property.bathrooms} Baths</span>`);
  if (property.area_size != null && property.area_size !== '') featureParts.push(`<span>${property.area_size} m²</span>`);
  const features = featureParts.length
    ? `<div class="property-features">${featureParts.join('')}</div>`
    : '';

  const imageHtml = property.main_image
    ? `<img src="${property.main_image}" alt="${property.title}" loading="lazy">`
    : `<div class="property-card-noimage" aria-label="No image available">No image</div>`;

  return `
    <article class="property-card">
      <div class="property-card-image">
        ${imageHtml}
        <span class="property-badge ${badgeClass}">${badgeText}</span>
        ${isOccupied ? '<span class="property-badge badge-occupied">Occupied</span>' : ''}
      </div>
      <div class="property-card-body">
        <div class="property-price">${price}</div>
        <div class="property-location">${formatLocation(property.location)}</div>
        ${features}
        <a href="property.html?id=${property.id}" class="btn btn-primary">View Details</a>
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
 * Fetch properties from backend API
 */
async function fetchProperties(params) {
  const data = await apiGet('/api/properties/', params || {});
  return normalizeApiList(data);
}

/**
 * Fetch locations from backend API (admin-added only)
 */
async function fetchLocations() {
  const data = await apiGet('/api/locations/', {});
  return Array.isArray(data) ? data : (data.results || []);
}

/**
 * Populate location select with admin-added locations
 */
async function populateLocationSelect() {
  const select = document.getElementById('location');
  if (!select) return;
  try {
    const locations = await fetchLocations();
    locations.forEach((loc) => {
      const display = loc.city ? `${loc.name}, ${loc.city}` : loc.name;
      const opt = document.createElement('option');
      opt.value = loc.name;
      opt.textContent = display;
      select.appendChild(opt);
    });
  } catch (e) {
    console.error('Could not load locations:', e);
  }
}

/**
 * Initialize quick filter form (home page)
 */
function initQuickFilter() {
  const form = document.getElementById('quickFilterForm');
  if (!form) return;

  populateLocationSelect();

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const type = form.querySelector('[name="type"]')?.value;
    const page = type === 'rent' ? 'rent.html' : 'buy.html';
    const params = new URLSearchParams();
    const location = form.querySelector('[name="location"]')?.value;
    const availability = form.querySelector('[name="availability"]')?.value;
    const minPrice = form.querySelector('[name="minPrice"]')?.value;
    const maxPrice = form.querySelector('[name="maxPrice"]')?.value;
    if (location) params.set('location', location);
    if (availability) params.set('availability', availability);
    if (minPrice) params.set('min_price', minPrice);
    if (maxPrice) params.set('max_price', maxPrice);
    window.location.href = page + (params.toString() ? '?' + params.toString() : '');
  });
}

/**
 * Initialize contact form (no backend - just feedback)
 */
function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      full_name: form.querySelector('[name="name"]')?.value?.trim() || '',
      email: form.querySelector('[name="email"]')?.value?.trim() || '',
      phone: form.querySelector('[name="phone"]')?.value?.trim() || '',
      message: form.querySelector('[name="message"]')?.value?.trim() || ''
    };
    try {
      await apiPost('/api/inquiries/', payload);
      alert('Thank you! Your inquiry has been sent.');
      form.reset();
    } catch (err) {
      alert('Sorry—your inquiry could not be sent. Please try again.');
      console.error(err);
    }
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
