import Link from 'next/link';

export function Navbar() {
  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-center h-16">
          {/* Logo Only */}
          <Link href="/" className="flex items-center gap-1">
            <span className="text-2xl font-bold text-primary italic">
              BiteWise AI
            </span>
          </Link>
        </div>
      </div>
    </header>
  );
}
