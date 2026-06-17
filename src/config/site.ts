export const SITE = {
  name: 'Clearbid',
  tagline: 'Google Ads Agency for Small Businesses in Delhi NCR',
  url: 'https://clearbid.in',
  description: 'We build, manage, and optimise Google Ads campaigns for SMBs across Delhi NCR. More qualified leads, less wasted ad spend.',
  locale: 'en-IN',
  phone: '[PLACEHOLDER: +91 XXXXX XXXXX]',
  phoneRaw: '[PLACEHOLDER: 91XXXXXXXXXX]',
  whatsapp: '[PLACEHOLDER: 91XXXXXXXXXX]',
  email: '[PLACEHOLDER: hello@clearbid.in]',
  address: 'Serving Delhi NCR',
  areaServed: ['Delhi', 'Gurgaon', 'Noida', 'Ghaziabad', 'Faridabad'],
} as const;

export const TRACKING = {
  gtmId: '[PLACEHOLDER: GTM-XXXXXXX]',
  ga4Id: '[PLACEHOLDER: G-XXXXXXXXXX]',
  googleAdsId: '[PLACEHOLDER: AW-XXXXXXXXX]',
  conversionLabel: '[PLACEHOLDER: conversion_label]',
} as const;

export const FORM = {
  endpoint: '[PLACEHOLDER: /api/contact]',
} as const;

export const NAV_LINKS = [
  { label: 'Services', href: '/services/' },
  { label: 'Results', href: '/results/' },
  { label: 'Pricing', href: '/pricing/' },
  { label: 'Industries', href: '/industries/' },
  { label: 'About', href: '/about/' },
  { label: 'Blog', href: '/blog/' },
] as const;
