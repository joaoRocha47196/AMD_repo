import sys
import Orange as DM

class Utils:
   def my_print(self, aStr):
      separator = lambda x: "_" * len( x )
      print( separator( aStr ) )
      print( aStr )

   def print_arr(self, name, head, arr):
      self.my_print( name)
      print(head)
      for _, values in arr.items():
         for value in values:
               print(value)
      print()


   def loggHeader(self, text):
      astr = "::::::::::::::::::::::" + text + "::::::::::::::::::::::"
      separator = lambda x: ":" * len( x )
      print()
      print(separator(astr))
      print("::::::::::::::::::::::" + text + "::::::::::::::::::::::"  )
      print(separator(astr))
      print()
   
   ## DELTE ALL BELOW
   def print_data_set(self, text, dataSet):
      print("::::::::::::::::::::::" + text + "::::::::::::::::::::::"  )
      print(dataSet)
      print(":::::::::::::::::::::::::::::::::::::::::::::::"  )
      print("")

   def print(self, text):
      print(text)

   def log(self, text):
      print("::" + text)

   

   def logSimpleLine(self, ):
      print("::::::::::::::::::::::::::::::::::::::::::::::::::::::"  )
      print("")

   def logHeader(self, text):
      print(":: [" + text + "]")

   def print_args(self, *args):
      for arg in args:
         print(arg)

   def print_variable_and_value(self, **kwargs):
      for name, value in kwargs.items():
         print(f"{name}: {value}")

   def load(self, fileName):
      self.log("Reading Input File")

      try:
         dataset = DM.data.Table(fileName)
      except Exception as e:
         self.my_print(f":: Error - cannot open the file: {fileName}")
         sys.exit(1)  # Exit with an error code
      return dataset
