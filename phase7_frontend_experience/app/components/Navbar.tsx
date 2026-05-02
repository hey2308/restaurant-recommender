'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Bell, Heart, MapPin, User } from 'lucide-react';

const navLinks = [
  { href: '/', label: 'Home' },
  { href: '/preferences', label: 'Discover' },
  { href: '/collections', label: 'Collections' },
  { href: '/pro', label: 'Pro' },
];

export function Navbar() {
  const pathname = usePathname();

  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-1">
            <span className="text-2xl font-bold text-primary italic">
              BiteWise AI
            </span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`text-sm font-medium transition-colors ${
                  pathname === link.href
                    ? 'text-primary border-b-2 border-primary pb-5 pt-5'
                    : 'text-secondary-light hover:text-secondary'
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          {/* Right Side Icons */}
          <div className="flex items-center gap-4">
            <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
              <Bell className="w-5 h-5 text-secondary-light" />
            </button>
            <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
              <Heart className="w-5 h-5 text-secondary-light" />
            </button>
            <button className="flex items-center gap-2 p-1 hover:bg-gray-100 rounded-full transition-colors">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-primary-dark rounded-full flex items-center justify-center">
                <User className="w-4 h-4 text-white" />
              </div>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
