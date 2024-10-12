'use client'

import React from "react"
import { Sparkles, FileText, Lock, GitBranch } from "lucide-react"

export function HarveyUi() {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white p-6 shadow-md">
        <h1 className="text-3xl font-serif mb-8">Harvey</h1>
        <nav className="space-y-4">
          <a href="#" className="flex items-center space-x-3 px-3 py-2 bg-gray-100 rounded-md">
            <Sparkles className="w-5 h-5" />
            <span className="font-medium">Assistant</span>
          </a>
          <a href="#" className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md">
            <FileText className="w-5 h-5" />
            <span>Research</span>
          </a>
          <a href="#" className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md">
            <Lock className="w-5 h-5" />
            <span>Vault</span>
          </a>
          <a href="#" className="flex items-center space-x-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-md">
            <GitBranch className="w-5 h-5" />
            <span>Workflows</span>
          </a>
        </nav>
      </div>

      {/* Main content */}
      <div className="flex-1 p-8 overflow-auto">
        <div className="bg-white rounded-lg shadow-md p-6 max-w-3xl mx-auto">
          <div className="border-b pb-4 mb-6">
            <div className="flex space-x-4">
              <button className="text-lg font-medium border-b-2 border-black pb-2">Assist</button>
              <button className="text-lg text-gray-400">Draft</button>
            </div>
          </div>

          <div className="mb-6">
            <h2 className="text-lg font-medium mb-2">Query</h2>
            <p className="text-gray-700">
              Compare how these opinions differ or agree on the causation standard under the federal Anti-Kickback Statute.
            </p>
          </div>

          <button className="w-full bg-gray-800 text-white py-3 rounded-md hover:bg-gray-700 transition-colors mb-6">
            Ask Harvey
          </button>

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
      </div>
    </div>
  )
}