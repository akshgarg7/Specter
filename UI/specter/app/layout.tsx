// app/layout.tsx
import React from 'react';
import Sidebar from '../components/sidebar';
import './globals.css'; // Import global styles if you have any

export const metadata = {
  title: 'Specter',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="flex h-screen bg-gray-100">
          <Sidebar />
          <div className="flex-1 p-8 overflow-auto">{children}</div>
        </div>
      </body>
    </html>
  );
}
