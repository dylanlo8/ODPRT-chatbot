// import * as XLSX from "xlsx";
// import { saveAs } from "file-saver";
// import { supabase } from "../supabaseClient"; // update path as needed

// export const exportDashboardDataToExcel = async () => {
//   try {
//     const { data, error } = await supabase
//       .from("dashboard_data") // to replace with actual table 
//       .select("*");

//     if (error) throw error;

//     if (!data || data.length === 0) {
//       alert("No data to export.");
//       return;
//     }

//     // Convert JSON to worksheet
//     const worksheet = XLSX.utils.json_to_sheet(data);

//     // Create a new workbook and append the worksheet
//     const workbook = XLSX.utils.book_new();
//     XLSX.utils.book_append_sheet(workbook, worksheet, "Dashboard Data");

//     // Write the workbook to binary Excel format
//     const excelBuffer = XLSX.write(workbook, {
//       bookType: "xlsx",
//       type: "array",
//     });

//     // Trigger the download
//     const blob = new Blob([excelBuffer], {
//       type:
//         "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
//     });
//     saveAs(blob, `dashboard_export_${new Date().toISOString()}.xlsx`);
//   } catch (err) {
//     console.error("Export failed:", err.message);
//     alert("Something went wrong while exporting Excel.");
//   }
// };