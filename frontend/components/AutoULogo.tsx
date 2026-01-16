"use client";

interface AutoULogoProps {
  className?: string;
  width?: number;
  height?: number;
}

export default function AutoULogo({ 
  className = "", 
  width = 165, 
  height = 55 
}: AutoULogoProps) {
  const gradientId = `autoU-gradient-${Math.random().toString(36).substr(2, 9)}`;
  
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 165 55"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`transition-all duration-200 hover:scale-105 ${className}`}
    >
      <defs>
        {/* Gradiente laranja preciso - bright orange para deep reddish-orange */}
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#FF9500" />
          <stop offset="15%" stopColor="#FF8C42" />
          <stop offset="40%" stopColor="#FF6B35" />
          <stop offset="70%" stopColor="#FF5C29" />
          <stop offset="100%" stopColor="#E55A27" />
        </linearGradient>
      </defs>

      {/* AutoU como texto com gradiente */}
      <text
        x="2"
        y="38"
        fontSize="42"
        fontWeight="700"
        fontFamily="'Nunito Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif"
        fill={`url(#${gradientId})`}
        letterSpacing="-2"
      >
        AutoU
      </text>
    </svg>
  );
}
