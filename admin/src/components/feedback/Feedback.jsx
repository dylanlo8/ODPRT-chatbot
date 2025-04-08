import { Box, Typography } from '@mui/material';
import { tokens } from "../../theme";

const Feedback = ({ feedbacks, dates }) => {
  const colors = tokens();

  return (
    <Box>
      <Box>
        {feedbacks.map((fdbk, index) => (
          <Typography
            key={index}
            variant="body2"
            sx={{
              color: colors.text,
              fontSize: "12px",
              lineHeight: 1,
              display: "flex",
              alignItems: "center",
              gap: "4px",
              maxWidth: "550px",
            }}
          >
            {index + 1}.{" "}
            <span style={{ flexShrink: 0 }}>&ldquo;</span>
            <span
              title={fdbk}
              style={{
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
                flexShrink: 1,
              }}
            >
              {fdbk}
            </span>
            <span style={{ flexShrink: 0 }}>&rdquo;</span>
            {dates?.[index] && (
              <span
                style={{
                  flexShrink: 0,
                  whiteSpace: "nowrap",
                  marginLeft: "4px",
                }}
              >
                - {dates[index]}
              </span>
            )}
          </Typography>
        ))}
      </Box>
    </Box>
  );
};

export default Feedback;
