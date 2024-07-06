import csv
import sys
import matplotlib.pyplot as plt

RECORDS = []
QI = []
K = 0
PARTITIONS = []
ANON_PARTITIONS = []


def plot_discernability_penalty(attributes, discernability_penalty_values, title):
    plt.figure(figsize=(10, 6))
    plt.plot(attributes, discernability_penalty_values, marker='o', label='Multidimensional')

    # Adding labels and title
    plt.xlabel('Number of Attributes')
    plt.ylabel('Discernability Penalty')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def calculate_discernability_penalty(equivalence_classes):
    total_records = sum(len(eq_class) for eq_class in equivalence_classes)
    total_penalty = 0

    for eq_class in equivalence_classes:
        eq_class_size = len(eq_class)
        penalty = (eq_class_size - 1) / (total_records - 1)
        total_penalty += penalty

    return total_penalty / len(equivalence_classes)

#importing data from csv file
def read_csv(path, delete_headers):
	with open(path, newline='') as datafile:
		datareader = csv.reader(datafile)
		if(delete_headers == "1"):
			next(datareader) 
		for rows in datareader:
			RECORDS.append(tuple(rows))
	datafile.close

def choosingBestAttr(divide, QI):
	attribute_array = []
	for i in QI:
		attriute_values = set(())
		for j in divide:
			attriute_values.add(j[i])
		attriute_values = list(attriute_values)
		attriute_values.sort()
		attribute_array.append(attriute_values)
	choice = -1
	choice_index = -1
	choice_size = 0
	for i, QID in enumerate(QI):
		if(len(attribute_array[i]) > choice_size):
			choice = QID
			choice_index = i
			choice_size = len(attribute_array[i])
	return attribute_array[choice_index], choice

def checkNumberArray(a):
	boolean = True
	for value in a:
		if not value.isnumeric():
			boolean = False
			break;
	return boolean

def countSets(attribute, attribute_domain, readdata):
	# creating orderered count set for the values in dataset
	count = []
	for i in range(0, len(attribute_domain)):
		count.append(0)
		for t in readdata:
			if t[attribute] == attribute_domain[i]:
				count[i] += 1
	return count

def calculateMedian(count, attribute_domain):
	# from an attribute value frequency set, determine the median value.
	all = sum(count)
	median = 0
	if all % 2 == 0:
		lhs = all/2
		rhs = (all/2)+1
		median = (lhs+rhs)//2
	else:
		median = (all+1)/2
	# real median is saved using staticMedian.
	staticMedian = median
	# until the median is exceeded, subtract frequency counts in order; index = median value.
	value_median = -1
	for index, count in enumerate(count):
		median = median - count
		if median <= 0:
			value_median = index
			break
	return (staticMedian, attribute_domain[value_median])

def strictDivide(attribute, median_value, attribute_domain, readdata):
	# Using strict partitioning, divide a set of data into two separate segments.
	x = []
	y = []
	median_index = attribute_domain.index(median_value)
	for data in readdata:
		if(attribute_domain.index(data[attribute]) <= median_index):
			x.append(data)
		else:
			y.append(data)
	return (x, y)

def realxing_partition(median, attribute, median_value, attribute_domain, readdata):
	# utilizing relaxed partitioning, divide a set of data into two partitions.
	x = []
	y = []
	median_tuples = []
	median_index = attribute_domain.index(median_value)
	i = 0
	for data in readdata:
		if(attribute_domain.index(data[attribute]) < median_index):
			x.append(data)
			i+=1
		elif(attribute_domain.index(data[attribute]) > median_index):
			y.append(data)
		else:
			median_tuples.append(data)
	# place tuples one at a time into other subsets from the median subset.
	for j in median_tuples:
		i+=1
		if(i <= median):
			x.append(j)
		else:
			y.append(j)
	return (x, y)


def Strict_MultiDimension(data_frame, split_QI):
	# Strict algorithm

	# It will check that if data frame can be splited.
	if (len(data_frame) < 2*K) or (len(split_QI) == 0):
		return data_frame
	
	(attrib_multi, top_data) = choosingBestAttr(data_frame, split_QI)
	repeatition = countSets(top_data, attrib_multi, data_frame)
	(median, median_value) = calculateMedian(repeatition, attrib_multi)
	if median_value == attrib_multi[-1]:
		# Here taking the median value as last value in list
		# If unable to split partition with this dimension it will try with next dimension recursively
		new_QI = split_QI[:]
		new_QI.remove(top_data)
		return Strict_MultiDimension(data_frame, new_QI)

	(lhs, rhs) = strictDivide(top_data, median_value, attrib_multi, data_frame)

	if(len(set(lhs)) < K or len(set(rhs)) < K):
		# IF size of lhs or rhs partition less than K it will try next dimension recursively
		new_QI = split_QI[:]
		new_QI.remove(top_data)
		return Strict_MultiDimension(data_frame, new_QI)

	# reseting the QI
	if QI != split_QI:
		split_QI = QI
	# discernability_penalty_lhs = len(lhs) / len(data_frame)
	# discernability_penalty_rhs = len(rhs) / len(data_frame)
	# print("k =", K, "discernability_penalty_lhs =", discernability_penalty_lhs)
	# print("k =", K, "discernability_penalty_rhs =", discernability_penalty_rhs)
	# recursively calling the new partitions as data frame that append partitions to global values
	PARTITIONS.append(Strict_MultiDimension(lhs, split_QI))
	PARTITIONS.append(Strict_MultiDimension(rhs, split_QI))

def Relaxed_MultiDimension(data_frame, split_QI):
	# Here partitioning the relaxed multidimension algorithm

	# Cheking the data_frame can be splited
	if len(data_frame) < 2*K or (len(split_QI) == 0):
		return data_frame
	
	(attrib_multi, top_data) = choosingBestAttr(data_frame, split_QI)
	repeatition = countSets(top_data, attrib_multi, data_frame)
	(median, median_value) = calculateMedian(repeatition, attrib_multi)
	(lhs, rhs) = realxing_partition(median, top_data, median_value, attrib_multi, data_frame)

	if(len(set(lhs)) < K or len(set(rhs)) < K):
		# size of either partition lower than K - recursively try next dimension
		new_QI = split_QI[:]
		new_QI.remove(top_data)
		return Relaxed_MultiDimension(data_frame, new_QI)

	# reset QIDs
	if QI != split_QI:
		split_QI = QI
	
	# recursive call with new partitions as data_frame - append optimal partitions to global container
	PARTITIONS.append(Relaxed_MultiDimension(lhs, split_QI))
	PARTITIONS.append(Relaxed_MultiDimension(rhs, split_QI))


def general_values(partition, QI):
	# anonymise partitions by generalisation

	L = [] # container for QID summarisations

	# cycle over QIDs and store all values in partition for given QID as a summarisation
	for i in QI:
		a_set = []
		for p in partition:
			a_set.append(p[i])
		a_set = set(a_set)
		a_set = list(a_set)
		if len(a_set) > 1:
			if(a_set[0].isnumeric()):
				a_set = list(map(int, a_set))
			a_set.sort()
			L.append(a_set)
		else:
			L.append(a_set[0])

	# convert partition to a transcribable list of anonymised tuples
	anon_partition = []
	for t in partition:
		anon_tuple = list(t)
		for i, QID in enumerate(QI):
			anon_tuple[QID] = L[i]
		anon_partition.append(tuple(anon_tuple))

	return anon_partition

def write_csv(dataset, filename):
	# write data to csv file
	with open(filename, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, dialect='excel')
		writer.writerows(dataset)
		csvfile.close

def anonymise(args):
	# main function

	# define globals
	global K
	global QI
	K = int(args[3])
	# K = k_value
	QI = list(args[2].split(","))
	QI = list(map(int, QI))
	print(f"line 247 {K}")

	# import entire data set
	read_csv(args[1], args[5])

	# execute Strict or Relaxed algorithm
	if(args[6] == "1"):
		Strict_MultiDimension(RECORDS, QI)
	else:
		Relaxed_MultiDimension(RECORDS, QI)
	
	# discernability_penalty_values = []

    # Vary the number of attributes and measure discernability penalty
	# for num_attributes in range(2, 11):
	# 	# Modify synthetic data generation with the desired number of attributes
	# 	# synthetic_data = generate_synthetic_data()

	# 	# Reset global variables
	# 	global PARTITIONS
	# 	PARTITIONS = []

		# Run the Mondrian algorithm
		# Strict_MultiDimension(synthetic_data, QI)

		# Calculate and store discernability penalty
		# In a real scenario, you would need to implement the discernability penalty calculation
	# discernability_penalty = calculate_discernability_penalty(PARTITIONS, QI)  # Replace with the actual discernability penalty calculation
	# discernability_penalty_values.append(discernability_penalty)

	# Plot the discernability penalty values
	# plot_discernability_penalty(list(range(2, 11)), discernability_penalty_values, 'Quality Comparison for Synthetic Data')

	# cycle over all non-anonymised partitions and general_values values to anonymise
	for i in PARTITIONS:
		if i != None and len(i) != 0:
			ANON_PARTITIONS.append(general_values(i, QI))

	K_annonimity = [] # container for full transcribable k-anonymisation

	equivalence_classes = []

	for i in ANON_PARTITIONS:
		# sanity check for size of equivalence classes
		# print(f"line 287 {i}")
		
		if len(i) < K:
			print("SIZE LOWER THAN K: ", len(i))
			return equivalence_classes
		# append anonymised tuple
		equivalence_classes.append(i)
		K_annonimity += i
	print(f"line 299 {len(equivalence_classes)}")

	discernability_penalty_values = []
	# check if k-anonymisation was made - if so then write output
	if(len(K_annonimity) > 0):
		write_csv(K_annonimity, "output_attr"+f"_k_value_{K}"+".csv")
		if(args[6] == "1"):
			print("Successful strict anonymisation. Output to: " + args[4])
		else:
			print("Successful relaxed anonymisation. Output to: " + args[4])
		discernability_penalty = calculate_discernability_penalty(equivalence_classes)  # Replace with the actual discernability penalty calculation
		discernability_penalty_values.append(discernability_penalty)
		print(discernability_penalty_values)
	else:
		# k-anonymisation not possible for selected parameters
		print("Can't be anonymised for K = ", K, " or selected QI.")
	return equivalence_classes


# get terminal argv to use as algorithm arguments
args = sys.argv
if(len(args) != 7):
	print("Incorrect No of arguments to run; apply this format : input Filename, QI, k, output Filename, header format 0/1 for F/T, strict format 0/1 F/T")
	sys.exit()
anonymise(args)
# k = [2, 3, 5, 10, 25, 50]
# discernability_penalty_values = []
# equivalence_classes = []
# for k_value in k:
# 	print(k_value)
# 	equivalence_classes = anonymise(args, k_value)
# 	print(f"line 329 {len(equivalence_classes)}")
# 	discernability_penalty = calculate_discernability_penalty(equivalence_classes)  # Replace with the actual discernability penalty calculation
# 	discernability_penalty_values.append(discernability_penalty)
# print(f"The penalty values are: {discernability_penalty_values}")