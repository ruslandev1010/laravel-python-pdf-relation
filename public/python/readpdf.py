import pdfplumber

listofstartword = [ "Policy Supported:", "Related Documents:"]
listofendword = [ "References:", "Audience:", "Preamble:","Approval and Implementation:","Revision History:"]
listofskiptest = ["There are no related documents."]
pref_list = ['Page', 'http', 'https']
dlist = []



def read_pdf(PDFFile, file, doc):
    plist = []
    with pdfplumber.open(PDFFile) as pdf:
        content = ''
        va = False
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            for text in page.extract_text().split('\n'):
                t = text.strip()
                content += text
                if(t in listofstartword):
                    va = True
                elif(t in listofendword):
                    va = False
                elif(va == True):
                    if (t in doc):
#                     if ((t not in listofskiptest) and not list(filter(t.startswith, pref_list)) != []
#                         and not t == ""):
                        plist.append(t)
        dlist.append((file,plist,content))

