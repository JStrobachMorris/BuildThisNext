# BuildThisNext

**BuildThisNext** is a data-driven tool for indie game developers, desgined to help them answer the age-old question:

*"What kind of game should I build next?"*

Developers (or anyone!) can use the app to pitch a future game idea, and will then be given a score on how successful their idea might be, as well as some suggestions for how to modify it.

BuildThisNext uses game data called from the RAWG API (see [https://rawg.io](https://rawg.io)) to train both a success-score regression algorithm and a recommender algorithm, based on an embedding representation of each game's description.

To see more details on the business problem, desired deliverables and planned project milestones, please see the design document at [DESIGN.md](DESIGN.md).

### License
![License](https://img.shields.io/badge/license-MIT-blue.svg)

### Languages
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)

## Project Status

Initial exploration and scoping complete.

Made an initial API call to get a dataset of just 100 games, performed data exploration on a subset of variables to engineer a suitable proxy label for game success (**rating * log(ratings_count + 0.25*added)**), then cleaned and vectorised game descriptions and tags to establish a baseline feature set. For a deep-dive into this initial work, see [Initial_Exploration](Initial_Exploration).

Scaled up to a full API call (18,000+ games), removed instances with null descriptions and no ratings (resulting in a dataset of 12,000+ games). API call and preprocessing .py files currently on the pre-processing branch.

Currently iteratively model building and evaluating, and considering looking back at data again to further engineer or perhaps change the problem from regression to multi-class classification.

All models currently overfitting beyond ~0.84 RMSE.


