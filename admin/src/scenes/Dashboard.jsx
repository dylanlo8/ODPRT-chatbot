import { useState } from "react";
import { Box, TextField } from "@mui/material";
import { tokens } from "../theme";
import { mockUserQueriesData, mockUserExperienceData, mockUsersData, mockInterventionData, mockCommonQueriesData, mockUnresolvedQueriesData } from "../data/mockData";
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import Header from "../components/Header";
import BarBox from "../components/bar/BarBox";
import LineBox from "../components/line/LineBox";
import PieBox from "../components/pie/PieBox";
import StatBox from "../components/StatBox";

const Dashboard = () => {
  const colors = tokens();

  // State to manage date filter
  const [dateRange, setDateRange] = useState({
    from: "",
    to: ""
  });

  // Function to filter data based on the selected date range
  const filterDataByDate = (data) => {
    if (!dateRange.from || !dateRange.to) return data; // If no date selected, return all data

    return data.filter((item) => {
      const itemDate = new Date(item.date); // Convert to Date object
      const fromDate = new Date(dateRange.from);
      const toDate = new Date(dateRange.to);
      return itemDate >= fromDate && itemDate <= toDate;
    });
  };

  return (
    <Box mt="30px" mx="30px">
    <Box display="flex" justifyContent="space-between">
      {/* HEADER */}
      <Header title="DASHBOARD" />

      {/* DATE FILTER */}
      <Box display="flex" gap="10px">
      <TextField
        label="From Date"
        type="date"
        InputLabelProps={{ shrink: true }}
        value={dateRange.from}
        onChange={(e) => setDateRange({ ...dateRange, from: e.target.value })}
        sx={{ width: "140px", "& .MuiInputBase-input": { fontSize: "14px", padding: "8px" } }}
      />
      <TextField
        label="To Date"
        type="date"
        InputLabelProps={{ shrink: true }}
        value={dateRange.to}
        onChange={(e) => setDateRange({ ...dateRange, to: e.target.value })}
        sx={{ width: "140px", "& .MuiInputBase-input": { fontSize: "14px", padding: "8px" } }}
      />
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
          <StatBox title="Conversations" figure="XX" percentage="x.x%" isIncreasing={true} arrow={<ArrowUpwardIcon sx={{ color: colors.green[500], fontSize: "20px" }} />} />
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Avg No. of Messages Per Conversation" figure="XX" percentage="x.x%" isIncreasing={false} arrow={<ArrowDownwardIcon sx={{ color: colors.red[500], fontSize: "20px" }} />} />
        </Box>

        <Box gridColumn="span 3" gridRow="span 2" backgroundColor={colors.white} display="flex" flexDirection="column" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <PieBox title="Users" figure="XX" data={filterDataByDate(mockUsersData)} />
        </Box>

        <Box gridColumn="span 3" gridRow="span 2" backgroundColor={colors.white} display="flex" flexDirection="column" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <PieBox title="Intervention" figure="XX" data={filterDataByDate(mockInterventionData)} />
        </Box>

        {/* ROW 2 */}
        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Turnaround Time" figure="XX" percentage="x.x%" isIncreasing={false} arrow={<ArrowDownwardIcon sx={{ color: colors.red[500], fontSize: "20px" }} />} />
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Resolved Conversations" figure="XX" percentage="x.x%" isIncreasing={true} arrow={<ArrowUpwardIcon sx={{ color: colors.green[500], fontSize: "20px" }} />} />
        </Box>

        {/* ROW 3 */}
        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <BarBox title="Top 10 Most Common Queries" data={filterDataByDate(mockCommonQueriesData)} keys={["unresolved", "resolved"]} index="query" showLegend={true} />
        </Box>

        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <LineBox title="User Queries Over Time" data={filterDataByDate(mockUserQueriesData)} />
        </Box>

        {/* ROW 4 */}
        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <BarBox title="Top 10 Most Common Unresolved Queries" data={filterDataByDate(mockUnresolvedQueriesData)} keys={["unresolved"]} index="query" showLegend={false} />
        </Box>

        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <LineBox title="User Experience Over Time" data={filterDataByDate(mockUserExperienceData)} />
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
