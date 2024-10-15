'use client'

import React, { useState, useEffect } from "react"
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom"
import { FileText, GitBranch, MessageSquare, UploadCloud } from "lucide-react"

export function SpecterUi() {
  const handlePracticeClick = () => {
    window.location.href = 'https://playground.outspeed.com/';
  };

  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        {/* Sidebar */}
        <div className="w-64 bg-white p-6 shadow-md">
          <h1 className="text-3xl font-serif mb-8">Specter</h1>
          <nav className="space-y-4">
            <Link to="/" className="flex items-center space-x-3 px-3 py-2 bg-gray-100 rounded-md">
              <UploadCloud className="w-5 h-5" />
              <span className="font-medium">Upload</span>
            </Link>
            <Link to="/runs" className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md">
              <FileText className="w-5 h-5" />
              <span>Run Status</span>
            </Link>
            <Link to="/view-runs" className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md">
              <MessageSquare className="w-5 h-5" />
              <span>View Runs</span>
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
            <Route path="/view-runs" element={<ViewRunsPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

function DefaultPage() {
  const [relevantDocs, setRelevantDocs] = useState<string[]>([]);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8080/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        alert(`File uploaded successfully: ${data.filename}`);

        // Fetch relevant documents
        const relevantResponse = await fetch(`http://localhost:8080/relevant-docs/${data.filename}`);
        if (relevantResponse.ok) {
          const relevantData = await relevantResponse.json();
          setRelevantDocs(relevantData.relevant_docs);
        }
      } else {
        alert('File upload failed');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 max-w-3xl mx-auto">
      <div className="border-b pb-4 mb-6">
        <div className="flex space-x-4">
          <button className="text-lg font-medium border-b-2 border-black pb-2">Your personal negotiation assistant</button>
          {/* Removed the Draft button */}
        </div>
      </div>

      <div className="mb-6 px-1 rounded-lg shadow-sm">
        <p className="text-gray-800 text-lg leading-relaxed">
          Welcome to <span className="font-semibold">Specter</span>, your AI-powered legal assistant. Negotiate your upcoming deals with ease. Upload your case documents and specify any precedents to follow. 
          Unsure of what&apos;s relevant? Let us identify key documents for you. We&apos;re ready to assist you whenever you&apos;re ready to proceed.
        </p>
      </div>

      <button onClick={() => document.getElementById('fileUpload')?.click()} className="w-full bg-gray-800 text-white py-3 rounded-md hover:bg-gray-700 transition-colors mb-6">
        Ask Specter
      </button>
      <input type="file" id="fileUpload" style={{ display: 'none' }} onChange={handleFileUpload} />

      <div>
        <h2 className="text-lg font-medium mb-4">Sources</h2>
        <div className="space-y-3">
          {relevantDocs.map((doc, index) => (
            <div key={index} className="flex items-center space-x-3 p-3 bg-gray-100 rounded-md">
              <FileText className="w-5 h-5" />
              <span>{doc}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function RunsPage() {
  const [loadingStates, setLoadingStates] = useState(Array(10).fill(true));

  useEffect(() => {
    const checkTaskStatus = async (index) => {
      try {
        const response = await fetch(`http://localhost:8080/status?task_id=${index + 1}`);
        const data = await response.json();
        console.log(data)
        if (data === true) {
          setLoadingStates((prevStates) => {
            const newStates = [...prevStates];
            newStates[index] = false;
            return newStates;
          });
        }
      } catch (error) {
        console.error("Error fetching task status:", error);
      }
    };

    loadingStates.forEach((_, index) => {
      checkTaskStatus(index);
    });

    const intervalId = setInterval(() => {
      loadingStates.forEach((_, index) => {
        checkTaskStatus(index);
      });
    }, 5000); // Check every 5 seconds

    return () => clearInterval(intervalId); // Cleanup interval on unmount
  }, [loadingStates]);

  const runs = Array.from({ length: 10 }, (_, index) => ({
    simulation: `Simulation ${index + 1}`,
    details: "(For case GTI vs. EPS - Triggered by Aksh)"
  }));

  const allTasksComplete = loadingStates.every(state => !state);

  return (
    <div className="min-h-screen bg-white p-8 flex flex-col">
      <div className="flex-1">
        <h1 className="text-4xl font-serif mb-8">View all your runs here</h1>
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
          onClick={() => window.location.href = 'https://playground.outspeed.com/'}
          className="mt-4 mb-8 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-500 transition-colors"
        >
          Click to Negotiate
        </button>
      )}
    </div>
  );
}

function ViewRunsPage() {
  const [conversations, setConversations] = useState([]);
  const [selectedRun, setSelectedRun] = useState(null);

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const response = await fetch(`http://localhost:8080/get-trajectory?task_id=${selectedRun}`);
        const data = await response.json();

        console.log(data)
        
        // Access the 'conversation' array from the response
        if (data && Array.isArray(data.conversation)) {
          setConversations(data.conversation);
        } else {
          console.error("Unexpected data format:", data);
          setConversations([]);
        }
      } catch (error) {
        console.error("Error fetching conversations:", error);
        setConversations([]);
      }
    };

    if (selectedRun !== null) {
      fetchConversations();
    }
  }, [selectedRun]);

  const handleRunChange = (event) => {
    setSelectedRun(event.target.value);
  };

  return (
    <div className="min-h-screen bg-white p-8">
      <h2 className="text-2xl font-serif mb-4">View Runs</h2>
      <select onChange={handleRunChange} className="mb-4 p-2 border rounded">
        <option value="">Select a run</option>
        {Array.from({ length: 10 }, (_, index) => (
          <option key={index} value={index + 1}>
            Run {index + 1}
          </option>
        ))}
      </select>
      <div className="bg-gray-50 rounded-lg shadow-sm p-4">
        {selectedRun !== null && conversations.map((message, index) => (
          <div key={index} className={`p-2 ${message.speaker.includes("GTI") ? "text-blue-600" : "text-green-600"}`}>
            <strong>{message.speaker}:</strong> {message.message}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SpecterUi;
