// app/components/Sidebar.tsx
'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { UploadCloud, FileText, MessageSquare, GitBranch } from 'lucide-react';

const Sidebar: React.FC = () => {
  const pathname = usePathname();

  const isLinkActive = (href: string) => {
    return pathname === href;
  };

  const getLinkClassName = (href: string) => {
    const baseClasses = "flex items-center space-x-3 px-3 py-2 rounded-md";
    const activeClasses = "bg-gray-100 text-gray-900";
    const inactiveClasses = "text-gray-600 hover:bg-gray-100";
    
    return `${baseClasses} ${isLinkActive(href) ? activeClasses : inactiveClasses}`;
  };

  return (
    <div className="w-64 bg-white p-6 shadow-md">
      <h1 className="text-3xl font-serif mb-8">Specter</h1>
      <nav className="space-y-4">
        <Link href="/" passHref className={getLinkClassName('/')}>
          <UploadCloud className="w-5 h-5" />
          <span className={isLinkActive('/') ? "font-medium" : ""}>Upload</span>
        </Link>
        <Link href="/runs" passHref className={getLinkClassName('/runs')}>
          <FileText className="w-5 h-5" />
          <span className={isLinkActive('/runs') ? "font-medium" : ""}>Run Status</span>
        </Link>
        <Link href="/view-runs" passHref className={getLinkClassName('/view-runs')}>
          <MessageSquare className="w-5 h-5" />
          <span className={isLinkActive('/view-runs') ? "font-medium" : ""}>View Runs</span>
        </Link>
        <a
          href="https://playground.outspeed.com/"
          className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md"
        >
          <GitBranch className="w-5 h-5" />
          <span>Practice</span>
        </a>
      </nav>
    </div>
  );
};

export default Sidebar;
