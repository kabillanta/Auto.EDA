/* eslint-disable @typescript-eslint/no-explicit-any */
import Link from "next/link";
import {
  BarChart3,
  Zap,
  BrainCircuit,
  ArrowRight,
  LayoutDashboard,
  Github
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white text-slate-900 font-sans selection:bg-[#5B7FFF]/20">
      {/* 1. Navbar */}
      <nav className="border-b border-slate-100 bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-[#5B7FFF] p-2 rounded-lg">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold tracking-tight text-slate-900">
              Auto.EDA
            </span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-500">
            <a
              href="#features"
              className="hover:text-[#5B7FFF] transition-colors"
            >
              Features
            </a>
            <Link
              href="/dashboard"
              className="bg-slate-900 text-white px-5 py-2.5 rounded-full hover:bg-[#5B7FFF] transition-colors flex items-center gap-2"
            >
              Launch App <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </nav>

      {/* 2. Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top_right,var(--tw-gradient-stops))] from-[#5B7FFF]/10 via-slate-50 to-white"></div>

        <div className="max-w-7xl mx-auto px-6 text-center lg:text-left lg:flex items-center gap-16">
          <div className="lg:w-1/2 space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-[#5B7FFF] text-xs font-bold uppercase tracking-wider border border-blue-100">
              <Zap className="w-3 h-3" /> v2.0 is live
            </div>
            <h1 className="text-5xl lg:text-7xl font-extrabold tracking-tight text-slate-900 leading-[1.1]">
              Data Analysis, <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#5B7FFF] to-blue-600">
                Automated.
              </span>
            </h1>
            <p className="text-xl text-slate-600 leading-relaxed max-w-2xl">
              Stop writing boilerplate Pandas code. Upload your dataset and get
              instant AI summaries, distribution charts, and correlation
              matrices in seconds.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Link
                href="/dashboard"
                className="inline-flex justify-center items-center px-8 py-4 text-base font-bold text-white bg-[#5B7FFF] rounded-xl shadow-lg shadow-blue-500/20 hover:bg-blue-600 hover:scale-[1.02] transition-all duration-200"
              >
                Start Analyzing Free
              </Link>
              <Link
                href="https://www.github.com/kabillanta/auto.eda"
                className="inline-flex justify-center items-center gap-2 px-8 py-4 text-base font-bold text-slate-700 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-all"
              >
             <Github/>   Github 
              
              </Link>
            </div>
            <div className="flex items-center gap-4 text-sm text-slate-500 pt-4">
              <div className="flex -space-x-2">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="w-8 h-8 rounded-full bg-slate-200 border-2 border-white"
                  ></div>
                ))}
              </div>
              <p>Used by 500+ Data Scientists</p>
            </div>
          </div>

          {/* Hero Image / Graphic */}
          <div className="hidden lg:block lg:w-1/2 relative">
            <div className="relative z-10 bg-white rounded-2xl shadow-2xl shadow-slate-200/50 border border-slate-100 p-2 transform rotate-2 hover:rotate-0 transition-transform duration-500">
              <div className="bg-slate-50 rounded-xl overflow-hidden border border-slate-100 aspect-[4/3] flex items-center justify-center relative">
                {/* Decorative UI elements mimicking the app */}
                <div className="absolute top-4 left-4 right-4 h-8 bg-white rounded-md shadow-sm"></div>
                <div className="absolute top-16 left-4 w-1/3 bottom-4 bg-white rounded-md shadow-sm"></div>
                <div className="absolute top-16 right-4 w-3/5 h-1/2 bg-[#5B7FFF]/10 rounded-md border border-[#5B7FFF]/20 flex items-center justify-center">
                  <BarChart3 className="w-12 h-12 text-[#5B7FFF]" />
                </div>
                <div className="absolute bottom-4 right-4 w-3/5 h-1/3 bg-white rounded-md shadow-sm"></div>
              </div>
            </div>
            {/* Decorative blobs */}
            <div className="absolute -top-10 -right-10 w-72 h-72 bg-[#5B7FFF]/20 rounded-full blur-3xl -z-10"></div>
          </div>
        </div>
      </section>

      {/* 3. Features Section */}
      <section
        id="features"
        className="py-24 bg-slate-50 border-t border-slate-100"
      >
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">
              Everything you need to understand your data
            </h2>
            <p className="text-lg text-slate-600">
              We combine traditional statistical methods with modern LLMs to
              give you the complete picture.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<BrainCircuit className="w-8 h-8 text-[#5B7FFF]" />}
              title="AI Summaries"
              desc="Our Gemini-powered engine reads your data and generates a plain-English executive summary highlighting key trends."
            />
            <FeatureCard
              icon={<BarChart3 className="w-8 h-8 text-[#5B7FFF]" />}
              title="Auto Visualization"
              desc="Automatically detects column types (categorical vs numerical) and generates the perfect chart for every feature."
            />
            <FeatureCard
              icon={<LayoutDashboard className="w-8 h-8 text-[#5B7FFF]" />}
              title="Correlation Matrix"
              desc="Instantly spot relationships between variables with our heatmap and pairwise scatter plot analysis."
            />
          </div>
        </div>
      </section>

      {/* 4. Footer */}
      <footer className="bg-white border-t border-slate-100 py-12">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
          {/* Brand & Copyright */}
          <div className="flex flex-col items-center md:items-start gap-2">
            <div className="flex items-center gap-2">
              <div className="bg-slate-900 p-1.5 rounded-lg">
                <BarChart3 className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-slate-900">Auto.EDA</span>
            </div>
            <p className="text-slate-500 text-sm">
              © 2024 Auto.EDA. Open Source Project.
            </p>
          </div>

          {/* Personal Branding */}
          <div className="text-center md:text-right">
            <p className="text-slate-600 font-medium">
              Designed & Built by{" "}
              <a
                href="https://kabillanta.me"
                target="_blank"
                className="text-[#5B7FFF] hover:underline"
              >
                Kabillan T A
              </a>
            </p>
            <div className="flex items-center justify-center md:justify-end gap-4 mt-2 text-sm text-slate-500">
              <a
                href="https://github.com/kabillanta"
                target="_blank"
                className="hover:text-slate-900 transition-colors"
              >
                GitHub
              </a>
              <span>•</span>
              <a
                href="https://linkedin.com/in/kabillan"
                target="_blank"
                className="hover:text-slate-900 transition-colors"
              >
                LinkedIn
              </a>
              <span>•</span>
              <a
                href="mailto:kabillan1905@example.com"
                className="hover:text-slate-900 transition-colors"
              >
                Contact
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

// Helper Component for Feature Cards
function FeatureCard({
  icon,
  title,
  desc,
}: {
  icon: any;
  title: string;
  desc: string;
}) {
  return (
    <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
      <div className="bg-blue-50 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-slate-900 mb-3">{title}</h3>
      <p className="text-slate-600 leading-relaxed">{desc}</p>
    </div>
  );
}
