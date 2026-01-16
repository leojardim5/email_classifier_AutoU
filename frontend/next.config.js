/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    // Em dev: usa localhost; em prod: use a env NEXT_PUBLIC_API_URL no Render
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

    return [
      {
        source: "/api/:path*",
        destination: `${apiUrl}/api/:path*`, // IMPORTANTE: mantém /api
      },
    ];
  },
};

module.exports = nextConfig;
