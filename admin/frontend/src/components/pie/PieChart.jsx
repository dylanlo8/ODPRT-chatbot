import { ResponsivePie } from "@nivo/pie";
import { tokens } from "../../theme";

const PieChart = ({ data }) => {
  const colors = tokens();
  const total = data.reduce((sum, item) => sum + item.value, 0);
  
  return (
    <ResponsivePie
      data={data}
      theme={{
        axis: {
          domain: {
            line: {
              stroke: colors.text,
            },
          },
          legend: {
            text: {
              fill: colors.text,
            },
          },
          ticks: {
            line: {
              stroke: colors.text,
              strokeWidth: 1,
            },
            text: {
              fill: colors.text,
            },
          },
        },
        legends: {
          text: {
            fill: colors.text,
          },
        },
      }}
      margin={{right: 80, bottom: 30, left: 80 }}
      innerRadius={0.5}
      padAngle={0.7}
      cornerRadius={3}
      activeOuterRadiusOffset={8}
      borderColor={{
        from: "color",
        modifiers: [["darker", 0.2]],
      }}
      enableArcLabels={true}
      enableArcLinkLabels={false}
      arcLabel={(e) => `${((e.value / total) * 100).toFixed(1)}%`} 
      arcLabelsRadiusOffset={0.475} 
      arcLabelsSkipAngle={10} 
      arcLabelsTextColor={({ data }) =>
        data.color === tokens().gray[500] ? "#000000" : "#FFFFFF"
      }
      colors={({ data }) => data.color} 
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
      legends={[
        {
          anchor: "bottom",
          direction: "row",
          justify: false,
          translateX: 0,
          translateY: 35,
          itemsSpacing: 0,
          itemWidth: 100,
          itemHeight: 30,
          itemTextColor: colors.text,
          itemDirection: "left-to-right",
          itemOpacity: 1,
          symbolSize: 15,
          symbolShape: "circle",
        },
      ]}
    />
  );
};

export default PieChart;