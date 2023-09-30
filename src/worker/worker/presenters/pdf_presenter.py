import os
import jinja2
from weasyprint import HTML

from .base_presenter import BasePresenter


class PDFPresenter(BasePresenter):
    type = "PDF_PRESENTER"
    name = "PDF Presenter"
    description = "Presenter for generating PDF documents"

    def generate(self, presenter_input):
        try:
            head, tail = os.path.split(presenter_input.parameter_values_map["BODY_TEMPLATE_PATH"])

            input_data = BasePresenter.generate_input_data(presenter_input)

            env = jinja2.Environment(loader=jinja2.FileSystemLoader(head))

            body = env.get_template(tail)
            output_text = body.render(data=input_data)

            html = HTML(string=output_text)

            data = html.write_pdf(target=None)

            return {"mime_type": "application/pdf", "data": data}
        except Exception as error:
            BasePresenter.print_exception(self, error)
            return {"error": str(error)}
