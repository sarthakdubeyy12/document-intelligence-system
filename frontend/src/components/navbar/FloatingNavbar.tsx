"use client";

import React, { useState, useEffect } from "react";
import { Menu, X } from "lucide-react";

interface NavLink {
  label: string;
  href: string;
}

const navLinks: NavLink[] = [
  { label: "Home", href: "#home" },
  { label: "Upload", href: "#upload" },
  { label: "Ask Questions", href: "#ask" },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [activeLink, setActiveLink] = useState("home");

  useEffect(() => {
    const handleScroll = () => {
      setIsOpen(false);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleLinkClick = (href: string) => {
    const id = href.replace("#", "");
    setActiveLink(id);
    setIsOpen(false);

    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <nav className="fixed top-4 left-1/2 transform -translate-x-1/2 w-[95%] max-w-4xl z-[999]">
      <div className="bg-black rounded-full px-6 py-4 shadow-2xl border border-gray-800">
        <div className="flex items-center justify-between">
          {/* Logo Section */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-sm">DI</span>
            </div>
            <span className="text-white font-semibold text-sm hidden sm:inline">
              Document Intelligence
            </span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <button
                key={link.href}
                onClick={() => handleLinkClick(link.href)}
                className={`text-sm font-medium transition-all duration-300 relative ${
                  activeLink === link.href.replace("#", "")
                    ? "text-white"
                    : "text-gray-400 hover:text-gray-200"
                }`}
              >
                {link.label}
                {activeLink === link.href.replace("#", "") && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full"></div>
                )}
              </button>
            ))}
          </div>

          {/* Right Section */}
          <div className="flex items-center gap-4">
            <button
              onClick={() => handleLinkClick("#upload")}
              className="hidden sm:block px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full text-sm font-semibold hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105"
            >
              Upload PDFs
            </button>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden text-white p-2 hover:bg-gray-900 rounded-full transition-colors duration-300"
            >
              {isOpen ? (
                <X size={24} />
              ) : (
                <Menu size={24} />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden absolute top-full left-0 right-0 mt-4 bg-black rounded-2xl border border-gray-800 shadow-2xl overflow-hidden">
            <div className="flex flex-col p-4 gap-3">
              {navLinks.map((link) => (
                <button
                  key={link.href}
                  onClick={() => handleLinkClick(link.href)}
                  className={`text-left px-4 py-3 rounded-lg transition-all duration-300 font-medium text-sm ${
                    activeLink === link.href.replace("#", "")
                      ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white"
                      : "text-gray-300 hover:bg-gray-900 hover:text-white"
                  }`}
                >
                  {link.label}
                </button>
              ))}
              <button
                onClick={() => handleLinkClick("#upload")}
                className="w-full px-4 py-3 mt-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-semibold hover:from-blue-600 hover:to-purple-700 transition-all duration-300"
              >
                Upload PDFs
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
