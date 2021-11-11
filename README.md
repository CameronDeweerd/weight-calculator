# weight-calculator

A calculator to save time at the Gym by splitting people into groups that minimize the number of barbells that need to be changed.

It takes time to add and remove the barbells from a benchpress bar and when you have 6+ people who all want to use it and only a limited time to workout then you want to avoid wasting time. This takes a list of each person's weight target and divides everyone into groups of 2 or 3 to minimize the number of changes that need to be made to the bar.

Gyms are also limited in the weights they have so it may not be possible to put 3x 5lb weights on the bar. This calculator takes into account all the different ways that a target weight can be reached using the weights available. 

>Given WEIGHT_LIST = [45, 35, 25, 10, 10, 5, 5, 2.5]
>
>35 -> 35
>
>35 -> 25, 10
>
>35 -> 25, 5, 5

## Example Output
The output shows how much weight you need to put on each side of the 45LB bar
![alt text](https://github.com/CameronDeweerd/weight-calculator/blob/master/weightCalcConsole.JPG?raw=true)
