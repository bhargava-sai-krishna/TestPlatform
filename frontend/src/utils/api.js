export async function apiRequest(endpoint, method = "GET", body = null, token = null) {
  const API_BASE = "http://127.0.0.1:8001";
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  return res.json();
}
