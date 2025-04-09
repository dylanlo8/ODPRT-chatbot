import { ResponsivePie } from "@nivo/pie";
import { tokens } from "../../theme";

const PieChart = ({ data }) => {
  const colors = tokens();
  const total = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <div style={{ width: "100%", height: "100%" }}>
      <ResponsivePie
        data={data}
        margin={{ right: 50, bottom: 60, left: 50 }}
        innerRadius={0.5}
        padAngle={0.7}
        cornerRadius={3}
        activeOuterRadiusOffset={8}
        borderWidth={1}
        borderColor={{ from: "color", modifiers: [["darker", 0.2]] }}

        // Arc label: shows percentage of each slice
        enableArcLabels={true}
        arcLabel={(e) => `${((e.value / total) * 100).toFixed(1)}%`}
        arcLabelsRadiusOffset={0.45}
        arcLabelsSkipAngle={10}
        arcLabelsTextColor={({ data }) =>
          data.color === tokens().gray[500] ? "#000000" : "#FFFFFF"
        }

        // Arc link labels are disabled for cleaner view
        enableArcLinkLabels={false}

        // Use per-slice colors
        colors={({ data }) => data.color}

        // Theme
        theme={{
          axis: {
            domain: { line: { stroke: colors.text } },
            legend: { text: { fill: colors.text} },
            ticks: {
              line: { stroke: colors.text, strokeWidth: 1 },
              text: { fill: colors.text },
            },
          },
          legends: {
            text: { fill: colors.text, fontSize: 8},
          },
        }}

        // Optional defs (can be removed if not using patterns)
        defs={[
          {
            id: "dots",
            type: "patternDots",
            background: "inherit",
            color: "rgba(255, 255, 255, 0.3)",
            size: 4,
            padding: 1,
            stagger: true,
          },
          {
            id: "lines",
            type: "patternLines",
            background: "inherit",
            color: "rgba(255, 255, 255, 0.3)",
            rotation: -45,
            lineWidth: 6,
            spacing: 10,
          },
        ]}

        // Legend styling
        legends={[
          {
            anchor: "bottom",
            direction: "column",
            translateX: -50,
            translateY: 0,
            itemsSpacing: 5,
            itemWidth: 100,
            itemHeight: 0,
            itemTextColor: colors.text,
            itemDirection: "left-to-right",
            itemOpacity: 1,
            symbolSize: 12,
            symbolShape: "circle",
          },
        ]}
      />
    </div>
  );
};

export default PieChart;
