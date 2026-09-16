"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type Tab = "match" | "caption" | "vqa";

interface MatchResult {
  text: string;
  score: number;
}

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 Mo — doit matcher settings.max_image_bytes côté backend

export default function Home() {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>("match");

  const [caption, setCaption] = useState<string | null>(null);
  const [captionLoading, setCaptionLoading] = useState(false);

  const [candidateTexts, setCandidateTexts] = useState(
    "a photo of a dog\na photo of a cat\na photo of a city street\na photo of a mountain landscape"
  );
  const [matchResults, setMatchResults] = useState<MatchResult[] | null>(null);
  const [matchLoading, setMatchLoading] = useState(false);

  const [question, setQuestion] = useState("What is in the picture?");
  const [answer, setAnswer] = useState<string | null>(null);
  const [vqaLoading, setVqaLoading] = useState(false);

  const [error, setError] = useState<string | null>(null);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > MAX_FILE_SIZE) {
      setError(`Image too large (${(file.size / 1024 / 1024).toFixed(1)} MB). Max size is 10 MB.`);
      e.target.value = "";
      return;
    }

    setImageFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setCaption(null);
    setMatchResults(null);
    setAnswer(null);
    setError(null);
  }

  async function handleCaption() {
    if (!imageFile) return;
    setCaptionLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", imageFile);

      const response = await fetch(`${API_URL}/api/caption`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error();

      const data = await response.json();
      setCaption(data.caption);
    } catch {
      setError("Couldn't generate a caption. Check that the backend is running.");
    } finally {
      setCaptionLoading(false);
    }
  }

  async function handleMatch() {
    if (!imageFile) return;
    if (!candidateTexts.trim()) {
      setError("Enter at least one candidate description.");
      return;
    }

    setMatchLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", imageFile);
      formData.append("texts", candidateTexts);

      const response = await fetch(`${API_URL}/api/match`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error();

      const data = await response.json();
      setMatchResults(data.results);
    } catch {
      setError("Couldn't match the image to those descriptions.");
    } finally {
      setMatchLoading(false);
    }
  }

  async function handleVqa() {
    if (!imageFile) return;
    if (!question.trim()) {
      setError("Enter a question.");
      return;
    }

    setVqaLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", imageFile);
      formData.append("question", question);

      const response = await fetch(`${API_URL}/api/vqa`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error();

      const data = await response.json();
      setAnswer(data.answer);
    } catch {
      setError("Couldn't get an answer for that question.");
    } finally {
      setVqaLoading(false);
    }
  }

  return (
    <main className="console">
      <header className="console-header">
        <div>
          <h1 className="console-title">Vision Console</h1>
          <p className="console-sub">Upload an image, then match, caption, or ask.</p>
        </div>
        <div className="status">
          <span className={`status-dot ${imageFile ? "is-active" : ""}`} />
          {imageFile ? "image loaded" : "no image"}
        </div>
      </header>

      <label
        className={`viewfinder ${imageFile ? "is-loaded" : "is-empty"}`}
        key={imageFile ? imageFile.name + imageFile.lastModified : "empty"}
      >
        <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handleFileChange} />
        <span className="corner corner-tl" />
        <span className="corner corner-tr" />
        <span className="corner corner-bl" />
        <span className="corner corner-br" />

        {previewUrl ? (
          <img src={previewUrl} alt="Uploaded" />
        ) : (
          <span className="drop-hint">
            <strong>Click to upload an image</strong>
            <span>JPG, PNG or WEBP · up to 10 MB</span>
          </span>
        )}
      </label>

      {imageFile && (
        <>
          <div className="segmented">
            {(["match", "caption", "vqa"] as Tab[]).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={activeTab === tab ? "is-active" : ""}
              >
                {tab === "match" && "Match"}
                {tab === "caption" && "Caption"}
                {tab === "vqa" && "Ask"}
              </button>
            ))}
          </div>

          {activeTab === "match" && (
            <div className="instrument">
              <textarea
                className="field"
                value={candidateTexts}
                onChange={(e) => setCandidateTexts(e.target.value)}
                rows={4}
                placeholder="One description per line"
              />
              <button className="run-btn" onClick={handleMatch} disabled={matchLoading}>
                {matchLoading && <span className="pulse" />}
                {matchLoading ? "Matching" : "Run match"}
              </button>

              {matchResults && (
                <div className="panel">
                  <p className="panel-label">Ranked by relevance</p>
                  <div className="meters">
                    {matchResults.map((r) => (
                      <div className="meter-row" key={r.text}>
                        <div className="meter-top">
                          <span>{r.text}</span>
                          <span className="meter-score">{(r.score * 100).toFixed(1)}%</span>
                        </div>
                        <div className="meter-track">
                          <div
                            className="meter-fill"
                            style={{ width: `${Math.min(r.score * 100, 100)}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === "caption" && (
            <div className="instrument">
              <button className="run-btn" onClick={handleCaption} disabled={captionLoading}>
                {captionLoading && <span className="pulse" />}
                {captionLoading ? "Generating" : "Generate caption"}
              </button>

              {caption && (
                <div className="panel">
                  <p className="panel-label">Caption</p>
                  <p>{caption}</p>
                </div>
              )}
            </div>
          )}

          {activeTab === "vqa" && (
            <div className="instrument">
              <input
                type="text"
                className="field"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask something about the image"
              />
              <button className="run-btn" onClick={handleVqa} disabled={vqaLoading}>
                {vqaLoading && <span className="pulse" />}
                {vqaLoading ? "Thinking" : "Ask"}
              </button>

              {answer && (
                <div className="panel">
                  <p className="panel-label">{question}</p>
                  <p>{answer}</p>
                </div>
              )}
            </div>
          )}
        </>
      )}

      {error && (
        <div className="panel panel-danger">
          <p>{error}</p>
        </div>
      )}
    </main>
  );
}