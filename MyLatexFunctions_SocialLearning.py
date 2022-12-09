#import libraries
import os
import subprocess
from io import open
import tempfile
import shutil
import math as math


def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)


def ProbCorrect_Bayesian(n, q):
    '''Based on Bayesian rule, the prob of making a correct guess by observing n signals '''
    nn = 0
    prob = 0
    
    while nn <=  (n/2):
        
        #print(nn)
        #if ((n-nn) % 2 ) == 0 & (nn!=0) :
        if nn ==  (n/2) :
            prob += nCr(n,(n-nn))*(q**(n-nn))*((1-q)**(nn))*(1/2)
            #print(prob)
        else :
            prob += nCr(n,(n-nn))*(q**(n-nn))*((1-q)**(nn))
            #print(prob)
        nn += 1
        
    
    return prob

def ProbLinear(n,q):
    # 1. the difference remain the same, ProbCorrect_Bayesian(5,q)-ProbCorrect_Bayesian(1,q) 
    # When q = 0.7, the difference is (ProbCorrect_Bayesian(5,0.7)-ProbCorrect_Bayesian(1,0.7))/4 = 0.3423
    # 2. Ensure that the middle point is the correct probability
    # ProbCorrect_Bayesian(3,0.7) = a + 0.3423*3
    # a = 0.68131
    
    b = (ProbCorrect_Bayesian(5,q)-ProbCorrect_Bayesian(1,q))/4
    a = ProbCorrect_Bayesian(3,q) - b*3
    
    return a+b*n
    


def clean_pdf_output(out_text,file_name):
    ''' create a pdf file in a temporary directory, then move pdf into the current directory and delete all other files '''

    current = os.getcwd()
    # create temporary directory where work will be temprorily stored
    temp = tempfile.mkdtemp()
    os.chdir(temp)

    # Output stored strings to file
    tex_file_name=file_name+".tex"
    f = open(tex_file_name, 'w')
    f.write(out_text)
    f.close()

    #Execute latex command
    pdf_command="pdflatex "+file_name+".tex"
    os.system(pdf_command)

    #copy pdf and tex files to the current working directory (where this file is)
    pdf_file_name=file_name+".pdf"
    shutil.copy(pdf_file_name,current)
    shutil.copy(tex_file_name,current)
    os.chdir(current)
    
    #open created file
    subprocess.Popen(pdf_file_name,shell=True)

    # delete the temporary directory (recommended)
    shutil.rmtree(temp)

    
    

def pdf_output(out_text,file_name):
    ''' create a pdf file (and all of the auxilary files)'''
    # Output stored strings to file
    tex_file_name=file_name+".tex"
    f = open(tex_file_name, 'w')
    f.write(out_text)
    f.close()

    #Execute latex command
    pdf_command="pdflatex "+file_name+".tex"
    os.system(pdf_command)
    
    #open created file
    subprocess.Popen(file_name+".pdf",shell=True)


    

def beginDocument():
    string = """
                \\documentclass[11pt]{article}
                \\usepackage{tikz}
                \\usepackage[active,tightpage]{preview}
                \\PreviewEnvironment{tikzpicture}
                \\setlength\\PreviewBorder{2mm}
                \\begin{document}
                \\begin{tikzpicture} 
                \n"""
    return string


def beginAutomataDocument():
    string = """\documentclass[11pt]{article}
				\\usepackage{tikz}
				\\usetikzlibrary{automata}
				\\usepackage[active,tightpage]{preview}
				\\PreviewEnvironment{tikzpicture}
				\\setlength\\PreviewBorder{2mm}

				\\definecolor{C}{rgb}{1,1,0}
				\\definecolor{D}{rgb}{.55,.84,1}

				\\begin{document}
				\\begin{tikzpicture} \n"""
    return string


def endDocument():
    string = """
                \\end{tikzpicture}
                \\end{document}"""
    return string



def texArrow(p1,p2,line_type,color="red",x_offset=0,y_offset=0):
    if line_type==1:
        temp="\\draw [->,color="+color+"] ("+str(p1[0]+x_offset)+","+str(p1[1]+y_offset)+") -- ("+str(p2[0]+x_offset)+","+str(p2[1]+y_offset)+"); \n"
    if line_type==2:
        temp="\\draw [color=gray,dashed] ("+str(p1[0]+x_offset)+","+str(p1[1]+y_offset)+") -- ("+str(p2[0]+x_offset)+","+str(p2[1]+y_offset)+"); \n"
    return temp

def texPoint(p1,color="red",pch="$\\circ$",x_offset=0,y_offset=0):

    temp="\\node [color="+color+"] at ("+str(p1[0]+x_offset)+","+str(p1[1]+y_offset)+") {"+pch+"}; \n"

    return temp

def texLineSeq(lineSeq,color="red",pch="$\\circ$",x_offset=0,y_offset=0):
    #print "x_offset=",x_offset
    n=len(lineSeq)
    temp="\\draw [color="+color+"] ("+str(lineSeq[0][0]+x_offset)+","+str(lineSeq[0][1]+y_offset)+")"
    for i in range(1,n-1):
        temp+="-- ("+str(lineSeq[i][0]+x_offset)+","+str(lineSeq[i][1]+y_offset)+")"
    temp+="-- ("+str(lineSeq[n-1][0]+x_offset)+","+str(lineSeq[n-1][1]+y_offset)+"); \n"

    return temp

def texLine(x1,y1,x2,y2,line_type=1):
    if line_type==1:
        temp="\\draw ("+str(x1)+","+str(y1)+") -- ("+str(x2)+","+str(y2)+"); \n"
    if line_type==2:
        temp="\\draw [color=gray,dashed] ("+str(x1)+","+str(y1)+") -- ("+str(x2)+","+str(y2)+"); \n"
    return temp


def texRectangle(points,color,x_offset=0,y_offset=0):
    temp="\\draw [color="+color+"] ("+str(points[0][0]+x_offset)+","+str(points[0][1]+y_offset)+")"
    for n in range(1,len(points)):
        temp+="-- ("+str(points[n][0]+x_offset)+","+str(points[n][1]+y_offset)+") "
    temp+="; \n"
    return temp

# In[16]:

def texCircle(c1,r1,color,fillcolor, x_offset=0,y_offset=0):

    temp="\\coordinate (center) at ("+str(c1[0]+x_offset)+","+str(c1[1]+y_offset)+"); \n"

    temp+="\\draw[color="+color+",fill="+fillcolor+"] (center) circle [radius="+str(r1)+"]; \n"


    return temp

def texSquare(c1,r1,color,fillcolor,x_offset=0,y_offset=0):

    temp="\\draw[color="+color+",fill="+fillcolor+"] ("+str(c1[0]+x_offset-r1)+","+str(c1[1]+y_offset+r1)+") rectangle ("+str(c1[0]+x_offset+r1)+","+str(c1[1]+y_offset-r1)+"); \n"


    return temp

# In[16]:

def texNode(text,x1,y1,rotate=",rotate=0",size="\\normalsize ",align=",align=center",width="text width=3cm "):

    temp="\\node ["+width+rotate+align+"] at ("+str(x1)+","+str(y1)+") {"+size+text+"}; \n"

    return temp
