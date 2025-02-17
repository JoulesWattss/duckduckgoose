import React from 'react';
import { motion } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

const Hero = () => {
  return (
    <div className="relative h-screen flex items-center justify-center">
      {/* Background with overlay */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: 'url("https://images.unsplash.com/photo-1581093458791-9d42cc407a2e?auto=format&fit=crop&q=80")',
        }}
      >
        <div className="absolute inset-0 bg-black/60" />
      </div>

      {/* First Duck Silhouette */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 0.5 }}
        className="absolute left-8 bottom-32 opacity-80"
      >
        <svg
          width="120"
          height="120"
          viewBox="0 0 100 100"
          className="fill-none stroke-white stroke-[1.5]"
        >
          {/* Body */}
          <path d="M30,60 C30,45 40,35 55,35 C70,35 80,45 80,60 C80,75 70,85 55,85 C40,85 30,75 30,60" />
          {/* Neck and head */}
          <path d="M55,35 C55,25 60,20 65,15 C70,10 80,10 85,15 C90,20 90,30 85,35 C80,40 75,40 70,35" />
          {/* Tail */}
          <path d="M30,60 C25,55 20,55 15,60 C10,65 10,75 15,80 C20,85 25,85 30,80" />
          {/* Bill */}
          <path d="M85,25 L95,20 L85,30" />
          {/* Eye */}
          <circle cx="82" cy="22" r="1.5" className="fill-white" />
        </svg>
      </motion.div>

      {/* Second Duck Silhouette (Smaller) - Facing right towards bigger duck */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 0.7 }}
        className="absolute left-40 bottom-36 opacity-60"
      >
        <svg
          width="80"
          height="80"
          viewBox="0 0 100 100"
          className="fill-none stroke-white stroke-[1.5] scale-x-[-1]"
        >
          {/* Body */}
          <path d="M30,60 C30,45 40,35 55,35 C70,35 80,45 80,60 C80,75 70,85 55,85 C40,85 30,75 30,60" />
          {/* Neck and head */}
          <path d="M55,35 C55,25 60,20 65,15 C70,10 80,10 85,15 C90,20 90,30 85,35 C80,40 75,40 70,35" />
          {/* Tail */}
          <path d="M30,60 C25,55 20,55 15,60 C10,65 10,75 15,80 C20,85 25,85 30,80" />
          {/* Bill */}
          <path d="M85,25 L95,20 L85,30" />
          {/* Eye */}
          <circle cx="82" cy="22" r="1.5" className="fill-white" />
        </svg>
      </motion.div>

      {/* Third Duck Silhouette (Top Right) - Facing left towards text */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 0.9 }}
        className="absolute right-8 top-24 opacity-70"
      >
        <svg
          width="100"
          height="100"
          viewBox="0 0 100 100"
          className="fill-none stroke-white stroke-[1.5] scale-x-[-1]"
        >
          {/* Body */}
          <path d="M30,60 C30,45 40,35 55,35 C70,35 80,45 80,60 C80,75 70,85 55,85 C40,85 30,75 30,60" />
          {/* Neck and head */}
          <path d="M55,35 C55,25 60,20 65,15 C70,10 80,10 85,15 C90,20 90,30 85,35 C80,40 75,40 70,35" />
          {/* Tail */}
          <path d="M30,60 C25,55 20,55 15,60 C10,65 10,75 15,80 C20,85 25,85 30,80" />
          {/* Bill */}
          <path d="M85,25 L95,20 L85,30" />
          {/* Eye */}
          <circle cx="82" cy="22" r="1.5" className="fill-white" />
        </svg>
      </motion.div>

      {/* Content */}
      <div className="relative z-10 text-center text-white max-w-4xl mx-auto px-4">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-5xl md:text-6xl font-bold leading-[2] tracking-[0.025em]"
        >
          Evaluating France's Pioneering HPAI Vaccination Campaign Through Interrupted Time Series Analysis
        </motion.h1>
      </div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        animate={{ y: [0, 10, 0] }}
        transition={{ duration: 1.5, repeat: Infinity }}
      >
        <ChevronDown className="text-white w-8 h-8" />
      </motion.div>
    </div>
  );
};

export default Hero;