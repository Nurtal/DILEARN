"""
Score function for the AG exploration
-> use support vector machine as a score
function for the exploration discretization
with genetic algorithm

"""

from sklearn import svm
import platform
import DataManager
import numpy
import sys
import os



def run_svm_scoring(strategy_filter, file_id):
	"""
	"""
	
	PathToMatrixFile = "Undef"
	PathToMatrixLabelFile = "Undef"	

	# => Filter & Reformat data
	if(platform.system() == "Windows"):
		DataManager.filter_input_data("DATA\\MATRIX\\data_dichotomized_pattern_individual_to_evaluate_"+str(file_id)+".csv", "DATA\\patientIndex_"+str(file_id)+".csv", strategy_filter)
		DataManager.reformat_inputFile("DATA\\MATRIX\\data_dichotomized_pattern_individual_to_evaluate_"+str(file_id)+".csv", "DATA\\patientIndex_"+str(file_id)+".csv", file_id)
		PathToMatrixFile = "DATA\\data_formated"+str(file_id)+".csv"
		PathToMatrixLabelFile = "DATA\\data_formated_label"+str(file_id)+".csv"
	elif(platform.system() == "Linux"):
		DataManager.filter_input_data("DATA/MATRIX/data_dichotomized_pattern_individual_to_evaluate_"+str(file_id)+".csv", "DATA/patientIndex_"+str(file_id)+".csv", strategy_filter)
		DataManager.reformat_inputFile("DATA/MATRIX/data_dichotomized_pattern_individual_to_evaluate_"+str(file_id)+".csv", "DATA/patientIndex_"+str(file_id)+".csv", file_id)
		PathToMatrixFile = "DATA/data_formated"+str(file_id)+".csv"
		PathToMatrixLabelFile = "DATA/data_formated_label"+str(file_id)+".csv"

	
	binaryClassification = 1
	sizeOfValidationSet = 60
	numberOfPatient = DataManager.get_NumberOfPatients(PathToMatrixFile)
	numberOfSample = numberOfPatient / sizeOfValidationSet
	numberOfPatient = DataManager.get_NumberOfPatients(PathToMatrixFile)

	matrix_sets = DataManager.cross_validation(PathToMatrixFile, PathToMatrixLabelFile, sizeOfValidationSet, binaryClassification)

	X_sets = matrix_sets[0]
	X_validation_sets = matrix_sets[1]
	y_sets = matrix_sets[2]
	y_validation_sets = matrix_sets[3]


	score_list = []
	for x in range(0, numberOfSample):
		X = X_sets[x]
		X_validation = X_validation_sets[x]
		y = y_sets[x]
		y_validation = y_validation_sets[x]

		clf = svm.SVC()
		clf.fit(X, y)

		prediction = clf.predict(X_validation)

		# evaluate score
		cmpt = 0
		good_answer = 0
		for diag_predicted in prediction:
			diag_real = y_validation[cmpt]

			if(diag_real == diag_predicted):
				good_answer += 1

			cmpt+=1


		score = float(good_answer) / float(len(y_validation))
		score = score*100
		score_list.append(score)


	# compute final score
	final_score = numpy.average(score_list)

	# write result in log file
	log_file = open("evaluation_score.log", "w")
	log_file.write(str(float(final_score))+"\n")
	log_file.close()

	# delete files
	os.remove(PathToMatrixFile)
	os.remove(PathToMatrixLabelFile)