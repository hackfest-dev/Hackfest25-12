'use client';

import { useEffect, useState } from 'react';

export default function DigitalTwinAnimation() {
  const [animate, setAnimate] = useState(false);
  
  useEffect(() => {
    setAnimate(true);
  }, []);

  return (
    <div className="relative w-full max-w-md mx-auto h-56 sm:h-64 mt-4 sm:mt-8 mb-8 sm:mb-12">
      {/* Background circle */}
      <div 
        className={`absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-44 sm:w-56 h-44 sm:h-56 rounded-full bg-indigo-100 dark:bg-indigo-900/30 transition-all duration-1000 ease-out ${animate ? 'scale-100 opacity-100' : 'scale-50 opacity-0'}`}
      ></div>
      
      {/* Human silhouette */}
      <div 
        className={`absolute top-1/2 left-1/4 transform -translate-x-1/2 -translate-y-1/2 scale-75 sm:scale-100 transition-all duration-700 delay-300 ${animate ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`}
      >
        <svg width="80" height="160" viewBox="0 0 80 160" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="40" cy="30" r="20" fill="#4C6EF5" />
          <path d="M40 50V110" stroke="#4C6EF5" strokeWidth="6" />
          <path d="M40 70L15 90" stroke="#4C6EF5" strokeWidth="6" />
          <path d="M40 70L65 90" stroke="#4C6EF5" strokeWidth="6" />
          <path d="M40 110L20 150" stroke="#4C6EF5" strokeWidth="6" />
          <path d="M40 110L60 150" stroke="#4C6EF5" strokeWidth="6" />
        </svg>
      </div>
      
      {/* Digital twin silhouette */}
      <div 
        className={`absolute top-1/2 left-3/4 transform -translate-x-1/2 -translate-y-1/2 scale-75 sm:scale-100 transition-all duration-700 delay-500 ${animate ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-10'}`}
      >
        <svg width="80" height="160" viewBox="0 0 80 160" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="40" cy="30" r="20" stroke="#4C6EF5" strokeWidth="2" strokeDasharray="3 3" fill="none" />
          <path d="M40 50V110" stroke="#4C6EF5" strokeWidth="2" strokeDasharray="5 5" />
          <path d="M40 70L15 90" stroke="#4C6EF5" strokeWidth="2" strokeDasharray="5 5" />
          <path d="M40 70L65 90" stroke="#4C6EF5" strokeWidth="2" strokeDasharray="5 5" />
          <path d="M40 110L20 150" stroke="#4C6EF5" strokeWidth="2" strokeDasharray="5 5" />
          <path d="M40 110L60 150" stroke="#4C6EF5" strokeWidth="2" strokeDasharray="5 5" />
          <circle cx="40" cy="30" r="16" stroke="#4C6EF5" strokeWidth="1" fill="rgba(76, 110, 245, 0.1)" />
        </svg>
      </div>
      
      {/* Connection lines */}
      <svg 
        className={`absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 scale-75 sm:scale-100 transition-all duration-1000 delay-700 ${animate ? 'opacity-100' : 'opacity-0'}`}
        width="160" 
        height="160" 
        viewBox="0 0 160 160" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M40 30H120" stroke="#4C6EF5" strokeWidth="2" strokeDasharray="4 4">
          <animate 
            attributeName="stroke-dashoffset" 
            from="24" 
            to="0" 
            dur="3s" 
            repeatCount="indefinite" 
          />
        </path>
        <path d="M40 70H120" stroke="#4C6EF5" strokeWidth="2" strokeDasharray="4 4">
          <animate 
            attributeName="stroke-dashoffset" 
            from="24" 
            to="0" 
            dur="3s" 
            repeatCount="indefinite" 
          />
        </path>
        <path d="M40 110H120" stroke="#4C6EF5" strokeWidth="2" strokeDasharray="4 4">
          <animate 
            attributeName="stroke-dashoffset" 
            from="24" 
            to="0" 
            dur="3s" 
            repeatCount="indefinite" 
          />
        </path>
      </svg>
      
      {/* Data points */}
      <div className={`absolute top-1/2 left-1/2 w-full h-full transition-all duration-1000 delay-1000 ${animate ? 'opacity-100' : 'opacity-0'}`}>
        {[1, 2, 3, 4, 5].map((i) => (
          <div 
            key={i}
            className={`absolute bg-indigo-500 rounded-full w-1.5 sm:w-2 h-1.5 sm:h-2 animate-pulse`}
            style={{
              top: `${Math.random() * 80 + 10}%`,
              left: `${Math.random() * 40 + 30}%`,
              animationDelay: `${i * 0.2}s`
            }}
          ></div>
        ))}
      </div>
    </div>
  );
} 