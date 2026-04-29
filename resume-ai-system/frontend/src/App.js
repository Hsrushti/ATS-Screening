import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [files, setFiles] = useState([]);
  const [jd, setJd] = useState("");
  const [results, setResults] = useState([]);

  const handleSubmit = async () => {
    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    formData.append("jd", jd);

    try {
      const res = await axios.post(
        "http://localhost:8000/bulk-match",
        formData
      );

      setResults(res.data.ranked_candidates);
    } catch (error) {
      alert("Error connecting to backend");
      console.log(error);
    }
  };

  return (
    <div className="container">
      <h1>Resume AI Screening</h1>

      <input
        type="file"
        multiple
        accept=".pdf,.txt,.doc,.docx"
        onChange={(e) => setFiles(e.target.files)}
      />

      <textarea
        placeholder="Paste Job Description Here..."
        rows="8"
        value={jd}
        onChange={(e) => setJd(e.target.value)}
      />

      <button onClick={handleSubmit}>Analyze Candidates</button>

      <div className="results">
        {results.map((item, index) => (
          <div className="card" key={index}>
            <h3>{index + 1}. {item.filename}</h3>
            <p>Fit Score: {item.fit_score}%</p>
            <p>{item.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;