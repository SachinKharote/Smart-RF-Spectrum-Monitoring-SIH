import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

function AdaptiveScanTimeline({ data }) {
  const chartData = {
    labels: data.map((item) => `T${item.time}`),

    datasets: [
      {
        label: "Scan Band",

        data: data.map((item) => item.band),

        borderColor: "#2563eb",

        backgroundColor: "#2563eb",

        borderWidth: 2,

        tension: 0.3,

        pointRadius: data.map((item) =>
          item.result === "hit" ? 6 : 4
        ),

        pointBackgroundColor: data.map((item) =>
          item.result === "hit"
            ? "#ef4444"
            : "#2563eb"
        ),

        pointBorderColor: "#ffffff",

        pointBorderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,

    maintainAspectRatio: false,

    plugins: {
      legend: {
        display: false,
      },

      tooltip: {
        callbacks: {
          label: (context) => {
            const event = data[context.dataIndex];

            return `${event.band} MHz — ${event.result.toUpperCase()}`;
          },
        },
      },
    },

    scales: {
      x: {
        grid: {
          color: "#eef2f7",
        },

        ticks: {
          color: "#64748b",
        },

        title: {
          display: true,
          text: "Scan Time",
        },
      },

      y: {
        min: 1000,

        max: 6000,

        grid: {
          color: "#eef2f7",
        },

        ticks: {
          color: "#64748b",

          callback: (value) => `${value} MHz`,
        },

        title: {
          display: true,
          text: "Frequency",
        },
      },
    },
  };

  return (
    <div className="w-full rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">

      {/* Header */}

      <div className="mb-4 flex items-center justify-between">

        <div>
          <h2 className="text-base font-bold text-slate-900">
            Adaptive Scan Timeline
          </h2>

          <p className="mt-1 text-xs text-slate-400">
            ML scheduler scan decisions over time
          </p>
        </div>

        <div className="flex items-center gap-4 text-[10px]">

          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-blue-600" />
            Scan
          </div>

          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-red-500" />
            Hit
          </div>

          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-blue-400" />
            Miss
          </div>

        </div>

      </div>

      {/* Chart */}

      <div className="relative h-[300px] w-full">

        <Line
          data={chartData}
          options={options}
        />

      </div>

    </div>
  );
}

export default AdaptiveScanTimeline;