import React, { useState, useEffect } from "react";
import { apiRequest } from "../utils/api";

export default function Exam({ token, onExit }) {
  const [sessionId, setSessionId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(30 * 60); // 30 mins
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(null);

  // start exam on mount
  useEffect(() => {
    async function startExam() {
      try {
        const res = await apiRequest("/api/exam/start", "POST", null, token);
        setSessionId(res.session_id);
        setQuestions(res.questions);
      } catch (err) {
        console.error("Error starting exam:", err);
      }
    }
    startExam();
  }, [token]);

  useEffect(() => {
    if (submitted) return;
    if (timeLeft <= 0) {
      handleSubmit(); 
      return;
    }
    const timer = setInterval(() => setTimeLeft((t) => t - 1), 1000);
    return () => clearInterval(timer);
    // eslint-disable-next-line
  }, [timeLeft, submitted]);

  function handleAnswer(option) {
    setAnswers({ ...answers, [questions[current].id]: option });
  }

  async function handleSubmit() {
    if (submitted) return;
    setSubmitted(true);

    try {
      const formatted = Object.keys(answers).map((qid) => ({
        question_id: parseInt(qid),
        chosen_option: answers[qid],
      }));

      const res = await apiRequest(
        "/api/exam/submit",
        "POST",
        { session_id: sessionId, answers: formatted },
        token
      );

      setScore(res.score);
    } catch (err) {
      console.error("Error submitting exam:", err);
    }
  }

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  if (!questions.length) return <p>Loading exam...</p>;

  const q = questions[current];

  return (
    <div style={{ padding: "20px" }}>
      <h2>📝 Exam</h2>
      <p>
        ⏰ Time left: {minutes}:{seconds.toString().padStart(2, "0")}
      </p>

      {!submitted ? (
        <div>
          <h3>{q.text}</h3>
          {Object.entries(q.options).map(([key, value]) => (
            <button
              key={key}
              style={{
                background: answers[q.id] === key ? "lightgreen" : "white",
                margin: "5px",
              }}
              onClick={() => handleAnswer(key)}
            >
              {key}. {value}
            </button>
          ))}

          <div style={{ marginTop: "10px" }}>
            <button
              disabled={current === 0}
              onClick={() => setCurrent((c) => c - 1)}
            >
              ⬅ Prev
            </button>
            <button
              disabled={current === questions.length - 1}
              onClick={() => setCurrent((c) => c + 1)}
            >
              Next ➡
            </button>
          </div>

          <div style={{ marginTop: "10px" }}>
            <button onClick={handleSubmit}>Submit Exam</button>
          </div>
        </div>
      ) : (
        <>
          <h3>✅ Exam submitted! Your score: {score}</h3>
          <button onClick={onExit}>Back to Profile</button>
        </>
      )}
    </div>
  );
}
