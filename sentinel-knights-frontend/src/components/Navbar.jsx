import {
  Search,
  Pause,
  Square,
  Settings,
  ChevronDown,
} from "lucide-react";

function Navbar() {
  return (
    <header className="fixed left-[220px] right-0 top-0 z-20 h-[72px] border-b border-slate-200 bg-white">
      <div className="flex h-full items-center px-7">

        {/* Search */}
        <div className="flex h-11 w-[360px] items-center gap-3 rounded-xl bg-slate-50 px-4">
          <Search
            size={19}
            className="text-slate-400"
          />

          <input
            type="text"
            placeholder="Search bands, emitters, or scenarios..."
            className="w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
          />
        </div>

        {/* Right controls */}
        <div className="ml-auto flex items-center gap-3">

          {/* Simulation status */}
          <div className="flex items-center gap-3 rounded-xl bg-emerald-50 px-4 py-2">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />

            <div>
              <div className="text-[11px] font-semibold text-emerald-700">
                Simulation Running
              </div>

              <div className="text-[10px] text-emerald-600">
                00:12:36
              </div>
            </div>
          </div>

          {/* Pause */}
          <button className="grid h-10 w-10 place-items-center rounded-full border border-slate-200 bg-white text-slate-700 transition hover:bg-slate-50">
            <Pause size={17} />
          </button>

          {/* Stop */}
          <button className="grid h-10 w-10 place-items-center rounded-full border border-red-100 bg-red-50 text-red-500 transition hover:bg-red-100">
            <Square
              size={14}
              fill="currentColor"
            />
          </button>

          {/* Scenario */}
          <div className="relative ml-2">
            <select className="h-10 appearance-none rounded-xl border border-slate-200 bg-white px-4 pr-9 text-sm font-medium text-slate-700 outline-none">
              <option>Scenario 1</option>
              <option>Scenario 2</option>
              <option>Scenario 3</option>
            </select>

            <ChevronDown
              size={15}
              className="pointer-events-none absolute right-3 top-3 text-slate-500"
            />
          </div>

          {/* Settings */}
          <button className="grid h-10 w-10 place-items-center text-slate-500 hover:text-slate-800">
            <Settings size={19} />
          </button>

          {/* Profile */}
          <div className="grid h-10 w-10 place-items-center rounded-full bg-[#321d77] text-xs font-bold text-white">
            SK
          </div>

        </div>
      </div>
    </header>
  );
}

export default Navbar;