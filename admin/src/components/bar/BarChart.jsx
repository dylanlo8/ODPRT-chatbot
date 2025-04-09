import { useState } from "react";
import { ResponsiveBar } from "@nivo/bar";
import { tokens } from "../../theme";
import PieChart from "../pie/PieChart"; // Ensure this path is correct

const BarChart = ({ data, keys, index, showLegend, hover, topicBreakdown }) => {
  const colors = tokens();
  const [hoveredFaculty, setHoveredFaculty] = useState(null);
  const pieColors = [
    colors.indigo[500],
    colors.gray[500],
    colors.indigo[600],
    colors.gray[600],
    colors.indigo[400],
    colors.gray[400]
  ];

  // Obtain the maximum bar plot value
  const maxY = Math.max(
    ...data.map((d) => Math.max(...keys.map((key) => d[key] ?? 0)))
  );

  // Generate number of ticks according to values
  const generateIntegerTicks = (max, maxTicks = 5) => {
    if (max === 0) return [0];
    const step = Math.ceil(max / maxTicks);
    const lastTick = Math.ceil(max / step) * step;
    return Array.from(
      { length: Math.floor(lastTick / step) + 1 },
      (_, i) => i * step
    );
  };

  const tickValues = generateIntegerTicks(maxY, 5); // Limit to max 5 ticks

  return (
    <div style={{ display: "flex", position: "relative", height: "100%" }}>
      <ResponsiveBar
        data={data}
        keys={keys}
        indexBy={index}
        colors={({ id, data }) => data[`${id}Color`]}
        margin={{ top: 30, right: 60, bottom: showLegend ? 60 : 20, left: 60 }}
        padding={0.5}
        valueScale={{ type: "linear" }}
        indexScale={{ type: "band", round: true }}
        theme={{
          axis: {
            domain: { line: { stroke: "transparent" } },
            legend: { text: { fill: colors.text } },
            ticks: {
              line: { stroke: colors.text, strokeWidth: 1 },
              text: { fill: colors.text },
            },
          },
          legends: {
            text: { fill: colors.comp_background },
          },
        }}
        defs={[
          {
            id: "dots",
            type: "patternDots",
            background: "inherit",
            color: "#38bcb2",
            size: 4,
            padding: 1,
            stagger: true,
          },
          {
            id: "lines",
            type: "patternLines",
            background: "inherit",
            color: "#eed312",
            rotation: -45,
            lineWidth: 6,
            spacing: 10,
          },
        ]}
        borderColor={{
          from: "color",
          modifiers: [["darker", "1.6"]],
        }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
          tickSize: 0,
          tickPadding: 5,
          tickRotation: 0,
          legendOffset: 32,
          renderTick: (tick) => {
            const value = tick.value ?? "";
            const displayValue =
              value.length > 10 ? value.slice(0, 10) + "…" : value;
            return (
              <g transform={`translate(${tick.x},${tick.y + 10})`}>
                <text
                  textAnchor="middle"
                  dominantBaseline="central"
                  style={{ fill: colors.text, fontSize: 11 }}
                >
                  <title>{value}</title>
                  {displayValue}
                </text>
              </g>
            );
          },
        }}
        axisLeft={{
          tickSize: 0,
          tickPadding: 5,
          tickRotation: 0,
          legendOffset: -40,
          fontSize: 11,
          tickValues: tickValues,
        }}
        enableLabel={true}
        label={(d) => `${d.value}`}
        enableGridY={false}
        labelSkipWidth={12}
        labelSkipHeight={12}
        labelTextColor={colors.white}
        legends={
          showLegend
            ? [
                {
                  dataFrom: "keys",
                  anchor: "bottom",
                  direction: "row",
                  justify: false,
                  translateX: 0,
                  translateY: 50,
                  itemsSpacing: 0,
                  itemWidth: 100,
                  itemHeight: 0,
                  itemTextColor: colors.text,
                  itemDirection: "left-to-right",
                  itemOpacity: 1,
                  symbolSize: 15,
                  symbolShape: "circle",
                },
              ]
            : []
        }
        role="application"
        onMouseEnter={(data) => hover && setHoveredFaculty(data.indexValue)}
        onMouseLeave={() => hover && setHoveredFaculty(null)}
        barAriaLabel={(e) =>
          e.id + ": " + e.formattedValue + " in faculty: " + e.indexValue
        }
      />

      {hover && hoveredFaculty && (
        <div
        style={{
          position: "absolute",
          bottom: 50,
          right: -150,
          width: "300px",
          height: "300px",
          background: colors.white,
          border: `1px solid ${colors.gray[200]}`,
          borderRadius: "8px",
          padding: "12px",
          boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
          zIndex: 10,
          }}>

            
          <PieChart
            data={topicBreakdown
              .filter((item) => item.dept?.toLowerCase() === hoveredFaculty?.toLowerCase())
              .map((item, index) => ({
                id: item.query,
                label: item.query,
                value: item.unresolved,
                color: pieColors[index % pieColors.length],
              }))}
          />
        </div>
      )}
    </div>
  );
};

export default BarChart;

