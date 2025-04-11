import { useState, useEffect } from "react";
import { Box } from "@mui/material";
import { tokens } from "../theme";
import DateFilter from "../components/DateFilter";
import ExportButton from "../components/export/ExportButton";
import Header from "../components/Header";
import BarBox from "../components/bar/BarBox";
import FeedbackBox from "../components/feedback/FeedbackBox";
import LineBox from "../components/line/LineBox";
import StatBox from "../components/StatBox";
import ThumbsBox from "../components/thumbs/ThumbsBox";
import TotalUsers from "../components/TotalUsers";
import { fetchDashboardData } from "../api/DashboardApi"; // Import the API function
import { exportDashboardDataToExcel } from "../components/export/Export";

// Helper function to get default date range (1 month ago to today)
const getDefaultDateRange = () => {
  const today = new Date();
  const oneMonthAgo = new Date();
  oneMonthAgo.setMonth(today.getMonth() - 1);
  
  return {
    from: oneMonthAgo.toISOString().split("T")[0], // Format as YYYY-MM-DD
    to: today.toISOString().split("T")[0],
  };
};

const Dashboard = () => {
  const colors = tokens();
  const [facultySummary, setFacultySummary] = useState([]);

  // State to manage date filter and dashboard data
  const [dateRange, setDateRange] = useState(getDefaultDateRange());
  const [data, setData] = useState({
    intervention: [],
    commonQueries: [],
    userQueries: [],
    interventions: [],
    userExperience: [],
  });
  const [result, setResult] = useState(null);

  // Function to fetch data from the backend
  const fetchData = async (range) => {
    try {
      const result = await fetchDashboardData(range); // Use the API function
      setResult(result || {}); // Store raw results with fallback to empty object

      // Format common queries data for BarBox with null checks
      const commonQueriesData = (result?.top_topics || []).map((item) => ({
        query: item.topic || "Unknown",
        no_intervention:
          (item.frequency || 0) -
          ((result?.top_intervention_by_faculty || []).find((t) => t.topic === item.topic)?.intervention_count || 0),
        no_interventionColor: tokens().gray[500],
        intervention: (result?.top_intervention_by_faculty || []).find((t) => t.topic === item.topic)?.intervention_count || 0,
        interventionColor: tokens().indigo[500],
      }));

      // Format intervention queries data for BarBox with null checks
      const interventionsData = (result?.top_intervention_by_faculty || []).map((item) => ({
        dept: item.faculty || "Unknown",
        query: item.topic || "Unknown",
        intervention: item.intervention_count || 0,
        interventionColor: tokens().indigo[500],
      }));

      // Format intervention queries into faculty-level summary 
      const facultySummary = interventionsData.reduce((acc, item) => {
        const existing = acc.find((entry) => entry.dept === item.dept);
        if (existing) {
          existing.intervention += item.intervention;
        } else {
          acc.push({
            dept: item.dept,
            intervention: item.intervention,
            interventionColor: item.interventionColor,
          });
        }
        return acc;
      }, []);

      setFacultySummary(facultySummary);

      // Format user queries over time data for LineBox with null checks
      const rawUserQueriesData = (result?.user_queries_over_time || []).map(item => ({
        x: new Date(item.date || new Date()).toLocaleDateString(),
        y: item.total || 0,
      }));
    
      
      const userQueriesData = [
        {
          id: "queries",
          color: tokens().indigo[500],
          data: rawUserQueriesData,
        }
      ];

      // Format user experience over time data for LineBox with null checks
      const userExperienceData = [
        {
          id: "ratings",
          color: tokens().indigo[500],
          data: (result?.user_experience_over_time || []).map((item) => ({
            x: new Date(item.date || new Date()).toLocaleDateString(),
            y: item.avg_rating || 0,
          })),
        },
      ];

      setData({
        commonQueries: commonQueriesData,
        userQueries: userQueriesData,
        interventions: interventionsData,
        userExperience: userExperienceData,
      });
    } catch (err) {
      console.error("Error fetching data:", err);
      // Set empty data on error
      setData({
        commonQueries: [],
        userQueries: [{ id: "queries", color: tokens().indigo[500], data: [] }],
        interventions: [],
        userExperience: [{ id: "ratings", color: tokens().indigo[500], data: [] }],
      });
    }
  };

  // Fetch data on component mount with default date range
  useEffect(() => {
    fetchData(dateRange);
  }, [dateRange]);

  // Function to handle date range changes
  const handleDateChange = (range) => {
    if (range.from && range.to) {
      fetchData(range); // Fetch data for the selected date range
    }
  };

  // Function to handle export
  const handleExport = () => {
    if (result) {
      exportDashboardDataToExcel(result); // Pass the result data to the export function
    } else {
      alert("No data available to export.");
    }
  };

  return (
    <Box mt="30px" mx="30px">
      <Box display="flex" justifyContent="space-between">
        {/* HEADER */}
        <Header title="DASHBOARD" />

        <Box display="flex" gap={2} alignItems="center" mb="10px">
          {/* TOTAL USERS */}
          <TotalUsers figure={result?.total_users || 0} />

          {/* DATE FILTER */}
          <Box display="flex" gap="10px">
            <DateFilter
              dateRange={dateRange}
              setDateRange={setDateRange}
              onDateChange={handleDateChange}
            />
          </Box>
          
          {/* EXPORT BUTTON */}
          <ExportButton onClick={handleExport} />
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
              { title: "Conversations Created", figure: result?.total_conversations || 0 },
              { title: "New Users", figure: result?.new_users_since_start || 0 },
              { title: "Interventions", figure: result?.intervention_count || 0 },
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
            upFigure={result?.total_thumbs_up || 0}
            upMessages={result?.recent_thumbs_up_messages?.map((msg) => msg.text) || ["No Records"]}
            downFigure={result?.total_thumbs_down || 0}
            downMessages={result?.recent_thumbs_down_messages?.map((msg) => msg.text) || ["No Records"]}
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
              { title: "Avg Messages per Conversation", figure: result?.avg_messages_per_conversation || 0 },
              { title: "Average Rating per Conversation", figure: result?.avg_rating || 0 },
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
            figure={result?.total_feedbacks || 0}
            feedbacks={result?.recent_feedbacks?.map((fb) => fb.feedback) || ["No Records Found"]}
            dates={result?.recent_feedbacks?.map((fb) => new Date(fb.created_at).toLocaleDateString()) || ["-"]}
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
            title="Common Conversation Topics"
            data={data.commonQueries}
            keys={["intervention", "no_intervention"]}
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
            title="Interventions across Faculty"
            data={ facultySummary }
            pieTitle="Breakdown by Topic"
            keys={["intervention"]}
            index="dept"
            showLegend={false}
            hover={true}
            topicBreakdown={data.interventions || []}
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
          <LineBox title="Average Rating Over Time" data={data.userExperience} showLegend={false} />
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;