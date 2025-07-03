"use client";
import { useEffect, useState } from "react";
import { getUserRole } from "@/services/userService";
import AdminDashboard from "@/components/AdminsDashboard";
import EmployeeDashboard from "@/components/EmployeeDashboard";
import EmployerDashboard from "@/components/EmployerDashboard";

export default function DashboardPage() {
  const [role, setRole] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchRole() {
      try {
        const response = await getUserRole();
        setRole(response.role);
      } catch (err) {
        setRole(null);
      } finally {
        setLoading(false);
      }
    }
    fetchRole();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (role === "Admin") return <AdminDashboard />;
  if (role === "Employee") return <EmployeeDashboard />;
  if (role === "Employer") return <EmployerDashboard />;
  return <div>Unauthorized</div>;
}
