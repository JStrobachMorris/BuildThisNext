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

Scaled up to a full API call (18,000+ games), removed instances with null descriptions and no ratings (resulting in a dataset of 17,000+ games). See [data](data) for the resulting csv files, and [src/data_utils](src_data_utils) for the py files used to process this data.

All work from here on found on the modelling branch. Here is a brief overview of the steps taken so far (more details on model performance will be added here later - for a preview, have a look at the model_evals folder on the modelling branch): 

### Regression - All Games with Ratings

The data is generally normally distributed (once rescaled to the success proxy) - with the exception of a notable number of games with a rating of zero, which therefore have a minimal success score. The resulting distribution appeared to cause our regressors to perform poorly, with them unable to reach an RMSE below 0.8. Models tried: ridge linear regression, XGB regression, neural network regression and Light GBM regression.

### Regression - All Games with Non-Zero Ratings

In order to get a better normal distribution, we dropped all games with a ratings of zero. To justify this potential loss of signal, a significant improvement in our model performance would need to occur. However, models stayed at a similar level of 0.8 RMSE, and so this approach was abandoned. Given the difficulty of dealing with the big peak at minimal success, a categorical binning approach was instead advocated next.

### Classification - Four Categories

Proxy success scores were binned into four categories - minimal, low, medium and high. However, after a quick run with logistic regression and XGB classification, it was evident that the models struggled clasifying the low and middle success categories. These categories aren't really that important for our use case - it would be enough to know whether a game might be likely to be promising (high) and not a good idea (minimal). As a result, we tried three categories instead of four.

### Classification - Three Categories

This was more successful - a number of models were tried, including logistic regression, XGB classification, random forest classification and various iterations of a neural networks.

The best neural network model architecture was then chosen to generate embeddings for the recommender system.

### Recommender System

This part is still very much in its infancy. The chosen neural network architecture from the classifier is used for the embedding model. The generated embeddings are then fit to a simple KNN model (with cosine similarity). These are then used to recommend tags. Given vectorised input tags, other tags are identified and recommended if they are among better-performing neighbours (but less frequent overall, in order to stimulate novelty).

In order to get decent recommendations, it was evident that a larger set of tags was necessary to train on in the first place. This required an adjustment of the tfidf vectorisation arguments. Consequently, we went through the whole preprocessing and modelling process again, generating new embeddings (and carefully cateloguing previous and current preprocessed datasets and vectoriser settings). Due to the extensive re-modelling, it was also necessary to carefully capture and catelogue model performance for each vectorisation setting.

The classification models and recommender systems are currently in the process of being adjusted and then tested with new prompts.


