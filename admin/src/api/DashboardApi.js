// Sample fetching from gpt, take it with a pinch of salt lol 
const express = require("express");
const cors = require("cors");
const app = express();
const db = require("./db");
const { tokens } = require("../theme"); 

app.use(cors());
app.use(express.json());


// Sample fetching for intervention data 
app.get("/api/intervention", async (req, res) => {
  const colors = tokens(); 

  const { from, to } = req.query;

  try {
    const result = await db.query(
      `SELECT intervention_type AS id, COUNT(*) AS value 
       FROM your_table 
       WHERE date_column BETWEEN $1 AND $2 
       GROUP BY intervention_type`,
      [from, to]
    );

    const formatted = result.rows.map((row) => ({
      id: row.id,
      label: row.id,
      value: parseInt(row.value, 10),
      color: row.id === "human" ? colors.gray[500] : colors.indigo[500],
    }));

    res.json(formatted); 
  } catch (err) {
    console.error("Error fetching intervention data", err);
    res.status(500).json({ error: "Database error" });
  }
});
  