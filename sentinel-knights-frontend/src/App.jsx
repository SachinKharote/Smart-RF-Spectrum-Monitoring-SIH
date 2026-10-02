import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";

import KpiCard from "./components/KpiCard";
import AdaptiveScanTimeline from "./components/AdaptiveScanTimeline";
import CurrentScan from "./components/CurrentScan";

import {
  adaptiveScanTimeline,
  currentScan,
} from "./data/mockData";
import {
  Radio,
  ShieldAlert,
  Zap,
  Crosshair,
  Radar,
} from "lucide-react";
function App() {
  return (
    <div className="min-h-screen bg-[#f4f7fb]">

      <Sidebar />

      <Navbar />

      <main className="ml-[220px] pt-[72px]">
        <div className="p-7">

          <h1 className="text-2xl font-bold text-slate-900">
            Smart Scan Strategy
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Adaptive electronic-warfare spectrum monitoring
          </p>

        </div>
      </main>
    <main className="ml-[220px] pt-[72px]">

  <div className="p-7">

    {/* Page Heading */}
    <div className="mb-5">
      <h1 className="text-2xl font-bold text-slate-900">
        Smart Scan Strategy
      </h1>

      <p className="mt-1 text-sm text-slate-500">
        Adaptive electronic-warfare spectrum monitoring
      </p>
    </div>

    {/* KPI Cards */}
    <section className="grid grid-cols-5 gap-3">

      <KpiCard
        icon={Radio}
        iconBg="bg-violet-50"
        iconColor="#7c3aed"
        title="Detection Rate"
        value="78.4"
        unit="%"
        change="+6.2%"
        description="vs. baseline sweep"
      />

      <KpiCard
        icon={ShieldAlert}
        iconBg="bg-red-50"
        iconColor="#ef4444"
        title="False Alarm Rate"
        value="6.8"
        unit="%"
        change="-2.1%"
        changeType="down"
        description="vs. baseline sweep"
      />

      <KpiCard
        icon={Zap}
        iconBg="bg-amber-50"
        iconColor="#f59e0b"
        title="Average Intercept Time"
        value="3.2"
        unit="s"
        change="-42%"
        changeType="down"
        description="vs. baseline sweep"
      />

      <KpiCard
        icon={Crosshair}
        iconBg="bg-blue-50"
        iconColor="#2563eb"
        title="Average Intercept Rate"
        value="4.7"
        unit="/min"
        change="+18%"
        description="vs. baseline sweep"
      />

      <KpiCard
        icon={Radar}
        iconBg="bg-emerald-50"
        iconColor="#16a34a"
        title="Current Scan"
        value="2.45"
        unit="GHz"
        change="150 ms"
        description="adaptive dwell"
      />
    {/* Adaptive Scan Section */}
<section className="mt-4 grid w-full grid-cols-1 gap-4 xl:grid-cols-[minmax(0,1fr)_320px]">

  <div className="min-w-0">
    <AdaptiveScanTimeline
      data={adaptiveScanTimeline}
    />
  </div>

  <div className="min-w-0">
    <CurrentScan
      data={currentScan}
    />
  </div>

</section>
    </section>

  </div>

</main>
    </div>
  );
}

export default App;