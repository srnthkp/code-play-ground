import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-cover bg-center bg-[url('/images/bg.png')] flex items-center justify-center">
      <main className="flex flex-col gap-8 items-center bg-white/30 border border-white/30 backdrop-blur-lg rounded-2xl shadow-2xl px-10 py-12 max-w-md w-full">
        <h1 className="text-4xl font-extrabold text-blue-800 mb-2 drop-shadow">
          Employment App
        </h1>
        <p className="text-gray-800 text-center mb-6 font-medium drop-shadow">
          Welcome! Please login or sign up to continue.
        </p>
        <div className="flex gap-4 w-full">
          <Link
            href="/login"
            className="flex-1 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 font-semibold shadow-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 text-center"
          >
            Login
          </Link>
          <Link
            href="/signup"
            className="flex-1 rounded-lg bg-gradient-to-r from-violet-600 to-blue-500 text-white px-6 py-3 font-semibold shadow-lg hover:from-violet-700 hover:to-blue-600 transition-all duration-200 text-center"
          >
            Signup
          </Link>
        </div>
      </main>
      <footer className="absolute bottom-6 text-gray-200 text-xs drop-shadow">
        &copy; {new Date().getFullYear()} Employment App. All rights reserved.
      </footer>
    </div>
  );
}
