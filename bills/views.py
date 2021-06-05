from django.shortcuts import (render, get_object_or_404, redirect)
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.http import FileResponse

from django_tex.core import compile_template_to_pdf
from django_tex.shortcuts import render_to_pdf

#from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    #Plot, Figure, Matrix, Alignat
#from pylatex.utils import italic
import os
from transactions.models import Transaction
from datetime import datetime
from decimal import Decimal
from qrbill.bill import QRBill
import tempfile
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def generate_PDF(request,pk):
    transaction = get_object_or_404(Transaction, id=pk)
    #image_filename = os.path.join(os.path.dirname(__file__), 'kitten.jpg')
    file_name = transaction.client.name+ '_' + transaction.client.firstName + '_' + str(transaction.execution_date)

    template_name = 'template.tex'
    context = {}

    product_list =  transaction.product_set.all()
    product_cost = []
    total_price = 0
    for product in product_list:
        total_price = total_price + product.price * product.quantity
        product_cost_tmp =  product.price * product.quantity
        product_cost.extend([product_cost_tmp])
    print(product_cost)
    total_price = total_price + transaction.delivery_fee
    mylist = zip(product_list, product_cost)
    print(mylist)
    context['mylist'] = mylist
    context['total_price'] = total_price
    context['product_list'] = product_list
    context['transaction'] = transaction
    context['bill_name'] = file_name+"_bill.pdf"
    context['TVA'] = total_price*Decimal(0.025)


    my_bill = QRBill(
        account='CH05 8080 8009 1475 8210 4',
        creditor={
            'name': 'Pétale Rouge, Alicia Lehman', 'street':'Route du Gottau 17' ,'pcode': '1566', 'city': 'St-Aubin', 'country': 'CH',
        },
        debtor={
            'name': transaction.client.firstName +' ' + transaction.client.name  , 'street':transaction.client.street, 'pcode': transaction.client.postal_code, 'city': transaction.client.city, 'country': 'CH',
        },
        language="fr",
        amount=total_price,
    )

    with tempfile.TemporaryFile(encoding='utf-8', mode='r+') as temp:
        my_bill.as_svg(temp)
        temp.seek(0)
        drawing = svg2rlg(temp)
    renderPDF.drawToFile(drawing, file_name+"_bill.pdf")

    PDF = compile_template_to_pdf(template_name, context)
    #return render_to_pdf(request, template_name, context, filename=file_name+'.pdf')

    f = open(file_name+".pdf", "wb")
    f.write(PDF)

    #response = FileResponse(f, as_attachment=True)


    response = HttpResponse(PDF,'application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+file_name+'.pdf'

    return response
"""
def generate_PDF(request,pk):

    transaction = get_object_or_404(Transaction, id=pk)
    print(transaction.client)
    #image_filename = os.path.join(os.path.dirname(__file__), 'kitten.jpg')
    file_name = transaction.client.name+ '_' + transaction.client.firstName + '_' + str(transaction.execution_date)

    geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section('The simple stuff')):
        doc.append('Some regular text and some')
        doc.append(italic('italic text. '))
        doc.append('\nAlso some crazy characters: $&#{}')
        with doc.create(Subsection('Math that is incorrect')):
            doc.append(Math(data=['2*3', '=', 9]))

        with doc.create(Subsection('Table of something')):
            with doc.create(Tabular('rc|cl')) as table:
                table.add_hline()
                table.add_row((1, 2, 3, 4))
                table.add_hline(1, 2)
                table.add_empty_row()
                table.add_row((4, 5, 6, 7))

    a = np.array([[100, 10, 20]]).T
    M = np.matrix([[2, 3, 4],
                   [0, 0, 1],
                   [0, 0, 2]])

    with doc.create(Section('The fancy stuff')):
        with doc.create(Subsection('Correct matrix equations')):
            doc.append(Math(data=[Matrix(M), Matrix(a), '=', Matrix(M * a)]))

        with doc.create(Subsection('Alignat math environment')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append(r'\frac{a}{b} &= 0 \\')
                agn.extend([Matrix(M), Matrix(a), '&=', Matrix(M * a)])

        with doc.create(Subsection('Beautiful graphs')):
            with doc.create(TikZ()):
                plot_options = 'height=4cm, width=6cm, grid=major'
                with doc.create(Axis(options=plot_options)) as plot:
                    plot.append(Plot(name='model', func='-x^5 - 242'))

                    coordinates = [
                        (-4.77778, 2027.60977),
                        (-3.55556, 347.84069),
                        (-2.33333, 22.58953),
                        (-1.11111, -493.50066),
                        (0.11111, 46.66082),
                        (1.33333, -205.56286),
                        (2.55556, -341.40638),
                        (3.77778, -1169.24780),
                        (5.00000, -3269.56775),
                    ]

                    plot.append(Plot(name='estimate', coordinates=coordinates))

        with doc.create(Subsection('Cute kitten pictures')):
            with doc.create(Figure(position='h!')) as kitten_pic:
                #kitten_pic.add_image(image_filename, width='120px')
                kitten_pic.add_caption('Look it\'s on its back')

    doc.generate_pdf(file_name, clean_tex=False, compiler='pdflatex')
    file = open(file_name +'.pdf', 'rb')
    response = FileResponse(file, as_attachment=True)
    return response

def generate_PDF(request):
    data = {}
    context = {}

    template = get_template('bill.html')
    #html  = template.render(Context(data))
    html  = template.render(context)

    file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
            encoding='utf-8')

    file.seek(0)
    pdf = file.read()
    file.close()
    response = HttpResponse(pdf,'application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="foo.pdf"'
    return response
"""
