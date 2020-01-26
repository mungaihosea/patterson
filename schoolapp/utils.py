from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from weasyprint import HTML


# def render_to_pdf(html_template, context_dic):
#     template = get_template(html_template)
#     html = template.render(context_dic)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type = 'application/pdf')
#     else:
#         return None

def generate_pdf_report(request, template_src, context):
    template = get_template(template_src)
    html = template.render(context)
    pdf_file = HTML(string = html, base_url = request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type = 'application/pdf')
    response['Content-Disposition'] = "file_name = 'report-card.pdf'"
    return response
    