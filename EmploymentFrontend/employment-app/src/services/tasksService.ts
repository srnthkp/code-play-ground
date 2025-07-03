import { apiFetch } from "@/utils/api";

export async function getTasks() {
    return apiFetch("tasks/read_tasks", {
        method: "GET",
    });
}