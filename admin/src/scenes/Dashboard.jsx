import axios from "axios";
import { useState } from "react";
import { Box } from "@mui/material";
import { tokens } from "../theme";
// import { mockUserQueriesData, mockUserExperienceData, mockInterventionData, mockCommonQueriesData, mockUnresolvedQueriesData } from "../data/mockData";
import DateFilter from "../components/date_filter/DateFilter"
// import { filterDataByDate } from "../components/date_filter/DateUtils"
import Header from "../components/Header";
import BarBox from "../components/bar/BarBox";
import LineBox from "../components/line/LineBox";
import PieBox from "../components/pie/PieBox";
import StatBox from "../components/StatBox";

const Dashboard = () => {
  const colors = tokens();

  // State to manage date filter
  const [dateRange, setDateRange] = useState({ from: "", to: "" });
  const [data, setData] = useState({
    intervention: [],
    commonQueries: [],
    userQueries: [],
    unresolvedQueries: [],
    userExperience: [], 
  })

const fetchData = async (range) => {
  try {
    const [
      interventionRes,
      commonRes,
      userRes,
      unresolvedRes,
      experienceRes,
    ] = await Promise.all([
      axios.get("/api/intervention", { params: range }),
      axios.get("/api/common-queries", { params: range }), 
      axios.get("/api/user-queries", { params: range }),
      axios.get("/api/unresolved-queries", { params: range }),
      axios.get("/api/user-experience", { params: range }),
    ]);

    setData({
      intervention: interventionRes.data,
      commonQueries: commonRes.data,
      userQueries: userRes.data,
      unresolvedQueries: unresolvedRes.data,
      userExperience: experienceRes.data,
    });
  } catch (err) {
    console.error("Error fetching data:", err);
  }
  };

  const handleDateChange = (range) => {
    if (range.from && range.to) {
      fetchData(range); // send to backend
    }
  };

  return (
    <Box mt="30px" mx="30px">
    <Box display="flex" justifyContent="space-between">
      {/* HEADER */}
      <Header title="DASHBOARD" />

      {/* DATE FILTER */}
      <Box display="flex" gap="10px">
      <DateFilter
        dateRange={dateRange}
        setDateRange={setDateRange}
        onDateChange={handleDateChange}
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
          <StatBox title="Conversations" figure="XX" />
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Avg No. of Messages per Conversation" figure="XX" />
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Total Users" figure="XX" />
        </Box>       

        <Box gridColumn="span 3" gridRow="span 2" backgroundColor={colors.white} display="flex" flexDirection="column" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <PieBox title="Intervention" figure="XX" data={data.intervention} />
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
          <BarBox title="Top 10 Most Common Queries" data={data.commonQueries} keys={["unresolved", "resolved"]} index="query" showLegend={true} />
        </Box>

        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <LineBox title="User Queries Over Time" data={data.userQueries} showLegend={false}/>
        </Box>

        {/* ROW 4 */}
        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <BarBox title="Top 10 Most Common Unresolved Queries" data={data.unresolvedQueries} keys={["unresolved"]} index="query" showLegend={false} />
        </Box>

        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <LineBox title="User Experience Over Time" data={data.userExperience} showLegend={true}/>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
