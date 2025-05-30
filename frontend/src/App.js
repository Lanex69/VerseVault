import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!keyword.trim()) {
      alert("Please enter a keyword to search.");
      return;
    }
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:5000/search?keyword=${keyword.trim()}`, {
        headers: {
          'Accept': 'application/json',
        },
      });
      console.log("Raw Response:", response);
      console.log("Response Data:", response.data);
      setResults(response.data);
    } catch (error) {
      console.error("Error fetching search results:", error);
      if (error.response) {
        console.error("Error Response Status:", error.response.status);
        console.error("Error Response Data:", error.response.data);
      }
      setResults([]);
      alert("Failed to fetch results. Please check if the server is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-6">VerseVault Search</h1>
      <div className="max-w-md mx-auto mb-6">
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Enter keyword (e.g., mercy)"
          className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleSearch}
          className="mt-3 w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition duration-200"
        >
          Search
        </button>
        <button
  onClick={() => {
    setKeyword("");
    setResults([]);
  }}
  className="mt-3 w-full bg-gray-500 text-white p-3 rounded-lg hover:bg-gray-600 transition duration-200"
>
  Clear
</button>
      </div>
      <div className="max-w-4xl mx-auto">
        {loading ? (
          <p className="text-center text-gray-500">Loading...</p>
        ) : results.length > 0 ? (
          results.map((verse, index) => (
            <div key={index} className="bg-white p-6 mb-4 rounded-lg shadow-md flex flex-col md:flex-row hover:shadow-lg transition duration-200">
              <div className="w-full md:w-1/2 text-right pr-0 md:pr-4 mb-4 md:mb-0">
                <p className="text-lg font-arabic" dir="rtl">{verse.arabic}</p>
              </div>
              <div className="w-full md:w-1/2 pl-0 md:pl-4">
                <p className="text-lg">{verse.english}</p>
                <p className="text-sm text-gray-500">
                  Surah {verse.surah}, Ayah {verse.ayah}
                </p>
              </div>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-500">No results found. Try a different keyword.</p>
        )}
      </div>
    </div>
  );
}

export default App;