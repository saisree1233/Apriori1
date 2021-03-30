from flask import Flask
from flask import request
import os
import sys
import csv
app = Flask(__name__)

import os
import sys
import csv


def create_lists(dataset):
    out = []
    for L in dataset:
        for t in L:
            if (t) not in out:
                out.append(t)
    out2 = []
    for item in out:
        to = []
        to.append(item)
        out2.append(to)
    return out2

def get_frequency(dataset,C1,min_sup):
    out = []
    keys = []
    frequent = []
    counter = 0
    
    for Row in dataset:
        for c in C1:
            
            cs = set(c)
            Rows = set(Row)
            if cs.issubset(Rows):
                if c not in keys:
                    keys.append(c)
                    frequent.append(0)
                    counter += 1
                index = keys.index(c)
                frequent[index] += 1
    out = []
    
    
    cnt = 0;
    for key in keys:
        if(frequent[cnt] >= min_sup):
            out.append((key))
        cnt += 1

    return (out)


def getorderList(single_out,order):
    out = []
    for i in range(len(single_out)):
        for j in range(i+1,len(single_out)):
            if len(set(single_out[i]) | set(single_out[j])) == order:
                item  = set(single_out[i]) | set(single_out[j])
                out.append(item)
    res = []
    for i in out:
        if i not in res:
            res.append(i)
    print(str(order)+"--"+str(len(res)))
    return res

def trim_allout(final):
    
    
    out = []
    item_count = 0
    for k in range(len(final)-1):
        out_sub = []
        for item in final[k]:
            exist = 0
            for rep in range(k+1,len(final)):
                for co in final[rep]:
                    if set(item).issubset(set(co)):
                        exist = 1
            if(exist == 0):
                out_sub.append(item)
                item_count = item_count + 1
        out.append(out_sub)      
    item_count =  item_count + len(final[len(final)-1])
    out.append(final[len(final)-1])
    return item_count,out
        


def Apriori(filename,min_sup):
    global threadoutstr
    with open(os.path.join(sys.path[0], filename), newline='') as f:
        reader = csv.reader(f, skipinitialspace=True)
        rows = list(reader)
    dataSet = rows

    new_dataset = []

    for item in dataSet:# remove index and convert each element to int
        item.pop(0)
        n_item = []
        for ele in item:
            n_item.append((ele))
        new_dataset.append(n_item)

    threadoutstr += "<br>dataSet Items Count:" + str(len(new_dataset))

    single_rep = create_lists(new_dataset)
    threadoutstr += "<br>Single index List Created"
    single_out = get_frequency(new_dataset,single_rep,min_sup)
    threadoutstr += "<br>Single index frquent items found"

    present_order = 2

    all_out = []
    all_out.append(single_out)

    while(1):
        threadoutstr += "<br>"+str(present_order)+" order processing"
        order_pair = getorderList(all_out[present_order-2],present_order)
        if len(order_pair) == 0:
            break;
        threadoutstr += "<br>getting order "+str(present_order)+" frequents"
        single_out = get_frequency(new_dataset,order_pair,min_sup)
        present_order += 1

        all_out.append(single_out)
    threadoutstr += "<br>Trimming the Output"    
    items_count,final_out = trim_allout(all_out)

    return items_count,final_out


@app.route('/')
def main():
    global threadoutstr
        
    st = '<html><body>  <center>	<h1>Apriori Algoritham</h1> <br> <br>	  	<h1>Select a Desired DataSet</h1>     <br>  <br>      <div align="center">  	<form action="/op" method="get">        <label for="min_sup">min_sup Value:</label>        <input type="text" id="min_sup" name="min_sup"><br><br>  	    	  <button name="subject" type="submit" value="1000-out1">1000-out1</button><br><br>  	  <button name="subject" type="submit" value="5000-out1">5000-out1</button><br><br>  	  <button name="subject" type="submit" value="20000-out1">20000-out1</button><br><br>  	  <button name="subject" type="submit" value="75000-out1">75000-out1</button><br><br>  	        </form>  	</div>  	  	  </center>	  </body></html>'
    threadoutstr = ""
    return st

gc = 0
apriorijob = 0
apriorifilename = ""
threadoutstr = ""
min_sup_input = ""
jobdone = 0
main_out = ""
@app.route('/op')
def op():
    global gc,apriorijob,apriorifilename,min_sup_input
    dataset = request.args.get('subject')
  
    datasetfilename = dataset + ".csv"
    min_sup = request.args.get('min_sup')
    st = "<html>   <body>      <script>  \
         setTimeout(function(){ \
            window.location.href = '/check';\
         }, 5000);\
        </script>\
        <p>Process Started and Web page will check output after 5 seconds.</p>\
        </body>\
        </html>"
    apriorifilename = datasetfilename
    min_sup_input = min_sup
    apriorijob = 1
    gc = gc + 1
    st = st + "selected Filename is :"     + str(datasetfilename)
    st = st + "<br>min_sup:" + str(min_sup)
    st = st + '<br>'
    
    
    return st



@app.route('/check')
def check():
    global gc,jobdone,threadoutstr,main_out
    if(jobdone == 1):
        st = "Job done<br><br>"
        st += main_out
        
        jobdone = 0
    else:
        st = "<html>   <body>      <script>  \
             setTimeout(function(){ \
                window.location.href = '/check';\
             }, 10000);\
            </script>\
            <p>Job In process and Web page will check output after 10 seconds.</p>"\
            +threadoutstr+\
            "</body>\
            </html>"
    gc = gc + 1
    return st

import time
import threading


def doaprioriJob(val):
    global apriorijob,threadoutstr,apriorifilename,min_sup_input,jobdone,main_out
    while(1):
        time.sleep(1)
        if(apriorijob == 1):
            threadoutstr = "Job Started"
            items_count,final_out = Apriori(apriorifilename,int(min_sup_input))
            main_out = "DataSet:" +  apriorifilename
            main_out += "<br><br>Out:<br>"
            main_out += str(final_out) + "<br><br>"
            main_out += "total Items: "+str(items_count)
                       
            apriorijob = 0
            jobdone = 1

t1 = threading.Thread(target=doaprioriJob, args=(10,))
t1.start()
  
if __name__ == "__main__":
    app.run()