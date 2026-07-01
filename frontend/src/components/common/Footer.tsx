"use client";

import Link from "next/link";

function LinkedInIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
    </svg>
  );
}

function XIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.73-8.835L1.254 2.25H8.08l4.258 5.63 5.906-5.63zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
    </svg>
  );
}

const FOOTER_COLS = [
  {
    heading: "Platform",
    links: [
      { label: "Upload Documents", href: "#upload" },
      { label: "Ask Questions", href: "#ask" },
      { label: "Citations", href: "#ask" },
    ],
  },
];

const SOCIAL_LINKS = [
  { icon: <LinkedInIcon />, href: "https://linkedin.com", label: "LinkedIn" },
  { icon: <XIcon />, href: "https://x.com", label: "X" },
];

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="w-full bg-black text-white">
      <div className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
        <div className="grid gap-10 border-b border-white/10 pb-12 md:grid-cols-3 lg:grid-cols-4">
          <div className="md:col-span-3 lg:col-span-1">
            <p className="text-2xl font-semibold tracking-tight">
              Document Intelligence
            </p>
            <p className="mt-4 max-w-sm text-sm leading-7 text-gray-400">
              Transform complex documents into actionable answers with a modern AI-powered workflow.
            </p>
          </div>

          {FOOTER_COLS.map((col) => (
            <div key={col.heading}>
              <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-gray-500">
                {col.heading}
              </p>
              <ul className="mt-4 flex flex-wrap items-center gap-4 sm:gap-6">
                {col.links.map((link) => (
                  <li key={link.label}>
                    <Link
                      href={link.href}
                      className="text-sm text-gray-300 transition-colors hover:text-white"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-8 flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-3">
            {SOCIAL_LINKS.map((social) => (
              <a
                key={social.label}
                href={social.href}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={social.label}
                className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 bg-white/5 text-gray-300 transition-colors hover:border-white/30 hover:bg-white/10 hover:text-white"
              >
                {social.icon}
              </a>
            ))}
          </div>

          <p className="text-xs uppercase tracking-[0.24em] text-gray-500">
            © {year} Document Intelligence. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
