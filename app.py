import json
from flask import *
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_iris
import pandas as pd
#Below importing train_test_split for splitting dataset on the bases of
#percentage we can define 0.20 for 20 percent and so on etc
from sklearn.model_selection import train_test_split
#below we are importing gausinaNB classifier from sklearn library #naive_bayes module
from sklearn.naive_bayes import GaussianNB,BernoulliNB,MultinomialNB
#below we import standard scaller from sklearn preprocessing to reduce the values of our 
# features in to small value for easy calculation
from sklearn.preprocessing import StandardScaler
#Importing confution matric function to calculate value matric values
from sklearn.metrics import confusion_matrix
#Importing accuracy_score function to calculate accuracy of the model by giving test y and predicted y
from sklearn.metrics import accuracy_score 
#Importing for displaying confusion matric in a proper format
import seaborn as sns
#We use this to create image of matplot graph of confusion matrics and than that image into base64 formate to display
#Infront of the user
import io
import urllib, base64

app = Flask(__name__)
entered_Name = ""


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

#Below is the custom function created to perform classification on iris dataset by apply any of the two
#Naive Bayes classification gaussian distribution or berboulli distribution
def NaiveBayesClassifier(Method):
    #Importing DataFrom dataset available for iris from official resources.
    csv_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    iris = pd.read_csv(csv_url, header = None)
    #Creating a header with our customs names
    col_names = ['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width','Species']
    iris =  pd.read_csv(csv_url, names = col_names)
    #Below is assigning first four colunms only rows means data into  as X because we treat it as features
    #So all features will go into X
    x = iris.iloc[:,:4].values
    #Assigning Species values as our output variable or response variable as y
    y = iris['Species'].values
    iris.head(5)

    #Divide all data into two parts like we set 20 percent data for testing and 80 percent data for training purpose
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

    #Scale feature into smaller value using sklearn provided scaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    #Selecting and Initializing classfier according to the Method choice of user
    if( Method == "Bernoulli"):  
        classifier = BernoulliNB()
    elif(Method == "Gaussian"):
        classifier = GaussianNB() 
    else:
        print("Error")
    #Applying to the training data
    classifier.fit(X_train, y_train)

    #Applying classification on the test data
    y_pred = classifier.predict(X_test) 

    #Applying confusion matrics to the y test and y pred
    cm = confusion_matrix(y_test, y_pred)
    ax = sns.heatmap(cm, annot=True, cmap='Blues')
    ax.set_title('Seaborn Confusion Matrix with labels\n\n');
    ax.set_xlabel('\nPredicted Flower Category')
    ax.set_ylabel('Actual Flower Category ');
    ## Ticket labels - List must be in alphabetical order
    ax.xaxis.set_ticklabels(['Iris-setosa','Iris-versicolor', 'Iris-virginia'])
    ax.yaxis.set_ticklabels(['Iris-setosa','Iris-versicolor', 'Iris-virginia'])
    ## Display the visualization of the Confusion Matrix.
    # plt.show();
    fig = plt.gcf()
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.clf()

    #Creating object for merging all data which includes base64 image confusion matrics converted from matplot
    # And Prediction  table which includes real and predicted values
    # Last it will append the accuracy value of the model
    OutputData = {"Output": []}
    OutputData["Output"].append({str("Base64Img"): uri})
    #To print the accuracy score and confustion matrics calculate by sklearn library confusion_matric function
    accuracy = accuracy_score(y_test, y_pred);

    #To print the comparison of real value and predicted value
    df = pd.DataFrame({'RealValues':y_test, 'PredictedValues':y_pred})
    predictionData = df.to_json(orient='columns')
    OutputData["Output"].append({str("Predictions"): json.loads(predictionData)})
    OutputData["Output"].append({str("ModelAccuracy"): str(accuracy)})
    # merged_dict = {key: value for (key, value) in (dictA.items() + dictB.items())}
    del buf,fig,string,cm,uri
    return jsonify(json.dumps(OutputData));

@app.route("/apply-model", methods=["GET", "POST"])
def apply_model():
    if((json.loads(request.data))["Main"] == "Bernoulli"):
      mainData =  NaiveBayesClassifier("Bernoulli")
    elif((json.loads(request.data))["Main"] == "Gaussian"):
      mainData =  NaiveBayesClassifier("Gaussian");
    else:
      print("Error")
    return mainData             

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
