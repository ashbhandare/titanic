from sknn.mlp import Classifier, Layer

import csv as csv
import pandas as pd
import numpy as np

def clean(data):

	data['Sex'] = data['Sex'].map( {'female': 0, 'male': 1} ).astype(int)
	if len(data.Embarked[ data.Embarked.isnull() ]) > 0:
		data.Embarked[ data.Embarked.isnull() ] = data.Embarked.dropna().mode().values
		# data.Embarked[ data.Embarked.isnull() ] = 3
	if len(data.Age[ data.Age.isnull() ]) > 0:
		data.Age[ data.Age.isnull() ] = data.Age.dropna().median()

	if len(data.Fare[ data.Fare.isnull() ]) > 0:
	    median_fare = np.zeros(3)
	    for f in range(0,3):                                              # loop 0 to 2
	        median_fare[f] = data[ data.Pclass == f+1 ]['Fare'].dropna().median()
	    for f in range(0,3):                                              # loop 0 to 2
	        data.loc[ (data.Fare.isnull()) & (data.Pclass == f+1 ), 'Fare'] = median_fare[f]

	data['Embarked'] = data['Embarked'].map( {'C': 0, 'Q': 1, 'S':2} ).astype(int)
	data = data.drop(['Name', 'Ticket', 'Cabin', 'PassengerId'], axis=1) 

	# use_train = np.array(data)
	clean_data = data.values
	# print data[0]
	# clean_data = data
	# clean_data = np.delete(clean_data , [0,3,8,9,10],1)
	return clean_data,data

# train_df = np.array(pd.read_csv('train.csv', header=0))
train_df = pd.read_csv('train.csv', header=0)
train_op = train_df['Survived'].values
train_df = train_df.drop(['Survived'],axis=1)

test_df  = pd.read_csv('test.csv', header=0)

use_train, use_train_csv= clean(train_df)
# print  use_train_csv
use_test, use_test_csv = clean(test_df)
# print use_test_csv
# print use_train[0]

nn = Classifier(
    layers=[
        Layer("Sigmoid", units=7),
        # Layer("Softmax",units=5),
        Layer("Softmax", units = 5 )],
    learning_rate=0.5,
    n_iter=5)

nn.fit(use_train,train_op)

result = nn.predict(use_test)

print result
# Copy the results to a pandas dataframe with an "id" column and
# # a "sentiment" column
# output = pd.DataFrame( data={"PassengerId":test_df["PassengerId"], "Survived":result} )

# # Use pandas to write the comma-separated output file
# output.to_csv( "Titanic_survival.csv", index=False, quoting=3 )
