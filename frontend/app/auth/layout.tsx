export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-900 dark:to-gray-800 p-4">
      <div className="w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-primary-600 dark:text-primary-400">
            SmartAsset
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Your AI Financial Advisor
          </p>
        </div>
        {children}
      </div>
    </div>
  );
}
