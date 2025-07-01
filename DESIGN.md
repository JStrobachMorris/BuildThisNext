# BuildThisNext - Design Document

## Project Overview
**BuildThisNext** aims to be a data-driven tool for indie game developers to help them answer the question:\
\
*"What kind of game will I build next?"*\
\
Publicly available game data is analysed using the RAWG API (see [https://rawg.io](https://rawg.io)) to identify emerging trends and under-served niches, which is then used to help developers to determine whether their new idea is worth pursuing - and if not, how to potentially modify it. Developers can then use this tool to prioritise with both more market traction and lower competition - avoiding a lot of wasted time making games that likely won't gain traction.
## Business Problem
Game developers often spend extensive time, effort and money on developing new games, hoping that their game will eventually be successful when launched. But what if the game never takes off? This risk can be minimised by making use of insights from the vast amount of data about existing games, and using this to point developers towards games that have actual potential.\
\
In this project, we will measure a game as "potentially successful" if it shares tags with games that are popular, whilst also addressing a gap in the market. The game will therefore be likely to capitalise on existing trends, whilst not being drowned by the established competition (which would happen if it were too similar to existing popular games).\
\
A naive approach to this goal would be to serve a simple recommender system that identifies gaps in popular genres, and outputs a universal recommendation to any developer using the app. There are two major problems with this approach:
1. If we assume this app is used sufficiently many times to inform actual game development, this would create a feedback loop where market gaps are quickly filled - perhaps even before a game's development cycle has been completed.
2. Universal recommendations ignore the individual developers' passions and original ideas, leading to a more homogenised and un-inspired landscape of available games.
<!-- -->
Consequently, this project will focus on taking game developer's original ideas and assessing whether they might be viable. It will then continue with recommendations to adjust these ideas, based both on market trends and the original proposed idea. This should hopefully result in more tailored and unique recommendations.
## Desired Deliverables
In this project, we will serve an app that uses a model trained on data from the RAWG API to make predictions and recommendations for viable game proposals, based on the user's original input. More specifically, this app should deliver:
- Evaluation of proposed game input, suggesting whether a game proposal is viable or not
- Recommendation of adjustments to the game proposal based on available market trends
- Resistance to malicious inputs
- Ethical recommendations
- GDPR compliance
## Why Machine Learning?
A simple recommendation system could be built without applying to any machine learning tools, but this would have to rely on basic heuristics and would certainly lack the flexibility to address the business case outlined above.\
\
An ML solution, on the other hand, would allow us to personalise recommendations, generalise to new recommendations (unseen in the dataset) and make use of more complex, nonlinear feature relationships.
## Costs
Given that this is a non-commercial project, we aim to keep the costs at zero (beside CPU use on a personal computer!). Consequently, we will have to remain within free-tier API limits (currently 20,000 requests per month), which motivates the use of a cache generated from offline training. In order to remain cost-free, we will also avoid hosting on larger, paid cloud hosting platforms such as AWS - instead aiming for a launch on Streamlit.
## Risks
There are three major risks that this app needs to be robust against: GDPR non-compliance, suceptibility to malicious input and non-ethical recommendations. In addition, it is worth considering the consequences of incorrect outputs (corner cases).
### GDPR Compliance
Model training will only use public, non-personal game metadata, obtained using the RAWG API.
### Ethical Recommendations
Since this app aims to make create business suggestions, there is a potential for it to produce less ethical recommendations. These might include the promotion of problematic content as well as perpetuating harmful stereotypes.\
\
In order to address these potential issues, model training will include a manual bias check (to see if certain narrow genres are over-recommended) as well as tag filtering.
### Resistance to Malicious Input
Small web apps can be easily attacked in a variety of ways, including script injections, large payloads, API abuse and DoS attempts.\
\
Here are some ways this project will try to mitigate these:
- Users will be rate-limited to 2 queries per minute.
- Client-side code should not feature any API key - backend offline training should mitigate this risk.
- We will explore two avenues for user input - raw text and sliders/list selection. If using raw text, we will limit character length and strip text from any HTML/JavaScript tags - Streamlit has this functionality.
- Users will not be shown detailed error breakdowns - instead just a generic error message.
### Corner Cases
What are the consequences if the app gets a recommendation or evaluation wrong? Given that this project doesn't make any financial decisions or store private user data, the main damage is reputational. The two main strategies to mitigate major reputational hits will be to include a disclaimer and provide the user with an estimated confidence score.
## Project Milestones
### Intial Data Collection
- Set up RAWG API access
- Define features needed
- Collect initial data for up to 2000 games
- Store data locally in csv files
### Data Preprocessing
- Clean data - address missing values, data duplication and poor formatting
- Engineer key features
- Encode categorical data
- Normalise data
- Check data balance and resample if required
- Perform train/dev/test split
- Save processed data to a csv file
### Data Analysis and Feature Engineering
- Analyse descriptive statistics for the training data
- Visualise training data
### Metric Determination
- Determine appropriate metrics to judge experiments by - these should be aligned with our business case
### Experimentation 1 - Classification/Regression
- Further engineer features, performing PCA if required
- Build baseline model
- Tune model type or hyperparameters
- Evaluate and iterate until metrics are sufficiently high
### Experimentation 2 - Recommendation
- Build recommender system (details TBD)
- Evaluate recommender system
### Feature Extraction from User Input
- Design synthetic test prompts (storing raw text and desired features)
- Build an NLP parser
- Create algorithm with follow-up questions for missing features
- Process parser and question output to prepare for model input
- Evaluate model performance with prompting
- Determine whether to go ahead with raw prompts or feature selectors
### Pipeline Building
- Moduralise data intake
- Automate preprocessing
- Create an input validation schema
- Create a flagging system for model degradation
- Consider building a re-training pipeline
- Set up a serving API (e.g. Flask)
### Pre-Deployment Testing and Safety
- Set up and test input sanisation (preventing malicious injections)
- Package and run unit testing
- Test edge cases - including unusual inputs
- Audit model behaviour for ethical recommedations
### Productionisation
- Build Streamlit app
- Set up monitoring system
- Deploy (probably on Streamlit cloud)


