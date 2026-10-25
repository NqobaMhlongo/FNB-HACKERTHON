from datetime import datetime, timezone
from flask import Blueprint, request, redirect, url_for, flash, session
from app import db
from app.models import (
    User,
    WorkProofChallenge,
    WorkProofSubmission,
    SkillsPassport,
)
from app.routes.auth import candidate_required
from app.services.verification_service import (
    evaluate_workproof_submission,
    sync_skills_passport,
)

assessment_bp = Blueprint("assessment", __name__, url_prefix="/assessment")


@assessment_bp.route("/start/<int:challenge_id>", methods=["GET", "POST"])
@candidate_required
def start_or_resume(challenge_id: int):
    challenge = db.get_or_404(WorkProofChallenge, challenge_id)
    user_id = session["user_id"]

    submission = WorkProofSubmission.query.filter_by(
        user_id=user_id, challenge_id=challenge.id
    ).first()

    if not submission:
        submission = WorkProofSubmission(
            user_id=user_id,
            challenge_id=challenge.id,
            status="in_progress",
            evidence_score=0,
            next_best_action=f"Complete the Build, Explain, and Adapt phases for '{challenge.title}'.",
        )
        db.session.add(submission)
        db.session.commit()

    return redirect(url_for("candidate.workproof_stepper", challenge_id=challenge.id))


@assessment_bp.route("/submit/<int:challenge_id>", methods=["POST"])
@candidate_required
def submit_workproof(challenge_id: int):
    challenge = db.get_or_404(WorkProofChallenge, challenge_id)
    user = db.get_or_404(User, session["user_id"])

    submission = WorkProofSubmission.query.filter_by(
        user_id=user.id, challenge_id=challenge.id
    ).first()

    if not submission:
        submission = WorkProofSubmission(user_id=user.id, challenge_id=challenge.id)
        db.session.add(submission)

    submission.build_repo_url = (request.form.get("build_repo_url") or "").strip()
    submission.build_code_snippet = (request.form.get("build_code_snippet") or "").strip()
    submission.explain_notes = (request.form.get("explain_notes") or "").strip()
    submission.adapt_solution = (request.form.get("adapt_solution") or "").strip()

    action = request.form.get("action", "submit")

    if action == "save_draft":
        if submission.status != "verified":
            submission.status = "in_progress"
        db.session.commit()
        flash("Draft progress saved. You can resume anytime.", "info")
        return redirect(url_for("candidate.workproof_stepper", challenge_id=challenge.id))

    evaluation = evaluate_workproof_submission(user, challenge, submission)

    submission.evidence_score = evaluation["evidence_score"]
    submission.status = evaluation["status"]
    submission.readiness_feedback = evaluation["readiness_feedback"]
    submission.next_best_action = evaluation["next_best_action"]
    submission.completed_at = datetime.now(timezone.utc)

    passport = SkillsPassport.query.filter_by(user_id=user.id).first()
    if not passport:
        passport = SkillsPassport(user_id=user.id)
        db.session.add(passport)

    sync_skills_passport(user, challenge, evaluation, passport)
    db.session.commit()

    if evaluation["status"] == "verified":
        flash(
            f"WorkProof Verified! Score: {evaluation['evidence_score']}/100 — "
            f"Your Skills Passport is now at Trust Level {passport.highest_trust_level}.",
            "success",
        )
    else:
        flash(
            f"WorkProof Evaluated: {evaluation['evidence_score']}/100. Review your Readiness Feedback "
            f"below to reach the {challenge.passing_score}/100 verification threshold.",
            "warning",
        )

    return redirect(url_for("candidate.dashboard"))
