import { useState } from "react";
import { Box } from "@mui/material";
import { tokens } from "../theme";
import { mockUserQueriesData, mockUserExperienceData, mockInterventionData, mockCommonQueriesData, mockUnresolvedQueriesData } from "../data/mockData";
import DateFilter from "../components/date_filter/DateFilter"
import { filterDataByDate } from "../components/date_filter/DateUtils"
import Header from "../components/Header";
import BarBox from "../components/bar/BarBox";
import LineBox from "../components/line/LineBox";
import PieBox from "../components/pie/PieBox";
import StatBox from "../components/StatBox";

const Dashboard = ({rawData}) => {
  const colors = tokens();

  // State to manage date filter
  const [dateRange, setDateRange] = useState({ from: "", to: "" });

  return (
    <Box mt="30px" mx="30px">
    <Box display="flex" justifyContent="space-between">
      {/* HEADER */}
      <Header title="DASHBOARD" />

      {/* DATE FILTER */}
      <Box display="flex" gap="10px">
      <DateFilter dateRange={dateRange} setDateRange={setDateRange} />
    </Box>
    </Box>

      {/* GRID & COMPONENTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="110px"
        gap="20px"
      >
        {/* ROW 1 */}
        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Conversations" figure="XX" />
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Avg No. of Messages per Conversation" figure="XX" />
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Total Users" figure="XX" />
        </Box>       

        <Box gridColumn="span 3" gridRow="span 2" backgroundColor={colors.white} display="flex" flexDirection="column" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <PieBox title="Intervention" figure="XX" data={filterDataByDate(mockInterventionData, dateRange)} />
        </Box>

        {/* ROW 2 */}
        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Avg Time Spent per Conversation" figure="XX"/>
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Avg Rating per Conversation" figure="XX"/>
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="New Users" figure="XX" />
        </Box> 

        {/* ROW 3 */}
        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <BarBox title="Top 10 Most Common Queries" data={filterDataByDate(mockCommonQueriesData, dateRange)} keys={["unresolved", "resolved"]} index="query" showLegend={true} />
        </Box>

        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <LineBox title="User Queries Over Time" data={filterDataByDate(mockUserQueriesData, dateRange)} showLegend={false}/>
        </Box>

        {/* ROW 4 */}
        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <BarBox title="Top 10 Most Common Unresolved Queries" data={filterDataByDate(mockUnresolvedQueriesData, dateRange)} keys={["unresolved"]} index="query" showLegend={false} />
        </Box>

        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <LineBox title="User Experience Over Time" data={filterDataByDate(mockUserExperienceData, dateRange)} showLegend={true}/>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
