import Link from 'next/link';
import { Globe, Twitter } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-white border-t border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-1">
            <h3 className="text-lg font-bold text-secondary mb-2">
              BiteWise AI
            </h3>
            <p className="text-sm text-secondary-light">
              Empowering your taste buds with artificial intelligence. Discover the best flavors in your city with precision and speed.
            </p>
          </div>

          {/* About Us */}
          <div>
            <h4 className="text-sm font-semibold text-secondary mb-4 uppercase tracking-wider">
              About Us
            </h4>
            <ul className="space-y-2">
              <li>
                <Link href="/about" className="text-sm text-secondary-light hover:text-secondary transition-colors">
                  About
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-sm text-secondary-light hover:text-secondary transition-colors">
                  Contact Support
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-sm text-secondary-light hover:text-secondary transition-colors">
                  Privacy Policy
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-sm font-semibold text-secondary mb-4 uppercase tracking-wider">
              Contact Support
            </h4>
            <ul className="space-y-2">
              <li>
                <Link href="/help" className="text-sm text-secondary-light hover:text-secondary transition-colors">
                  Help Center
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-sm text-secondary-light hover:text-secondary transition-colors">
                  Terms of Service
                </Link>
              </li>
            </ul>
          </div>

          {/* Add Restaurant */}
          <div>
            <h4 className="text-sm font-semibold text-secondary mb-4 uppercase tracking-wider">
              Add a Restaurant
            </h4>
            <ul className="space-y-2">
              <li>
                <Link href="/claim" className="text-sm text-secondary-light hover:text-secondary transition-colors">
                  Claim Listing
                </Link>
              </li>
            </ul>
            <div className="flex items-center gap-4 mt-4">
              <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                <Twitter className="w-4 h-4 text-secondary-light" />
              </button>
              <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                <Globe className="w-4 h-4 text-secondary-light" />
              </button>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-8 pt-8 border-t border-gray-100">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-secondary-light">
              © 2024 BITEWISE AI RESTAURANT DISCOVERY. POWERED BY HUNGER.
            </p>
            <div className="flex items-center gap-4">
              <Globe className="w-4 h-4 text-secondary-light" />
              <Twitter className="w-4 h-4 text-secondary-light" />
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
