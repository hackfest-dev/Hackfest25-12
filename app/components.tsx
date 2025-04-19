import React from "react";
import Image from "next/image";
import { features, ethics, blackMirror } from "./landing-data";

export const FeatureCard: React.FC<{ title: string; description: string; icon: string }> = ({ title, description, icon }) => (
  <div className="bg-white rounded-2xl shadow-md p-6 w-72 flex flex-col items-center border border-pink-100 hover:shadow-xl transition">
    <span className="text-4xl mb-3">{icon}</span>
    <h3 className="font-bold text-lg text-gray-800 mb-2 text-center">{title}</h3>
    <p className="text-gray-600 text-center text-base">{description}</p>
  </div>
);

export const PlaceholderChart: React.FC<{ label: string }> = ({ label }) => (
  <div className="flex flex-col items-center">
    <div className="w-20 h-16 bg-gradient-to-t from-pink-200 to-blue-100 rounded-xl mb-1 flex items-end justify-center">
      <svg width="56" height="36" viewBox="0 0 56 36" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4 32L20 20L28 28L40 8L52 32" stroke="#ec4899" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    </div>
    <span className="text-xs text-gray-500 mt-1">{label}</span>
  </div>
);

export const EthicsSection: React.FC = () => (
  <section className="w-full bg-gradient-to-r from-pink-50 via-white to-blue-50 py-12 px-4 flex flex-col items-center">
    <h2 className="text-2xl font-bold text-blue-700 mb-4">{ethics.title}</h2>
    <ul className="list-disc pl-6 text-gray-700 max-w-xl">
      {ethics.points.map((p, i) => (
        <li key={i} className="mb-2">{p}</li>
      ))}
    </ul>
  </section>
);

export const BlackMirrorSection: React.FC = () => (
  <section className="w-full bg-white/80 py-12 px-4 flex flex-col items-center">
    <h2 className="text-2xl font-bold text-pink-700 mb-4">Black Mirror Inspiration</h2>
    <div className="flex flex-wrap gap-6 justify-center">
      {blackMirror.map((item, i) => (
        <div key={i} className="bg-pink-50 rounded-xl p-6 w-80 border border-pink-100">
          <h3 className="font-semibold text-lg mb-2">{item.title}</h3>
          <p className="text-gray-600">{item.description}</p>
        </div>
      ))}
    </div>
  </section>
);
