const BASE = "/api/auth";

async function request(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const data = await res.json();

  if (!res.ok) {
    // DRF wraps field errors and non-field errors differently.
    // Pull the first human-readable message we find.
    const message =
      data?.non_field_errors?.[0] ||
      Object.values(data)?.[0]?.[0] ||
      "Something went wrong.";
    throw new Error(message);
  }

  return data;
}

export function memberLogin(email, password) {
  return request(`${BASE}/member/login/`, { email, password });
}

export function memberSignup(email, password, first_name, last_name) {
  return request(`${BASE}/member/register/`, { email, password, first_name, last_name });
}

export function providerLogin(email, password) {
  return request(`${BASE}/provider/login/`, { email, password });
}

export function providerSignup(email, password, first_name, last_name) {
  return request(`${BASE}/provider/register/`, {
    email,
    password,
    first_name,
    last_name,
  });
}
