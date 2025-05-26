import React, { useState } from "react";

const RedditScraper: React.FC = () => {
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleScrape = async () => {
    setLoading(true);
    const response = await fetch("http://localhost:5000/api/scrape_reddit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ limit: 5 }),
    });
    const data = await response.json();
    setPosts(data);
    setLoading(false);
  };

  return (
    <div>
      <button onClick={handleScrape} disabled={loading}>
        {loading ? "Scraping..." : "Scrape Reddit"}
      </button>
      <ul>
        {posts.map((post, idx) => (
          <li key={idx}>
            <strong>{post.title}</strong>
            <p>{post.selftext}</p>
            <a href={post.url} target="_blank" rel="noopener noreferrer">
              View Post
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RedditScraper;
