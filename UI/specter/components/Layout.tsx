import React from 'react';
import Link from 'next/link';
import { UploadCloud, FileText, MessageSquare, GitBranch } from 'lucide-react';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white p-6 shadow-md">
        <h1 className="text-3xl font-serif mb-8">Specter</h1>
        <nav className="space-y-4">
          <Link
            href="/"
            passHref
            className="flex items-center space-x-3 px-3 py-2 bg-gray-100 rounded-md">

            <UploadCloud className="w-5 h-5" />
            <span className="font-medium">Upload</span>

          </Link>
          <Link
            href="/runs"
            passHref
            className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md">

            <FileText className="w-5 h-5" />
            <span>Run Status</span>

          </Link>
          <Link
            href="/view-runs"
            passHref
            className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md">

            <MessageSquare className="w-5 h-5" />
            <span>View Runs</span>

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

      {/* Main content */}
      <div className="flex-1 p-8 overflow-auto">{children}</div>
    </div>
  );
};

export default Layout;
