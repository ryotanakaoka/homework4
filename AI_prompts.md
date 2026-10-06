# AI Prompt Log — Homework 4

This file records the prompts actually used while completing Homework 4. It is documentation only, not a runtime prompt file. Do not add prompts that were not actually entered.

## Problem 1 — Vibe Coder Prompts

**Prompt 1 (actually entered):**

> here is Homework4.
> here is the problem 1. the title is Vibe Coder Prompts.
> crate AI\\_prompts.md. for each problem, include the problem number and title my initail prompt and if needed a follow up prompt whit one sentece expaining what was missing from the initial prompt. iwill updeate this file as i complete each problme

**Evidence of problem-by-problem work:** This prompt establishes the Homework 4 prompt-recording format for Problem 1.

## Problem 2 — Analyze the Database

**Prompt 1 (actually entered):**

> here is problme 2. the title is Analyze the Database.
> inspect data/campus\_customs.db and identify all tables and their fields. including at least catalougue,inventory, and users. do not modify the database. create output/harness.md and list each table and its fields whit one shor explanation of why each fields matter for the shop or chabot.

**What was missing from the first response:** The requested database file is not currently present in Homework 4, so its schema cannot yet be inspected.

**Evidence of problem-by-problem work:** This prompt is limited to read-only database schema inspection and documentation for Problem 2.

## Problem 3 — Build the Campus Customs Website

**Prompt 1 (actually entered):**

> here is problme 3. the title is Build the Campus Customs Website.
> build a React + vite + typescript campus customs website with navigation for Home, Products. about us, log in and create account. use the database and product images alresy in data/ to show product cards with image, name price and short description. each card shold open a single product page with a large image , full description, price and availbale size/stock. add a floating chat interface at the bottom right as a stub for now. use campus customs-style content for home and bout us without copying original website text. create a simple fastapi backend if needed to serve the database product and images.

**Evidence of problem-by-problem work:** This prompt is limited to building the React/Vite storefront, database-backed product pages, navigation, chat stub, and optional FastAPI API for Problem 3.

## Problem 4 — Create account and login

**Prompt 1 (actually entered):**

> here is problem 4. the title is Create account and login.
> create account should use first name, last name, email, and password, store new users in the users table and store password. test loging with the provided test user and with a new account. update output/harness.md with how authenticaiton works

**What was missing from the first response:** The provided test user's password was not present in the project, so only the new-account registration and login could be credential-tested.

**Evidence of problem-by-problem work:** This prompt is limited to account registration, password storage, login verification, authentication testing, and documentation for Problem 4.

**Follow-up prompt 2 (actually entered):**

> the provided test user password is "password". test login with test\@campuscustoms.yale.edu and password.

**What was missing after the first prompt:** The test user's credentials were needed to complete the requested seeded-user login test.

## Problem 5 — PydanticAI agent backend

**Prompt 1 (actually entered):**

> here is problem 5. the title is PydanticAI agent backend. build the shop chatbot as a pydanticai agent with fastapi and connect is to the frontend chat. create backend/main.py, backend/prompts/prompt.md, backend/agent.py, backend/tool.py, and backend/model.py. add the campus customs voice and basic safety rules to prompt.md. update output/harness.md and test that the backend runs from the backend folder withb the required unicorn command

**Evidence of problem-by-problem work:** This prompt is limited to the PydanticAI chatbot, FastAPI endpoint, tools, prompt, models, frontend connection, documentation, and backend startup test for Problem 5.

## Problem 6 — Tools: product info and stock

**Prompt 1 (actually entered):**

> here is problme6. the title is Tools: product info and stock.
> add tools so the chatbot can look up real product informatiom, price, and stock by size from compus.db. update the prompt and models.py as required, and document the tools and lookup fields in output/harness.md. make sure the agent never invents proces or stock quantities.

**Evidence of problem-by-problem work:** This prompt is limited to verified product, price, and size-stock tools, model/prompt updates, and documentation for Problem 6.

## Problem 7 — Chat search that updates the page

**Prompt 1 (actually entered):**

> here is problem 7. the title is Chat search that updates the page.
> implement chat product search so the agent return structured product matches and the website dynamically displays them as product cards. make the cards clickable to open the exisiting product detail page. update prompt.md and harness.md as requreid

**Evidence of problem-by-problem work:** This prompt is limited to structured chatbot matches, dynamic product-card display, clickable product details, and related documentation for Problem 7.

## Problem 8 — Customer memory

**Prompt 1 (actually entered):**

> here is problem 8. the title is Customer memory. add customer memorey so logged in users' chat history is saved and resotred. give the agent user's name/email and current page/product context. guests can still chat without persistend history. update harness.md as required

**Evidence of problem-by-problem work:** This prompt is limited to logged-in chat persistence, safe customer/page context, guest behavior, and harness documentation for Problem 8.

## Problem 9 — Usability improvements

**Prompt 1 (actually entered):**

> here is problem 9. the title is Usability improvements. iwant to make the shop easier to use. on the frontend, add a product search bar and clear loading/error messages. for the agent/backend, improve product search so it can handle partial or similar product names, and provide helpful responses when a product or size is not found. make sure all four improvenmetn work in the ruuning app. decument what you added and why each improvement helps in output/usability.md

**Evidence of problem-by-problem work:** This prompt is limited to the four requested usability improvements, running-app verification, and the usability documentation for Problem 9.

## Problem 10 — Style the website

**Prompt 1 (actually entered):**

> here is problem 10. the title is Style the website. redesign the site to feel like a polished Yale campus store. use a clean Yale-inspired color scheme, stronger typography and visual hierachy, better product cards and images, subtle hover animation, and a more polished chat interface. keep it modern and easy to use. ducument the design changes and why they help customers i  output/design.md

**Evidence of problem-by-problem work:** This prompt is limited to the visual redesign, interaction polish, chat styling, and design rationale documentation for Problem 10.

## Problem 11 — Site testing (app check)

**Prompt 1 (actually entered):**

> here is problme 11. the title is Site testing (app check).
> test the live site and create output/app\_check.html with screensshots of: chat checking real inventory/price, dynamic product cards from a category search and one usability feature from problem9. save the screenshots in output/app\_check\_images/. add a heading and a short explanation for each test

**Evidence of problem-by-problem work:** This prompt is limited to live app checks, three screenshot captures, and the HTML test report for Problem 11.

## Problem 12 — Audit trail, safety, finish harness

**Prompt 1 (actually entered):**

> here is problem 12. the title is Audit trail,safety, finish harness. add an append-only audit trail in output/audit_trail.json that records agent activity, including time, tool name, short arguments/results, and stop reason. add appropriate safety rules to prompts/prompt.md. finally, complete output/harness.md with the model fields and reasons, tools and ability,safety rules, and system specs including loop limits, result caps, models and how to run the frontend and backend

**Follow-up prompt 2 (actually entered):**

> before making any changes, review the current homework4 files and review the entire current project and check problem 1 to 13 against the assignment requirement. inspect the actual files and implementations and identify anything missing, incorrect or broken. do not make any change. give me a checklist for each problem and explain what needs to be fixed

**Follow-up prompt 3 (actually entered):**

> based on your review, fix the issues necessary to fully satisfy problem 1 to 12. focus on unifying the backend so product, login/account creation, chat, and chat history work together, fixing customer memory/history as required by the assignment, completing the audit trail and required documentation. do not add any feature not required by the assignment. preserve existing working feature then test the final project end to end. do not push to github yet

**Evidence of problem-by-problem work:** This work adds the runtime audit trail, safety rules, unified backend routes, customer-history checks, and final harness documentation without changing the database schema.

## Problem 13 — Push to GitHub and submit the URL

**Prompt 1 (actually entered):**

> here is problem 13. the title is push to GitHub and submit the URL. prepare the project in the required hw4/structure. create the required .gitignore, .env.example, requirements.txt, and README.md. make sure .env, campus_customs.db, product images, node_modules, and __pycache__ are not included in GitHub. add this prompt to AI_prompts.md. verify everything, but do not push to GitHub yet

**Evidence of problem-by-problem work:** The Homework 4 submission package now includes `.gitignore`, `.env.example`, `requirements.txt`, and `README.md`; GitHub-sensitive files are excluded; and the package is ready for verification before the user performs the push.
