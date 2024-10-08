from fasthtml.common import *
from hasseDiagram import getDiagram
import time

poset = []
relations = []
frm_relations = []
rels = []

app, rt, = fast_app(live=True)


@rt('/')
def get():
    global frm_relations, relations, rels
    relations = []
    frm_relations = []
    rels = []

    frm = Form(Group(Input(placeholder="Enter poset separated with commas", id='Inset'),
                     Button("Enter")),
               hx_post='/', target_id='rel'
               )
    frm1 = Form(Div(id='rel', align='center'),
                hx_post='/generate', target_id='img')
    img = P(id='img')
    content = Card(frm1, Div(img, align='center'), header=frm)

    return Titled("Hasse Diagram", content)


@rt('/')
def post(Inset: str):
    try:
        global poset, frm_relations
        poset = [x for x in Inset.split(',')]
        frm_relations = [
            Li(Input(placeholder=f"Enter relations of {i}", id='rid')) for i in poset]
    except Exception as e:
        get()
        print("poset", poset)
        return ("Error1")

    return Ul(*frm_relations), Button('Save')


@rt('/generate')
def post(rid: str):
    try:
        relations = []
        timestamp = int(time.time())
        filename = f'fig_{timestamp}.png'
        rels = []
        print(rid)
        for i in rid:
            rels = [x.split(',') if x else []for x in rid]
        print("rels", rels)
        for i in range(len(rels)):
            if len(rels[i]) == 0:
                continue
            for j in range(len(rels[i])):
                relations.append([poset[i], rels[i][j]])
        print(poset)
        print(relations)
    except Exception as e:
        print(e)
        get()
        return "error2"
    hasse = getDiagram(poset, relations, filename)
    if hasse == 'Error':
        print("error")
        get()
        return "error3"
    else:
        if hasse:
            response = Img(src=filename), H2("It is a Lattice")
            return response
        else:
            response = Img(src=filename), H2("It is not a Lattice")
            return response


serve()
