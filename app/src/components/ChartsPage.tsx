import React, { useState } from "react";
import Plot from "react-plotly.js";
import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";

const ChartsPage = () => {
  const [selectedChart, setSelectedChart] = useState("comparative");
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  // Data for comparative timeline
  const comparativeData = {
    data: [
      {
        x: [
          "2021-11",
          "2021-12",
          "2022-01",
          "2022-02",
          "2022-03",
          "2022-04",
          "2022-05",
          "2022-06",
          "2022-07",
          "2022-08",
          "2022-09",
          "2022-10",
          "2022-11",
          "2022-12",
          "2023-01",
          "2023-02",
          "2023-03",
          "2023-04",
          "2023-05",
          "2023-06",
          "2023-07",
          "2023-08",
          "2023-09",
          "2023-10",
          "2023-11",
          "2023-12",
          "2024-01",
          "2024-02",
          "2024-03",
          "2024-04",
          "2024-05",
          "2024-06",
          "2024-07",
          "2024-08",
          "2024-09",
          "2024-10",
          "2024-11",
          "2024-12",
          "2025-01",
        ],
        y: [
          43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61,
          43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61,
          43.61, 43.61, 43.61, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08,
          0.08, 0.08, 0.08, 0.08, 0.75, 0.75, 0.75, 0.75,
        ],
        type: "scatter",
        name: "France",
        line: { color: "rgb(55, 83, 109)" },
      },
      {
        x: [
          "2021-11",
          "2021-12",
          "2022-01",
          "2022-02",
          "2022-03",
          "2022-04",
          "2022-05",
          "2022-06",
          "2022-07",
          "2022-08",
          "2022-09",
          "2022-10",
          "2022-11",
          "2022-12",
          "2023-01",
          "2023-02",
          "2023-03",
          "2023-04",
          "2023-05",
          "2023-06",
          "2023-07",
          "2023-08",
          "2023-09",
          "2023-10",
          "2023-11",
          "2023-12",
          "2024-01",
          "2024-02",
          "2024-03",
          "2024-04",
          "2024-05",
          "2024-06",
          "2024-07",
          "2024-08",
          "2024-09",
          "2024-10",
          "2024-11",
          "2024-12",
          "2025-01",
        ],
        y: [
          71.7, 71.7, 71.7, 71.7, 71.7, 71.7, 71.7, 71.7, 71.7, 71.7, 71.7,
          71.7, 71.7, 71.7, 71.7, 71.7, 71.7, 71.7, 71.7, 71.7, 71.7, 71.7,
          71.7, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0,
          24.0, 24.0, 99.0, 99.0, 99.0, 99.0,
        ],
        type: "scatter",
        name: "Control Group",
        line: { color: "rgb(26, 118, 255)" },
      },
      {
        x: ["2023-10", "2024-10"],
        y: [0, 150],
        type: "scatter",
        name: "Vaccination Period",
        fill: "tozeroy",
        fillcolor: "rgba(255, 255, 0, 0.2)",
        line: { width: 0 },
        showlegend: true,
      },
    ],
    layout: {
      title: "HPAI Outbreaks Over Time",
      xaxis: { title: "Date" },
      yaxis: { title: "Number of Outbreaks" },
      hovermode: "closest",
      showlegend: true,
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: {
        family: "Arial, sans-serif",
      },
    },
  };

  // Data for period comparison
  const periodComparisonData = {
    data: [
      {
        type: "bar",
        x: ["Pre-Vaccination", "Vaccination", "Post-Vaccination"],
        y: [43.61, 0.08, 0.75],
        name: "France",
        error_y: {
          type: "data",
          array: [74.78, 0.28, 0.5],
          visible: true,
        },
        marker: {
          color: "rgb(55, 83, 109)",
        },
      },
      {
        type: "bar",
        x: ["Pre-Vaccination", "Vaccination", "Post-Vaccination"],
        y: [71.7, 24.0, 99.0],
        name: "Control Group",
        error_y: {
          type: "data",
          array: [68.53, 27.26, 57.64],
          visible: true,
        },
        marker: {
          color: "rgb(26, 118, 255)",
        },
      },
    ],
    layout: {
      title: "Average Monthly Outbreaks by Period",
      barmode: "group",
      xaxis: { title: "Period" },
      yaxis: { title: "Average Number of Outbreaks" },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: {
        family: "Arial, sans-serif",
      },
    },
  };

  // Data for seasonal patterns
  const seasonalData = {
    data: [
      {
        type: "heatmap",
        z: [
          [
            43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61, 43.61,
            43.61, 43.61, 43.61,
          ],
          [
            0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08,
            0.08,
          ],
          [
            0.75,
            0.75,
            0.75,
            0.75,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
          ],
        ],
        x: [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
        ],
        y: ["Pre-Vaccination", "Vaccination", "Post-Vaccination"],
        colorscale: "YlOrRd",
      },
    ],
    layout: {
      title: "Seasonal Pattern of HPAI Outbreaks",
      xaxis: { title: "Month" },
      yaxis: { title: "Period" },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: {
        family: "Arial, sans-serif",
      },
    },
  };

  const charts = {
    comparative: {
      data: comparativeData.data,
      layout: comparativeData.layout,
    },
    periods: {
      data: periodComparisonData.data,
      layout: periodComparisonData.layout,
    },
    seasonal: {
      data: seasonalData.data,
      layout: seasonalData.layout,
    },
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToAdd: ["hoverclosest", "hovercompare"],
    modeBarButtonsToRemove: ["lasso2d", "select2d"],
  };

  return (
    <section id="charts" className="py-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 50 }}
          animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-8">
            Interactive Analysis
          </h2>

          <div className="flex justify-center gap-4 mb-12">
            <button
              onClick={() => setSelectedChart("comparative")}
              className={`px-6 py-3 rounded-lg transition-all duration-300 ${
                selectedChart === "comparative"
                  ? "bg-blue-600 text-white shadow-lg"
                  : "bg-white text-gray-700 hover:bg-blue-50"
              }`}
            >
              Timeline Comparison
            </button>
            <button
              onClick={() => setSelectedChart("periods")}
              className={`px-6 py-3 rounded-lg transition-all duration-300 ${
                selectedChart === "periods"
                  ? "bg-blue-600 text-white shadow-lg"
                  : "bg-white text-gray-700 hover:bg-blue-50"
              }`}
            >
              Period Analysis
            </button>
            <button
              onClick={() => setSelectedChart("seasonal")}
              className={`px-6 py-3 rounded-lg transition-all duration-300 ${
                selectedChart === "seasonal"
                  ? "bg-blue-600 text-white shadow-lg"
                  : "bg-white text-gray-700 hover:bg-blue-50"
              }`}
            >
              Seasonal Patterns
            </button>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={
            inView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.95 }
          }
          transition={{ duration: 0.8, delay: 0.2 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <Plot
            data={charts[selectedChart].data}
            layout={charts[selectedChart].layout}
            config={config}
            useResizeHandler={true}
            className="w-full h-[500px]"
          />
        </motion.div>
      </div>
    </section>
  );
};

export default ChartsPage;
