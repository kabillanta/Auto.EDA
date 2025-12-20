import { Download, FileX } from "lucide-react";

interface DownloadButtonProps {
  isReady: boolean; // Controls if the report is ready
  onDownload: () => void; // Function to trigger download
}

export default function DownloadButton({ isReady, onDownload }: DownloadButtonProps) {
  return (
    <button
      onClick={onDownload}
      disabled={!isReady}
      className={`
        relative overflow-hidden group flex items-center gap-3 px-6 py-3 rounded-xl font-bold transition-all duration-300
        ${
          isReady
            ? "bg-[#5B7FFF] text-white shadow-lg shadow-blue-500/25 hover:bg-blue-600 hover:scale-[1.02] active:scale-95 cursor-pointer"
            : "bg-slate-100 text-slate-400 border border-slate-200 cursor-not-allowed"
        }
      `}
    >
      {/* Icon Switcher */}
      {isReady ? (
        <Download className="w-5 h-5 animate-bounce-short" />
      ) : (
        <FileX className="w-5 h-5" />
      )}

      <span>
        {isReady ? "Download Analysis Report" : "Waiting for Report..."}
      </span>

      {/* Optional: Shine Effect when ready */}
      {isReady && (
        <div className="absolute inset-0 -translate-x-full group-hover:animate-[shimmer_1.5s_infinite] bg-gradient-to-r from-transparent via-white/20 to-transparent z-10" />
      )}
    </button>
  );
}