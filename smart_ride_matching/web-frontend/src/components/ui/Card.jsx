import React from 'react';
import { cn } from '../../lib/utils';

export function Card({ className, children, ...props }) {
  return (
    <div
      className={cn(
        'bg-white rounded-2xl border border-pink-100/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function GlassCard({ className, children, ...props }) {
  return (
    <div
      className={cn(
        'bg-white/70 backdrop-blur-md rounded-2xl border border-white/50 shadow-xl overflow-hidden',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
