import { getTasks } from "@/services/tasksService";
import { getEmployees } from "@/services/userService";
import { useEffect, useState } from "react";

const tabClasses = (active: boolean) =>
  `px-4 py-2 rounded-t-lg font-semibold transition ${
    active
      ? "bg-blue-600 text-white shadow"
      : "bg-white/30 text-blue-700 hover:bg-blue-100"
  }`;

const AdminDashboard = () => {
  const [tab, setTab] = useState<"employees" | "tasks">("employees");
  const [employees, setEmployees] = useState<any[]>([]);
  const [tasks, setTasks] = useState<any[]>([]);
  useEffect(() => {
    async function fetchEmployees() {
      onClickEmployeesTab();
    }
    if (employees.length === 0) {
      fetchEmployees();
    }
  }, []);

  const onClickEmployeesTab = async () => {
    setTab("employees");
    try {
      // Make sure getEmployees is imported from your API/service file
      const response = await getEmployees();
      setEmployees(response.employee);
    } catch (err) {
      setEmployees([]);
    }
  };

  const onClickTasksTab = async () => {
    setTab("tasks");
    try {
      // Make sure getEmployees is imported from your API/service file
      const response = await getTasks();
      setTasks(response.tasks);
    } catch (err) {
      setTasks([]);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto mt-10 bg-white/80 rounded-2xl shadow-2xl p-8">
      <h1 className="text-3xl font-extrabold text-blue-800 mb-8 text-center drop-shadow">
        Admin Dashboard
      </h1>
      <div className="flex border-b border-blue-200 mb-6">
        <button
          className={tabClasses(tab === "employees")}
          onClick={() => onClickEmployeesTab()}
        >
          Employees
        </button>
        <button
          className={tabClasses(tab === "tasks")}
          onClick={() => onClickTasksTab()}
        >
          Tasks
        </button>
      </div>
      <div>
        {tab === "employees" && (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white rounded-lg shadow">
              <thead>
                <tr>
                  <th className="py-2 px-4 text-left text-blue-700 font-bold">
                    Name
                  </th>
                  <th className="py-2 px-4 text-left text-blue-700 font-bold">
                    Email
                  </th>
                </tr>
              </thead>
              <tbody>
                {employees.map((emp) => (
                  <tr key={emp.employee_id} className="hover:bg-blue-50">
                    <td className="py-2 px-4">{emp.full_name}</td>
                    <td className="py-2 px-4">{emp.email}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {tab === "tasks" && (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white rounded-lg shadow">
              <thead>
                <tr>
                  <th className="py-2 px-4 text-left text-blue-700 font-bold">
                    Title
                  </th>
                  <th className="py-2 px-4 text-left text-blue-700 font-bold">
                    Assigned To
                  </th>
                  <th className="py-2 px-4 text-left text-blue-700 font-bold">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task) => (
                  <tr key={task.id} className="hover:bg-blue-50">
                    <td className="py-2 px-4">{task.title}</td>
                    <td className="py-2 px-4">{task.assigned_to_name}</td>
                    <td className="py-2 px-4">
                      <span
                        className={`px-2 py-1 rounded text-xs font-semibold ${
                          task.status === "Completed"
                            ? "bg-green-100 text-green-700"
                            : "bg-yellow-100 text-yellow-700"
                        }`}
                      >
                        {task.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
