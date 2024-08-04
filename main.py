from fasthtml.common import *
from hasseDiagram import getDiagram
import os
import time

poset = []
relations = []
frm_relations = []

app, rt, = fast_app(live=True)


@rt('/')
def get():
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
    global poset, frm_relations
    poset = [int(x) for x in Inset.split(',')]
    frm_relations = [
        Li(Input(placeholder=f"Enter relations of {i}", id='rid')) for i in poset]

    return Ul(*frm_relations), Button('Save')


@rt('/generate')
def post(rid: str):
    timestamp = int(time.time())
    filename = f'fig_{timestamp}.png'
    if os.path.exists("fig.png"):
        os.remove("fig.png")
    rels = []
    print(rid)
    for i in rid:
        rels = [list(map(int, x.split(','))) for x in rid if x]
    print(rels)
    for i in range(len(rels)):
        for j in range(len(rels[i])):
            relations.append([poset[i], rels[i][j]])
    print(poset)
    print(relations)
    getDiagram(poset, relations, filename)
    return Img(src=filename)


serve()
