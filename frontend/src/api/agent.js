import { get, post } from "./client.js";

const SESSION_KEY = "chat_session_id";

export function getSessionId() {
  return localStorage.getItem(SESSION_KEY) || null;
}

export function setSessionId(id) {
  localStorage.setItem(SESSION_KEY, id);
}

export function clearSessionId() {
  localStorage.removeItem(SESSION_KEY);
}

export function getSession(sessionId) {
  return get(`/api/agent/session/?session_id=${sessionId}`);
}

export function sendChatMessage(sessionId, message) {
  const body = { message };
  if (sessionId) body.session_id = sessionId;
  return post("/api/agent/chat/", body);
}
