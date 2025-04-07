import { useState } from "react";
import { Box } from "@mui/material";
import { tokens } from "../theme";
import DateFilter from "../components/DateFilter";
import Header from "../components/Header";
import BarBox from "../components/bar/BarBox";
import FeedbackBox from "../components/feedback/FeedbackBox";
import LineBox from "../components/line/LineBox";
import StatBox from "../components/StatBox";
import ThumbsBox from "../components/thumbs/ThumbsBox";
import TotalUsers from "../components/TotalUsers";
import { fetchDashboardData } from "../api/DashboardApi"; // Import the API function

const Dashboard = () => {
  const colors = tokens();

  // State to manage date filter and dashboard data
  const [dateRange, setDateRange] = useState({ from: "", to: "" });
  const [data, setData] = useState({
    intervention: [],
    commonQueries: [],
    userQueries: [],
    unresolvedQueries: [],
    userExperience: [],
  });
  const [result, setResult] = useState(null);

  // Function to fetch data from the backend
  const fetchData = async (range) => {
    try {
      const result = await fetchDashboardData(range); // Use the API function
      setResult(result); // Store raw results

      // Format common queries data for BarBox
      const commonQueriesData = result.top_topics.map((item) => ({
        query: item.topic,
        resolved:
          item.frequency -
          (result.top_unresolved_topics.find((t) => t.topic === item.topic)?.unresolved_count || 0),
        resolvedColor: tokens().gray[500],
        unresolved: result.top_unresolved_topics.find((t) => t.topic === item.topic)?.unresolved_count || 0,
        unresolvedColor: tokens().indigo[500],
      }));

      // Format unresolved queries data for BarBox
      const unresolvedQueriesData = result.top_unresolved_topics.map((item) => ({
        query: item.topic,
        unresolved: item.unresolved_count,
        unresolvedColor: tokens().indigo[500],
      }));

      // Format user queries over time data for LineBox
      const userQueriesData = [
        {
          id: "queries",
          color: tokens().indigo[500],
          data: result.user_queries_over_time.map((item) => ({
            x: new Date(item.date).toLocaleDateString(),
            y: item.total,
          })),
        },
      ];

      // Format user experience over time data for LineBox
      const userExperienceData = [
        {
          id: "ratings",
          color: tokens().indigo[500],
          data: result.user_experience_over_time.map((item) => ({
            x: new Date(item.date).toLocaleDateString(),
            y: item.avg_rating,
          })),
        },
      ];

      setData({
        commonQueries: commonQueriesData,
        userQueries: userQueriesData,
        unresolvedQueries: unresolvedQueriesData,
        userExperience: userExperienceData,
      });
    } catch (err) {
      console.error("Error fetching data:", err);
    }
  };

  // Function to handle date range changes
  const handleDateChange = (range) => {
    if (range.from && range.to) {
      fetchData(range); // Fetch data for the selected date range
    }
  };

  return (
    <Box mt="30px" mx="30px">
      <Box display="flex" justifyContent="space-between">
        {/* HEADER */}
        <Header title="DASHBOARD" />

        <Box display="flex" gap={2} alignItems="center" mb="10px">
          {/* TOTAL USERS */}
          <TotalUsers figure={result?.total_users || "XX"} />

          {/* DATE FILTER */}
          <Box display="flex" gap="10px">
            <DateFilter
              dateRange={dateRange}
              setDateRange={setDateRange}
              onDateChange={handleDateChange}
            />
          </Box>
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
        <Box
          gridColumn="span 6"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <StatBox
            stats={[
              { title: "Conversations Created", figure: result?.total_conversations || "XX" },
              { title: "New Users", figure: result?.new_users_since_start || "XX" },
              { title: "Interventions", figure: result?.intervention_count || "XX" },
            ]}
          />
        </Box>

        <Box
          gridColumn="span 6"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <ThumbsBox
            upFigure={result?.total_thumbs_up || "XX"}
            upMessages={result?.recent_thumbs_up_messages?.map((msg) => msg.text) || ["XX"]}
            downFigure={result?.total_thumbs_down || "XX"}
            downMessages={result?.recent_thumbs_down_messages?.map((msg) => msg.text) || ["XX"]}
          />
        </Box>

        {/* ROW 2 */}
        <Box
          gridColumn="span 6"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <StatBox
            stats={[
              { title: "Avg Messages per Conversation", figure: result?.avg_messages_per_conversation || "XX" },
              { title: "Average Rating per Conversation", figure: result?.avg_rating || "XX" },
            ]}
          />
        </Box>

        <Box
          gridColumn="span 6"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <FeedbackBox
            feedbacks={result?.recent_feedbacks?.map((fb) => fb.feedback) || ["XX"]}
            dates={result?.recent_feedbacks?.map((fb) => new Date(fb.created_at).toLocaleDateString()) || ["XX"]}
          />
        </Box>

        {/* ROW 3 */}
        <Box
          gridColumn="span 6"
          gridRow="span 2"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <BarBox
            title="Top 10 Conversation Topics"
            data={data.commonQueries}
            keys={["unresolved", "resolved"]}
            index="query"
            showLegend={true}
          />
        </Box>

        <Box
          gridColumn="span 6"
          gridRow="span 2"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <LineBox title="Number of Messages Over Time" data={data.userQueries} showLegend={false} />
        </Box>

        {/* ROW 4 */}
        <Box
          gridColumn="span 6"
          gridRow="span 2"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <BarBox
            title="Top 10 Conversation Topics requiring Intervention"
            data={data.unresolvedQueries}
            keys={["unresolved"]}
            index="query"
            showLegend={false}
          />
        </Box>

        <Box
          gridColumn="span 6"
          gridRow="span 2"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <LineBox title="Average Rating Over Time" data={data.userExperience} showLegend={true} />
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;