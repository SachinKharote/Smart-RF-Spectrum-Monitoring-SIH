import { TrendingUp, TrendingDown } from "lucide-react";

function KpiCard({
  icon,
  iconBg,
  iconColor,
  title,
  value,
  unit,
  change,
  changeType = "up",
  description,
}) {
  const Icon = icon;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md">

      {/* Top */}
      <div className="flex items-start gap-3">

        {/* Icon */}
        <div
          className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full ${iconBg}`}
        >
          <Icon
            size={21}
            color={iconColor}
            strokeWidth={2}
          />
        </div>

        {/* Information */}
        <div className="min-w-0">

          <p className="text-[12px] font-medium text-slate-500">
            {title}
          </p>

          <div className="mt-1 flex items-baseline gap-1">

            <span className="text-[26px] font-bold tracking-tight text-slate-900">
              {value}
            </span>

            {unit && (
              <span className="text-[13px] font-semibold text-slate-600">
                {unit}
              </span>
            )}

          </div>

          <div className="mt-1 flex items-center gap-2">

            {changeType === "up" ? (
              <TrendingUp
                size={13}
                className="text-emerald-500"
              />
            ) : (
              <TrendingDown
                size={13}
                className="text-emerald-500"
              />
            )}

            <span className="text-[11px] font-semibold text-emerald-600">
              {change}
            </span>

            <span className="text-[10px] text-slate-400">
              {description}
            </span>

          </div>

        </div>
      </div>

      {/* Mini graph */}
      <div className="mt-4 flex h-7 items-end gap-[3px]">

        {[30, 45, 35, 55, 42, 62, 48, 68, 53, 72, 60, 75, 64, 82].map(
          (height, index) => (
            <div
              key={index}
              className="w-[5px] rounded-t-sm opacity-60"
              style={{
                height: `${height}%`,
                backgroundColor: iconColor,
              }}
            />
          )
        )}

      </div>
    </div>
  );
}

export default KpiCard;