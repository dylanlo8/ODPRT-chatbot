import { ResponsiveBar } from "@nivo/bar";
import { tokens } from "../../theme";

const BarChart = ({ data, keys, index, showLegend}) => {
  const colors = tokens();

  return (
    <ResponsiveBar
      data={data}
      theme={{

        axis: {
          domain: {
            line: {
              stroke: "transparent",
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
            fill: colors.comp_background,
          },
        },
      }}
      keys={ keys }
      indexBy={ index }
      colors={({ id, data }) => data[`${id}Color`]}
      margin={{ top: 30, right: 60 , bottom: showLegend? 60:20, left: 60 }}
      padding={0.5}
      valueScale={{ type: "linear" }}
      indexScale={{ type: "band", round: true }}
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
        renderTick: (tick) => { // limit number of characters for axis 
          const value = tick.value ?? ""; 
          const displayValue = value.length > 10 ? value.slice(0, 10) + "…" : value;
      
          return (
            <g transform={`translate(${tick.x},${tick.y + 10})`}>
              <title>{value}</title> 
              <text
                textAnchor="middle"
                dominantBaseline="central"
                style={{
                  fill: colors.text,
                  fontSize: 12,
                }}
              >
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
        tickValues: 5,
      }}
      enableLabel={false}
      enableGridY={false}
      labelSkipWidth={12}
      labelSkipHeight={12}
      labelTextColor={{
        from: "color",
        modifiers: [["darker", 1.6]],
      }}
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
      barAriaLabel={function (e) {
        return e.id + ": " + e.formattedValue + " in country: " + e.indexValue;
      }}
    />
  );
};

export default BarChart;