export default function ProductView() {
  const product = {
    name: "AI Study Assistant",
    description: "Personalized learning platform for students",
    features: ["Personalized study plans", "Question generation", "Progress tracking"],
    pricing: 199,
    quality_score: 70,
    target_segments: ["Students", "Tech Workers"],
  };

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-6">Product View</h1>

      <div className="border rounded-lg p-6 max-w-2xl">
        <h2 className="text-xl font-semibold">{product.name}</h2>
        <p className="text-gray-500 mb-4">{product.description}</p>

        <div className="mb-4">
          <p className="text-sm text-gray-500 mb-1">Features</p>
          <ul className="list-disc list-inside">
            {product.features.map((f) => (
              <li key={f}>{f}</li>
            ))}
          </ul>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <p className="text-sm text-gray-500">Price</p>
            <p className="font-semibold">₹{product.pricing}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Quality Score</p>
            <p className="font-semibold">{product.quality_score}/100</p>
          </div>
        </div>

        <div>
          <p className="text-sm text-gray-500 mb-1">Target Segments</p>
          <div className="flex gap-2">
            {product.target_segments.map((seg) => (
              <span key={seg} className="px-3 py-1 bg-gray-100 rounded-full text-sm">
                {seg}
              </span>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}