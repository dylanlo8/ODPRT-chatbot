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
  
  export const mockUsersData = [
    {
      id: "new",
      label: "new",
      value: 38,
      color: tokens().gray[500],
    },
    {
      id: "returning",
      label: "returning",
      value: 62,
      color: tokens().indigo[500],
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
      id: "userexperience",
      color: tokens().indigo[500],
      data: Array.from({ length: 7 }, (_, i) => ({
        x: format(addDays(new Date(2025, 0, 1), i), "dd/MM/yyyy"), 
        y: Math.floor(Math.random() * 300), 
      })),
    },
  ];

  export const mockDataContacts = [
    {
      id: 1,
      name: "Jon Snow",
      email: "jonsnow@gmail.com",
      age: 35,
      phone: "(665)121-5454",
      address: "0912 Won Street, Alabama, SY 10001",
      city: "New York",
      zipCode: "10001",
      registrarId: 123512,
    },
    {
      id: 2,
      name: "Cersei Lannister",
      email: "cerseilannister@gmail.com",
      age: 42,
      phone: "(421)314-2288",
      address: "1234 Main Street, New York, NY 10001",
      city: "New York",
      zipCode: "13151",
      registrarId: 123512,
    },
    {
      id: 3,
      name: "Jaime Lannister",
      email: "jaimelannister@gmail.com",
      age: 45,
      phone: "(422)982-6739",
      address: "3333 Want Blvd, Estanza, NAY 42125",
      city: "New York",
      zipCode: "87281",
      registrarId: 4132513,
    },
    {
      id: 4,
      name: "Anya Stark",
      email: "anyastark@gmail.com",
      age: 16,
      phone: "(921)425-6742",
      address: "1514 Main Street, New York, NY 22298",
      city: "New York",
      zipCode: "15551",
      registrarId: 123512,
    },
    {
      id: 5,
      name: "Daenerys Targaryen",
      email: "daenerystargaryen@gmail.com",
      age: 31,
      phone: "(421)445-1189",
      address: "11122 Welping Ave, Tenting, CD 21321",
      city: "Tenting",
      zipCode: "14215",
      registrarId: 123512,
    },
    {
      id: 6,
      name: "Ever Melisandre",
      email: "evermelisandre@gmail.com",
      age: 150,
      phone: "(232)545-6483",
      address: "1234 Canvile Street, Esvazark, NY 10001",
      city: "Esvazark",
      zipCode: "10001",
      registrarId: 123512,
    },
    {
      id: 7,
      name: "Ferrara Clifford",
      email: "ferraraclifford@gmail.com",
      age: 44,
      phone: "(543)124-0123",
      address: "22215 Super Street, Everting, ZO 515234",
      city: "Evertin",
      zipCode: "51523",
      registrarId: 123512,
    },
    {
      id: 8,
      name: "Rossini Frances",
      email: "rossinifrances@gmail.com",
      age: 36,
      phone: "(222)444-5555",
      address: "4123 Ever Blvd, Wentington, AD 142213",
      city: "Esteras",
      zipCode: "44215",
      registrarId: 512315,
    },
    {
      id: 9,
      name: "Harvey Roxie",
      email: "harveyroxie@gmail.com",
      age: 65,
      phone: "(444)555-6239",
      address: "51234 Avery Street, Cantory, ND 212412",
      city: "Colunza",
      zipCode: "111234",
      registrarId: 928397,
    },
    {
      id: 10,
      name: "Enteri Redack",
      email: "enteriredack@gmail.com",
      age: 42,
      phone: "(222)444-5555",
      address: "4123 Easer Blvd, Wentington, AD 142213",
      city: "Esteras",
      zipCode: "44215",
      registrarId: 533215,
    },
    {
      id: 11,
      name: "Steve Goodman",
      email: "stevegoodmane@gmail.com",
      age: 11,
      phone: "(444)555-6239",
      address: "51234 Fiveton Street, CunFory, ND 212412",
      city: "Colunza",
      zipCode: "1234",
      registrarId: 92197,
    },
  ];
  
  