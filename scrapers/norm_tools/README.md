Data Normalization

Basic Functions:

densityBasedMerge: merge several sets of data based on the density information. If there is value associated with any set of data, change the value information to density information by creating points around the point.

valueBasedMerge: merge several sets of data based on the value information. If there is no value associated with any set of data, put all the points into several clusters and condense the density information to be value information.


Basic Tools:

normValue: normalize the value data.

normDensity: normalize the density data.

densityToValue: create value data according to density data

adjustDensity: change the density data according to the weight.

valueToDensity: create density data according to value data and the weight