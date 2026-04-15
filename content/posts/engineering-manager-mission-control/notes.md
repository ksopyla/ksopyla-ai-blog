

Post about my engineering manager mission control, how I use AI and MCP to help me manage my team and projects.

The engineering manager work is not easy, it's a lot of context gathering, a lot of decisions to make, a lot of communication to do.
For some time I was trying to use AI to help me with my work, but I was not able to get the results I wanted.

I have stared slowly buildin the system step by step that will help me to manage my team and projects.


1. I have create a repository for my markdown files: 
2. I have connect my company Cursor with MCP: 
    * attlassian Mcp server - for Jira and Confluence
    * intially I have connected my comapny Githu MCP, but later switched to GH cli 
    * Azure CLI - for checking Azure resources and deployments, subscritpions, costs, quotas, etc.
    * Azure MCP server for documentation - for my arechitecture and design documentation
    * AWS cursor plugins
    * SNYK mcp server - for checking vulnerabilities in my company's dependencies
    * the repository has convigured python with uv - to have one consistent python environment when agent wanted to create a script to do some work, small tools for data analysis, word or excel file doc creation - for stakeholders

 using those tools I have asked the AI to create a markdown files that have a context of my company, my teams, my projects, dependent projects, API

3. Then I have created a "problems" folder, which contains all the problems I need to work on: 
    * like template for promotion, to check if the team member filling all the checkboxes for the carrer framework prepared by HR
    * problem for assesing our delivery speed, metrics like velocity etc, with explanations: team member was away, ticket was blocked for a week, the wrong assigment etc
    * where our delivery blockers are? I appears that one of the most common was waiting for PR review by peer developer - we switched to AI PR reviewer
    * some architecture reviews and sollutioniong - with AWS and Azure MCP servers that could pull the documentation I was able to quickly asses the feasability of the solution
    * assesing some of the team estimations, if the estimation is too low or to high, espeaccialy for infrastructure work (DevOps) that I'm not an expert in, but comparing the actual work with the previous and what we already have on AWS or Azure help a lot, I have more argument to challenge 
    * deal with one problem at a time, add as much context  to the problem folder as possible
    * the problem folder is a living document, it's not static, it's growing and changing as I work on the problems
    * 



What I can do with this approach:
* I was able to asses the quality of our documenttion - and ways to improve it
* I'm reviwieng the team RFC's and proposals - assesing the proposals, brain strorming with other potential sollutions
* building quick healthy checks for jira and sprints, 
* building a tool that helps me build a roadmaps, define the epics - assesing their scope and complexity, checking the status of other teams work that we depend on
* generate the marmaid diagrams for the architecture and design documentation

Some skills that I created for the AI to use:
* RFC reviewer - for reviewing the RFC's and proposals, assesing the proposals, brain strorming with other potential sollutions
* Sprint health checker - for building quick healthy checks for jira and sprints
* Roadmap builder - for building a roadmaps, define the epics - assesing their scope and complexity, checking the status of other teams work that we depend on
* Architecture and design documentation reviewer - for reviewing the architecture and design documentation, assesing the documentation, brain strorming with other potential sollutions
* Documentation quality checker - for assesing the quality of the documentation, and ways to improve it
* Dependency vulnerability checker - for checking vulnerabilities in my company's dependencies


My realizations: 

- you need to spent more time to refine the skills to make it accurate, it didn't work out of the box
- collection the context was quate easy, and this give me a lot of insight 
- try to work sequentially
- I observe compunding effect while my "problems" folder is growing, the more problems I have, the more I can use the AI to help me with my work
- you need to have an kind of self improvement loop, I have a skill for that, 
- the hardest part was to collect my way of thininking, this takes a lot of time, and I still working on this "skill" to capture the way I like doing things, comment, communicate etc  