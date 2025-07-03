const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000/";

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const xhtrOptions: RequestInit = {
        ...options,
        credentials: "include",
    };
    const response = await fetch(url, xhtrOptions);
    console.log(response);
    let data;
    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        throw new Error(data?.message || "API request failed");
    }

    return data;
}