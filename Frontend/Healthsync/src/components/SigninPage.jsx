import React from 'react';
import ReactDOM from 'react-dom/client';
import { ClerkProvider, SignedIn, SignedOut, SignInButton, UserButton, RedirectToSignIn } from '@clerk/clerk-react';

// Import your publishable key from environment variables
const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!PUBLISHABLE_KEY) {
  throw new Error("Missing Publishable Key");
}

// Landing page component
function LandingPage() {
  return (
    <div className="flex h-screen w-[100vw] items-center justify-center align-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">Welcome to HealthSync</h1>
        <p className="text-lg text-gray-700 mb-8">Sign in to get started</p>
        <SignedOut>
          <SignInButton mode="modal" >
            <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              Sign In
            </button>
          </SignInButton>
        </SignedOut>
        <SignedIn RedirectAfterSignIn="/">
          <UserButton  />
        </SignedIn>
      </div>
    </div>
  );
}

export default LandingPage;
