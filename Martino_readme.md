# Meteorites
Meteorites - json parser in Python

# Solution:
This Python parser process entries in dataset based on these 3 questions:

- How many entries are in the dataset?
- What is the name and mass of the most massive meteorite in this dataset?
- What is the most frequent year in this dataset?

Firstly I tried to solve it in BASH, using jq command.
After this consideration, I've changed my mind and used better Python instead.

Here are the most important points in script
--------------------------------------------
json.load() → loading JSON file/dataset ("meteorite_landings.json")
- in Windows systems it is recommended to use something like that => ("/METEORITES/meteorite_landings.json")

len() → number of records

float() → converting mass from text to a number

years dictionary → counting occurrences by year

max() → finding the maximum value

Note
----
in the actual dataset there are some records that do not have the mass key at all.

Therefore => meteorite["mass"] will fall into KeyError: 'mass'

The simplest fix is to use .get("mass").

This returns None if "mass" is not present in the record at all.


And most importantly, I wouldn't use pandas or any external libraries.

In my opinion, that would be unnecessarily complicated for a task like this.

The one thing I would watch out for with a real dataset is that some records might have an empty mass or year field.
The script already partially handles empty mass/year values.

One more thing: if a meteorite doesn't have a mass, there won't be a problem with this line:

float(heaviest["mass"])

the script will select `heaviest` only from records that actually have a mass.
