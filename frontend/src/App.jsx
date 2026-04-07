import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState("SELECT * FROM sales;");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  
  const handleAnalyze = async () => {
    if (!query) return;
    setLoading(true);
    setResult(null);
    try {
      const response = await axios.post('http://127.0.0.1:8000/optimize', { query });
      setResult(response.data);
    } catch (error) {
      console.error("Error optimizing query:", error);
      alert("Failed to analyze query. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full bg-background text-slate-200">
      {/* Sidebar */}
      <aside className="w-64 bg-secondary p-4 flex flex-col border-r border-slate-700 shadow-xl z-10">
        <h2 className="text-xl font-black tracking-tight text-white mb-8 border-b border-slate-700 pb-4">
          Athena <span className="text-primary">Optimizer</span>
        </h2>
        
        <div className="flex-1">
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4 px-2">Data Catalog</h3>
          <ul className="space-y-1 text-sm font-medium">
            <li className="px-3 py-2 bg-slate-700/50 text-white rounded-md cursor-pointer border border-slate-600 transition-colors">
              optimizer_db
            </li>
            <div className="pl-4 pt-2">
              <li className="px-3 py-1.5 text-slate-300 hover:text-white hover:bg-slate-700/50 rounded-md cursor-pointer transition-colors flex items-center">
                <span className="w-1.5 h-1.5 rounded-full bg-accent mr-2"></span> sales
              </li>
            </div>
          </ul>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full bg-background relative overflow-hidden">
        {/* Top Navbar */}
        <header className="h-16 border-b border-slate-700/80 bg-secondary/80 backdrop-blur-sm flex items-center px-8 justify-between shrink-0">
          <div className="flex items-center space-x-2 text-sm text-slate-400">
            <span>Editor</span> <span>/</span> <span className="text-slate-200">New Query</span>
          </div>
          <button 
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-primary hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-2 rounded-md text-white font-semibold text-sm transition-all shadow-lg shadow-primary/20 hover:shadow-primary/40 active:scale-95"
          >
            {loading ? "Analyzing..." : "Analyze & Optimize"}
          </button>
        </header>

        {/* Editor & Results Area */}
        <div className="flex-1 flex overflow-hidden">
          {/* Editor Splitting */}
          <div className="flex-1 p-8 flex flex-col border-r border-slate-700/50 overflow-y-auto">
            <div className="mb-4 flex justify-between items-center group">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">SQL Input</span>
            </div>
            
            <textarea
              className="w-full bg-[#1e1e1e] text-[#d4d4d4] p-6 rounded-xl font-mono text-sm leading-relaxed focus:ring-2 focus:ring-primary/50 outline-none resize-none shadow-inner border border-slate-800 transition-all min-h-[250px]"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              spellCheck="false"
              placeholder="Paste your Athena SQL query here..."
            />

            {result && result.rewrite_preview && (
              <div className="mt-8 animate-in slide-in-from-bottom-4 fade-in duration-500 flex-1">
                <div className="mb-4 flex justify-between items-center">
                  <span className="text-xs font-semibold text-emerald-500 uppercase tracking-wider">Optimized SQL Output</span>
                  <button className="text-xs bg-slate-800 hover:bg-slate-700 px-3 py-1 rounded text-slate-300 transition-colors">Copy</button>
                </div>
                <div className="w-full bg-emerald-950/20 text-emerald-200 p-6 rounded-xl font-mono text-sm leading-relaxed border border-emerald-500/30 shadow-inner overflow-x-auto min-h-[150px]">
                  {result.rewrite_preview}
                </div>
              </div>
            )}
          </div>

          {/* AI Insights & Results pane */}
          <div className="w-[450px] p-8 flex flex-col bg-secondary/10 overflow-y-auto">
            <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-6 flex items-center">
              <span className="text-accent mr-2">✦</span> AI Insights
            </h3>
            
            {/* Cost Module */}
            <div className="bg-secondary/80 p-5 rounded-xl border border-slate-700 shadow-xl mb-6 relative overflow-hidden group hover:border-slate-500 transition-colors shrink-0">
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 20 20"><path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path><path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path></svg>
              </div>
              <h4 className="text-slate-400 text-xs uppercase font-bold tracking-wider mb-1">Estimated Cost</h4>
              
              <p className="text-3xl font-black text-white tracking-tight">
                ${result?.estimated_cost?.estimated_cost ? result.estimated_cost.estimated_cost.toFixed(5) : "0.00"}
              </p>
              
              <div className="mt-3 inline-flex items-center px-2 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-semibold rounded-md border border-emerald-500/20">
                {result?.estimated_cost?.scan_bytes ? (result.estimated_cost.scan_bytes / 1024).toFixed(2) + " KB" : "0 KB"} Scanned
              </div>
            </div>

            {/* Explanation Module */}
            <div className="bg-gradient-to-br from-indigo-900/20 to-purple-900/20 p-6 rounded-xl border border-indigo-500/20 shadow-xl flex-1 backdrop-blur-md">
              <h4 className="text-indigo-400 text-xs font-bold uppercase tracking-wider mb-4 flex items-center">
                Google Gemini Analytics
              </h4>
              
              {loading ? (
                <div className="flex space-x-2 items-center text-slate-400 text-sm animate-pulse">
                  <div className="w-2 h-2 bg-indigo-500 rounded-full"></div>
                  <div className="w-2 h-2 bg-indigo-500 rounded-full delay-75"></div>
                  <div className="w-2 h-2 bg-indigo-500 rounded-full delay-150"></div>
                  <span className="ml-2">Analyzing query execution path...</span>
                </div>
              ) : result?.ai_explanation ? (
                <div className="prose prose-invert prose-sm max-w-none text-slate-300">
                  {/* Primitive Markdown render: Just split by newline and bold asterisks for now since it's a simple dashboard */}
                  {result.ai_explanation.split('\n').map((line, i) => {
                    const l = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\*(.*?)\*/g, '<em>$1</em>');
                    return <p key={i} dangerouslySetInnerHTML={{__html: l}} className="mb-2" />
                  })}
                </div>
              ) : (
                <div className="text-slate-400 text-sm leading-relaxed">
                  Submit a query to see an intelligent breakdown of its performance impact, specific Athena rules applied, and actionable optimization strategies to reduce data scan costs.
                </div>
              )}
            </div>
            
            {/* Tactical Suggestions */}
            {result?.suggestions && result.suggestions.length > 0 && (
              <div className="mt-6">
                <h4 className="text-amber-400/90 text-xs font-bold uppercase tracking-wider mb-3 px-1">Optimization Flags</h4>
                <div className="space-y-2">
                  {result.suggestions.map((s, i) => (
                    <div key={i} className="bg-amber-900/10 border border-amber-500/20 text-amber-200/90 text-sm px-4 py-3 rounded-lg shadow-sm">
                      {s}
                    </div>
                  ))}
                </div>
              </div>
            )}
            
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
