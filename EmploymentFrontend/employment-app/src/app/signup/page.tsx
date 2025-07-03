"use client";
import { useState } from "react";
import FormInput from "@/components/forminput";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/utils/api";
import { registerUser } from "@/services/userService";

export default function SignupPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    employee_name: "",
    phone_number: "",
    date_of_birth: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  // Handle input changes
  // This function updates the form state when the user types in the input fields
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Update form state on input change
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    // Prevent default form submission
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      await registerUser(form);
      setSuccess(true);
      setTimeout(() => router.push("/login"), 1500);
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
          Create an Account
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-5">
            <FormInput
              label="Username"
              name="username"
              type="text"
              placeholder="Username"
              required
              value={form.username}
              onChange={handleChange}
            />
          </div>
          <div className="mb-5">
            <FormInput
              label="Email"
              name="email"
              type="email"
              placeholder="Email"
              required
              value={form.email}
              onChange={handleChange}
            />
          </div>
          <div className="mb-5">
            <FormInput
              label="Password"
              name="password"
              type="password"
              placeholder="********"
              required
              value={form.password}
              onChange={handleChange}
            />
          </div>
          <div className="mb-5">
            <FormInput
              label="Name"
              name="employee_name"
              type="text"
              placeholder="Name"
              required
              value={form.employee_name}
              onChange={handleChange}
            />
          </div>
          <div className="mb-5">
            <FormInput
              label="Date of birth"
              name="date_of_birth"
              type="date"
              placeholder="Date of Birth"
              required
              value={form.date_of_birth}
              onChange={handleChange}
            />
          </div>
          <div className="mb-5">
            <FormInput
              label="Phone Number"
              name="phone_number"
              type="phone"
              placeholder="Phone Number"
              required
              value={form.phone_number}
              onChange={handleChange}
            />
          </div>
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-violet-600 via-blue-600 to-indigo-600 text-white font-semibold py-2.5 rounded-lg shadow-lg hover:from-violet-700 hover:to-indigo-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-violet-400"
            disabled={loading}
          >
            {loading ? "Signing up..." : "Sign Up"}
          </button>
          {error && (
            <div className="mt-4 text-red-200 text-center font-medium">
              {error}
            </div>
          )}
          {success && (
            <div className="mt-4 text-green-200 text-center font-medium">
              Signup successful! Redirecting to login...
            </div>
          )}
        </form>
        <div className="mt-6 text-center">
          <span className="text-white/80">Already have an account? </span>
          <a
            href="/login"
            className="text-blue-200 hover:underline font-semibold"
          >
            Login
          </a>
        </div>
      </div>
    </div>
  );
}
