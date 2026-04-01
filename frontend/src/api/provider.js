import { get, patch } from "./client.js";

export const getProfile = () => get("/api/provider/profile");

export const updateProfile = (specialty, bio) =>
  patch("/api/provider/profile", { specialty, bio });
