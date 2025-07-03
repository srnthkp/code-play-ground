"use client";
import FormInput from "@/components/forminput";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { getUserRole, loginUser } from "@/services/userService";

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    username: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await loginUser(form);
      setTimeout(() => router.push("/dashboard"), 1500);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-cover bg-center bg-[url('/images/bg.png')] flex items-center justify-center">
      <div className="bg-white/20 border border-white/30 backdrop-blur-lg p-10 rounded-2xl w-full max-w-md shadow-2xl">
        <h2 className="text-3xl font-extrabold text-center mb-8 text-white drop-shadow">
          Welcome Back
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-5">
            <FormInput
              label="Username"
              name="username"
              type="text"
              placeholder="Username"
              required
              onChange={handleChange}
              value={form.username}
            />
          </div>
          <div className="mb-5">
            <FormInput
              label="Password"
              name="password"
              type="password"
              placeholder="********"
              required
              onChange={handleChange}
              value={form.password}
            />
          </div>
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600 text-white font-semibold py-2.5 rounded-lg shadow-lg hover:from-blue-700 hover:to-violet-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
          {error && (
            <div className="mt-4 text-red-200 text-center font-medium">
              {error}
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
