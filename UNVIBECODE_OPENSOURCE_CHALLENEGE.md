# 🏆 UnvibeCode Engineering Challenge 2026

## Hosted by Alphashots.ai

**Unvibe complex code. Trace business workflows.**

Install UnvibeCode, run it on a real open-source repository, explore how the code connects, review a prebuilt business workflow, and make a useful GitHub contribution.

👉 **[VIEW UNVIBECODE ON GITHUB](https://github.com/FinanceFlash/unvibecode)**

⭐ Like the project? Click **Star** in the top-right corner of the GitHub repository to support UnvibeCode and follow future updates. Starring is optional and does not affect judging.

- **Registration opens:** 10 August 2026 
- **Submission deadline:** 31 August 2026 (No registartion, you can submit directly)
- **Results announced:** 7 September 2026

## Who can participate?

- Engineering students
- Techie searching for job
- Software engineers
- Participate individually or as a team

---

# ✅ What You Must Submit

Every participant or team must complete **three submissions**:

| Submission | What you do | Where you submit it |
| --- | --- | --- |
| **1. Repository Analysis** | Run UnvibeCode on an open-source repository and review the results | Google Form |
| **2. Prebuilt Workflow Feedback** | Review one prebuilt workflow and share what was useful, unclear, or missing | The same Google Form |
| **3. GitHub Contribution** | Choose Track A, B, or C and submit a GitHub Issue or Pull Request | GitHub first, then add its link to the same Google Form |

Only **one Google Form** is required. It collects all three submissions.

For Submission 3, you must submit at least one contribution. You may submit a second contribution if you want. Each contribution must use a separate GitHub Issue or Pull Request.

---

# 🔍 Submission 1: Analyze an Open-Source Repository

## Step 1: Install UnvibeCode

```bash
pip install unvibecode
```

## Step 2: Choose a repository

You can:

- Use your own open GitHub repository, or
- Download any publicly available open-source repository from GitHub

UnvibeCode currently works best with Python, JavaScript, TypeScript, Rust, PHP, Ruby, HTML and CSS repositories.

## Step 3: Run UnvibeCode

```bash
python -m unvibecode review --repository "/path/to/repository"
```

Windows example:

```powershell
python -m unvibecode review --repository "D:\your-repository"
```

No activation key or OpenAI API key is required.

For installation help and examples, read the [UnvibeCode README](https://github.com/FinanceFlash/unvibecode).

## Step 4: Explore the results

### Small and medium repositories

You normally receive four outputs:

1. **Connected Code Map**

   See how files, functions, imports and calls connect. Click a file to explore and download its connected code for an LLM.

2. **Complete Repository Context**

   Get a ZIP containing organized code chunks and connections that can be used with an LLM.

3. **Business Workflow Map**

   See how the code performs workflows such as registration, payments, booking, approvals or notifications.

4. **Business Risk Findings**

   Review important workflow risks, supporting code evidence, possible business impact and suggested improvements.

### Very large repositories

Repositories above approximately two million source-code tokens receive:

- Connected Code Map
- Complete Repository Context

The Business Workflow Map and Business Risk Findings may not be generated for very large repositories.

Receiving these two outputs for a very large repository is still a valid submission.

## Step 5: Submit your analysis feedback

The Google Form will ask:

- Which repository and programming language you analyzed
- Which UnvibeCode version you used
- Whether installation and analysis completed
- How long the analysis took
- Which outputs were generated
- How useful each output was
- Which output was most useful
- Whether UnvibeCode helped you understand something you had missed
- Whether you would use or recommend UnvibeCode again

Positive and negative feedback are treated equally while judging.

⭐ Did UnvibeCode help you understand the repository? Consider giving the [GitHub project a Star](https://github.com/FinanceFlash/unvibecode) and sharing it with another developer who may find it useful.

---

# 🧭 Submission 2: Review One Prebuilt Workflow

Visit the [UnvibeCode Prebuilt Workflow Collection](https://github.com/FinanceFlash/unvibecode/tree/main/prebuilt-workflow-paths).

## Step 1: Choose a workflow

Choose one workflow that is related to the repository you analyzed or to a software product you understand.

You can use the [Checkout Payment Workflow](https://github.com/FinanceFlash/unvibecode/tree/main/prebuilt-workflow-paths/checkout-payment-authorization-and-capture) as a complete example.

## Step 2: Open the workflow files

Inside the workflow folder:

1. Open `README.md` to understand where the workflow starts, where it ends, and what is included or excluded.
2. Open `PRODUCT_AND_BUSINESS_GUIDE.md` and review these exact sections:

   - `People and systems`
   - `Things created or changed`
   - `Stages`
   - `Happy paths`
   - `Negative paths`
   - `Edge cases`
   - `Acceptance criteria`
   - `Business risks`

3. Open `CORE_20_SCENARIOS.md` to review its 20 important scenarios and what `Must not happen`.
4. Open `TESTING_GUIDE.md` if you want the complete Given, When, Expect, and Must not happen details.
5. You may also review the permission, abuse, retry and recovery guides.

## Step 3: Submit your workflow feedback

The Google Form will ask:

- Which workflow you reviewed
- Whether `People and systems` were clear
- Whether `Things created or changed` were clear
- Whether the workflow `Stages` were clear
- Whether the 20 core scenarios were useful
- Whether testing, retry, recovery and permission guidance was useful
- Whether an important scenario was missing
- Whether you would use the workflow while developing or testing software
- What was unclear or could be improved

---

# 🛠️ Submission 3: Make a GitHub Contribution

Choose at least one of the following tracks. You may submit a second contribution under the same or a different track.

## Track A: Suggest a New Business Risk

Open a GitHub Issue suggesting a business risk or workflow problem that UnvibeCode should detect.

Examples:

- A payment is processed twice after a retry
- A user receives access before payment is confirmed
- A cancelled booking does not release capacity
- Browser information is trusted without checking it on the server

### How to submit Track A

Open a [new GitHub Issue](https://github.com/FinanceFlash/unvibecode/issues/new).

Use this title format:

```text
[Challenge 2026][Track A] Short name of your idea
```

Example:

```text
[Challenge 2026][Track A] Detect duplicate payment after a lost response
```

Include:

```markdown
## Problem

What can go wrong?

## Where it happens

What type of code or workflow may contain this problem?

## Why it matters

How could it affect users, developers or the business?

## Suggested check

What should UnvibeCode look for?

## Example

Add a simple example or public repository if available.
```

Track A requires a GitHub Issue. It does not require a Pull Request.

---

## Track B: Improve a Prebuilt Workflow

You can:

- Improve an unclear scenario
- Replace a repeated or weak scenario
- Add a missing failure, permission, retry or recovery situation
- Improve a workflow guide
- Create a new workflow that is not already available

Every workflow must contain exactly **20 core scenarios**.

If you add a missing scenario to an existing workflow, replace or combine another scenario so that the total remains 20.

Read the [workflow contribution rules](https://github.com/FinanceFlash/unvibecode/blob/main/.github/CONTRIBUTING.md#contributing-a-pre-built-workflow-pack) before making your change.

### MECE made simple

MECE means:

- Do not repeat the same situation using different words.
- Cover the important ways the workflow can succeed, fail or recover.

For a new workflow:

1. Define where the workflow starts and ends in `README.md`.
2. State what is included and excluded.
3. List the `People and systems`.
4. List the `Things created or changed`.
5. Define the possible `Stages`.
6. Write exactly 20 different core scenarios.
7. State what `Must not happen` for every scenario.
8. Cover success, invalid input, denied actions, timing, simultaneous actions, permissions, external failures, partial completion, retry and recovery where relevant.
9. Use the same names in every file.
10. Check that another workflow pack does not already cover the same workflow.

Use an existing complete workflow pack as your starting structure. A new pack must contain all 13 files listed in the [contribution guide](https://github.com/FinanceFlash/unvibecode/blob/main/.github/CONTRIBUTING.md#contributing-a-pre-built-workflow-pack).

### Track B Pull Request example

```text
[Challenge 2026][Track B] Improve payment lost-response recovery
```

Example description:

```markdown
## Problem

The checkout payment workflow did not clearly explain recovery when payment succeeds but the provider response is lost.

## What I changed

- Improved the lost-response scenario
- Added a reconciliation step
- Updated retry guidance
- Kept exactly 20 core scenarios

## Files changed

- CORE_20_SCENARIOS.md
- TESTING_GUIDE.md
- RETRY_AND_RECOVERY_GUIDE.md

## Checked

- People and systems use the same names
- Things created or changed use the same names
- Stages use the same names
- Every scenario says what Must not happen
- GitHub Quality Checks passed
```

---

## Track C: Improve the Repository

Make a real improvement that helps developers use or understand UnvibeCode.

Examples:

- Improve installation instructions
- Fix broken or confusing documentation
- Add a useful example
- Improve automated tests
- Improve GitHub Actions
- Improve accessibility or navigation
- Improve explanations of the reports

The public repository currently contains documentation, prebuilt workflows and repository-quality tests. Do not submit analyzer or CLI source changes because that source is not part of this repository.

An idea without a repository change should be submitted under Track A. Track C must contain an actual improvement.

### Track C Pull Request example

```text
[Challenge 2026][Track C] Add clearer Windows installation help
```

Example description:

```markdown
## Problem

Windows users may not know what to do when the `python` command is unavailable.

## What I changed

- Added a `py -m pip` example
- Added a short Python PATH explanation
- Added a troubleshooting link

## Files changed

- docs/QUICKSTART.md
- docs/TROUBLESHOOTING.md

## Checked

- Commands are correct
- Markdown links work
- GitHub Quality Checks passed
```

---

# 🔀 How to Submit a Track B or Track C Pull Request

## Step 1: Fork the repository

Open [FinanceFlash/unvibecode](https://github.com/FinanceFlash/unvibecode) and click **Fork**.

## Step 2: Create a branch in your fork

Track B example:

```text
challenge/your-name-track-b
```

Track C example:

```text
challenge/your-name-track-c
```

## Step 3: Make one focused change

Do not combine unrelated changes in one Pull Request.

## Step 4: Commit the change to your branch

Use a short message explaining what you changed.

## Step 5: Open the Pull Request

Open the Pull Request from your branch to:

```text
FinanceFlash/unvibecode → main
```

## Step 6: Wait for Quality Checks

GitHub automatically checks the files, links and workflow structure.

If a check fails, open it, read the reported problem, update your branch, and wait for the check to run again.

---

# 📤 Submit All Three Parts

Complete one Google Form after finishing:

1. Repository Analysis
2. Prebuilt Workflow Feedback
3. GitHub Contribution

👉 **[SUBMIT THROUGH THE GOOGLE FORM](https://docs.google.com/forms/d/e/1FAIpQLSfUUzk9zxbmrERW_ymxdV0ViyCGYaHmF4dFo5VAEiXvXSA1dQ/viewform?usp=sharing&ouid=106408874025328506622)**

The form will ask for:

- Your name or team name
- Email address
- GitHub profile
- Repository analyzed
- UnvibeCode analysis feedback
- Prebuilt workflow feedback
- Your first GitHub Issue or Pull Request link
- Your optional second contribution link
- One final open-ended improvement comment

You do not need to create a `submissions/your-name/` folder in the repository.

---

# ✅ Submission Rules

- All three submissions are required.
- Submission 1 and Submission 2 are completed inside the Google Form.
- Submission 3 requires at least one GitHub Issue or Pull Request.
- Track A must be submitted as a GitHub Issue.
- Tracks B and C must be submitted as Pull Requests.
- Submit only one contribution in each Issue or Pull Request.
- You may submit one optional second contribution using a separate Issue or Pull Request.
- Use the required title format.
- Keep every contribution focused on one problem.
- For Track B, keep exactly 20 core scenarios.
- Wait for GitHub Quality Checks to pass.
- Do not upload passwords, API keys, access tokens, private source code, customer information or generated reports containing source code.
- Pull Request contributions will use the repository's [Apache License 2.0](https://github.com/FinanceFlash/unvibecode/blob/main/LICENSE).
- Incomplete, copied or unrelated submissions may be rejected.
- The organizers' decision on the final rankings will be final.

---

# 🎁 Prizes and Career Rewards

## 💰 Cash Prizes

- 🥇 **1st Place:** **₹5,000 / Cash Equivalent** + Named as a **Core Project Maintainer** on GitHub.
- 🥈 **2nd Place:** **₹3,000 / Cash Equivalent** + Featured Open-Source Contributor badge.
- 🥉 **3rd Place:** **₹2,000 / Cash Equivalent** + Featured Open-Source Contributor badge.

## 💼 Career and CV-Boosting Rewards

- 🚀 **Top 10 Ranks:** Personalized **LinkedIn Recommendations** from our founding team to boost your profile visibility to top-tier recruiters.
- 📈 **Top 50 Ranks:** Official **Certificate of Open-Source Contribution** signed by the Alphashots.ai founding team, plus your code permanently merged into the main production repository.
- ⚡ **Scale-Up Bonus:** If student participation crosses milestone thresholds, we will unlock **exclusive resume review sessions** and **mock technical interview slots** with industry veterans for top participants.

---

# 📏 How Submissions Will Be Scored

| Area | Points |
| --- | ---: |
| Repository analysis and understanding | 25 |
| Quality and honesty of UnvibeCode feedback | 15 |
| Prebuilt workflow review | 20 |
| Usefulness of the GitHub contribution | 30 |
| Clarity and completeness | 10 |
| **Total** | **100** |

Large repositories do not automatically receive more points. We care more about what you understood, what you observed and what you contributed.

---

# 🏢 About Us

Alphashots.ai is a pre-seed funded AI Fintech startup building opensource tools for developer productivity, code understanding and advanced analytics.

- **Divya — IIM L** Leading strategy, product architecture and growth.
- **Suresh Rajendran -IIT G** Leading technical architecture, engineering pipelines and LLM infrastructure.

Ready to unvibe some code?

👉 **[VISIT UNVIBECODE ON GITHUB](https://github.com/FinanceFlash/unvibecode)**
