// 'use client'

// import React from 'react';
// import Link from 'next/link';
// import { UploadCloud, FileText, MessageSquare, GitBranch } from 'lucide-react';
// import DefaultPage from './default-page';
// import RunsPage from './runs-page';
// import ViewRunsPage from './view-runs-page';

// export function SpecterUi() {
//     const handlePracticeClick = () => {
//       window.location.href = 'https://playground.outspeed.com/';
//     };
  
//     return (
//       <Router>
//         <div className="flex h-screen bg-gray-100">
//           {/* Sidebar */}
//           <div className="w-64 bg-white p-6 shadow-md">
//             <h1 className="text-3xl font-serif mb-8">Specter</h1>
//             <nav className="space-y-4">
//               <Link
//                 to="/"
//                 className="flex items-center space-x-3 px-3 py-2 bg-gray-100 rounded-md"
//                 legacyBehavior>
//                 <UploadCloud className="w-5 h-5" />
//                 <span className="font-medium">Upload</span>
//               </Link>
//               <Link
//                 to="/runs"
//                 className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md"
//                 legacyBehavior>
//                 <FileText className="w-5 h-5" />
//                 <span>Run Status</span>
//               </Link>
//               <Link
//                 to="/view-runs"
//                 className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md"
//                 legacyBehavior>
//                 <MessageSquare className="w-5 h-5" />
//                 <span>View Runs</span>
//               </Link>
//               <a href="#" onClick={handlePracticeClick} className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md">
//                 <GitBranch className="w-5 h-5" />
//                 <span>Practice</span>
//               </a>
//             </nav>
//           </div>
  
//           {/* Main content */}
//           <div className="flex-1 p-8 overflow-auto">
//             <Routes>
//               <Route path="/" element={<DefaultPage />} />
//               <Route path="/runs" element={<RunsPage />} />
//               <Route path="/view-runs" element={<ViewRunsPage />} />
//             </Routes>
//           </div>
//         </div>
//       </Router>
//     );
//   }

// export default SpecterUi;
