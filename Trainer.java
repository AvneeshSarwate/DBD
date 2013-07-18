 /*
 * Main.java
 *
 * Created on July 2, 2007, 3:37 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */


 import java.io.File;
 import java.util.Iterator;
 import weka.classifiers.Classifier;
 import weka.classifiers.meta.AdaBoostM1;
 import weka.classifiers.trees.J48;
 import weka.core.*;
 import weka.core.converters.ArffLoader;

 /**
 *
 * @author rebecca
 */
 public class Trainer {

    /** Creates a new instance of Main */
    public Trainer() {

    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

      String concept = args[0]; 
      //System.out.println("mogofaga");
      Classifier this_classifier = new AdaBoostM1();

      //choose the component "weak" classifier
      Classifier component_classifier = new J48(); //weka's built-in decision tree classifier

      //set any parameters of the weak classifier here

      ((AdaBoostM1) this_classifier).setClassifier(component_classifier);

      //Get training instances using arff loader (from arff file)
      // (There are other ways to instantiate instances, like using csvloader)
      try {
          ArffLoader arffloader= new ArffLoader();
          arffloader.setFile(new File(concept + "/train.arff"));
          Instances training = arffloader.getDataSet();
          training.setClassIndex(training.numAttributes() - 1); //specify that the last attribute is the class
          this_classifier.buildClassifier(training);

          //Get testing instances using arff loader
          ArffLoader arffloader2= new ArffLoader();     //THIS ARFF MADE FROM SEEDED RANDOM MELODIES
          arffloader2.setFile(new File(concept + "/test.arff"));
          Instances testing = arffloader2.getDataSet();
          testing.setClassIndex(testing.numAttributes() - 1); //specify that the last attribute is the class

          //if label is 1st attribute, and it's a number (a bit extra required if it's a string)
          double[] label_vals = testing.attributeToDoubleArray(testing.numAttributes()-1);
          //testing.deleteAttributeAt(testing.numAttributes() - 1); //changed: dummy tags to be added and removed? 

          //Iterate through testing instances
          for (int i=0; i < testing.numInstances(); i++) {
              //Now, your label for each of the testing instances might be an attribute, if you've included it as a field in the file
              //you could yank this field and print it out later like this:
              Instance this_instance = testing.instance(i);

              double result = this_classifier.classifyInstance(this_instance);
              // or could use 
              double resultsD[] = this_classifier.distributionForInstance(this_instance);

              //do stuff with the result
              
              System.out.println(/*label_vals[i]+ ": " + */resultsD[0] /*+ " " + resultsD.length*/);
          }

      } catch (Exception ex) {
          ex.printStackTrace();
      }
    }

 }
