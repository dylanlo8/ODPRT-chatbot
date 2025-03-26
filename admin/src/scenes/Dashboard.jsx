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
  });
  const [result, setResult] = useState(null);

const fetchData = async (range) => {
  try {
    const BASE_URL = "http://localhost:8000";
      
    const response = await axios.post(`${BASE_URL}/dashboard/fetch`, {
      start_date: String(range.from),
      end_date: String(range.to),
    });

    const result = response.data;
    setResult(result); // Store raw results
    
    // Format intervention data for PieBox
    const interventionData = [
      {
        id: "intervention required",
        label: "Intervention Required",
        value: result.intervention_count,
        color: tokens().indigo[500],
      },
      {
        id: "no intervention",
        label: "No Intervention",
        value: result.total_conversations - result.intervention_count,
        color: tokens().gray[500],
      }
    ];

    // Format common queries data for BarBox
    const commonQueriesData = result.top_topics.map(item => ({
      query: item.topic,
      resolved: item.frequency - (result.top_unresolved_topics.find(t => t.topic === item.topic)?.unresolved_count || 0),
      resolvedColor: tokens().gray[500],
      unresolved: result.top_unresolved_topics.find(t => t.topic === item.topic)?.unresolved_count || 0,
      unresolvedColor: tokens().indigo[500],
    }));

    // Format unresolved queries data for BarBox
    const unresolvedQueriesData = result.top_unresolved_topics.map(item => ({
      query: item.topic,
      unresolved: item.unresolved_count,
      unresolvedColor: tokens().indigo[500],
    }));

    // Format user queries over time data for LineBox
    const userQueriesData = [
      {
        id: "queries",
        color: tokens().indigo[500],
        data: result.user_queries_over_time.map(item => ({
          x: new Date(item.date).toLocaleDateString(),
          y: item.total,
        })),
      }
    ];

    // Format user experience over time data for LineBox
    const userExperienceData = [
      {
        id: "ratings",
        color: tokens().indigo[500],
        data: result.user_experience_over_time.map(item => ({
          x: new Date(item.date).toLocaleDateString(),
          y: item.avg_rating,
        })),
      }
    ];

    setData({
      intervention: interventionData,
      commonQueries: commonQueriesData,
      userQueries: userQueriesData,
      unresolvedQueries: unresolvedQueriesData,
      userExperience: userExperienceData,
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
          <StatBox title="Conversations Created" figure={result?.total_conversations || "XX"} />
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Avg No. of Messages per Conversation" figure={result?.avg_messages_per_conversation || "XX"} />
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Total Users" figure={result?.total_users || "XX"} />
        </Box>       

        <Box gridColumn="span 3" gridRow="span 2" backgroundColor={colors.white} display="flex" flexDirection="column" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <PieBox title="Interventions" figure={result?.intervention_count || "XX"} data={data.intervention} />
        </Box>

        {/* ROW 2 */}
        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Avg Time Spent per Conversation" figure={result?.avg_time_spent_per_conversation_seconds ? `${Math.floor(result.avg_time_spent_per_conversation_seconds / 60)}m ${Math.floor(result.avg_time_spent_per_conversation_seconds % 60)}s` : "XX"}/>
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="Avg Rating per Conversation" figure={result?.avg_rating || "XX"}/>
        </Box>

        <Box gridColumn="span 3" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <StatBox title="New Users" figure={result?.new_users_since_start || "XX"} />
        </Box> 

        {/* ROW 3 */}
        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <BarBox title="Top 10 Conversation Topics" data={data.commonQueries} keys={["unresolved", "resolved"]} index="query" showLegend={true} />
        </Box>

        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <LineBox title="Number of User Queries Over Time" data={data.userQueries} showLegend={false}/>
        </Box>

        {/* ROW 4 */}
        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <BarBox title="Top 10 Converstion Topics requiring Intervention" data={data.unresolvedQueries} keys={["unresolved"]} index="query" showLegend={false} />
        </Box>

        <Box gridColumn="span 6" gridRow="span 2" backgroundColor={colors.white} display="flex" alignItems="center" justifyContent="center" borderRadius="12px" border={`2px solid ${colors.gray[200]}`}>
          <LineBox title="Average Rating Over Time" data={data.userExperience} showLegend={true}/>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;