# PandANOVA

Uses a dataframe with a column for an independent variable (IV) and a dependent variable (DV) and performs an Analysis of Variance (ANOVA) test to determine if three or more groups are statistically different. 
The IV column labels each row as belonging to a particular group. PandANOVA will return the F-statistic and the P-value. The grandmean function can return the [weighted mean](https://en.wikipedia.org/wiki/Weighted_arithmetic_mean#Basic_example) (for different sized groups) or unweighted mean; the default is a weighted mean.

# Prerequisites:
* Numpy
* Pandas
* Scipy

# To Do:
* check code and make sure variables/functions are consistent with best practices
* eventually add [MANOVA](https://en.wikipedia.org/wiki/Multivariate_analysis_of_variance) (multivariate analysis of variance), which is the original goal of this project. 

# Author:
* [Hiram Foster](mailto:hiramfoster.co@gmail.com)

# License:
This project is licensed under the MIT license. See the LICENSE.md file for details.
