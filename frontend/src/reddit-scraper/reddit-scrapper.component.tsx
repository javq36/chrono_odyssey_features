import React, { useState } from "react";
import { Button } from "primereact/button";
import { Card } from "primereact/card";
import { ProgressSpinner } from "primereact/progressspinner";
import { Message } from "primereact/message";
import { Accordion, AccordionTab } from "primereact/accordion"; // For displaying comments

interface RedditComment {
  id: string;
  body: string;
  author: string | null;
  score: number;
  created_utc: number;
}

interface RedditPost {
  id: string;
  title: string;
  selftext: string;
  url: string;
  created_utc: number; // Added
  comments: RedditComment[]; // Added
  // Consider adding from your backend if available and useful:
  // author?: string; // Post author, if you decide to fetch it
  // score?: number; // Post score, if you decide to fetch it
  // num_comments?: number; // Total number of comments on Reddit, if fetched
}

const RedditScraper: React.FC = () => {
  const [posts, setPosts] = useState<RedditPost[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleScrape = async () => {
    setLoading(true);
    setError(null);
    setPosts([]);
    try {
      const response = await fetch("http://localhost:5000/api/scrape_reddit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Body can be empty if backend defaults limit and comment_limit
        // Or send specific limits:
        body: JSON.stringify({ post_limit: 5, comment_limit_per_post: 3 }),
      });
      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({ message: `HTTP error! status: ${response.status}` }));
        throw new Error(
          errorData.message || `HTTP error! status: ${response.status}`
        );
      }
      const data = await response.json();
      setPosts(
        data.map((post: any) => ({
          ...post,
          id: post.id || post.name || Math.random().toString(),
          comments: post.comments || [], // Ensure comments is an array
        }))
      );
    } catch (e: any) {
      setError(e.message || "Failed to scrape Reddit posts.");
      console.error("Scraping error:", e);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString();
  };

  const postCardFooter = (post: RedditPost) => (
    <div className="flex justify-content-between align-items-center pt-2 text-xs text-gray-500">
      <span>Posted: {formatDate(post.created_utc)}</span>
      <Button
        label="View on Reddit"
        icon="pi pi-external-link"
        className="p-button-sm p-button-text" // Changed to text for less emphasis
        onClick={() => window.open(post.url, "_blank")}
      />
    </div>
  );

  const postCardHeader = (title: string) => (
    <div className="p-card-title text-lg font-semibold px-3 pt-3 pb-0">
      {title}
    </div>
  );

  return (
    <div className="p-4">
      <div className="flex justify-content-between align-items-center mb-4">
        <h2 className="text-2xl font-semibold m-0">Reddit Posts</h2>
        <Button
          label={loading ? "Scraping..." : "Scrape Reddit"}
          icon={loading ? "pi pi-spin pi-spinner" : "pi pi-reddit"}
          onClick={handleScrape}
          disabled={loading}
          className="p-button-raised p-button-primary"
        />
      </div>

      {loading && (
        <div className="flex justify-content-center my-4 py-4">
          <ProgressSpinner
            style={{ width: "60px", height: "60px" }}
            strokeWidth="6"
            animationDuration=".8s"
          />
        </div>
      )}

      {error && (
        <Message severity="error" text={error} className="my-4 w-full" />
      )}

      {!loading && posts.length === 0 && !error && (
        <div className="text-center text-gray-500 py-4 my-4 border-1 border-dashed border-gray-300 p-4 rounded-md">
          <i className="pi pi-inbox text-4xl mb-2"></i>
          <p className="text-lg">No posts to display.</p>
          <p>Click the "Scrape Reddit" button to fetch the latest posts.</p>
        </div>
      )}

      {!loading && posts.length > 0 && (
        <div className="grid">
          {posts.map((post) => (
            <div key={post.id} className="col-12 md:col-6 xl:col-4 p-2">
              <Card
                header={postCardHeader(post.title)}
                footer={postCardFooter(post)} // Pass the whole post object
                className="h-full shadow-md hover:shadow-lg transition-shadow duration-200"
                style={{ display: "flex", flexDirection: "column" }}
              >
                <div
                  className="p-card-content px-3 pb-0"
                  style={{ flexGrow: 1, overflowY: "auto", maxHeight: "150px" }}
                >
                  <p className="m-0 text-sm text-gray-700 leading-relaxed">
                    {post.selftext ? (
                      post.selftext.length > 200 ? (
                        `${post.selftext.substring(0, 200)}...`
                      ) : (
                        post.selftext
                      )
                    ) : (
                      <span className="text-gray-500 italic">
                        No text content available for this post.
                      </span>
                    )}
                  </p>
                </div>
                {post.comments && post.comments.length > 0 && (
                  <Accordion className="mt-2 text-sm">
                    <AccordionTab
                      header={`View ${post.comments.length} Comment(s)`}
                    >
                      <div style={{ maxHeight: "200px", overflowY: "auto" }}>
                        {post.comments.map((comment) => (
                          <div
                            key={comment.id}
                            className="p-2 border-bottom-1 border-gray-200"
                          >
                            <p className="font-semibold text-xs mb-1">
                              {comment.author || "Anonymous"} (Score:{" "}
                              {comment.score}) -{" "}
                              {formatDate(comment.created_utc)}
                            </p>
                            <p className="m-0 text-xs">{comment.body}</p>
                          </div>
                        ))}
                      </div>
                    </AccordionTab>
                  </Accordion>
                )}
              </Card>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RedditScraper;
