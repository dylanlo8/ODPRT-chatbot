import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

export const exportDashboardDataToExcel = (data) => {
  try {
    if (!data || Object.keys(data).length === 0) {
      alert("No data to export.");
      return;
    }

    // Prepare data for each sheet
    const summarySheet = [
      {
        "Total Conversations": data.total_conversations || "N/A",
        "Avg Messages per Conversation": data.avg_messages_per_conversation || "N/A",
        "Total Users": data.total_users || "N/A",
        "Intervention Count": data.intervention_count || "N/A",
        "Avg Rating": data.avg_rating || "N/A",
        "New Users Since Start": data.new_users_since_start || "N/A",
      },
    ];

    const topTopicsSheet = data.top_topics?.map((topic) => ({
      Topic: topic.topic || "Unknown",
      Frequency: topic.frequency || 0,
    })) || [];

    const userQueriesOverTimeSheet = data.user_queries_over_time?.map((query) => ({
      Date: new Date(query.date).toLocaleDateString(),
      "Total Queries": query.total || 0,
    })) || [];

    const topInterventionByFacultySheet = data.top_intervention_by_faculty?.map((entry) => ({
      Faculty: entry.faculty || "Unknown",
      Topic: entry.topic || "Unknown",
      "Intervention Count": entry.intervention_count || 0,
    })) || [];

    const userExperienceOverTimeSheet = data.user_experience_over_time?.map((entry) => ({
      Date: new Date(entry.date).toLocaleDateString(),
      "Average Rating": entry.avg_rating || "N/A",
    })) || [];

    const recentFeedbacksSheet = data.recent_feedbacks?.map((feedback) => ({
      "Conversation ID": feedback.conversation_id || "N/A",
      "User ID": feedback.user_id || "N/A",
      Feedback: feedback.feedback || "N/A",
      "Created At": new Date(feedback.created_at).toLocaleString(),
    })) || [];

    const recentThumbsUpMessagesSheet = data.recent_thumbs_up_messages?.map((message) => ({
      "Message ID": message.message_id || "N/A",
      "Conversation ID": message.conversation_id || "N/A",
      Sender: message.sender || "N/A",
      Text: message.text || "N/A",
      "Created At": new Date(message.created_at).toLocaleString(),
    })) || [];

    const recentThumbsDownMessagesSheet = data.recent_thumbs_down_messages?.map((message) => ({
      "Message ID": message.message_id || "N/A",
      "Conversation ID": message.conversation_id || "N/A",
      Sender: message.sender || "N/A",
      Text: message.text || "N/A",
      "Created At": new Date(message.created_at).toLocaleString(),
    })) || [];

    // Create a new workbook
    const workbook = XLSX.utils.book_new();

    // Add sheets to the workbook
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(summarySheet), "Summary");
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(topTopicsSheet), "Top Topics");
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(userQueriesOverTimeSheet), "User Queries Over Time");
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(topInterventionByFacultySheet), "Top Interventions");
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(userExperienceOverTimeSheet), "User Experience");
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(recentFeedbacksSheet), "Recent Feedbacks");
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(recentThumbsUpMessagesSheet), "Thumbs Up Messages");
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(recentThumbsDownMessagesSheet), "Thumbs Down Messages");

    // Write the workbook to binary Excel format
    const excelBuffer = XLSX.write(workbook, {
      bookType: "xlsx",
      type: "array",
    });

    // Trigger the download
    const blob = new Blob([excelBuffer], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    saveAs(blob, `dashboard_export_${new Date().toISOString()}.xlsx`);
  } catch (err) {
    console.error("Export failed:", err.message);
    alert("Something went wrong while exporting Excel.");
  }
};