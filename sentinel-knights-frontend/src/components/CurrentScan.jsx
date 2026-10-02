import {
  Radio,
  Clock3,
  Target,
  Activity,
} from "lucide-react";

function CurrentScan({ data }) {
  const priorityPercent = Math.round(data.priority * 100);

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">

      {/* Header */}
      <div className="flex items-center justify-between">

        <div className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-50">
            <Radio
              size={18}
              className="text-blue-600"
            />
          </div>

          <div>
            <h2 className="text-[16px] font-bold text-slate-900">
              Current Scan
            </h2>

            <p className="text-[10px] text-slate-400">
              Active receiver decision
            </p>
          </div>
        </div>

        {/* Status */}
        <div className="flex items-center gap-1.5 rounded-full bg-emerald-50 px-2.5 py-1">

          <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-500" />

          <span className="text-[10px] font-semibold text-emerald-600">
            SCANNING
          </span>

        </div>

      </div>

      {/* Frequency */}
      <div className="mt-7">

        <p className="text-[11px] font-medium uppercase tracking-wider text-slate-400">
          Frequency
        </p>

        <div className="mt-1 flex items-baseline gap-1">

          <span className="text-[32px] font-bold tracking-tight text-slate-900">
            {(data.band / 1000).toFixed(2)}
          </span>

          <span className="text-sm font-semibold text-slate-500">
            GHz
          </span>

        </div>

      </div>

      {/* Priority */}
      <div className="mt-6">

        <div className="mb-2 flex items-center justify-between">

          <span className="text-[11px] font-medium text-slate-500">
            Scan Priority
          </span>

          <span className="text-sm font-bold text-blue-600">
            {priorityPercent}%
          </span>

        </div>

        <div className="h-2 overflow-hidden rounded-full bg-slate-100">

          <div
            className="h-full rounded-full bg-blue-600 transition-all"
            style={{
              width: `${priorityPercent}%`,
            }}
          />

        </div>

      </div>

      {/* Details */}
      <div className="mt-6 space-y-3">

        <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-3">

          <div className="flex items-center gap-2">

            <Clock3
              size={16}
              className="text-slate-400"
            />

            <span className="text-[11px] text-slate-500">
              Dwell Time
            </span>

          </div>

          <span className="text-sm font-semibold text-slate-800">
            {data.dwell_ms} ms
          </span>

        </div>

        <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-3">

          <div className="flex items-center gap-2">

            <Target
              size={16}
              className="text-slate-400"
            />

            <span className="text-[11px] text-slate-500">
              Priority Score
            </span>

          </div>

          <span className="text-sm font-semibold text-slate-800">
            {data.priority.toFixed(2)}
          </span>

        </div>

        <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-3">

          <div className="flex items-center gap-2">

            <Activity
              size={16}
              className="text-slate-400"
            />

            <span className="text-[11px] text-slate-500">
              Scan Status
            </span>

          </div>

          <span className="text-[10px] font-bold text-emerald-600">
            ACTIVE
          </span>

        </div>

      </div>

    </div>
  );
}

export default CurrentScan;