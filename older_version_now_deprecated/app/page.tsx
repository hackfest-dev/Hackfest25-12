import Image from "next/image";
import { hero, cta, features } from "./landing-data";
import { FeatureCard, PlaceholderChart, EthicsSection, BlackMirrorSection } from "./components";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-100 via-white to-blue-100 flex flex-col font-sans">
      {/* Header */}
      <header className="flex justify-between items-center p-6 max-w-7xl mx-auto w-full">
        <div className="flex items-center gap-3">
          <span className="bg-pink-200 rounded-full p-2"><Image src="/favicon.ico" alt="Logo" width={32} height={32} /></span>
          <span className="font-bold text-xl text-pink-600">Digital Twin</span>
        </div>
        <nav className="hidden md:flex gap-8 text-gray-700 font-medium">
          <a href="#features" className="hover:text-pink-600">Features</a>
          <a href="#ethics" className="hover:text-pink-600">Ethics</a>
        </nav>
        <div className="flex items-center gap-4">
          <span className="rounded-full border-2 border-pink-300 overflow-hidden w-10 h-10 flex items-center justify-center bg-white">
  <Image src="/profile.png" alt="Profile" width={40} height={40} className="object-cover w-10 h-10" />
</span>
        </div>
      </header>

      {/* Hero Section */}
      <section className="flex flex-col md:flex-row items-center justify-between gap-8 max-w-7xl mx-auto w-full py-12 px-4 md:px-8">
        <div className="flex-1 flex flex-col items-start gap-4">
          <h1 className="text-5xl font-extrabold text-gray-900 leading-tight mb-2">
            {hero.title}
          </h1>
          <h2 className="text-2xl font-semibold text-pink-500 mb-2">{hero.subtitle}</h2>
          <p className="text-gray-700 text-lg mb-4 max-w-xl">{hero.description}</p>
          <a href={cta.url} className="bg-pink-500 hover:bg-pink-600 text-white rounded-full px-7 py-3 font-bold text-lg shadow-lg transition">
            {cta.label}
          </a>
        </div>
        <div className="flex-1 flex flex-col gap-4 items-center">
          <Image src="/hero.png" alt="Hero" width={320} height={320} className="rounded-3xl shadow-xl border-4 border-pink-100" />
          <div className="flex gap-4 mt-4">
            <PlaceholderChart label="Mood Risk" />
            <PlaceholderChart label="Lifestyle Score" />
            <PlaceholderChart label="Genetic Risk" />
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="w-full bg-white/60 py-12 px-4 flex flex-col items-center">
        <h2 className="text-3xl font-bold text-pink-600 mb-8">How Digital Twin Works</h2>
        <div className="flex flex-wrap justify-center gap-6">
          {features.map((f, i) => <FeatureCard key={i} {...f} />)}
        </div>
      </section>

      {/* Ethics & Privacy */}
      <section id="ethics"><EthicsSection /></section>

      {/* Footer */}
      <footer className="mt-auto py-6 text-center text-gray-500 text-sm">
        &copy; {new Date().getFullYear()} Digital Twin. For demonstration only.
      </footer>
    </div>
  );
}
