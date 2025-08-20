import React, { useState, useEffect } from "react";

// Dummy questions for now
const QUESTIONS = [
  { id: 1, text: "What is 2 + 2?", options: ["2", "3", "4", "5"] },
  { id: 2, text: "Capital of France?", options: ["Berlin", "Madrid", "Paris", "Rome"] },
  { id: 3, text: "React is a ___?", options: ["Framework", "Library", "Language", "Tool"] },
];

export default function Exam() {
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(30 * 60); // 30 mins in seconds
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    if (timeLeft <= 0 || submitted) return;
    const timer = setInterval(() => setTimeLeft(t => t - 1), 1000);
    return () => clearInterval(timer);
  }, [timeLeft, submitted]);

  function handleAnswer(option) {
    setAnswers({ ...answers, [QUESTIONS[current].id]: option });
  }

  function handleSubmit() {
    setSubmitted(true);
    console.log("Submitted answers:", answers);
    alert("✅ Exam submitted! Check console for answers.");
  }

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const q = QUESTIONS[current];

  return (
    <div>
      <h2>Exam</h2>
      <p>⏰ Time left: {minutes}:{seconds.toString().padStart(2, "0")}</p>

      {!submitted ? (
        <div>
          <h3>{q.text}</h3>
          {q.options.map((opt, i) => (
            <button
              key={i}
              style={{
                background: answers[q.id] === opt ? "lightgreen" : "white",
                margin: "5px"
              }}
              onClick={() => handleAnswer(opt)}
            >
              {opt}
            </button>
          ))}
          <div style={{ marginTop: "10px" }}>
            <button disabled={current === 0} onClick={() => setCurrent(c => c - 1)}>⬅ Prev</button>
            <button disabled={current === QUESTIONS.length - 1} onClick={() => setCurrent(c => c + 1)}>Next ➡</button>
          </div>
          <div style={{ marginTop: "10px" }}>
            <button onClick={handleSubmit}>Submit Exam</button>
          </div>
        </div>
      ) : (
        <h3>✅ Exam submitted successfully!</h3>
      )}
    </div>
  );
}
