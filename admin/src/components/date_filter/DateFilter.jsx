// DateFilter.js
import React from "react";
import { Box, TextField } from "@mui/material";

const DateFilter = ({ dateRange, setDateRange }) => {
  return (
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
  );
};

export default DateFilter;
