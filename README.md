# Agent-assisted software development with Google Cloud

This repo intends to showcase how to tackle software development using AI agents and tools from Google, including Gemini CLI, Gemini Code Assist, Antigravity, and of course the Gemini model family.

## Pre-reqs

1. **VS Code / Zed**: Install the IDE of your preference. We'll be relaying on gemini CLI to do the lab
2. **Gemini CLI**: Refer to https://github.com/google-gemini/gemini-cli for installation procedure
3. **gcloud**: Refr to https://docs.cloud.google.com/sdk/docs/install-sdk for installation procedure
4. **Clone the lab repo**: git clone -b steps/02-base-app https://github.com/jorgenogales/agiles
5. **Python**: A recent Python version available in your system.

Once we start the lab part, after lunch, you'll be given an account and there will be a pre-lab work were
we'll make use of the above tools

## Steps

This is the overall procedure you should use:

1. Create (or update) the Product Requirements Document (PRD) based on the info from the CEO's mail.
2. Create (or update) the Technical Design Document (TDD) based on the PRD. Ensure that all app-wide technical specifications are well defined here. For example:
   1. Gemini models to use.
   2. Languages and frameworks.
   3. If the bucket should be public, or if signed URLs should be used instead.
   4. Any other technical implementation or architectural detail that is important and should be clearly followed by the agent, without ambiguity.
3. Produce user stories from the PRD and TDD for each of the features to be implemented.

## Example prompts

### PRD

```
Given the CEO email in @mails-from-the-ceo/first.txt , create a Product Requirement Definition (PRD) in Markdown under the `docs/` folder. Be exhaustive without getting into the technical details.
```

### TDD

```
From the Product Requirements Document (PRD) in @docs/PRD.md, create a Technical Design Document (TDD) in Markdown under the same `docs/` folder.
```

Or you can be more specific:

```
From the Product Requirements Document (PRD) in @docs/PRD.md, create a Technical Design Document (TDD) in Markdown under the same `docs/` folder. Take into account the following:

* The app must be a Python monolith using Flask.
* Video uploads must be sycnrhonous. Don't use any async worker or processing thread.
* No database should be used, all data must be stored in Google Cloud Storage, which will be the source of truth.
* If Gen AI models are necessary, always use Gemini 2.5 Flash via Vertex AI.
```

### User stories

```
Given the PRD in @docs/PRD.md and the overall technical specification in @docs/TDD.md , create separate docs outlining the different user stories for the individual, atomic features that must be implemented. Create them under docs/user-stories.
```

## Tips

* Consider instructing the agent to keep the latest status of all the features in a separate file.

## Bonus points

These are some additional things you can try to go the extra mile:

* Try adding a new feature, such as the ability to delete a video, or video moderation to block inappropriate content.
* Try modifying the UI by providing an image of a UI mockup to the agent.
