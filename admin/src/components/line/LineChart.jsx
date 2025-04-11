import { ResponsiveLine } from "@nivo/line";
import { tokens } from "../../theme";


const LineChart = ({ data, showLegend }) => {
  const colors = tokens();
  const xLabels = data[0]?.data.map(d => d.x) || [];
  const tickValues = xLabels.length > 0
    ? [xLabels[0], xLabels[xLabels.length - 1]]
    : [];

  return (
    <ResponsiveLine
      data={data}
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
        tooltip: {
          container: {
            color: colors.indigo[500],
          },
        },
      }}
      colors={{ datum: "color" }}
      margin={{ top: 50, right: showLegend ? 150 : 90, bottom: 50, left: 100 }}
      xScale={{ type: "point" }}
      yScale={{
        type: "linear",
        min: "auto",
        max: "auto",
        stacked: true,
        reverse: false,
      }}
      yFormat=" >-.2f"
      curve="catmullRom"
      axisTop={null}
      axisRight={null}
      axisBottom={{
        orient: "bottom",
        tickSize: 0,
        tickPadding: 20,
        tickRotation: 0,
        tickValues, // limit x-axis ticks
      }}
      axisLeft={{
        orient: "left",
        tickValues: 5,
        tickSize: 0,
        tickPadding: 20,
        tickRotation: 0,
      }}
      legends={
        showLegend
          ? [
              {
                dataFrom: "keys",
                anchor: "right",
                direction: "column",
                justify: false,
                translateX: 120,
                translateY: 0,
                itemsSpacing: 0,
                itemWidth: 100,
                itemHeight: 20,
                itemTextColor: colors.text,
                itemDirection: "left-to-right",
                itemOpacity: 1,
                symbolSize: 15,
                symbolShape: "circle",
              },
            ]
          : []
      }
      enableGridX={false}
      enableGridY={false}
      enablePoints={false}
      useMesh={true}
    />
  );
};

export default LineChart;