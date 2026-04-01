import { get, post, del } from "./client.js";

export const getAvailability = () => get("/api/availability/");

export const createSlot = (date, start_time, end_time) =>
  post("/api/availability/", { date, start_time, end_time });

export const deleteSlot = (id) => del(`/api/availability/${id}/`);
