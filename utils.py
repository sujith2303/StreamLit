import pytesseract
import re
import string

def preprocess_mcqs(questions):
    options = []
    Questions = []
    for i in questions:
        if 'a)' in i:
            q,o = i.split('a)')
        else:
            q,o = i.split('A)')
        Questions.append(q)

        if 'b)' in i:
            a,o = o.split('b)')
        else:
            a,o = o.split('B)')
            
        if 'c)' in i:
            b,o = o.split('c)')
        else:
            b,o = o.split('C)')

        if 'd)' in i:
            c,d = o.split('d)')
        else:
            c,d = o.split('D)')
        
        options.append([a,b,c,d])
    print(options,Questions)
    return options,Questions

def clean_text(input_text):
    # Remove punctuation
    no_punctuations = ''.join(char for char in input_text if char not in string.punctuation)

    # Remove extra spaces
    no_extra_spaces = ' '.join(no_punctuations.split())

    # Remove unknown characters using regular expression
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', no_extra_spaces)

    return clean_text


def text_detection(img):
    pytesseract.pytesseract.tesseract_cmd = r"D:\Other Files\Tesseract\tesseract\tesseract.exe"
    boxes = pytesseract.image_to_boxes(img)
    s1 = pytesseract.image_to_string(img)
    s = ''
    for b in boxes.splitlines():
        b = b.split(' ')
        s = s + b[0]
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    if s == '~':
        return 'No Text Detected'
    else:
        return  clean_text(s1.split('  '))

if __name__=="__main__":
    print(text_detection(r"D:\PC_Downloads\pc1.jpg"))
    