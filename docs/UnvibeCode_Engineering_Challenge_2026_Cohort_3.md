# 🏆 UnvibeCode Engineering Challenge 2026 — Cohort 3

## Find a real engineering issue. Or solve a real developer-adoption problem.

**Submission deadline: 15 November 2026 (11:59 PM IST)**  
**Results announced: 23 November 2026**  
**Format:** Individual participation · Choose Track 1, Track 2, or both  
**For:** Engineering students, MCA/BCA students, freshers, job seekers, and early-career developers

Want to demonstrate skills beyond certificates and classroom projects? Cohort 3 challenges you to examine an actual developer tool and produce work that can inform real engineering or product decisions.

**Both tracks require you to install and run UnvibeCode on a real public repository, then complete the Google submission form.** Only Track 1 requires a GitHub issue.

## 🚀 Start here — common to both tracks

1. ⭐ **[Star the UnvibeCode GitHub repository](https://github.com/FinanceFlash/unvibecode)** to save it and find the installation instructions, issue tracker, and challenge resources again.
2. Install the tool:

   ```bash
   python -m pip install --upgrade unvibecode
   ```

3. Download or clone a public GitHub repository (or use your own public repository). For example, [Flask](https://github.com/pallets/flask).
4. Run UnvibeCode against the local repository folder:

   ```bash
   python -m unvibecode review --repository "/path/to/repository"
   ```

   Windows example:

   ```powershell
   python -m unvibecode review --repository "D:\flask"
   ```

5. Review the **Business Workflow Map**, **Connected Code Map**, **Business Risk Findings**, and **Complete Repository Context** where available. Verify important claims against the source code rather than assuming the output is always correct.
6. Choose one or both tracks and **submit your response through the Google form by 15 November 2026**.

**Submission form:** [Google Form — challenge entry](https://docs.google.com/forms/d/1an-hce3EQ8bUVArnZJnD1VwxQIxgmNzLKYQ8h814CVE/viewform)  
*Organizers: Confirm that the Cohort 3 form is accepting responses and collects the required fields for both tracks before sharing it with participants.*

---

# 🔧 Track 1 — Engineering Issue Investigation

### Problem statement

Find **one original, non-duplicate, technically meaningful issue** in UnvibeCode by using it on a real repository. Investigate its cause or boundaries, gather reproducible evidence, and submit it as a well-structured GitHub issue.

You can investigate incorrect code relationships, missing or misleading workflow links, unsupported claims in risk findings, inaccurate or missing context, runtime failures, platform-specific problems, or a specific engineering usability defect.

**Depth matters more than issue count.** One thoroughly investigated, reproducible, high-impact issue can make a stronger case for **internship selection or a cash prize** than several superficial reports. Finding a genuine defect is not the same as merely requesting a new feature.

### Before you file

- Search [open and closed UnvibeCode issues](https://github.com/FinanceFlash/unvibecode/issues) and check whether the same underlying problem has already been reported. Do not submit duplicate issues with slightly different wording.
- Verify expected behavior against the repository's actual source code or reliable product behavior.
- Re-run the case where possible. Differentiate a repeatable defect from a hypothesis or misunderstanding.
- Pick one well-scoped issue; do not bundle unrelated bugs together.
- Remove private repository content, credentials, tokens, customer data, and other secrets from evidence.

### Required GitHub issue format

Create your issue at [UnvibeCode Issues → New issue](https://github.com/FinanceFlash/unvibecode/issues/new) using this template:

```markdown
Title: [Bug] <component> — <specific observable failure>

## 1. Problem summary
What is wrong, and why does it matter to a developer?

## 2. Test environment
- UnvibeCode version:
- Operating system / Python version:
- Public repository URL and commit or release:
- Relevant command:

## 3. Steps to reproduce
1. <Exact preparation step>
2. <Exact command or user action>
3. <Where to inspect the result>

## 4. Expected behavior
What should happen? Point to supporting source code or an explicit product expectation.

## 5. Actual behavior
What happened instead? Include the exact error or incorrectly generated result.

## 6. Evidence
- Relevant file/function names and line numbers:
- Small sanitized log excerpt, output excerpt, or screenshot:
- Source-code comparison supporting the finding:

## 7. Impact and scope
Who is affected? Is this a wrong answer, missing context, crash, or usability problem?
Does it occur on one repository or multiple tested cases?

## 8. Suspected cause / suggested fix (if known)
Explain your hypothesis and how an engineer could validate it.
If not known, write "Not yet identified" rather than guessing.

## 9. Duplicate check
Links to the closest existing issues checked, and why this is distinct.
```

**Reproduction quality:** Another engineer should be able to follow the steps, observe the same outcome, and understand the expected-versus-actual difference without asking you to explain the report. If your finding is non-deterministic, say how often it occurs and under which conditions.

**Track 1 deliverable:** Submit **one non-duplicate GitHub issue** and paste its URL, the analyzed repository URL, and a short summary into the Google form. **Do not submit a pull request** for this challenge.

### Track 1 judging — 100 points

| Criterion | Points |
|---|---:|
| Technical depth, root-cause investigation, and reasoning | 35 |
| Reproducibility and strength of evidence | 30 |
| Real developer impact and usefulness | 20 |
| Originality / verified non-duplicate scope | 10 |
| Clarity of issue report | 5 |

---

# 💡 Track 2 — Developer Adoption & Repeat-Usage Challenge

### Problem statement

**UnvibeCode has been used by 1,000+ developers.** Initial interest is encouraging, but **daily adoption and repeat usage are weaker than first-time usage**. One potential reason is that UnvibeCode is not yet readily accessible through enough of the channels and formats developers use in their everyday workflows.

Integrating UnvibeCode as an **MCP tool** inside ChatGPT, Claude, Cursor, or similar assistants could improve access. However, that alone is **not an attractive standalone solution for this challenge**: MCP interactions can feel seamless and invisible, so users may benefit from UnvibeCode without remembering its name or deliberately returning to it.

**Your challenge:** How would you make UnvibeCode **easy to access, useful during daily development, and memorable as a product**, without relying solely on invisible MCP integrations?

Think beyond acquiring more first-time users. The goal is to create a practical reason for developers to return and use it again in real engineering work.

### What to submit — short written proposal

In the Google form, provide:

1. **Your recommended approach:** State the delivery channel, product format, feature, or workflow you would introduce to drive repeat usage.
2. **2–3 supporting points:** Explain *why* your approach would fit into a developer's daily routine, reduce friction, and preserve visible UnvibeCode brand recognition. Use reasoned arguments, concrete examples, or evidence from your own trial.
3. **Implementation plan (2–3 lines):** Describe what you would build first, where it would integrate, and how you would test whether developers repeatedly use it.

Focus on **one strong approach or a tightly connected set of methods**, not a long list of generic growth tactics. Consider the developer's trigger to use the product, how quickly they can access value, and why they would return tomorrow or next week.

**Track 2 deliverable:** Paste the write-up **directly into the Google form**. **No GitHub issue, public social post, video, or pull request is required.** You must still install and try UnvibeCode before proposing your solution.

### Track 2 judging — 100 points

| Criterion | Points |
|---|---:|
| Likelihood of driving real repeat usage | 35 |
| Fit with everyday developer workflows and ease of access | 25 |
| Feasibility and specificity of implementation | 20 |
| Visible product recall / brand attribution | 10 |
| Original reasoning and clear supporting points | 10 |

---

# 🎁 Internship and Challenge Rewards

### Paid AI Engineering Internship — Alphashots.AI

This challenge is a **primary evaluation input** for selecting candidates for our technical internship, which starts in the **third week of November 2026**.

- **Open positions:** 1–2
- **Duration:** 1 month
- **Time commitment:** 3–5 hours per week
- **Mode:** Remote, flexible
- **Stipend:** **₹25,000–₹30,000 fixed per month**
- **Work:** Python open-source engineering, MCP development, OpenCode integration, LLM workflows, AI context optimization, and code intelligence

High-quality work in **either track** can strengthen your candidacy. Particularly detailed Track 1 investigations are valuable evidence of technical engineering ability; Track 2 proposals are assessed for practical product and implementation reasoning. Shortlisted candidates may be invited to a technical interview. Selection is not automatic.

### Additional rewards

- **₹10,000 total cash prize pool** shared equally among **4 winners** (2 from each track, subject to valid entries).
- **Top 10:** Personalized recommendation letters, based on demonstrated work.
- **Top 50:** Challenge achievement certificates.
- **First 100 eligible completers:** AI System Design Interview Preparation Pack.

Entries must be complete, original, and valid. Rankings, prizes, and recognition are determined from submission quality, not GitHub stars or social-media popularity.

---

# 📤 Submission Checklist

| Requirement | Track 1 | Track 2 |
|---|---|---|
| Install and run UnvibeCode | Required | Required |
| Analyze a real public repository | Required | Required |
| Submit a new, non-duplicate GitHub issue | **Required** | **Not required** |
| Include exact reproduction and expected/actual results | **Required** | Not required |
| Submit a 2–3-point adoption rationale and 2–3-line implementation plan | Not required | **Required** |
| Fill the Google form | **Required** | **Required** |

**Submission deadline: 15 November 2026, 11:59 PM IST. Results announced: 23 November 2026.** You can enter either track or both. If entering both, supply both deliverables through the form.

⭐ **[Star UnvibeCode on GitHub](https://github.com/FinanceFlash/unvibecode)** if you want to keep the repository in your saved projects and find future challenge updates, results, and certificate announcements easily. Stars are **not** part of the evaluation.

**[Open the challenge submission Google Form](https://docs.google.com/forms/d/1an-hce3EQ8bUVArnZJnD1VwxQIxgmNzLKYQ8h814CVE/viewform)**

---

## About Alphashots.AI

Alphashots.AI is a pre-seed-funded AI technology startup working on applied AI and open-source engineering tools. **[UnvibeCode](https://github.com/FinanceFlash/unvibecode)** helps developers understand unfamiliar repositories through business workflow maps, connected code maps, business risk findings, and repository context.

**Your submission should show what you observed, how you reasoned, and what another engineer could actually use.**