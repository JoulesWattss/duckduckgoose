import React, { useState, useEffect } from 'react';
import { Menu } from 'lucide-react';
import { motion } from 'framer-motion';

const Navigation = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState('');

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);

      // Update active section based on scroll position
      const sections = document.querySelectorAll('section[id]');
      const scrollPosition = window.scrollY + 100;

      sections.forEach((section) => {
        const sectionTop = (section as HTMLElement).offsetTop;
        const sectionHeight = (section as HTMLElement).offsetHeight;
        const sectionId = section.getAttribute('id') || '';

        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
          setActiveSection(sectionId);
        }
      });
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled ? 'bg-[#99ccff]/95 backdrop-blur-sm shadow-lg py-2' : 'bg-transparent py-4'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <span className={`text-2xl font-bold ${isScrolled ? 'text-gray-900' : 'text-white'}`}>
              Duck Duck Goose
            </span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-8">
            {['Introduction', 'Methodology', 'Analysis', 'Charts', 'Results', 'Conclusion'].map((item) => (
              <a
                key={item}
                href={`#${item.toLowerCase()}`}
                className={`${
                  isScrolled ? 'text-gray-900' : 'text-white'
                } hover:text-blue-500 transition-colors duration-200 relative ${
                  activeSection === item.toLowerCase() ? 'font-semibold' : ''
                }`}
              >
                {item}
                {activeSection === item.toLowerCase() && (
                  <motion.div
                    layoutId="activeSection"
                    className="absolute -bottom-1 left-0 right-0 h-0.5 bg-blue-500 rounded-full"
                    initial={false}
                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                  />
                )}
              </a>
            ))}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className={`${isScrolled ? 'text-gray-900' : 'text-white'} p-2 rounded-lg hover:bg-white/10 transition-colors duration-200`}
            >
              <Menu size={24} />
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden mt-2 py-2 bg-white/95 backdrop-blur-sm rounded-lg shadow-xl">
            {['Introduction', 'Methodology', 'Analysis', 'Charts', 'Results', 'Conclusion'].map((item) => (
              <a
                key={item}
                href={`#${item.toLowerCase()}`}
                className={`block px-4 py-2 text-gray-900 hover:bg-gray-100 transition-colors duration-200 ${
                  activeSection === item.toLowerCase() ? 'bg-blue-50 font-semibold' : ''
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                {item}
              </a>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;