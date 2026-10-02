import {
  LayoutDashboard,
  Radar,
  SlidersHorizontal,
  Radio,
  BarChart3,
  FileText,
  Settings,
  Shield,
  Activity,
} from "lucide-react";

const navigation = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    label: "Spectrum View",
    icon: Radar,
  },
  {
    label: "Scan Strategy",
    icon: SlidersHorizontal,
  },
  {
    label: "Emitters",
    icon: Radio,
  },
  {
    label: "Analytics",
    icon: BarChart3,
  },
  {
    label: "Logs",
    icon: FileText,
  },
];

function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 flex h-screen w-[220px] flex-col bg-[#101a2d] text-white">
      
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600">
          <Shield size={22} />
        </div>

        <div>
          <h1 className="text-[16px] font-bold leading-5">
            Sentinel
          </h1>

          <h1 className="text-[16px] font-bold leading-5">
            Knights
          </h1>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4">
        <div className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.15em] text-slate-500">
          Operations
        </div>

        <div className="space-y-1">
          {navigation.map((item, index) => {
            const Icon = item.icon;
            const active = index === 0;

            return (
              <button
                key={item.label}
                className={`group flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-[13px] transition-all ${
                  active
                    ? "bg-blue-600 text-white shadow-lg shadow-blue-900/30"
                    : "text-slate-400 hover:bg-white/5 hover:text-white"
                }`}
              >
                <Icon
                  size={18}
                  strokeWidth={active ? 2.3 : 1.8}
                />

                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </nav>

      {/* Bottom section */}
      <div className="px-3 pb-4">
        <button className="mb-3 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-[13px] text-slate-400 transition hover:bg-white/5 hover:text-white">
          <Settings size={18} />
          <span>Settings</span>
        </button>

        {/* Simulation Card */}
        <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-4">
          <div className="mb-3 flex items-center gap-2">
            <Activity size={15} className="text-blue-400" />

            <span className="text-[11px] font-medium text-slate-300">
              Simulation Time
            </span>
          </div>

          <div className="text-[18px] font-bold tracking-tight">
            2h 14m 32s
          </div>

          <div className="mt-3 text-[10px] text-slate-500">
            SCENARIO ENVIRONMENT
          </div>

          <div className="mt-1 text-[12px] font-medium text-slate-300">
            Urban EW Environment
          </div>

          <div className="mt-3 flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]" />

            <span className="text-[10px] font-medium text-emerald-400">
              SIMULATION ACTIVE
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;