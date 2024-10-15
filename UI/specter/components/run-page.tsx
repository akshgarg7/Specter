export default function Component() {
  const runs = ["Run 1", "Run 2", "Run 3", "Run 4"]

  return (
    <div className="min-h-screen bg-white p-8">
      <h1 className="text-4xl font-serif mb-8">Specter</h1>
      <div className="max-w-md mx-auto bg-gray-50 rounded-lg shadow-sm">
        <ul className="divide-y divide-gray-200">
          {runs.map((run, index) => (
            <li key={index} className="p-4">
              <span className="text-lg text-gray-900">{run}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
