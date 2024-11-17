from dotenv import load_dotenv

load_dotenv()

import gradio as gr

from standardizer import chroma, notion, standard_generator

with gr.Blocks() as interface:
    gr.Markdown("""
Standard Bootstrapper
==                
L'interface Standard Bootstrapper permet de créer facilement un premier jet d'un standard en répondant à un prompt.
Elle aide l'utilisateur à formuler des standards à l'aide de :
- Intention : Pourquoi ce standard est important et ce qu'il doit accomplir pour le client.
- Points de contrôle : Les éléments essentiels pour garantir la qualité du travail.
- Erreurs courantes : Les pièges à éviter et leurs conséquences.
""")
    with gr.Row():
        with gr.Column(scale=2):
            subject = gr.Textbox(
                label="Quel est le sujet de votre standard ?",
                placeholder="Décrivez le sujet du standard ici",
            )
            source_type = gr.Radio(
                key="source_type",
                label="Documentation",
                choices=["Pédagogie", "Notion page"],
                interactive=True,
            )
            notion_page_id = gr.Textbox(
                label="Notion page URL",
                visible=False,
                interactive=True,
                key="notion_page_id",
            )

            quality_elements = gr.TextArea(
                label="Comment identifiez vous la qualité d'une pièce produite ? ",
                placeholder="Décrivez les éléments clés qui définisse la qualité d'une pièce",
            )
            problems = gr.TextArea(
                label="Aves vous des problèmes à partager ? ",
                placeholder="Décrivez des problèmes que vous avez rencontré : causes, impacts sur la qualité, ...",
            )
            good_examples = gr.TextArea(
                label="Aves vous de bon exemples ? ",
                placeholder='Décrivez des pièces "parfaites"',
            )
            generate_button = gr.Button("Générer", variant="primary")

        with gr.Column(scale=4):
            standard_output = gr.Markdown(show_copy_button=True, value="Remplissez le formulaire sur la gauche")

    @source_type.change(inputs=[source_type], outputs=[notion_page_id])
    def update_source_visibility(source_type: str):
        is_page_url_visible = source_type == "Notion page"
        return gr.Textbox(visible=is_page_url_visible)

    @generate_button.click(
        inputs=[
            subject,
            source_type,
            notion_page_id,
            quality_elements,
            problems,
            good_examples,
        ],
        outputs=standard_output,
    )
    def generate(
        subject: str,
        source_type: str,
        notion_page_id: str,
        quality_elements: str,
        problems: str,
        good_examples: str,
    ):
        if source_type == "Notion page":
            retriever = notion.get_notion_retriever(notion_page_id)
        else:
            retriever = chroma.get_retriever(source_type)
        standard = standard_generator.create_standard(retriever, subject, quality_elements, problems, good_examples)
        return standard


def launch_ui():
    interface.launch()


if __name__ == "__main__":
    # gradio standardizer/main.py --demo-name=interface
    launch_ui
