import json
from datetime import datetime, timezone
from app import create_app, db
from app.models import (
    User,
    Pathway,
    WorkProofChallenge,
    WorkProofSubmission,
    SkillsPassport,
    EmployerShortlist,
)


def seed_database():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ---------------------------------------------------------------------
        # 1. Create 9 South African IT Pathways (Total = 100% Market Share)
        # ---------------------------------------------------------------------
        pathway_dev = Pathway(
            title="Junior Software Developer",
            slug="junior-software-developer",
            description=(
                "Backend & full-stack application engineering focused on clean API design, "
                "input validation, error handling, and production bug resolution."
            ),
            market_share_pct=26,
        )
        pathway_cloud = Pathway(
            title="IT Support / Cloud",
            slug="it-support-cloud",
            description=(
                "Linux server administration, automated bash diagnostics, network firewall "
                "hardening (UFW), and cloud infrastructure incident response."
            ),
            market_share_pct=18,
        )
        pathway_data = Pathway(
            title="Junior Data Analyst",
            slug="junior-data-analyst",
            description=(
                "Data cleaning, SQL/Python aggregation, missing-record imputation, and KPI "
                "reporting for South African retail and financial operations."
            ),
            market_share_pct=12,
        )
        pathway_cyber = Pathway(
            title="Junior Cybersecurity & SOC Analyst",
            slug="junior-cybersecurity-analyst",
            description=(
                "SIEM log triage, credential-stuffing detection, POPIA personal data masking, "
                "and incident containment for South African banking and telecoms."
            ),
            market_share_pct=11,
        )
        pathway_qa = Pathway(
            title="Junior QA & Test Automation Engineer",
            slug="junior-qa-automation",
            description=(
                "Automated API regression testing, boundary value analysis, payment double-debit "
                "prevention, and CI test integration using Pytest/Playwright."
            ),
            market_share_pct=9,
        )
        pathway_devops = Pathway(
            title="Junior DevOps & Cloud Native Engineer",
            slug="junior-devops-engineer",
            description=(
                "Docker containerization, multi-stage image hardening, GitHub Actions CI/CD "
                "pipelines, and Kubernetes health-probe resilience during load-shedding."
            ),
            market_share_pct=8,
        )
        pathway_mobile = Pathway(
            title="Junior Mobile App Developer",
            slug="junior-mobile-developer",
            description=(
                "Offline-first Android/Flutter/React Native architecture, local SQLite sync queues, "
                "and low-bandwidth resilience for township & rural field operations."
            ),
            market_share_pct=7,
        )
        pathway_bi = Pathway(
            title="Junior Business Intelligence & SQL Developer",
            slug="junior-bi-sql-developer",
            description=(
                "Data warehouse star-schema modelling, complex SQL window functions, and "
                "National Credit Act (NCA) arrears cohort reporting."
            ),
            market_share_pct=5,
        )
        pathway_frontend = Pathway(
            title="Junior UI/UX & Frontend Engineer",
            slug="junior-frontend-uiux",
            description=(
                "Accessible WCAG 2.1 AA responsive interfaces, semantic HTML/JS validation, "
                "multi-language support, and sub-100KB low-data performance optimization."
            ),
            market_share_pct=4,
        )

        db.session.add_all(
            [
                pathway_dev,
                pathway_cloud,
                pathway_data,
                pathway_cyber,
                pathway_qa,
                pathway_devops,
                pathway_mobile,
                pathway_bi,
                pathway_frontend,
            ]
        )
        db.session.flush()

        # ---------------------------------------------------------------------
        # 2. Create 1 Complete WorkProof Challenge per Pathway (9 Challenges)
        # ---------------------------------------------------------------------
        challenge_dev = WorkProofChallenge(
            pathway_id=pathway_dev.id,
            title="RESTful API & Bug Resolution",
            scenario=(
                "You have joined a Cape Town fintech startup building a voucher disbursement API. "
                "Production logs show duplicate redemptions and unhandled 500 crashes when malformed "
                "payloads hit the `/api/v1/vouchers/redeem` endpoint. You need to implement a resilient "
                "endpoint with strict validation, explain your architectural choices, and adapt it for scale."
            ),
            build_prompt=(
                "Implement the `POST /api/v1/vouchers/redeem` endpoint in Python (Flask/FastAPI). "
                "Include input payload validation (voucher_code, user_id, amount_zar), idempotency or "
                "state checks to prevent double-redemption, and appropriate HTTP status codes. "
                "Provide your GitHub repository link and core endpoint code snippet."
            ),
            explain_prompt=(
                "Justify your choice of data structures, transaction locking/idempotency strategy, "
                "and why you selected specific HTTP status codes (e.g., 400 vs 409 vs 422) for each failure mode."
            ),
            adapt_prompt=(
                "CHANGE REQUEST: A retail partner now queries `GET /api/v1/vouchers/history` during month-end "
                "spikes, causing database timeouts and abusive scraping. Modify or extend your solution to "
                "handle cursor/offset pagination and rate-limiting (e.g., 60 requests/min per API key)."
            ),
            passing_score=70,
        )

        challenge_cloud = WorkProofChallenge(
            pathway_id=pathway_cloud.id,
            title="Linux Server Diagnostics & Firewall Config",
            scenario=(
                "An Ubuntu 22.04 cloud VM hosting a student portal in a Johannesburg data center is experiencing "
                "high CPU load and unauthorized SSH brute-force attempts. You must automate system health "
                "diagnostics and lock down network access without disrupting HTTPS traffic."
            ),
            build_prompt=(
                "Write a Bash diagnostic script that captures CPU/memory usage, disk I/O, top 5 processes, "
                "and failed SSH logins, plus a set of UFW firewall rules that enforce least-privilege access. "
                "Provide your repository link and full script."
            ),
            explain_prompt=(
                "Explain your port security choices, why default deny policies matter, and how your diagnostic "
                "script isolates root causes during an active production incident."
            ),
            adapt_prompt=(
                "CHANGE REQUEST: Attackers are rotating IPs to bypass simple static blocks. Update your bash "
                "workflow and configuration to integrate automated `fail2ban` jail rules and dispatch a webhook "
                "alert whenever an IP is banned more than 3 times in 10 minutes."
            ),
            passing_score=70,
        )

        challenge_data = WorkProofChallenge(
            pathway_id=pathway_data.id,
            title="Retail Sales Data Cleaning & Aggregation",
            scenario=(
                "A national grocery retailer in Gauteng exports daily POS transaction logs from 140 stores. "
                "Due to intermittent load-shedding sync issues, 8% of records have missing `unit_price` "
                "or duplicate `transaction_id` entries. Finance needs an accurate provincial KPI summary."
            ),
            build_prompt=(
                "Write a Python (Pandas) or SQL pipeline that deduplicates transaction records, handles "
                "missing `unit_price` and `store_region` values, and computes total revenue, average basket "
                "size, and top 5 categories per province. Attach your repository URL and code."
            ),
            explain_prompt=(
                "Defend your imputation strategy (e.g., category median vs mean vs dropping rows) and explain "
                "how your choice prevents distortion of provincial revenue KPIs."
            ),
            adapt_prompt=(
                "CHANGE REQUEST: The retailer has acquired stores in Namibia (NAD) and Botswana (BWP), and "
                "historical CSV dumps now mix ZAR, NAD, and BWP with timestamps in different timezones. "
                "Adapt your aggregation logic to normalize multi-currency transactions using daily FX rates."
            ),
            passing_score=70,
        )

        challenge_cyber = WorkProofChallenge(
            pathway_id=pathway_cyber.id,
            title="POPIA Breach Triage & Phishing Log Investigation",
            scenario=(
                "A Sandton digital bank's SOC alerts on a spike in `/api/auth/login` failures followed by "
                "unusual customer profile exports containing South African ID numbers. Under POPIA, you must "
                "parse the authentication logs, identify credential-stuffing IPs, and redact PII before "
                "exporting the incident report."
            ),
            build_prompt=(
                "Write a Python log-triage script that parses JSON auth logs, flags source IPs with >10 failed "
                "logins followed by a 200 OK within 5 minutes, and masks 13-digit SA ID numbers and emails "
                "using SHA-256 or partial redaction for POPIA compliance."
            ),
            explain_prompt=(
                "Explain how your detection threshold distinguishes normal forgotten-password retries from "
                "automated credential stuffing, and why PII masking is mandatory under POPIA Section 19 & 22 "
                "before sharing logs with third-party responders."
            ),
            adapt_prompt=(
                "CHANGE REQUEST: The attacker switches to distributed residential proxies (max 2 requests per IP) "
                "sharing a single custom User-Agent fingerprint and stolen JWT refresh tokens. Adapt your "
                "detection script to correlate by User-Agent/ASN and trigger automated JWT session revocation."
            ),
            passing_score=70,
        )

        challenge_qa = WorkProofChallenge(
            pathway_id=pathway_qa.id,
            title="EFT Payment Gateway Regression & API Test Suite",
            scenario=(
                "A Durban e-commerce platform integrating Instant EFT & PayShap suffered a production bug where "
                "clicking 'Pay Now' twice on a slow 3G connection double-debited customers or accepted negative "
                "ZAR amounts. You must build an automated Pytest regression suite."
            ),
            build_prompt=(
                "Write an automated `pytest` test suite covering `POST /api/v1/payments/eft` for happy-path ZAR "
                "settlement, negative/zero amount rejection, missing reference fields, and duplicate idempotency-key "
                "replay protection. Provide your GitHub repo and test code."
            ),
            explain_prompt=(
                "Explain how you applied Boundary Value Analysis (BVA) and Equivalence Partitioning to select your "
                "test cases, and why mocking external bank webhooks is essential for deterministic tests."
            ),
            adapt_prompt=(
                "CHANGE REQUEST: The engineering team wants your test suite to run on every Pull Request in GitHub "
                "Actions, fail the build if coverage drops below 80%, and automatically quarantine flaky network "
                "tests. Write the GitHub Actions workflow YAML and pytest configuration."
            ),
            passing_score=70,
        )

        challenge_devops = WorkProofChallenge(
            pathway_id=pathway_devops.id,
            title="Containerized Microservice & CI/CD Pipeline Recovery",
            scenario=(
                "A Johannesburg logistics startup deploys its Python tracking API manually via SSH. Image sizes "
                "exceed 1.2GB, containers run as `root`, and whenever a municipal power trip restarts the node, "
                "traffic routes to the container before the database connection pool is ready."
            ),
            build_prompt=(
                "Write a production-grade, multi-stage `Dockerfile` (using a slim/alpine base, non-root user, and "
                "`HEALTHCHECK`) along with a GitHub Actions workflow that lints, tests, and builds the container image."
            ),
            explain_prompt=(
                "Explain why running containers as a non-root user and separating build dependencies from runtime "
                "layers reduces attack surface and speeds up image pulls across South African cloud regions."
            ),
            adapt_prompt=(
                "CHANGE REQUEST: The team is migrating to Kubernetes (EKS/AKS) and experiencing 502 Bad Gateway "
                "errors during deployments. Write a Kubernetes `Deployment` manifest with `readinessProbe`, "
                "`livenessProbe`, resource limits, and a zero-downtime `RollingUpdate` strategy."
            ),
            passing_score=70,
        )

        challenge_mobile = WorkProofChallenge(
            pathway_id=pathway_mobile.id,
            title="Offline-First Spaza Field-Agent Inventory Sync",
            scenario=(
                "Field agents visiting spaza shops in KwaZulu-Natal and Limpopo record stock orders on mobile "
                "devices where cellular connectivity frequently drops between 3G and offline mode. Orders are "
                "currently lost whenever the app closes without signal."
            ),
            build_prompt=(
                "Implement an offline-first synchronization module (JavaScript/TypeScript or Python client logic) "
                "that persists stock orders to a local queue with a client-generated UUID, tracks sync state "
                "(`PENDING`, `SYNCED`, `FAILED`), and flushes queued records when connectivity returns."
            ),
            explain_prompt=(
                "Explain how client-generated UUIDs and idempotency keys prevent duplicate stock orders when "
                "a 2G connection drops mid-flight after the server has already committed the request."
            ),
            adapt_prompt=(
                "CHANGE REQUEST: Two field agents occasionally update the same spaza shop's stock count while "
                "offline, causing last-write-wins data loss, and battery drain is high from constant polling. "
                "Adapt your sync engine to use exponential backoff with jitter and vector/timestamp conflict resolution."
            ),
            passing_score=70,
        )

        challenge_bi = WorkProofChallenge(
            pathway_id=pathway_bi.id,
            title="Credit Risk Cohort & Arrears Warehouse Modelling",
            scenario=(
                "A micro-lender regulated under South Africa's National Credit Act (NCA) needs a monthly vintage "
                "arrears report showing 30-, 60-, and 90-day delinquency rates across provinces and income bands "
                "from raw loan repayment ledger tables."
            ),
            build_prompt=(
                "Write a structured SQL query using Common Table Expressions (CTEs) and Window Functions (`SUM() OVER`, "
                "`ROW_NUMBER()`) that joins `loans`, `repayments`, and `customers` to classify accounts into Current, "
                "30-DPD, 60-DPD, and 90+ DPD arrears buckets per origination month."
            ),
            explain_prompt=(
                "Explain why CTEs and window functions outperform correlated subqueries on multi-million-row ledger "
                "tables, and how you handled customers with zero repayment rows (`LEFT JOIN` + `COALESCE`)."
            ),
            adapt_prompt=(
                "CHANGE REQUEST: Executive dashboards in Power BI are timing out because the query scans 5 years of "
                "historical ledger rows on every refresh. Redesign the target into an incremental Star Schema "
                "(`fact_loan_snapshots` + `dim_customer` SCD Type 2) with partitioning and composite indexes."
            ),
            passing_score=70,
        )

        challenge_frontend = WorkProofChallenge(
            pathway_id=pathway_frontend.id,
            title="Low-Bandwidth Accessible e-Government Portal",
            scenario=(
                "A provincial clinic appointment booking portal suffers a 65% drop-off rate among mobile users on "
                "prepaid data bundles and fails WCAG 2.1 AA accessibility audits for visually impaired citizens "
                "using screen readers."
            ),
            build_prompt=(
                "Build a semantic, accessible appointment booking form component (HTML5 + Vanilla JS/Tailwind) "
                "featuring proper `<label>`, `aria-live` validation error announcements, keyboard focus management, "
                "and South African ID / mobile number client-side validation."
            ),
            explain_prompt=(
                "Explain how your semantic markup, ARIA attributes, and color-contrast choices satisfy WCAG 2.1 AA, "
                "and why avoiding heavy third-party JS bundles is critical for users on costly prepaid mobile data."
            ),
            adapt_prompt=(
                "CHANGE REQUEST: Users frequently lose their form inputs when their browser tab refreshes on low-memory "
                "devices, and clinics require instant switching between English, isiZulu, and Afrikaans labels. "
                "Adapt your component to auto-save draft state in `localStorage` and support dynamic i18n dictionary switching."
            ),
            passing_score=70,
        )

        db.session.add_all(
            [
                challenge_dev,
                challenge_cloud,
                challenge_data,
                challenge_cyber,
                challenge_qa,
                challenge_devops,
                challenge_mobile,
                challenge_bi,
                challenge_frontend,
            ]
        )
        db.session.flush()

        # ---------------------------------------------------------------------
        # 3. Create 8 Demo Candidates + 2 Demo Employers
        # ---------------------------------------------------------------------
        cand_sipho = User(
            email="sipho.dlamini@richfield.ac.za",
            full_name="Sipho Dlamini",
            role="candidate",
            institution="Richfield Graduate Institute of Technology",
            graduation_year=2026,
        )
        cand_sipho.set_password("password123")

        cand_zanele = User(
            email="zanele.khumalo@wits.ac.za",
            full_name="Zanele Khumalo",
            role="candidate",
            institution="University of the Witwatersrand (Wits)",
            graduation_year=2026,
        )
        cand_zanele.set_password("password123")

        cand_thabo = User(
            email="thabo.nkosi@uct.ac.za",
            full_name="Thabo Nkosi",
            role="candidate",
            institution="University of Cape Town (UCT)",
            graduation_year=2026,
        )
        cand_thabo.set_password("password123")

        cand_pieter = User(
            email="pieter.vdm@sun.ac.za",
            full_name="Pieter van der Merwe",
            role="candidate",
            institution="Stellenbosch University",
            graduation_year=2026,
        )
        cand_pieter.set_password("password123")

        cand_ayanda = User(
            email="ayanda.zulu@dut.ac.za",
            full_name="Ayanda Zulu",
            role="candidate",
            institution="Durban University of Technology (DUT)",
            graduation_year=2026,
        )
        cand_ayanda.set_password("password123")

        cand_amahle = User(
            email="amahle.ndlovu@ukzn.ac.za",
            full_name="Amahle Ndlovu",
            role="candidate",
            institution="University of KwaZulu-Natal (UKZN)",
            graduation_year=2026,
        )
        cand_amahle.set_password("password123")

        cand_kabelo = User(
            email="kabelo.mahlangu@uj.ac.za",
            full_name="Kabelo Mahlangu",
            role="candidate",
            institution="University of Johannesburg (UJ)",
            graduation_year=2026,
        )
        cand_kabelo.set_password("password123")

        cand_lerato = User(
            email="lerato.mokoena@tut.ac.za",
            full_name="Lerato Mokoena",
            role="candidate",
            institution="Tshwane University of Technology (TUT)",
            graduation_year=2026,
        )
        cand_lerato.set_password("password123")

        employer_payflow = User(
            email="talent@paystack-sa.co.za",
            full_name="Nomsa Dlamini (Tech Recruiter)",
            role="employer",
            institution="PayFlow FinTech SA",
            graduation_year=None,
        )
        employer_payflow.set_password("password123")

        employer_cloud = User(
            email="careers@cloudsmiths.co.za",
            full_name="Gareth Naidoo (Engineering Manager)",
            role="employer",
            institution="CloudSmiths South Africa",
            graduation_year=None,
        )
        employer_cloud.set_password("password123")

        db.session.add_all(
            [
                cand_sipho,
                cand_zanele,
                cand_thabo,
                cand_pieter,
                cand_ayanda,
                cand_amahle,
                cand_kabelo,
                cand_lerato,
                employer_payflow,
                employer_cloud,
            ]
        )
        db.session.flush()

        # ---------------------------------------------------------------------
        # 4. Seed Submissions & Skills Passports Across the New Pathways
        # ---------------------------------------------------------------------
        now = datetime.now(timezone.utc)

        # --- 1. SIPHO DLAMINI (Level 5 Employer Verified, Score 94/100: Software Dev + DevOps) ---
        sipho_sub_dev = WorkProofSubmission(
            user_id=cand_sipho.id,
            challenge_id=challenge_dev.id,
            build_repo_url="https://github.com/sipho-dlamini/fintech-voucher-service",
            build_code_snippet=(
                "@voucher_bp.route('/api/v1/vouchers/redeem', methods=['POST'])\n"
                "def redeem_voucher():\n"
                "    data = request.get_json(silent=True) or {}\n"
                "    code = str(data.get('voucher_code', '')).strip()\n"
                "    user_id = data.get('user_id')\n"
                "    amount_zar = data.get('amount_zar')\n"
                "    if not code or not user_id or not isinstance(amount_zar, (int, float)) or amount_zar <= 0:\n"
                "        return jsonify({'error': 'Invalid request payload', 'status': 422}), 422\n"
                "    voucher = db.session.query(Voucher).filter_by(code=code).with_for_update().first()\n"
                "    if not voucher:\n"
                "        return jsonify({'error': 'Voucher not found'}), 404\n"
                "    if voucher.status == 'REDEEMED':\n"
                "        return jsonify({'error': 'Voucher already redeemed'}), 409\n"
                "    voucher.status = 'REDEEMED'\n"
                "    voucher.redeemed_by = user_id\n"
                "    db.session.commit()\n"
                "    return jsonify({'status': 'success', 'voucher_code': code, 'amount_zar': amount_zar}), 200"
            ),
            explain_notes=(
                "Used pessimistic row-level locking (`with_for_update`) inside an atomic transaction to guarantee "
                "idempotency under concurrent requests. Returned HTTP 422 for domain validation failures, HTTP 404 "
                "for missing voucher keys, and HTTP 409 Conflict when attempting to re-redeem an exhausted voucher."
            ),
            adapt_solution=(
                "Implemented cursor-based pagination (`WHERE id < :cursor ORDER BY id DESC LIMIT 50`) to eliminate "
                "offset scan overhead on large tables, paired with a Redis sliding-window rate limiter enforcing "
                "60 req/min per `X-API-Key` and returning HTTP 429 with `Retry-After` headers."
            ),
            status="verified",
            evidence_score=94,
            readiness_feedback=(
                "Score Breakdown — Build: 38/40 | Explain: 28/30 | Adapt: 28/30. "
                "Strengths: Production-grade pessimistic locking, clear HTTP status semantics, and Redis rate-limiting. "
                "Readiness Gap: None — endorsed to Trust Level 5 by PayFlow FinTech SA."
            ),
            next_best_action="You have achieved Trust Level 5 (Employer Verified) and been invited to technical interviews.",
            completed_at=now,
        )

        sipho_sub_devops = WorkProofSubmission(
            user_id=cand_sipho.id,
            challenge_id=challenge_devops.id,
            build_repo_url="https://github.com/sipho-dlamini/k8s-tracking-microservice",
            build_code_snippet=(
                "FROM python:3.12-slim AS builder\n"
                "WORKDIR /build\n"
                "COPY requirements.txt .\n"
                "RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt\n\n"
                "FROM python:3.12-slim\n"
                "RUN groupadd -r appgroup && useradd -r -g appgroup appuser\n"
                "WORKDIR /app\n"
                "COPY --from=builder /wheels /wheels\n"
                "RUN pip install --no-cache /wheels/*\n"
                "COPY . .\n"
                "USER appuser\n"
                "EXPOSE 8000\n"
                "HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/healthz || exit 1\n"
                "CMD [\"gunicorn\", \"-b\", \"0.0.0.0:8000\", \"wsgi:app\"]"
            ),
            explain_notes=(
                "Multi-stage builds strip compiler toolchains from the final runtime image, shrinking image size from "
                "1.2GB to 145MB for faster pulls during node recovery. Running as non-root `appuser` prevents host "
                "privilege escalation if the container process is compromised."
            ),
            adapt_solution=(
                "Configured Kubernetes `Deployment` with `readinessProbe` hitting `/healthz/db` so pods only receive "
                "Service traffic once PostgreSQL connections are established, plus `livenessProbe` and `RollingUpdate` "
                "(`maxUnavailable: 0, maxSurge: 1`) for zero-downtime rollouts."
            ),
            status="verified",
            evidence_score=91,
            readiness_feedback=(
                "Score Breakdown — Build: 37/40 | Explain: 27/30 | Adapt: 27/30. "
                "Strengths: Multi-stage non-root Dockerfile and zero-downtime Kubernetes readiness probe design."
            ),
            next_best_action="Cross-functional Backend + DevOps Cloud Native readiness verified.",
            completed_at=now,
        )

        sipho_passport = SkillsPassport(
            user_id=cand_sipho.id,
            readiness_score=94,
            highest_trust_level=5,
            verified_skills_json=json.dumps(
                [
                    {
                        "pathway": "Junior Software Developer",
                        "challenge_title": "RESTful API & Bug Resolution",
                        "score": 94,
                        "trust_level": 5,
                        "skills": [
                            "RESTful API Implementation",
                            "Payload Validation & Error Handling",
                            "Database Concurrency & Idempotency",
                            "Pagination & Rate-Limiting Architecture",
                        ],
                        "verified_at": "2026-10-20",
                    },
                    {
                        "pathway": "Junior DevOps & Cloud Native Engineer",
                        "challenge_title": "Containerized Microservice & CI/CD Pipeline Recovery",
                        "score": 91,
                        "trust_level": 5,
                        "skills": [
                            "Multi-Stage Docker Containerization",
                            "Container Hardening (Non-Root & Minimal Image)",
                            "CI/CD Pipeline Automation",
                            "Kubernetes Probes & Zero-Downtime Rollouts",
                        ],
                        "verified_at": "2026-10-22",
                    },
                ]
            ),
        )

        # --- 2. ZANELE KHUMALO (Level 4 Verified Data Analyst + BI SQL Developer, Score 89/100) ---
        zanele_sub = WorkProofSubmission(
            user_id=cand_zanele.id,
            challenge_id=challenge_data.id,
            build_repo_url="https://github.com/zanele-khumalo/gauteng-retail-kpi-pipeline",
            build_code_snippet=(
                "import pandas as pd\n\n"
                "df = pd.read_csv('pos_transactions.csv')\n"
                "df = df.drop_duplicates(subset=['transaction_id'], keep='first')\n"
                "df['store_region'] = df['store_region'].fillna('UNKNOWN_REGION')\n"
                "df['unit_price'] = df.groupby('category')['unit_price'].transform(\n"
                "    lambda x: x.fillna(x.median())\n"
                ")\n"
                "df['line_total_zar'] = df['quantity'] * df['unit_price']\n"
                "kpi_summary = df.groupby('store_region').agg(\n"
                "    total_revenue=('line_total_zar', 'sum'),\n"
                "    avg_basket=('line_total_zar', 'mean')\n"
                ").reset_index()"
            ),
            explain_notes=(
                "I chose category-level median imputation (`groupby('category')['unit_price'].transform(median)`) "
                "over global mean imputation because retail unit prices are right-skewed by bulk electronics and "
                "appliances. Dropping 8% of rows would systematically understate total provincial revenue KPIs."
            ),
            adapt_solution=(
                "Normalized timestamps to UTC (`pd.to_datetime(df['tx_time'], utc=True)`) and performed a left merge "
                "against `daily_fx_rates` on `(tx_date, currency)` to convert NAD and BWP transactions into ZAR "
                "before running provincial aggregations."
            ),
            status="verified",
            evidence_score=89,
            readiness_feedback=(
                "Score Breakdown — Build: 36/40 | Explain: 27/30 | Adapt: 26/30. "
                "Strengths: Category-grouped median imputation preserves revenue distribution; clean FX join logic."
            ),
            next_best_action="Share your Level 4 Verified Data & BI Passport with retail and banking employers.",
            completed_at=now,
        )

        zanele_sub_bi = WorkProofSubmission(
            user_id=cand_zanele.id,
            challenge_id=challenge_bi.id,
            build_repo_url="https://github.com/zanele-khumalo/nca-credit-arrears-sql",
            build_code_snippet=(
                "WITH loan_repayments AS (\n"
                "    SELECT l.loan_id, l.province, l.origination_month, l.instalment_zar,\n"
                "           COALESCE(SUM(r.paid_zar), 0) AS total_paid_zar,\n"
                "           DATEDIFF(day, MAX(COALESCE(r.payment_date, l.disbursement_date)), CURRENT_DATE) AS days_past_due\n"
                "    FROM loans l\n"
                "    LEFT JOIN repayments r ON l.loan_id = r.loan_id\n"
                "    GROUP BY l.loan_id, l.province, l.origination_month, l.instalment_zar\n"
                ")\n"
                "SELECT origination_month, province,\n"
                "       COUNT(*) AS total_loans,\n"
                "       SUM(CASE WHEN days_past_due BETWEEN 30 AND 59 THEN 1 ELSE 0 END) AS dpd_30_count,\n"
                "       SUM(CASE WHEN days_past_due >= 90 THEN 1 ELSE 0 END) AS npl_90_plus_count\n"
                "FROM loan_repayments\n"
                "GROUP BY origination_month, province;"
            ),
            explain_notes=(
                "Used a CTE with `LEFT JOIN` and `COALESCE` so loans with zero repayments are not silently dropped "
                "from the arrears denominator. Window aggregations avoid repeated table scans across historical cohorts."
            ),
            adapt_solution=(
                "Designed a monthly partitioned `fact_loan_snapshots` table joined to an SCD Type 2 `dim_customer` "
                "dimension with a composite index on `(origination_month, province, arrears_bucket)` for sub-second Power BI queries."
            ),
            status="verified",
            evidence_score=87,
            readiness_feedback=(
                "Score Breakdown — Build: 35/40 | Explain: 26/30 | Adapt: 26/30. "
                "Strengths: Accurate NCA arrears bucketing and star-schema warehouse optimization."
            ),
            next_best_action="Dual Data Analyst + BI SQL Developer verification complete.",
            completed_at=now,
        )

        zanele_passport = SkillsPassport(
            user_id=cand_zanele.id,
            readiness_score=89,
            highest_trust_level=4,
            verified_skills_json=json.dumps(
                [
                    {
                        "pathway": "Junior Data Analyst",
                        "challenge_title": "Retail Sales Data Cleaning & Aggregation",
                        "score": 89,
                        "trust_level": 4,
                        "skills": [
                            "Data Cleaning & Deduplication",
                            "Statistical Missing-Data Imputation",
                            "Provincial KPI Aggregation",
                            "Multi-Currency Normalization",
                        ],
                        "verified_at": "2026-10-21",
                    },
                    {
                        "pathway": "Junior Business Intelligence & SQL Developer",
                        "challenge_title": "Credit Risk Cohort & Arrears Warehouse Modelling",
                        "score": 87,
                        "trust_level": 4,
                        "skills": [
                            "Advanced SQL CTEs & Window Functions",
                            "Star Schema & Warehouse Fact Modelling",
                            "Credit Risk & Arrears Cohort Analytics",
                            "Query Indexing & Partition Optimization",
                        ],
                        "verified_at": "2026-10-23",
                    },
                ]
            ),
        )

        # --- 3. THABO NKOSI (Level 4 Verified Software Developer, Score 86/100) ---
        thabo_sub = WorkProofSubmission(
            user_id=cand_thabo.id,
            challenge_id=challenge_dev.id,
            build_repo_url="https://github.com/thabo-nkosi/path2work-voucher-api",
            build_code_snippet=(
                "@voucher_bp.route('/api/v1/vouchers/redeem', methods=['POST'])\n"
                "def redeem_voucher():\n"
                "    payload = request.get_json(silent=True) or {}\n"
                "    code = payload.get('voucher_code', '').strip()\n"
                "    user_id = payload.get('user_id')\n"
                "    amount_zar = payload.get('amount_zar')\n"
                "    if not code or not user_id or not isinstance(amount_zar, (int, float)) or amount_zar <= 0:\n"
                "        return jsonify({'error': 'Unprocessable Entity: invalid payload fields'}), 422\n"
                "    voucher = Voucher.query.filter_by(code=code).with_for_update().first()\n"
                "    if not voucher:\n"
                "        return jsonify({'error': 'Voucher not found'}), 404\n"
                "    if voucher.is_redeemed:\n"
                "        return jsonify({'error': 'Conflict: Voucher already redeemed'}), 409\n"
                "    voucher.is_redeemed = True\n"
                "    db.session.commit()\n"
                "    return jsonify({'status': 'redeemed', 'voucher_code': code}), 200"
            ),
            explain_notes=(
                "Used `with_for_update()` row-level locking inside the database transaction so concurrent POST "
                "requests with the same `voucher_code` cannot race past the `voucher.is_redeemed` check. Returned "
                "422 for domain validation errors, 404 for unknown codes, and 409 Conflict for duplicate redemptions."
            ),
            adapt_solution=(
                "Replaced offset pagination with keyset cursor pagination (`WHERE id < :cursor ORDER BY id DESC LIMIT 50`) "
                "and added a Redis token-bucket rate limiter keyed by `X-API-Key` (60 requests/min, HTTP 429 response)."
            ),
            status="verified",
            evidence_score=86,
            readiness_feedback=(
                "Score Breakdown — Build: 35/40 | Explain: 26/30 | Adapt: 25/30. "
                "Strengths: Strong command of database concurrency (`with_for_update`) and HTTP status semantics."
            ),
            next_best_action="Share your Level 4 Verified Skills Passport with hiring partners.",
            completed_at=now,
        )

        thabo_passport = SkillsPassport(
            user_id=cand_thabo.id,
            readiness_score=86,
            highest_trust_level=4,
            verified_skills_json=json.dumps(
                [
                    {
                        "pathway": "Junior Software Developer",
                        "challenge_title": "RESTful API & Bug Resolution",
                        "score": 86,
                        "trust_level": 4,
                        "skills": [
                            "RESTful API Implementation",
                            "Payload Validation & Error Handling",
                            "Database Concurrency & Idempotency",
                            "Pagination & Rate-Limiting Architecture",
                        ],
                        "verified_at": "2026-10-19",
                    }
                ]
            ),
        )

        # --- 4. PIETER VAN DER MERWE (Level 4 Verified Cybersecurity & Cloud, Score 84/100) ---
        pieter_sub_cyber = WorkProofSubmission(
            user_id=cand_pieter.id,
            challenge_id=challenge_cyber.id,
            build_repo_url="https://github.com/pieter-vdm/popia-soc-log-triage",
            build_code_snippet=(
                "import json, re, hashlib\n"
                "from collections import defaultdict\n\n"
                "SA_ID_REGEX = re.compile(r'\\b\\d{13}\\b')\n"
                "failed_by_ip = defaultdict(int)\n\n"
                "def mask_popia_pii(raw_text: str) -> str:\n"
                "    return SA_ID_REGEX.sub(lambda m: 'SAID-SHA256-' + hashlib.sha256(m.group(0).encode()).hexdigest()[:10], raw_text)\n\n"
                "def triage_log_line(line: str):\n"
                "    event = json.loads(mask_popia_pii(line))\n"
                "    ip = event.get('src_ip')\n"
                "    if event.get('status') == 401:\n"
                "        failed_by_ip[ip] += 1\n"
                "    elif event.get('status') == 200 and failed_by_ip[ip] >= 10:\n"
                "        return {'alert': 'CREDENTIAL_STUFFING_BREACH', 'src_ip': ip, 'failures': failed_by_ip[ip]}"
            ),
            explain_notes=(
                "Correlating >=10 HTTP 401 failures followed by a 200 OK isolates successful credential-stuffing "
                "breaches from normal user typos. Hashing 13-digit SA ID numbers with SHA-256 before writing to SIEM "
                "storage satisfies POPIA Section 19 de-identification requirements while preserving correlation tokens."
            ),
            adapt_solution=(
                "Grouped events by `(user_agent_hash, asn_number)` inside a 10-minute sliding window to catch "
                "low-and-slow proxy rotation, and added an automated webhook call to revoke active JWT refresh tokens "
                "in Redis and quarantine the affected account."
            ),
            status="verified",
            evidence_score=84,
            readiness_feedback=(
                "Score Breakdown — Build: 34/40 | Explain: 25/30 | Adapt: 25/30. "
                "Strengths: POPIA-compliant SHA-256 SA ID masking and proxy-rotation ASN correlation."
            ),
            next_best_action="Your Level 4 Cybersecurity & SOC Analyst Passport is verified.",
            completed_at=now,
        )

        pieter_passport = SkillsPassport(
            user_id=cand_pieter.id,
            readiness_score=84,
            highest_trust_level=4,
            verified_skills_json=json.dumps(
                [
                    {
                        "pathway": "Junior Cybersecurity & SOC Analyst",
                        "challenge_title": "POPIA Breach Triage & Phishing Log Investigation",
                        "score": 84,
                        "trust_level": 4,
                        "skills": [
                            "SIEM Log Parsing & Threat Triage",
                            "POPIA PII Masking & Compliance",
                            "Brute-Force & Credential Stuffing Detection",
                            "Automated Incident Containment",
                        ],
                        "verified_at": "2026-10-18",
                    }
                ]
            ),
        )

        # --- 5. AYANDA ZULU (Level 4 Verified Mobile Developer & QA Automation, Score 81/100) ---
        ayanda_sub_mobile = WorkProofSubmission(
            user_id=cand_ayanda.id,
            challenge_id=challenge_mobile.id,
            build_repo_url="https://github.com/ayanda-zulu/spaza-offline-sync-engine",
            build_code_snippet=(
                "async function enqueueOrder(orderPayload) {\n"
                "  const record = {\n"
                "    idempotency_uuid: crypto.randomUUID(),\n"
                "    shop_id: orderPayload.shop_id,\n"
                "    items: orderPayload.items,\n"
                "    updated_at: new Date().toISOString(),\n"
                "    status: 'PENDING'\n"
                "  };\n"
                "  await sqliteDb.run('INSERT INTO sync_queue VALUES (?, ?, ?, ?)', [\n"
                "    record.idempotency_uuid, JSON.stringify(record), record.status, record.updated_at\n"
                "  ]);\n"
                "  return record;\n"
                "}\n\n"
                "async function flushSyncQueue() {\n"
                "  const pending = await sqliteDb.all(\"SELECT * FROM sync_queue WHERE status = 'PENDING'\");\n"
                "  for (const row of pending) {\n"
                "    const res = await fetch('/api/v1/orders/sync', {\n"
                "      method: 'POST',\n"
                "      headers: {'Idempotency-Key': row.idempotency_uuid, 'Content-Type': 'application/json'},\n"
                "      body: row.payload\n"
                "    });\n"
                "    if (res.ok) await sqliteDb.run(\"UPDATE sync_queue SET status = 'SYNCED' WHERE id = ?\", [row.idempotency_uuid]);\n"
                "  }\n"
                "}"
            ),
            explain_notes=(
                "Persisting orders locally to SQLite with a client-generated `idempotency_uuid` ensures zero data loss "
                "when KZN field agents lose 3G signal. If the connection drops after the server commits, replaying the "
                "same `Idempotency-Key` returns the cached 200 OK instead of duplicating the spaza stock order."
            ),
            adapt_solution=(
                "Added exponential backoff with random jitter (`min(60000, (2 ** attempt) * 1000 + Math.random() * 500)`) "
                "and gzip delta batching to save battery and data on 2G/3G, plus per-field HLC timestamp conflict resolution."
            ),
            status="verified",
            evidence_score=81,
            readiness_feedback=(
                "Score Breakdown — Build: 33/40 | Explain: 24/30 | Adapt: 24/30. "
                "Strengths: Resilient SQLite offline queue with UUID idempotency and exponential backoff."
            ),
            next_best_action="Your Level 4 Mobile App Developer Passport is ready for employer inspection.",
            completed_at=now,
        )

        ayanda_passport = SkillsPassport(
            user_id=cand_ayanda.id,
            readiness_score=81,
            highest_trust_level=4,
            verified_skills_json=json.dumps(
                [
                    {
                        "pathway": "Junior Mobile App Developer",
                        "challenge_title": "Offline-First Spaza Field-Agent Inventory Sync",
                        "score": 81,
                        "trust_level": 4,
                        "skills": [
                            "Offline-First Local Persistence",
                            "Idempotent Background Sync Queues",
                            "Timestamp & Version Conflict Resolution",
                            "Low-Bandwidth Exponential Backoff",
                        ],
                        "verified_at": "2026-10-17",
                    }
                ]
            ),
        )

        # --- 6. AMAHLE NDLOVU (Level 3 Source Verified QA Engineer, Score 65/100) ---
        amahle_sub = WorkProofSubmission(
            user_id=cand_amahle.id,
            challenge_id=challenge_qa.id,
            build_repo_url="https://github.com/amahle-ndlovu/payshap-eft-pytest-suite",
            build_code_snippet=(
                "import pytest\n\n"
                "@pytest.mark.parametrize('amount_zar,expected_status', [\n"
                "    (150.00, 200),\n"
                "    (0.00, 400),\n"
                "    (-50.00, 400),\n"
                "])\n"
                "def test_eft_payment_boundaries(client, amount_zar, expected_status):\n"
                "    res = client.post('/api/v1/payments/eft', json={'amount_zar': amount_zar, 'ref': 'INV-01'})\n"
                "    assert res.status_code == expected_status"
            ),
            explain_notes=(
                "Used `@pytest.mark.parametrize` to test boundary values around 0.00 ZAR and negative amounts so "
                "invalid EFT debits are rejected with HTTP 400."
            ),
            adapt_solution=(
                "I would add a GitHub Actions workflow file that runs pytest on every push and checks coverage."
            ),
            status="submitted",
            evidence_score=65,
            readiness_feedback=(
                "Score Breakdown — Build: 29/40 | Explain: 18/30 | Adapt: 18/30. "
                "Strengths: Clean parameterized boundary test cases and `.ac.za` source verification (Level 3). "
                "Readiness Gap: Add explicit duplicate idempotency-key replay assertions and full GitHub Actions YAML."
            ),
            next_best_action=(
                "You scored 65/100 (5 pts away from Level 4 verification). Expand your Adapt CI workflow YAML and re-submit!"
            ),
            completed_at=now,
        )

        amahle_passport = SkillsPassport(
            user_id=cand_amahle.id,
            readiness_score=65,
            highest_trust_level=3,
            verified_skills_json=json.dumps([]),
        )

        # --- 7. KABELO MAHLANGU (Level 2 Evidence Attached Frontend UI/UX, Score 54/100) ---
        kabelo_sub = WorkProofSubmission(
            user_id=cand_kabelo.id,
            challenge_id=challenge_frontend.id,
            build_repo_url="https://github.com/kabelo-m/clinic-booking-ui",
            build_code_snippet=(
                "<form aria-label='Clinic Appointment Booking'>\n"
                "  <label for='sa_id'>South African ID Number</label>\n"
                "  <input id='sa_id' name='sa_id' required pattern='\\d{13}' aria-describedby='id_err' />\n"
                "  <span id='id_err' aria-live='polite'></span>\n"
                "  <button type='submit'>Book Clinic Slot</button>\n"
                "</form>"
            ),
            explain_notes="Added labels and aria-live so screen readers announce validation errors.",
            adapt_solution="Save form fields in localStorage so users do not lose data on refresh.",
            status="submitted",
            evidence_score=54,
            readiness_feedback=(
                "Score Breakdown — Build: 24/40 | Explain: 15/30 | Adapt: 15/30. "
                "Strengths: Semantic HTML form with `aria-live` region attached (Level 2). "
                "Readiness Gap: Include JS SA ID validation logic and isiZulu/Afrikaans i18n switcher code."
            ),
            next_best_action="Add the JavaScript `localStorage` persistence and i18n dictionary code to pass 70/100.",
            completed_at=now,
        )

        kabelo_passport = SkillsPassport(
            user_id=cand_kabelo.id,
            readiness_score=54,
            highest_trust_level=2,
            verified_skills_json=json.dumps([]),
        )

        # --- 8. LERATO MOKOENA (Level 1 Self-Declared, Score 20/100 - Fresh Account) ---
        lerato_passport = SkillsPassport(
            user_id=cand_lerato.id,
            readiness_score=20,
            highest_trust_level=1,
            verified_skills_json=json.dumps([]),
        )

        # ---------------------------------------------------------------------
        # 5. Seed Employer Shortlist Entries
        # ---------------------------------------------------------------------
        shortlist_1 = EmployerShortlist(
            employer_id=employer_payflow.id,
            candidate_id=cand_sipho.id,
            notes="Endorsed to Trust Level 5! Verified across both Backend Software Dev (94%) and Cloud Native DevOps (91%).",
            status="invited",
        )
        shortlist_2 = EmployerShortlist(
            employer_id=employer_payflow.id,
            candidate_id=cand_zanele.id,
            notes="Top Data & BI SQL candidate — verified on both Retail Data Cleaning (89%) and NCA Credit Arrears SQL (87%).",
            status="shortlisted",
        )
        shortlist_3 = EmployerShortlist(
            employer_id=employer_payflow.id,
            candidate_id=cand_pieter.id,
            notes="Strong POPIA log triage and SHA-256 PII masking for our FinTech SOC team.",
            status="shortlisted",
        )

        db.session.add_all(
            [
                sipho_sub_dev,
                sipho_sub_devops,
                sipho_passport,
                zanele_sub,
                zanele_sub_bi,
                zanele_passport,
                thabo_sub,
                thabo_passport,
                pieter_sub_cyber,
                pieter_passport,
                ayanda_sub_mobile,
                ayanda_passport,
                amahle_sub,
                amahle_passport,
                kabelo_sub,
                kabelo_passport,
                lerato_passport,
                shortlist_1,
                shortlist_2,
                shortlist_3,
            ]
        )
        db.session.commit()

        print("=========================================================================")
        print("Path2Work Seeded with 9 South African IT Pathways & 10 Demo Accounts!")
        print("-------------------------------------------------------------------------")
        print("9 PATHWAYS:")
        print("1. Junior Software Developer (26%)")
        print("2. IT Support / Cloud (18%)")
        print("3. Junior Data Analyst (12%)")
        print("4. Junior Cybersecurity & SOC Analyst (11%)")
        print("5. Junior QA & Test Automation Engineer (9%)")
        print("6. Junior DevOps & Cloud Native Engineer (8%)")
        print("7. Junior Mobile App Developer (7%)")
        print("8. Junior Business Intelligence & SQL Developer (5%)")
        print("9. Junior UI/UX & Frontend Engineer (4%)")
        print("=========================================================================")


if __name__ == "__main__":
    seed_database()