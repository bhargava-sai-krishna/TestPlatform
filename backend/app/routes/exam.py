from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Question, ExamSession, ExamQuestion, Answer
import random

bp = Blueprint("exam", __name__, url_prefix="/api/exam")


@bp.route("/start", methods=["POST"])
@jwt_required()
def start_exam():
    """
    Start a new exam session
    ---
    tags:
      - Exam
    security:
      - Bearer: []
    responses:
      200:
        description: Exam started, returns 10 randomized questions
        content:
          application/json:
            schema:
              type: object
              properties:
                session_id:
                  type: integer
                  example: 12
                questions:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 3
                      text:
                        type: string
                        example: "What is the capital of France?"
                      options:
                        type: object
                        properties:
                          A:
                            type: string
                            example: "Paris"
                          B:
                            type: string
                            example: "Berlin"
                          C:
                            type: string
                            example: "Madrid"
                          D:
                            type: string
                            example: "Rome"
      401:
        description: Unauthorized, missing or invalid token
    """
    uid = get_jwt_identity()

    session = ExamSession(user_id=uid)
    db.session.add(session)
    db.session.commit()

    all_questions = Question.query.all()
    selected = random.sample(all_questions, 10)

    for q in selected:
        eq = ExamQuestion(exam_session_id=session.id, question_id=q.id)
        db.session.add(eq)
    db.session.commit()

    questions_payload = [
        {
            "id": q.id,
            "text": q.question_text,
            "options": {
                "A": q.option_a,
                "B": q.option_b,
                "C": q.option_c,
                "D": q.option_d,
            }
        }
        for q in selected
    ]

    return jsonify({
        "session_id": session.id,
        "questions": questions_payload
    }), 200


@bp.route("/submit", methods=["POST"])
@jwt_required()
def submit_exam():
    """
    Submit answers for an exam session
    ---
    tags:
      - Exam
    security:
      - Bearer: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              session_id:
                type: integer
                example: 12
              answers:
                type: array
                items:
                  type: object
                  properties:
                    question_id:
                      type: integer
                      example: 3
                    chosen_option:
                      type: string
                      enum: [A, B, C, D]
                      example: "A"
    responses:
      200:
        description: Exam submitted successfully with calculated score
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "submitted"
                score:
                  type: integer
                  example: 8
      400:
        description: Invalid or already submitted session
      401:
        description: Unauthorized, missing or invalid token
    """
    data = request.get_json(force=True)
    session_id = data.get("session_id")
    answers = data.get("answers")

    session = ExamSession.query.get(session_id)
    if not session or session.submitted:
        return jsonify({"error": "invalid or already submitted"}), 400

    score = 0
    for ans in answers:
        q = Question.query.get(ans["question_id"])
        chosen = ans["chosen_option"]

        answer = Answer(
            exam_session_id=session.id,
            question_id=q.id,
            chosen_option=chosen
        )
        db.session.add(answer)

        if q.correct_option == chosen:
            score += 1

    session.score = score
    session.submitted = True
    db.session.commit()

    return jsonify({"message": "submitted", "score": score}), 200
