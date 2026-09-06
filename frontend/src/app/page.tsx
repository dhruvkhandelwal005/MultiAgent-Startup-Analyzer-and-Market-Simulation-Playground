import Link from "next/link";

export default function Dashboard() {
  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-6">Market Sim Platform</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="border rounded-lg p-4">
          <p className="text-sm text-gray-500">Active Users</p>
          <p className="text-2xl font-semibold">--</p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-sm text-gray-500">Revenue</p>
          <p className="text-2xl font-semibold">--</p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-sm text-gray-500">Cash Remaining</p>
          <p className="text-2xl font-semibold">--</p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-sm text-gray-500">Market Share</p>
          <p className="text-2xl font-semibold">--</p>
        </div>
      </div>

      <nav className="flex gap-4">
        <Link href="/team-builder" className="px-4 py-2 bg-black text-white rounded-lg">
          Team Builder
        </Link>
        <Link href="/product" className="px-4 py-2 bg-black text-white rounded-lg">
          Product View
        </Link>
        <Link href="/market" className="px-4 py-2 bg-black text-white rounded-lg">
          Market Playground
        </Link>
      </nav>
    </main>
  );
}