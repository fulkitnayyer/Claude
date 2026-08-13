export const SITE = {
  name: 'Structure',
  legalName: 'Structure Ads',
  tagline: 'Google Ads and Meta Ads, run by an ex-Google Account Strategist',
  url: 'https://structureads.in',
  description:
    "Google Ads and Meta Ads management for local businesses and white-label execution for agencies. Run by a former Google Ads Account Strategist. Free account audit before you pay anything.",
  locale: 'en-IN',
  phone: '[PLACEHOLDER: +91 XXXXX XXXXX]',
  phoneRaw: '[PLACEHOLDER: 91XXXXXXXXXX]',
  whatsapp: '[PLACEHOLDER: 91XXXXXXXXXX]',
  email: '[PLACEHOLDER: hello@structureads.in]',
  address: 'Remote-first. Working with businesses across India.',
  areaServed: ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Pune', 'Hyderabad', 'Chandigarh', 'Jaipur', 'Ahmedabad'],
  founderName: 'Arjun Mehra',
} as const;

export const TRACKING = {
  gtmId: '[PLACEHOLDER: GTM-XXXXXXX]',
  ga4Id: '[PLACEHOLDER: G-XXXXXXXXXX]',
  googleAdsId: '[PLACEHOLDER: AW-XXXXXXXXX]',
  conversionLabel: '[PLACEHOLDER: conversion_label]',
} as const;

export const FORM = {
  endpoint: '[PLACEHOLDER: /api/lead]',
  whiteLabelEndpoint: '[PLACEHOLDER: /api/partner-lead]',
} as const;

export const NAV_LINKS = [
  { label: 'Services', href: '/services/' },
  { label: 'Industries', href: '/industries/' },
  { label: 'White-label', href: '/white-label/' },
  { label: 'How it works', href: '/how-it-works/' },
  { label: 'About', href: '/about/' },
  { label: 'Contact', href: '/contact/' },
] as const;

// Grouped for the lead-form Industry dropdown — home-services subcategories listed individually.
export const INDUSTRY_OPTIONS = [
  {
    group: 'Home & trade services',
    options: [
      'Plumbing',
      'Electrical',
      'HVAC / AC repair',
      'Pest control',
      'Home & office cleaning',
      'Appliance repair',
      'Roofing & waterproofing',
      'Interior design / renovation',
    ],
  },
  {
    group: 'Local services',
    options: [
      'Clinic / healthcare practice',
      'Salon / spa',
      'Gym / fitness studio',
      'Coaching centre / tuition',
      'Real estate agent / broker',
    ],
  },
  {
    group: 'Other',
    options: ['Other local business', 'Marketing agency (white-label)'],
  },
] as const;

export const AD_SPEND_RANGES = [
  { value: 'not-running', label: 'Not running ads yet' },
  { value: 'under-25k', label: 'Under ₹25,000/month' },
  { value: '25k-50k', label: '₹25,000 – ₹50,000/month' },
  { value: '50k-1.5l', label: '₹50,000 – ₹1,50,000/month' },
  { value: '1.5l-5l', label: '₹1,50,000 – ₹5,00,000/month' },
  { value: 'above-5l', label: 'Above ₹5,00,000/month' },
] as const;
