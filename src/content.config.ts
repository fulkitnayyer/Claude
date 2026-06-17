import { defineCollection, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

const testimonials = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/testimonials' }),
  schema: z.object({
    quote: z.string(),
    name: z.string(),
    company: z.string(),
    industry: z.string(),
    photo: z.string().optional(),
    resultMetric: z.string().optional(),
    consent: z.boolean().default(false),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    author: z.string().default('Clearbid'),
    tags: z.array(z.string()).default([]),
    ogImage: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const caseStudies = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/case-studies' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    industry: z.string(),
    location: z.string(),
    pubDate: z.date(),
    heroMetric: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(true),
  }),
});

export const collections = { testimonials, blog, caseStudies };
