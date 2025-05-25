import { useState } from "react";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { Card } from "primereact/card";
import { ProgressSpinner } from "primereact/progressspinner";
import "primereact/resources/themes/lara-light-blue/theme.css";
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";

function Transcriber() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");
  const [summaryLoading, setSummaryLoading] = useState(false);

  const handleTranscribe = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult("");
    setSummary(""); // Clear summary on new transcription
    try {
      const response = await fetch("http://127.0.0.1:5000/api/transcribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      setResult(data.transcription || data.error || "Unknown error");
    } catch (err) {
      setResult("Network error");
    }
    setLoading(false);
  };

  const handleSummarize = async () => {
    setSummaryLoading(true);
    setSummary("");
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/chatgpt_keypoints",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: result }),
        }
      );
      const data = await response.json();
      setSummary(data.keypoints || data.error || "Unknown error");
    } catch (err) {
      setSummary("Network error");
    }
    setSummaryLoading(false);
  };

  return (
    <div className="transcriber-root">
      {/* Input Box */}
      <div className="transcriber-input-container">
        <Card title="YouTube Transcriber">
          <form className="transcriber-form" onSubmit={handleTranscribe}>
            <span className="p-input-icon-left">
              <i className="pi pi-link" />
              <InputText
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Paste YouTube URL"
                required
              />
            </span>
            <Button
              className="transcriber-submit-btn"
              type="submit"
              label={loading ? "Transcribing..." : "Transcribe"}
              icon={
                loading ? (
                  <ProgressSpinner
                    style={{ width: 18, height: 18 }}
                    strokeWidth="6"
                  />
                ) : (
                  "pi pi-send"
                )
              }
              iconPos="left"
              disabled={loading}
            />
            {/* Summarize button appears only when transcript is available and not loading */}
            {result && !loading && (
              <Button
                className="transcriber-submit-btn"
                type="button"
                label={
                  summary
                    ? summaryLoading
                      ? "Summarizing..."
                      : "Summarize Again"
                    : summaryLoading
                    ? "Summarizing..."
                    : "Summarize"
                }
                icon={summary ? "pi pi-refresh" : "pi pi-list"}
                loading={summaryLoading}
                onClick={handleSummarize}
                style={{ marginTop: "1rem" }}
              />
            )}
          </form>
        </Card>
      </div>

      {/* Results Section */}
      {summary ? (
        <div className="transcriber-results-row">
          <div className="transcriber-result-box">
            <div className="transcriber-result-title">Transcript</div>
            <pre className="transcriber-result-text">{result}</pre>
          </div>
          <div className="transcriber-result-box">
            <div className="transcriber-result-title">Summary</div>
            <pre className="transcriber-result-text">{summary}</pre>
          </div>
        </div>
      ) : (
        <div className="transcriber-result-box">
          {loading ? (
            <div className="transcriber-loading-row">
              <span className="transcriber-loading-text">
                Transcribing...
                <ProgressSpinner
                  style={{
                    width: 18,
                    height: 18,
                    marginLeft: 12,
                    verticalAlign: "middle",
                  }}
                  strokeWidth="6"
                />
              </span>
            </div>
          ) : (
            <>
              <div className="transcriber-result-title">Transcript</div>
              <pre className="transcriber-result-text">
                {result || "The transcription will appear here."}
              </pre>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default Transcriber;
