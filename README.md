# Agent-assisted software development with Google Cloud

## Pre-reqs

* Gemini Code Assist enabled.
* Gemini CLI installed and configured.
* A recent Python version available in your system.

## Steps

1. Produce a Product Requirements Document (PRD) from the CEO's mail.
2. Produce a Technical Design Document (TDD) from the PRD.
   2. Specify the correct Gemini model.
   3. Ensure languages and frameworks here.
   4. Specify if the bucket should be public, or if signed URLs should be used instead.
   5. Any other technical implementation or architectural detail must be defined here.
3. Produce user stories from the PRD and TDD for each of the features to be implemented.

    ```
    Given the PRD in @docs/PRD.md and the overall technical specification in @docs/TDD.md , create separate docs outlining the different user stories for the individual, atomic features that must be implemented. Create them under docs/user-stories.
    ```

## Bonus tracks

* Try adding a new feature, such as the ability to delete a video.
* Try modifying the UI by providing an image of a UI mockup to the agent.
