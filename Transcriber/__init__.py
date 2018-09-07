#Imports necessary libraries
from pip._vendor.distlib._backport.tarfile import TSVTX
import re

#A class that reads a file and passes on data to another class
class SpectralLibrary:
    #Initializes all necessary variables for the class
    fileName = ""
    
    #Creates an initializer method that takes a file name
    def __init__( self, fileName ):
        #Sets the classes own fileName variable
        self.fileName = fileName
        
    #A method that reads all the lines of a file and passes them individually to a Spectrum object
    def read( self ):
        #Initializes a list that holds all of the buffered lines objects
        buffList = []
        
        #Creates a spectrum object with the buffered list 
        spec = Spectrum()
        
        #Opens the file using a with-loop
        with open( self.fileName, "r" ) as file:
            #Runs through the file line-by-line:
            for line in file:
                #Checks if line is empty
                if line in [ '\n', '\r\n' ]:            
                    #Calls the Spectrum objects parse() method passing the buffered list as an argument
                    spec.parse( buffList )
                    
                    #Resets the buffered list
                    buffList = []
                                        
                #If the line is not empty
                else:
                    #Adds the line to the list
                    buffList.append( line )
    
        #Returns the spectrum list
        return spec.allSpecs
    
    #A method that writes each of the objects's attributes from the spectrumList into a .tsv file
    def write( self, spectrumList, column, fileName ):
        #Opens the file using a with-loop
        with( open( fileName, "w" ) ) as file:            
            #Runs through all of the spectrums in the spectrum list
            for spectrum in spectrumList:                     
                #Adds a new line
                file.write( '\n' )    
                       
                #Runs through all of the columns
                for column in columns:
                    #Gets rid of any new line characters in the string
                    spectrum[ column ] = spectrum[ column ].replace( '\n', '' )
                    
                    #Checks if the column is a key in the dictionary
                    if column in spectrum:
                        #Writes the line 
                        file.write( spectrum[ column ] + "\t\t" )
                        
                    #If the column is not their writes a statement in the file that tells the user
                    else:
                        file.write( "Column not found"  + "\t\t" )
                 
                
                
#A class that holds data for each spectrum that is read from the SpectralLibrary class
class Spectrum:
    #Initializes all the necessary data stores
    attributes = {}
    peakList = []
    allSpecs = []
    
    #A parse method that takes a buffered list of lines and parses them into one dictionary and one list
    def parse( self, buffList ):
        #Sets a boolean flag variable
        flag = True
        
        #Resets attributes
        self.attributes = {}
        
        #Loops through each line in the buffered list
        for line in buffList:
            #Checks if the flag is true    
            if flag:
                #Sets key-value variables using the split() method, splits only by colon and only splits once               
                key, value = re.split( ":", line, 1 )
                
                #Adds the key-value pair to the dictionary
                self.attributes[ key ] = value
                
                #Checks if the key is a certain value
                if key == "Num peaks":
                    #Changes the flag to false
                    flag = False
                    
                #Checks if key is equal to another value
                if key == "Comment":
                    #Splits the comment values properly
                    commentItems = re.split( ",\D| ", value )
                    
                    #Runs through each comment in the commentItems list
                    for comment in commentItems:
                        #Checks if the length of comment is over two and if when it is split it has two elements in the list
                        if len( comment ) >= 2 and ( len( comment.split( "=" ) ) == 2 ):
                            #Splits each comment one more time
                            commentKey, commentValue = comment.split( "=" )
                        
                            #Store the key-value pair in the dictionary
                            self.attributes[ commentKey ] = commentValue
                    
            #If the flag is not true checks if the flag is false
            elif not flag:
                #Splits the line
                mz, intensity, interpretations = line.split( "\t" )
                
                #Adds the values into the list
                self.peakList.append( [ mz, intensity, interpretations ] )
        
        #Adds the peak list to the attributes dictionary then returns the attributes dictionary
        self.attributes[ "Peaks" ] = self.peakList        
        
        #Adds the attributes to the list of spectrums
        self.allSpecs.append( self.attributes )
        
#Initializes the list that holds all the Spectrum class objects
Spectrums = []
    
#Takes user input about the file name and stores in a variable
fileName = input( "Enter in the file name (If the file is not in the directory, please give the full path): " );

#Takes user input for what kind of columns they want
col = input( "What kind of columns do you want (Seperate with spaces): " )
columns = col.split()

#Takes user input for which file to write into
fileNameWrite = input( "What file should I write into? " )

#Creates an instance of the SpectralLibrary object, passing the variable that holds the file name
library = SpectralLibrary( fileName );

#Calls the SpectralLibrary's read method and stores the result in a list
spectrumList = library.read()

#Calls the library's write() method passing on the spectrumList
library.write( spectrumList, columns, fileNameWrite )
