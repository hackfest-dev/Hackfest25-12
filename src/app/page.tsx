'use client';

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import DigitalTwinAnimation from "./components/DigitalTwinAnimation";

export default function Home() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <section className="pt-20 pb-16">
        <div className="container mx-auto px-4">
          <div className="flex flex-col lg:flex-row items-center">
            <div className="lg:w-1/2 mb-10 lg:mb-0">
              <h1 className="text-4xl md:text-5xl font-bold text-blue-900 mb-4">
                Healthcare Digital Twin
              </h1>
              <h2 className="text-2xl md:text-3xl text-blue-700 mb-6">
                Optimizing Health Outcomes with Personalized Digital Twins
              </h2>
              <p className="text-lg text-gray-700 mb-8">
                Experience the future of personalized healthcare with our advanced digital twin technology.
                Monitor, predict, and optimize your health in real-time with AI-powered insights.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <a
  href="https://platypuses-pharma.streamlit.app/"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 text-center"
>
  Drug Testing
</a>
                <a
  href="https://platypuses-enduser.streamlit.app/"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-block bg-white hover:bg-gray-100 text-blue-600 font-semibold py-3 px-6 rounded-lg border border-blue-600 transition-colors duration-200 text-center"
>
  Individual Twin
</a>
              </div>
            </div>
            <div className="lg:w-1/2 flex justify-center lg:justify-end">
              <div className="relative w-full max-w-lg h-80 md:h-96">
                <Image 
                  src="/healthcare-twin.png" 
                  alt="Healthcare Digital Twin Illustration" 
                  fill
                  className="object-contain"
                  priority
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-blue-900 mb-12">Key Features</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-blue-50 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
              <div className="w-14 h-14 bg-blue-600 rounded-full flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-blue-900 mb-2">Health Monitoring</h3>
              <p className="text-gray-700">
                Continuous monitoring of vital signs, activity levels, and health metrics in a comprehensive dashboard.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-blue-50 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
              <div className="w-14 h-14 bg-blue-600 rounded-full flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-blue-900 mb-2">Predictive Analytics</h3>
              <p className="text-gray-700">
                AI-powered predictions of health risks and personalized recommendations to improve health outcomes.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-blue-50 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
              <div className="w-14 h-14 bg-blue-600 rounded-full flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-blue-900 mb-2">ML Integration</h3>
              <p className="text-gray-700">
                Trained on various datasets, and multiple models to provide the best possible predictions.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-blue-50 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
              <div className="w-14 h-14 bg-blue-600 rounded-full flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-blue-900 mb-2">Data Security</h3>
              <p className="text-gray-700">
                State-of-the-art encryption and privacy controls to keep your sensitive health data secure and protected.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="bg-blue-50 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
              <div className="w-14 h-14 bg-blue-600 rounded-full flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-blue-900 mb-2">Medication Management</h3>
              <p className="text-gray-700">
                Track medications, set reminders, and receive alerts about potential interactions to ensure safety.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="bg-blue-50 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
              <div className="w-14 h-14 bg-blue-600 rounded-full flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-blue-900 mb-2">Wellness Integration</h3>
              <p className="text-gray-700">
                Connect with fitness apps, wearables, and smart devices for a comprehensive health and wellness ecosystem.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-blue-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-blue-900 mb-12">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-white">1</span>
              </div>
              <h3 className="text-xl font-semibold text-blue-900 mb-3">Create Your Digital Twin</h3>
              <p className="text-gray-700">
                Input your health data, connect devices, and establish your personalized digital health profile.
              </p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-white">2</span>
              </div>
              <h3 className="text-xl font-semibold text-blue-900 mb-3">Monitor & Analyze</h3>
              <p className="text-gray-700">
                Our AI continuously monitors your health metrics and analyzes patterns to provide personalized insights.
              </p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-white">3</span>
              </div>
              <h3 className="text-xl font-semibold text-blue-900 mb-3">Optimize Your Health</h3>
              <p className="text-gray-700">
                Receive personalized recommendations and connect with healthcare providers for improved outcomes.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="bg-blue-600 rounded-2xl p-8 md:p-12 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">Ready to Transform Your Healthcare Experience?</h2>
            <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
              Join thousands of users who are already experiencing the benefits of personalized digital health management.
            </p>
            <Link href="https://platypuses-enduser.streamlit.app/" 
                  className="inline-block bg-white hover:bg-gray-100 text-blue-600 font-semibold py-3 px-8 rounded-lg transition-colors duration-200">
              Get Started Today
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
