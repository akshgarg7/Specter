'use client'

import React, { useState, useRef } from 'react';
import { FileText } from 'lucide-react';
import { BACKEND_URL } from '../lib/config';

function DefaultPage() {
    const [relevantDocs, setRelevantDocs] = useState<string[]>([]);
    const [filename, setFilename] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
  
    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;
    
  
      const formData = new FormData();
      formData.append('file', file);
  
      try {
        const response = await fetch(`${BACKEND_URL}/upload`, {
          method: 'POST',
          body: formData,
        });
  
        if (response.ok) {
          const data = await response.json();
          alert(`File uploaded successfully: ${data.filename}`);
  
          // Fetch relevant documents
          const relevantResponse = await fetch(`${BACKEND_URL}/relevant-docs/${data.filename}`);
          if (relevantResponse.ok) {
            const relevantData = await relevantResponse.json();
            setRelevantDocs(relevantData.relevant_docs);
            setFilename(data.filename);
          }
        } else {
          alert('File upload failed');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        alert('Error uploading file');
      }
    };
  
    const handleRunTrajectories = async () => {
      if (!filename) {
        alert('Please upload a file first');
        return;
      }

      try {
        const response = await fetch(`${BACKEND_URL}/run-trajectories`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ n: 10 }), // Assuming n is 10 for this example
        });

        if (response.ok) {
          await response.json(); // Consume the response without assigning it
          alert('Trajectories simulation completed successfully');
          // Handle the response data as needed in the future
        } else {
          alert('Failed to run trajectories simulation');
        }
      } catch (error) {
        console.error('Error running trajectories:', error);
        alert('Error running trajectories simulation');
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
  
        <button
            onClick={() => fileInputRef.current?.click()}
            className="w-full bg-gray-800 text-white py-3 rounded-md hover:bg-gray-700 transition-colors mb-6"
        >
            Ask Specter
        </button>
        <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileUpload}
        />
  
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
  
        {relevantDocs.length > 0 && (
          <button
            onClick={handleRunTrajectories}
            className="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 transition-colors mt-6"
          >
            Run Trajectory Simulations
          </button>
        )}
      </div>
    );
  }

export default DefaultPage;
