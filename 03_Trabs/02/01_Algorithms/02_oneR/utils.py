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
   
   def print_data_set(self, text, dataSet):
      print("::::::::::::::::::::::" + text + "::::::::::::::::::::::"  )
      print(dataSet)
      print(":::::::::::::::::::::::::::::::::::::::::::::::"  )
      print("")

   
