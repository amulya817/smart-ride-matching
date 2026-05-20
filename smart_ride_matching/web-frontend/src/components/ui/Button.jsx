import React from 'react';
import { cn } from '../../lib/utils';

export function Button({ className, variant = 'primary', size = 'default', children, ...props }) {
  const variants = {
    primary: 'bg-[#F9A8D4] hover:bg-[#EC4899] text-white shadow-md hover:shadow-lg',
    secondary: 'bg-white border border-[#F9A8D4] text-[#EC4899] hover:bg-pink-50',
    ghost: 'hover:bg-pink-50 text-gray-700 hover:text-[#EC4899]',
    danger: 'bg-red-500 hover:bg-red-600 text-white shadow-md',
  };

  const sizes = {
    sm: 'h-9 px-3 text-sm',
    default: 'h-11 px-6',
    lg: 'h-14 px-8 text-lg',
    icon: 'h-11 w-11 flex items-center justify-center',
  };

  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-full font-medium transition-all duration-200 active:scale-95 disabled:opacity-50 disabled:pointer-events-none',
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
