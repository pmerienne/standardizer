from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack_integrations.components.connectors.langfuse import LangfuseConnector

from standardizer import chroma


def create_pipeline(retriever) -> Pipeline:
    pipeline = Pipeline()
    # Add components to your pipeline
    pipeline.add_component("retriever", retriever)
    pipeline.add_component(
        "prompt_builder",
        PromptBuilder(
            template="""                                                         
    Create a lean standard of work :
    - Provide concise and clear orientations to support someone who will produce something (a "piece").
    - Keep the standard easy to remember
    - Focus on the added value and user needs

    # About standard
    ## What's a standard
    A standard is a training material associated to the production of a piece. 
    It should give anyone the capacity to assess the quality of the piece they are producing.
    It should not be too specific, people need to apply this standard to their context

    A good standard captures :
    - **The intention**: why is it important? what do we want to achieve?
    - **The control points**: Key elements for identifying piece quality and why they are important
    - **The common mistakes** : Actions/gestures to avoid and with their consequences

    # Example of standard on (subject: cooking a apricot tart)
    ## 🎯 Intention
    A great apricot tart is one of the best dessert in the world when the technique is mastered, but few people have this talent. 

    ## ✅ Control points
    - the apricots are melting and slightly caramelized
    - the crust is golden
    - the taste is between acid and sweet
    - every slice has a bit of side crust

    ## 🚨 Common errors
    - cook with unripped abricots → there won't be enough sugar in them to caramelize
    - make a square shape →  some people won't have any side crust or have too much of it
    - cook too hot → the crust will appear faster but the abricots will burn

    # Documentation
    Use the following information to answer the question.

    {% for document in documents %}
        {{ document.content }}
    {% endfor %}


    # Standard Subject
    {{ subject }}

    {% if quality_elements %}
    # Identified quality elements
    {{ quality_elements }}
    {% endif %}

    {% if problems %}
    # Identified problems
    {{ problems }}
    {% endif %}

    {% if good_examples %}
    # Example of quality
    {{ good_examples }}
    {% endif %}


    # Additional information
    - Language: Français
    - Structure : Intention, Points de contrôle, Erreurs courantes

    Answer:
    """
        ),
    )
    pipeline.add_component("llm", OpenAIGenerator(model="gpt-4o-mini"))
    pipeline.add_component("tracer", LangfuseConnector("Standard generator"))

    # Now, connect the components to each other
    pipeline.connect("retriever", "prompt_builder.documents")
    pipeline.connect("prompt_builder", "llm")

    return pipeline


def create_standard(
    retriever,
    subject: str,
    quality_elements: str = "",
    problems: str = "",
    good_examples: str = "",
):
    pipeline = create_pipeline(retriever)
    response = pipeline.run(
        {
            "retriever": {"query": subject},
            "prompt_builder": {
                "subject": subject,
                "quality_elements": quality_elements,
                "problems": problems,
                "good_examples": good_examples,
            },
        }
    )
    response_content = response["llm"]["replies"][0]
    return response_content


if __name__ == "__main__":
    # delete_all()
    retriever = chroma.get_retriever("Pédagogie")
    print(create_standard(retriever, "Gérer un conflit dans son équipe"))
