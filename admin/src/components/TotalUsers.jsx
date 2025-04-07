import React from 'react';
import { Typography, Box } from '@mui/material';

const TotalUsers = ({ figure }) => {

  return (
    <Box>
      <Typography variant="h5" fontWeight="bold">
        Total Users: {figure}
      </Typography>
    </Box>
  );
};

export default TotalUsers;