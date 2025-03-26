import { tokens } from "../theme";
import { format, addDays } from "date-fns";

  export const mockCommonQueriesData = [
    {
      query: "A",
      resolved: 6,
      resolvedColor: tokens().gray[500],
      unresolved: 2,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "B",
      resolved: 3,
      resolvedColor: tokens().gray[500],
      unresolved: 10,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "C",
      resolved: 5,
      resolvedColor: tokens().gray[500],
      unresolved: 7,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "D",
      resolved: 3,
      resolvedColor: tokens().gray[500],
      unresolved: 7,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "E",
      resolved: 2,
      resolvedColor: tokens().gray[500],
      unresolved: 4,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "F",
      resolved: 8,
      resolvedColor: tokens().gray[500],
      unresolved: 4,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "G",
      resolved: 1,
      resolvedColor: tokens().gray[500],
      unresolved: 10,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "H",
      resolved: 3,
      resolvedColor: tokens().gray[500],
      unresolved: 2,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "I",
      resolved: 9,
      resolvedColor: tokens().gray[500],
      unresolved: 7,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "J",
      resolved: 6,
      resolvedColor: tokens().gray[500],
      unresolved: 10,
      unresolvedColor: tokens().indigo[500],
    },
  ];

  export const mockUnresolvedQueriesData = [
    {
      query: "A",
      unresolved: 2,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "B",
      unresolved: 10,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "C",
      unresolved: 7,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "D",
      unresolved: 7,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "E",
      unresolved: 4,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "F",
      unresolved: 4,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "G",
      unresolved: 10,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "H",
      unresolved: 2,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "I",
      unresolved: 7,
      unresolvedColor: tokens().indigo[500],
    },
    {
      query: "J",
      unresolved: 10,
      unresolvedColor: tokens().indigo[500],
    },
  ];

  export const mockInterventionData = [
    {
      id: "human",
      label: "human",
      value: 17,
      color: tokens().gray[500],
    },
    {
      id: "no intervention",
      label: "no intervention",
      value: 83,
      color: tokens().indigo[500],
    },
  ];
  
  export const mockUserQueriesData = [
    {
      id: "userqueries",
      color: tokens().indigo[500],
      data: Array.from({ length: 7 }, (_, i) => ({
        x: format(addDays(new Date(2025, 0, 1), i), "dd/MM/yyyy"), 
        y: Math.floor(Math.random() * 300), 
      })),
    },
  ];

  export const mockUserExperienceData = [
    {
      id: "thumbs up",
      color: tokens().indigo[500],
      data: Array.from({ length: 7 }, (_, i) => ({
        x: format(addDays(new Date(2025, 0, 1), i), "dd/MM/yyyy"), 
        y: Math.floor(Math.random() * 300), 
      })),
    },
    {
      id: "thumbs down",
      color: tokens().gray[500],
      data: Array.from({ length: 7 }, (_, i) => ({
        x: format(addDays(new Date(2025, 0, 1), i), "dd/MM/yyyy"), 
        y: Math.floor(Math.random() * 300), 
      })),
    },
  ];

  export const mockUploadedFiles = [
    {
      id:1, 
      file_name: "[ODPRT] Chatbot Project #472.pdf",
      file_size:"197KB",
      upload_date: "19/05/2021 10:10:00",
    },
    {
      id: 2,
      file_name: "BT4103_CourseIntroduction_AY2425Sem2.pdf",
      file_size:"336KB",
      upload_date: "18/05/2021 15:12:00",
    },
    {
      id: 3,
      file_name: "Business Analytics Capstone Project introduction.pdf",
      file_size:"188KB",
      upload_date: "17/05/2021 14:15:00",
    },
    {
      id: 4,
      file_name: "NUS_logo.png",
      file_size:"29KB",
      upload_date: "23/04/2021 13:15:00",
    },
    {
      id: 5,
      file_name: "ODPRT_Website.png",
      file_size:"4.3MB",
      upload_date: "20/04/2021 08:01:00",
    },
  ];
  
  