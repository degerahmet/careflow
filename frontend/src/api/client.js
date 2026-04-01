async function apiRequest(method, url, body = null) {
  const token = localStorage.getItem("access_token");

  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  };

  const res = await fetch(url, options);

  if (res.status === 204) return null;

  const data = await res.json();

  if (!res.ok) {
    const message =
      data?.non_field_errors?.[0] ||
      Object.values(data)?.[0]?.[0] ||
      "Something went wrong.";
    throw new Error(message);
  }

  return data;
}

export const get   = (url)        => apiRequest("GET", url);
export const post  = (url, body)  => apiRequest("POST", url, body);
export const patch = (url, body)  => apiRequest("PATCH", url, body);
export const del   = (url)        => apiRequest("DELETE", url);
