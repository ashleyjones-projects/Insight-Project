# Insight-Project
Money-Puck: A tool to help GM's value players

This 3 weeks project was designed to investigate NHL player (skaters here, and not goalies) salaries in relation to their performance. Traditional hockey metrics have been along the lines of Goals, Assists, plus/minus etc.. but in the last decade or so there has been a move towards a more advanced set of metrics to do with player possession and situational behaviour. Whilst there is a clear correlation between the total number of points and increased salary, perhaps there are other metrics involved that also determine a player's value? 

What's more imoressive? Consider a player who may score 40 goals in a season, but perhaps most of those goals came on the power player or perhaps against a poorer quality of competition. Then consider a player who has 20 goals who were scored at even-strength and against tougher opponents. There are more advanced stats that can be investiagted and take these factors into consideration, but how much weight are considered in salary value?.

I have used a beautifulsoup algorthm (hockeyreference.py) to extract tradtional and salary information as well as obtained advanced metrics in the form of CSV and produced a database of about 2000 NHL players spanning from 2008-2018. Data are sorted, joined, and cleaned in corsica_cleaning.py. I performed some data visualization to identify some key metrics and relationships between salary and performance (Data_visualization.py).

I then considered exploring which features are most important concerning player role and so decided to filter players into their positional roles using Offensive zone starts as a proxy and by using K-means such that Forwards were seperated into defensive,two-way, and offensive, whilst Defensemen were divided into offensive and defensive type roles. I used a random-forest algorithm to determine the most important features by filtering players (from each role seperately) into one of three salary bins. Many of the key features were similar for each player role (such as Time On Ice paramters,age, draft position, and point production), although there were some differences which were expected between each role (see multivariate_analysis_final.py).

Once the key features were identified, I used Value inflation Factors (ViF) to minimize those features that shared strong correlation relationships between each other, to just one. I used mulitvariate linear regression using a combination of these key independent features to predict player salaries based on two markets: One for forwards and one for defensemen. Players that were considered were in the final year of their contract and were seperated to into groups. One where players saw a salary increase and one that saw a salary decrease (see multivariate_analysis_final.py). 

The model predicted defensemen and forwards salary fairley well, 59 and 66% (r2) respecively, for where players made more salary, but predicted poorly (~42.5% r2) for where players saw a decrease in salary. Whilst the former model is quite respectable, it goes to show that performance alone cannot predict a player's salary and that there are many other factors involved that are market driven or due to human behavioural factors (see multivariate_analysis_final.py). 

NB/ The choice to do a random forest to determine the key features is for the sake of experimentation. The insight project encourages you to use as many tools as possible for learning aids. Key features of course can be identified by multivariate regression by use of P-values and F-scores.

For more information, I wrote a blog that explains in more details the process, visualization and results.

https://medium.com/@ashcan.jones/can-nhl-player-performance-metrics-help-predict-salary-294dd347fcd3


