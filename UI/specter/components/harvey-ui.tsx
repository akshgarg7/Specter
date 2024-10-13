'use client'

import React, { useState, useEffect } from "react"
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom"
import { Sparkles, FileText, GitBranch } from "lucide-react"
import { Separator } from "@/components/ui/separator"

export function SpecterUi() {
  const handlePracticeClick = () => {
    window.location.href = 'https://playground.outspeed.com/';
  };

  const handleAskSpecterClick = () => {
    document.getElementById('fileUpload').click();
  };

  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        {/* Sidebar */}
        <div className="w-64 bg-white p-6 shadow-md">
          <h1 className="text-3xl font-serif mb-8">Specter</h1>
          <nav className="space-y-4">
            <Link to="/" className="flex items-center space-x-3 px-3 py-2 bg-gray-100 rounded-md">
              <Sparkles className="w-5 h-5" />
              <span className="font-medium">Upload</span>
            </Link>
            <Link to="/runs" className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md">
              <FileText className="w-5 h-5" />
              <span>Precedent</span>
            </Link>
            <a href="#" onClick={handlePracticeClick} className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md">
              <GitBranch className="w-5 h-5" />
              <span>Practice</span>
            </a>
          </nav>
        </div>

        {/* Main content */}
        <div className="flex-1 p-8 overflow-auto">
          <Routes>
            <Route path="/" element={<DefaultPage />} />
            <Route path="/runs" element={<RunsPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

function DefaultPage() {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 max-w-3xl mx-auto">
      <div className="border-b pb-4 mb-6">
        <div className="flex space-x-4">
          <button className="text-lg font-medium border-b-2 border-black pb-2">Negotiation Prep Tool</button>
          {/* Removed the Draft button */}
        </div>
      </div>

      <div className="mb-6">
        <h2 className="text-lg font-medium mb-2">Upload your case below</h2>
        <p className="text-gray-700">
          Practice your negotiation skills with Specter. Upload your case details as well as which side you represent below. 
        </p>
      </div>

      <button onClick={() => document.getElementById('fileUpload').click()} className="w-full bg-gray-800 text-white py-3 rounded-md hover:bg-gray-700 transition-colors mb-6">
        Ask Specter
      </button>
      <input type="file" id="fileUpload" style={{ display: 'none' }} />

      <div>
        <h2 className="text-lg font-medium mb-4">Sources</h2>
        <div className="space-y-3">
          <div className="flex items-center space-x-3 p-3 bg-gray-100 rounded-md">
            <FileText className="w-5 h-5" />
            <span>U.S. ex rel Cairns.pdf</span>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-gray-100 rounded-md">
            <FileText className="w-5 h-5" />
            <span>U.S. ex rel Greenfield.pdf</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function RunsPage() {
  const [loadingStates, setLoadingStates] = useState(Array(10).fill(true));

  useEffect(() => {
    const timers = loadingStates.map((_, index) => {
      const randomTime = Math.floor(Math.random() * 1000) + 5000; // Random time between 5 and 15 seconds
      return setTimeout(() => {
        setLoadingStates((prevStates) => {
          const newStates = [...prevStates];
          newStates[index] = false;
          return newStates;
        });
      }, randomTime);
    });

    return () => timers.forEach(clearTimeout); // Cleanup timers on unmount
  }, []);

  const runs = Array.from({ length: 10 }, (_, index) => ({
    simulation: `Simulation ${index + 1}`,
    details: "(For case GTI vs. EPS - Triggered by Aksh)"
  }));

  const allTasksComplete = loadingStates.every(state => !state);

  const handleNegotiateClick = () => {
    window.location.href = 'https://playground.outspeed.com/';
  };

  return (
    <div className="min-h-screen bg-white p-8 flex flex-col">
      <div className="flex-1">
        <h1 className="text-4xl font-serif mb-8">Specter</h1>
        <div className="bg-gray-50 rounded-lg shadow-sm">
          <ul className="divide-y divide-gray-200">
            {runs.map((run, index) => (
              <li key={index} className="p-4 flex justify-between items-center">
                <div>
                  <span className="text-lg font-bold text-gray-900">{run.simulation}</span>
                  <span className="text-sm text-gray-500"> {run.details}</span>
                </div>
                {loadingStates[index] && (
                  <div className="loader border-t-2 border-b-2 border-gray-900 w-6 h-6 rounded-full animate-spin"></div>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>
      {allTasksComplete && (
        <button
          onClick={handleNegotiateClick}
          className="mt-4 mb-8 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-500 transition-colors"
        >
          Click to Negotiate
        </button>
      )}
    </div>
  );
}

export default SpecterUi;
