import { Box } from "@mui/material";
import { tokens } from "../theme";
import { mockUserQueriesData, mockUserExperienceData, mockUsersData, mockInterventionData, mockCommonQueriesData, mockUnresolvedQueriesData } from "../data/mockData";
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import Header from "../components/Header";
import BarBox from "../components/bar/BarBox";
import LineBox from "../components/line/LineBox"
import PieBox from "../components/pie/PieBox";
import StatBox from "../components/StatBox";

const Dashboard = () => {
  const colors = tokens();

  return (
    <Box mt="40px" mx="50px" pb="40px">
      {/* HEADER */}
      <Header title="DASHBOARD"/>

      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="150px"
        gap="25px"
      >
        {/* ROW 1 */}
        {/* CONVERSATIONS */}
        <Box
          gridColumn="span 3"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <StatBox
            title="Conversations"
            figure="XX"
            percentage="x.x%"
            isIncreasing={true}
            arrow={
              <ArrowUpwardIcon
                sx={{ color: colors.green[500], fontSize: "20px" }}
              />
            }
          />
        </Box>

        {/* ACTIVE CONVERSATIONS */}
        <Box
          gridColumn="span 3"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <StatBox
            title="Active Conversations"
            figure="XX"
            percentage="x.x%"
            isIncreasing={false}
            arrow={
              <ArrowDownwardIcon
                sx={{ color: colors.red[500], fontSize: "20px" }}
              />
            }
          />
        </Box>

        {/* USERS */}
        <Box
          gridColumn="span 3"
          gridRow="span 2"
          backgroundColor={colors.white}
          display="flex"
          flexDirection="column"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <PieBox
            title="Users"
            figure="XX"
            data={mockUsersData}
          />
        </Box>
        
        {/* INTERVENTION */}
        <Box
          gridColumn="span 3"
          gridRow="span 2"
          backgroundColor={colors.white}
          display="flex"
          flexDirection="column"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <PieBox
            title="Intervention"
            figure="XX"
            data={mockInterventionData}
          />
        </Box>

        {/* ROW 2 */}
        {/* TURNAROUND TIME */}
        <Box
          gridColumn="span 3"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <StatBox
            title="Turnaround Time"
            figure="XX"
            percentage="x.x%"
            isIncreasing={false}
            arrow={
              <ArrowDownwardIcon
                sx={{ color: colors.red[500], fontSize: "20px" }}
              />
            }
          />
        </Box>
        
        {/* RESOLVED CONVERSATIONS */}
          <Box
          gridColumn="span 3"
          backgroundColor={colors.white}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="12px"
          border={`2px solid ${colors.gray[200]}`}
        >
          <StatBox
            title="Resolved Conversations"
            figure="XX"
            percentage="x.x%"
            isIncreasing={true}
            arrow={
              <ArrowUpwardIcon
                sx={{ color: colors.green[500], fontSize: "20px" }}
              />
            }
          />
        </Box>
        
        {/* ROW 3 */}
        {/* TOP 10 MOST COMMON QUERIES */}
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
            title="Top 10 Most Common Queries"
            data={mockCommonQueriesData}
            keys= {["unresolved", "resolved"]}
            index="query"
            showLegend={true}
          />
        </Box>

        {/* TOP 10 USER QUERIES OVER TIME */}
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
          <LineBox
            title="User Queries Over Time"
            data={mockUserQueriesData}
          />
        </Box>       

        {/* ROW 4 */}
        {/* TOP 10 MOST COMMON UNRESOLVED QUERIES */}
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
            title="Top 10 Most Common Unresolved Queries"
            data={mockUnresolvedQueriesData}
            keys= {["unresolved"]}
            index="query"
            showLegend={false}
          />
        </Box>

        {/* TOP 10 USER EXPERIENCE OVER TIME */}
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
          <LineBox
            title="User Experience Over Time"
            data={mockUserExperienceData}
          />
        </Box>           
      </Box>
    </Box>
  );
};

export default Dashboard;