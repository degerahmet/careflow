import { get, patch } from "./client.js";

export const getProviderAppointments = () => get("/api/appointments/provider/");
export const getMemberAppointments = () => get("/api/appointments/member/");

export const updateAppointmentStatus = (id, status) =>
  patch(`/api/appointments/${id}/status/`, { status });
