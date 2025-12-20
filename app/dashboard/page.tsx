/* eslint-disable @next/next/no-img-element */
/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import {
  UploadCloud,
  Activity,
  BarChart2,
  GitMerge,
  Terminal,
  Cpu,
  FileCode,
  AlertCircle,
} from "lucide-react";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

export default function Dashboard() {
  const [file, setFile] = useState<File | null>(null);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setData(null);

    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const res = await axios.post(
  `${API_BASE}/api/analyze`,
  formData
);
      setData(res.data);
    } catch (err) {
      console.error(err);
      setError("Connection refused. Ensure backend is running on :8000");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-300 font-sans selection:bg-indigo-500/30">
      {/* 1. Technical Navbar */}
      <nav className="border-b border-zinc-800 bg-zinc-950/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-indigo-500/10 p-2 rounded-md border border-indigo-500/20">
              <Terminal className="w-5 h-5 text-indigo-400" />
            </div>
            <h1 className="text-lg font-bold tracking-tight text-white font-mono">
              AUTO_EDA<span className="text-zinc-600">.v2</span>
            </h1>
          </div>
          <div className="flex items-center gap-4 text-xs font-mono text-zinc-500">
            <span className="flex items-center gap-2">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              SYSTEM_ONLINE
            </span>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* 2. Control Panel (Sidebar) */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-6 sticky top-24">
            <div className="flex items-center gap-2 mb-6 border-b border-zinc-800 pb-4">
              <Cpu className="w-4 h-4 text-indigo-400" />
              <h2 className="text-sm font-semibold text-white uppercase tracking-wider font-mono">
                Input Stream
              </h2>
            </div>

            {/* Upload Zone */}
            <div className="group relative border border-dashed border-zinc-700 bg-zinc-900/50 hover:bg-zinc-900 hover:border-indigo-500/50 transition-all duration-300 rounded-lg p-8 text-center cursor-pointer">
              <input
                type="file"
                accept=".csv,.xlsx,.json,.parquet"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              />
              <div className="flex flex-col items-center gap-3">
                <div className="p-3 bg-zinc-800 rounded-full group-hover:scale-110 transition-transform duration-300">
                  <UploadCloud className="w-6 h-6 text-zinc-400 group-hover:text-indigo-400" />
                </div>
                <div>
                  <p className="text-sm font-medium text-zinc-300 group-hover:text-white transition-colors">
                    {file ? file.name : "Drop dataset here"}
                  </p>
                  <p className="text-xs text-zinc-500 mt-1 font-mono">
                    .CSV .PARQUET .JSON
                  </p>
                </div>
              </div>
            </div>

            {/* Action Button */}
            <button
              onClick={handleUpload}
              disabled={loading || !file}
              className="w-full mt-4 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:hover:bg-indigo-600 text-white py-3 rounded-lg text-sm font-medium transition-all shadow-lg shadow-indigo-900/20 border border-indigo-500/20 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Activity className="w-4 h-4 animate-spin" />
                  <span className="font-mono">PROCESSING...</span>
                </>
              ) : (
                <>
                  <span>Initialize Analysis</span>
                  <div className="bg-indigo-500 text-[10px] px-1.5 py-0.5 rounded text-white/80 font-mono">
                    ⏎
                  </div>
                </>
              )}
            </button>

            {error && (
              <div className="mt-4 p-3 bg-red-950/30 border border-red-900/50 rounded-lg flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-red-500 shrink-0" />
                <p className="text-xs text-red-400">{error}</p>
              </div>
            )}
          </div>
        </div>

        {/* 3. Output Console (Results) */}
        <div className="lg:col-span-8 space-y-6">
          {data ? (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              {/* Summary Module */}
              <div className="bg-zinc-900/50 border border-zinc-800 rounded-lg overflow-hidden">
                <div className="bg-zinc-900 border-b border-zinc-800 px-4 py-3 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <FileCode className="w-4 h-4 text-emerald-500" />
                    <span className="text-xs font-mono text-zinc-400 uppercase">
                      Executive_Summary.md
                    </span>
                  </div>
                  <div className="flex gap-3 text-[10px] font-mono text-zinc-500">
                    <span>ROWS: {data.rows}</span>
                    <span className="text-zinc-700">|</span>
                    <span>COLS: {data.columns}</span>
                  </div>
                </div>
                <div className="p-6">
                  {/* <article className="prose prose-invert prose- max-w-none prose-headings:font-semibold prose-headings:text-indigo-100 prose-p:text-zinc-400 prose-strong:text-indigo-300"> */}
                  <article className="">
                    <ReactMarkdown
                      remarkPlugins={[remarkMath]}
                      rehypePlugins={[rehypeKatex]}
                    >
                      {data.summary}
                    </ReactMarkdown>
                  </article>
                </div>
              </div>

              {/* Visualization Grid: Univariate */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <BarChart2 className="w-4 h-4 text-indigo-400" />
                  <h3 className="text-sm font-mono text-zinc-400 uppercase tracking-wider">
                    Feature_Distributions
                  </h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {data.univariate_graphs.map((graph: any) => (
                    <div
                      key={graph.id}
                      className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-4 hover:border-zinc-600 transition-colors group"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-xs font-mono text-zinc-500 group-hover:text-indigo-400 transition-colors">
                          {graph.title}
                        </span>
                        <div className="w-2 h-2 rounded-full bg-zinc-800 group-hover:bg-indigo-500 transition-colors"></div>
                      </div>
                      <div className="bg-white/5 rounded-md p-2">
                        <img
                          src={graph.image}
                          alt={graph.title}
                          className="w-full h-auto rounded opacity-90 hover:opacity-100 transition-opacity"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Visualization Grid: Pairwise */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <GitMerge className="w-4 h-4 text-purple-400" />
                  <h3 className="text-sm font-mono text-zinc-400 uppercase tracking-wider">
                    Correlation_Matrix
                  </h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {data.pairwise_graphs.map((graph: any) => (
                    <div
                      key={graph.id}
                      className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-4 hover:border-zinc-600 transition-colors group"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-xs font-mono text-zinc-500 group-hover:text-purple-400 transition-colors">
                          {graph.title}
                        </span>
                        <div className="w-2 h-2 rounded-full bg-zinc-800 group-hover:bg-purple-500 transition-colors"></div>
                      </div>
                      <div className="bg-white/5 rounded-md p-2">
                        <img
                          src={graph.image}
                          alt={graph.title}
                          className="w-full h-auto rounded opacity-90 hover:opacity-100 transition-opacity"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            // Empty State
            <div className="h-[60vh] flex flex-col items-center justify-center border border-dashed border-zinc-800 rounded-lg bg-zinc-900/20">
              <div className="p-4 bg-zinc-900 rounded-full mb-4 border border-zinc-800">
                <Terminal className="w-8 h-8 text-zinc-600" />
              </div>
              <p className="text-zinc-400 font-medium">Awaiting Data Stream</p>
              <p className="text-zinc-600 text-sm mt-2 font-mono">
                Upload a dataset to begin execution
              </p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
