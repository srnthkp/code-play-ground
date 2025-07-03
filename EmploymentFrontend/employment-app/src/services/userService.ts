import { apiFetch } from "@/utils/api";

export async function loginUser(postData: any) {
    return apiFetch("auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(postData),
    });
}

export async function registerUser(postData: any) {
    await apiFetch("auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(postData),
    });
}

export async function getUserRole() {
    return apiFetch("auth/get_user_role", {
        method: "GET",
    });
}

export async function getEmployees() {
    return apiFetch("auth/get_employees", {
        method: "GET",
    });
}