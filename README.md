# Agent-assisted software development with Google Cloud

## Pre-reqs

* Gemini Code Assist enabled.
* Gemini CLI installed and configured.
* A recent Python version available in your system.

## Steps

1. Update the Product Requirements Document (PRD) based on the info from the CEO's mail.
2. Update the Technical Design Document (TDD) based on the modified PRD. Ensure that all app-wide technical specifications are well defined here. For example:
   1. Gemini models to use.
   2. Languages and frameworks.
   3. If the bucket should be public, or if signed URLs should be used instead.
   4. Any other technical implementation or architectural detail that is important and should be clearly followed by the agent, without ambiguity.
3. Produce user stories from the PRD and TDD for each of the features to be implemented.

    ```
    Given the PRD in @docs/PRD.md and the overall technical specification in @docs/TDD.md , create separate docs outlining the different user stories for the individual, atomic features that must be implemented. Create them under docs/user-stories.
    ```

## Tips

* Consider instructing the agent to keep the latest status of all the features in a separate file.

## Bonus points

These are some additional things you can try to go the extra mile:

* Try adding a new feature, such as the ability to delete a video, or video moderation to block inappropriate content.
* Try modifying the UI by providing an image of a UI mockup to the agent.
